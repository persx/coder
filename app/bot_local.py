import os, json, subprocess, pathlib, textwrap, yaml
from typing import Dict, Any
import httpx
from anthropic import Anthropic

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)

class Env:
    model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    local_repo = os.getenv("LOCAL_REPO_PATH")  # Path to local persx repo
    owner_repo = os.getenv("TARGET_OWNER_REPO", "persx/persx")
    pr_base = os.getenv("PR_BASE","main")
    task_file = os.getenv("TASK_FILE","tasks/persx.yaml")
    safeops_file = os.getenv("SAFEOPS","configs/safeops_persx.json")
    loops = int(os.getenv("MAX_LOOPS","6"))
    budget_tokens = int(os.getenv("ANTHROPIC_BUDGET_TOKENS","0"))
    api_key = os.environ["ANTHROPIC_API_KEY"]
    gh_token = os.getenv("GH_TOKEN", "")  # Optional for local mode

def gh_api(method, path, body=None):
    if not Env.gh_token:
        print(f"[DRY RUN] Would call GitHub API: {method} {path}")
        return {"html_url": "http://localhost/pr/mock", "number": 999}

    r = httpx.request(method, f"https://api.github.com{path}",
                      headers={
                          "Authorization": f"Bearer {Env.gh_token}",
                          "Accept": "application/vnd.github+json"
                      },
                      json=body, timeout=60)
    r.raise_for_status()
    return r.json()

# ---------- Tools ----------
class Tools:
    def __init__(self, repo_dir: pathlib.Path, safeops: Dict[str, Any]):
        self.repo_dir = repo_dir
        self.safeops = safeops

    def read_repo(self, glb: str = "**/*.{ts,tsx,md}")->Dict[str,Any]:
        root = self.repo_dir
        out = []
        for p in root.glob(glb):
            try:
                if p.is_file() and p.stat().st_size < 180_000:
                    rel = str(p.relative_to(root))
                    if self._allowed(rel):
                        out.append({"path": rel, "content": p.read_text(errors="ignore")})
            except Exception:
                pass
        return {"files": out[:200]}

    def write_file(self, path: str, content: str)->Dict[str,Any]:
        if not self._allowed(path):
            return {"error": f"path '{path}' forbidden by safeops"}
        p = self.repo_dir / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        print(f"✓ Wrote: {path}")
        return {"ok": True}

    def run_checks(self)->Dict[str,Any]:
        out = {}
        # install deps if package.json exists
        if (self.repo_dir / "package.json").exists():
            print("📦 Running npm ci...")
            out["npm_ci"] = run(["bash","-lc","npm ci --no-audit --no-fund"], cwd=self.repo_dir).returncode
            print("🔍 Running lint...")
            lint = run(["bash","-lc","npm run -s lint"], cwd=self.repo_dir)
            print("🏗️  Running build...")
            build = run(["bash","-lc","npm run -s build"], cwd=self.repo_dir)
            out.update({
                "lint_rc": lint.returncode, "lint": (lint.stdout+lint.stderr)[-8000:],
                "build_rc": build.returncode, "build": (build.stdout+build.stderr)[-8000:]
            })
            print(f"✓ Checks complete - lint: {lint.returncode}, build: {build.returncode}")
        else:
            out["note"] = "No package.json; skipping JS checks."
        return out

    def open_pr(self, title: str, body: str, branch: str)->Dict[str,Any]:
        print(f"\n{'='*60}")
        print(f"📝 Would create PR:")
        print(f"Title: {title}")
        print(f"Branch: {branch}")
        print(f"Body:\n{body}")
        print(f"{'='*60}\n")

        # In local mode, just show what would happen
        if not Env.gh_token:
            print("[LOCAL MODE] Skipping actual PR creation")
            print("✓ Changes remain in local repo for inspection")
            return {"url": "http://localhost/pr/mock", "number": 999, "local_mode": True}

        # If GH_TOKEN provided, actually create the PR
        run(["git","checkout","-b",branch], cwd=self.repo_dir)
        run(["git","add","-A"], cwd=self.repo_dir)
        commit = run(["bash","-lc",f'git commit -m "{title}"'], cwd=self.repo_dir)
        if commit.returncode != 0:
            return {"error":"nothing to commit?"}

        print("⚠️  [LOCAL MODE] Would push to remote - skipping")
        return {"url": "http://localhost/pr/mock", "number": 999, "local_mode": True}

    def _allowed(self, rel_path: str)->bool:
        from fnmatch import fnmatch
        for pat in self.safeops.get("forbidden", []):
            if fnmatch(rel_path, pat): return False
        allowed = self.safeops.get("allowed_globs")
        if not allowed: return True
        return any(fnmatch(rel_path, pat) for pat in allowed)

