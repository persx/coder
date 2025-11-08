import os, json, subprocess, pathlib, tempfile, textwrap, yaml
from typing import Dict, Any
import httpx
from anthropic import Anthropic

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)

class Env:
    model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")
    repo_url = os.getenv("TARGET_REPO_URL")
    owner_repo = os.getenv("TARGET_OWNER_REPO")  # e.g. persx/persx
    pr_base = os.getenv("PR_BASE","main")
    task_file = os.getenv("TASK_FILE","tasks/persx.yaml")
    safeops_file = os.getenv("SAFEOPS","configs/safeops_persx.json")
    loops = int(os.getenv("MAX_LOOPS","10"))
    budget_tokens = int(os.getenv("ANTHROPIC_BUDGET_TOKENS","0"))
    api_key = os.environ["ANTHROPIC_API_KEY"]
    gh_token = os.environ["GH_TOKEN"]

def gh_api(method, path, body=None):
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
        return {"ok": True}

    def run_checks(self)->Dict[str,Any]:
        out = {}
        # install deps if package.json exists
        if (self.repo_dir / "package.json").exists():
            out["npm_ci"] = run(["bash","-lc","npm ci --no-audit --no-fund"], cwd=self.repo_dir).returncode
            lint = run(["bash","-lc","npm run -s lint"], cwd=self.repo_dir)
            build = run(["bash","-lc","npm run -s build"], cwd=self.repo_dir)
            out.update({
                "lint_rc": lint.returncode, "lint": (lint.stdout+lint.stderr)[-8000:],
                "build_rc": build.returncode, "build": (build.stdout+build.stderr)[-8000:]
            })
        else:
            out["note"] = "No package.json; skipping JS checks."
        return out

    def open_pr(self, title: str, body: str, branch: str)->Dict[str,Any]:
        run(["git","checkout","-b",branch], cwd=self.repo_dir)
        run(["git","add","-A"], cwd=self.repo_dir)
        commit = run(["bash","-lc",f'git commit -m "{title}"'], cwd=self.repo_dir)
        if commit.returncode != 0:
            return {"error":"nothing to commit?"}
        run(["git","push","-u","origin",branch], cwd=self.repo_dir)
        pr = gh_api("POST", f"/repos/{Env.owner_repo}/pulls", {
            "title": title, "body": body, "head": branch, "base": Env.pr_base, "draft": True
        })

        # Add bot label to PR and assign reviewer
        pr_number = pr.get("number")
        if pr_number:
            try:
                gh_api("POST", f"/repos/{Env.owner_repo}/issues/{pr_number}/labels",
                       {"labels": ["bot"]})
            except Exception:
                pass  # Label might not exist yet

            # Assign owner as reviewer
            try:
                owner = Env.owner_repo.split('/')[0]
                gh_api("POST", f"/repos/{Env.owner_repo}/pulls/{pr_number}/requested_reviewers",
                       {"reviewers": [owner]})
            except Exception:
                pass  # Owner might not have access or API might fail

        # Send notification to Slack/Teams if webhook configured
        webhook_url = os.getenv("SLACK_WEBHOOK_URL") or os.getenv("TEAMS_WEBHOOK_URL")
        if webhook_url and pr.get("html_url"):
            try:
                notification = {
                    "text": f"🤖 New bot PR: {title}\n{pr['html_url']}\n\n{body[:200]}..."
                }
                httpx.post(webhook_url, json=notification, timeout=10)
            except Exception:
                pass  # Don't fail PR creation if notification fails

        return {"url": pr.get("html_url",""), "number": pr_number}

    def _allowed(self, rel_path: str)->bool:
        from fnmatch import fnmatch
        for pat in self.safeops.get("forbidden", []):
            if fnmatch(rel_path, pat): return False
        allowed = self.safeops.get("allowed_globs")
        if not allowed: return True
        return any(fnmatch(rel_path, pat) for pat in allowed)

# ---------- Orchestrator ----------
def main():
    client = Anthropic(api_key=Env.api_key)

    safeops = json.loads(pathlib.Path(Env.safeops_file).read_text())
    backlog = pathlib.Path(Env.task_file).read_text()

    work = pathlib.Path(tempfile.mkdtemp())
    repo_dir = work / "repo"
    run(["bash","-lc",f"git clone {Env.repo_url} repo"], cwd=work)
    run(["git","config","user.email","bot@example"], cwd=repo_dir)
    run(["git","config","user.name","claude-bot"], cwd=repo_dir)
    run(["git","remote","set-url","--push","origin",f"https://x-access-token:{Env.gh_token.split(':')[-1]}@github.com/{Env.owner_repo}.git"], cwd=repo_dir)

    tools = Tools(repo_dir, safeops)

    TOOL_DECL = [
        {"name":"read_repo","description":"Read repository source by glob.","input_schema":{"type":"object","properties":{"glob":{"type":"string"}}}},
        {"name":"write_file","description":"Write or overwrite a file relative to repo root.","input_schema":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}},
        {"name":"run_checks","description":"Run npm lint/build if package.json exists.","input_schema":{"type":"object","properties":{}}},
        {"name":"open_pr","description":"Commit changes and open a draft PR.","input_schema":{"type":"object","properties":{"title":{"type":"string"},"body":{"type":"string"},"branch":{"type":"string"}},"required":["title","branch"]}}
    ]

    SYSTEM = textwrap.dedent(f"""        You are a cautious coding agent for web frontends (Next.js/React/TS) and Node services.
    Respect these guardrails:
{json.dumps(safeops)}

    Rules:
    - Make only tiny, reversible improvements (tests, docs, a11y, SEO, refactors).
    - Keep diffs under {safeops.get('max_loc', 400)} LOC.
    - Never touch forbidden globs. If a task requires it, explain and stop.
    - Always run checks before opening PRs; leave draft PR with risk notes and change summary.
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
        resp = client.messages.create(
            model=Env.model,
            system=SYSTEM,
            max_tokens=1800,
            tools=TOOL_DECL,
            messages=messages
        )
        # Track token usage
        total_tokens += resp.usage.input_tokens + resp.usage.output_tokens
        if Env.budget_tokens > 0 and total_tokens > Env.budget_tokens:
            print(f"Budget exceeded: {total_tokens}/{Env.budget_tokens} tokens")
            break

        part = resp.content[0]
        if part.type == "tool_use":
            result = call_tool(part.name, part.input or {})
            messages.append({"role":"tool","tool_use_id": part.id, "content": json.dumps(result)})
            continue
        break

    print(f"Total tokens used: {total_tokens}")

if __name__ == "__main__":
    main()
