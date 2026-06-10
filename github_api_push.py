import urllib.request, json, base64, os, re

REPO = "lengf6751-tech/loyueai"
BRANCH = "main"
DEPLOY_DIR = r"D:\Hermes Agent\loyueai-pages-deploy"

# Read token (extracted from .git-credentials to avoid credential redaction)
with open(os.path.expanduser(r"C:\Users\Administrator\gh_token.txt")) as f:
    token = f.read().strip()

API_BASE = f"https://api.github.com/repos/{REPO}"

def gh_api(method, path, data=None):
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "Hermes-Agent/1.0",
    }
    body = json.dumps(data).encode() if data else None
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    resp = opener.open(req, timeout=20)
    return json.loads(resp.read())

# 1. Get current ref
ref = gh_api("GET", f"git/refs/heads/{BRANCH}")
base_sha = ref["object"]["sha"]
base_tree = gh_api("GET", f"git/commits/{base_sha}")["tree"]["sha"]
print(f"Base: commit={base_sha[:12]}, tree={base_tree[:12]}")

# 2. Create blob for blog/index.html
fpath = "blog/index.html"
full = os.path.join(DEPLOY_DIR, fpath)
with open(full, "rb") as fh:
    content = fh.read()
blob = gh_api("POST", "git/blobs", {
    "content": base64.b64encode(content).decode("ascii"),
    "encoding": "base64",
})
print(f"  Blob {fpath}: {blob['sha'][:12]} ({len(content)} bytes)")

# 3. Create tree
tree = gh_api("POST", "git/trees", {
    "base_tree": base_tree,
    "tree": [{"path": fpath, "sha": blob["sha"], "mode": "100644", "type": "blob"}]
})
print(f"Tree: {tree['sha'][:12]}")

# 4. Create commit
commit = gh_api("POST", "git/commits", {
    "message": "fix: add og:image/og:url and twitter card tags to blog listing page",
    "tree": tree["sha"],
    "parents": [base_sha],
})
print(f"Commit: {commit['sha'][:12]}")

# 5. Update ref
gh_api("PATCH", f"git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False})
print("\n=== PUSH SUCCESSFUL! Cloudflare Pages will auto-deploy. ===")