# ---------- Orchestrator ----------
def main():
    if not Env.local_repo:
        print("❌ ERROR: LOCAL_REPO_PATH not set!")
        print("Usage: LOCAL_REPO_PATH=/path/to/persx python app/bot_local.py")
        return

    repo_dir = pathlib.Path(Env.local_repo)
    if not repo_dir.exists():
        print(f"❌ ERROR: Local repo not found: {repo_dir}")
        return

    print(f"🤖 Claude Bot - LOCAL MODE")
    print(f"📁 Local repo: {repo_dir}")
    print(f"🎯 Target: {Env.owner_repo}")
    print(f"🔧 Model: {Env.model}")
    print(f"💰 Token budget: {Env.budget_tokens if Env.budget_tokens > 0 else 'unlimited'}")
    print(f"\n{'='*60}\n")

    client = Anthropic(api_key=Env.api_key)

    safeops = json.loads(pathlib.Path(Env.safeops_file).read_text())
    backlog = pathlib.Path(Env.task_file).read_text()

    tools = Tools(repo_dir, safeops)

    TOOL_DECL = [
        {"name":"read_repo","description":"Read repository source by glob.","input_schema":{"type":"object","properties":{"glob":{"type":"string"}}}},
        {"name":"write_file","description":"Write or overwrite a file relative to repo root.","input_schema":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}},
        {"name":"run_checks","description":"Run npm lint/build if package.json exists.","input_schema":{"type":"object","properties":{}}},
        {"name":"open_pr","description":"Show what PR would be created (local mode).","input_schema":{"type":"object","properties":{"title":{"type":"string"},"body":{"type":"string"},"branch":{"type":"string"}},"required":["title","branch"]}}
    ]

    SYSTEM = textwrap.dedent(f"""You are a cautious coding agent for web frontends (Next.js/React/TS) and Node services.
    Respect these guardrails:
{json.dumps(safeops)}

    Rules:
    - Make only tiny, reversible improvements (tests, docs, a11y, SEO, refactors).
    - Keep diffs under {safeops.get('max_loc', 400)} LOC.
    - Never touch forbidden globs. If a task requires it, explain and stop.
    - Always run checks before proposing changes; summarize risk notes and changes.

    LOCAL MODE: Changes will be written to the local repo for inspection. No PR will be created.
    """)

    with open(Env.task_file, "r") as f:
        tasks_yaml = f.read()

    messages = [{
        "role":"user",
        "content": f"Target repo: {Env.owner_repo}\nBacklog (choose one tiny task):\n\n{tasks_yaml}"
    }]

    def call_tool(name, args):
        if name=="read_repo": return tools.read_repo(**args)
        if name=="write_file": return tools.write_file(**args)
        if name=="run_checks": return tools.run_checks()
        if name=="open_pr": return tools.open_pr(**args)
        return {"error":"unknown tool"}

    total_tokens = 0
    for loop_num in range(Env.loops):
        print(f"\n🔄 Loop {loop_num + 1}/{Env.loops}")
        resp = client.messages.create(
            model=Env.model,
            system=SYSTEM,
            max_tokens=1800,
            tools=TOOL_DECL,
            messages=messages
        )
        # Track token usage
        total_tokens += resp.usage.input_tokens + resp.usage.output_tokens
        print(f"💰 Tokens this loop: {resp.usage.input_tokens} in + {resp.usage.output_tokens} out = {resp.usage.input_tokens + resp.usage.output_tokens}")

        if Env.budget_tokens > 0 and total_tokens > Env.budget_tokens:
            print(f"⚠️  Budget exceeded: {total_tokens}/{Env.budget_tokens} tokens")
            break

        part = resp.content[0]
        if part.type == "tool_use":
            print(f"🔧 Tool: {part.name}")
            result = call_tool(part.name, part.input or {})
            messages.append({"role":"assistant", "content": resp.content})
            messages.append({"role":"user", "content": [{"type": "tool_result", "tool_use_id": part.id, "content": json.dumps(result)}]})
            continue

        # Text response means bot is done
        if part.type == "text":
            print(f"\n💬 Bot says:\n{part.text}\n")
        break

    print(f"\n{'='*60}")
    print(f"✅ Complete! Total tokens used: {total_tokens}")
    print(f"📁 Check your local repo for changes: {repo_dir}")
    print(f"💡 Use 'git diff' to see what changed")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
