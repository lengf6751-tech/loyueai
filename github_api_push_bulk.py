import urllib.request, json, base64, os, re

REPO = "lengf6751-tech/loyueai"
BRANCH = "main"
DEPLOY_DIR = r"D:\Hermes Agent\loyueai-pages-deploy"

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

# Get base
ref = gh_api("GET", f"git/refs/heads/{BRANCH}")
base_sha = ref["object"]["sha"]
base_tree = gh_api("GET", f"git/commits/{base_sha}")["tree"]["sha"]
print(f"Base: commit={base_sha[:12]}, tree={base_tree[:12]}")

FILES = ["blog/divination/28-constellations.html", "blog/divination/bazi-compatibility.html", "blog/divination/bazi-day-master-guide.html", "blog/divination/bazi-four-pillars.html", "blog/divination/bazi-luck-cycles.html", "blog/divination/chinese-metaphysics-vs-western.html", "blog/divination/chinese-zodiac.html", "blog/divination/divination-birthstone-meanings.html", "blog/divination/divination-lucky-numbers.html", "blog/divination/divination-palm-reading-secrets.html", "blog/divination/face-moles-reading.html", "blog/divination/face-reading-basics.html", "blog/divination/face-reading-ears-eyebrows.html", "blog/divination/feng-shui-colors-directions.html", "blog/divination/feng-shui-home-basics.html", "blog/divination/five-elements-daily-life.html", "blog/divination/how-to-ask-divination.html", "blog/divination/learn-own-bazi-chart.html", "blog/divination/qimen-daily-applications.html", "blog/divination/qimen-dunjia.html", "blog/divination/qimen-eight-doors-guide.html", "blog/divination/taoism-divination-roots.html", "blog/divination/wu-xing-five-elements.html", "blog/divination/yin-yang-balance.html", "blog/divination/zhouyi-i-ching-beginners.html", "blog/divination/zhouyi-intro.html", "blog/divination/ziwei-12-palaces-extended.html", "blog/divination/ziwei-12-palaces.html", "blog/divination/ziwei-14-major-stars.html", "blog/divination/ziwei-si-hua.html", "blog/divination/zodiac-2026-predictions.html", "blog/divination/zodiac-love-compatibility.html", "blog/dream/color-symbolism-dreams.html", "blog/dream/colors-emotions-in-dreams.html", "blog/dream/common-dream-symbols-a-z.html", "blog/dream/dream-blood.html", "blog/dream/dream-chased.html", "blog/dream/dream-dead.html", "blog/dream/dream-exam.html", "blog/dream/dream-falling.html", "blog/dream/dream-fire.html", "blog/dream/dream-floods.html", "blog/dream/dream-flying.html", "blog/dream/dream-ghosts.html", "blog/dream/dream-houses-rooms.html", "blog/dream/dream-journal-mastery.html", "blog/dream/dream-marriage.html", "blog/dream/dream-money.html", "blog/dream/dream-pregnancy.html", "blog/dream/dream-snakes.html", "blog/dream/dream-teeth.html", "blog/dream/dream-water.html", "blog/dream/how-to-decode-dreams.html", "blog/dream/how-to-remember-dreams.html", "blog/dream/lucid-dreaming-chinese-methods.html", "blog/dream/nightmares-to-wisdom.html", "blog/dream/recurring-dreams-decoded.html", "blog/dream/recurring-dreams-guide.html", "blog/dream/top-10-common-dreams.html"]

tree_items = []
for fpath in FILES:
    full = os.path.join(DEPLOY_DIR, fpath)
    with open(full, "rb") as fh:
        raw = fh.read()
    blob = gh_api("POST", "git/blobs", {
        "content": base64.b64encode(raw).decode("ascii"),
        "encoding": "base64",
    })
    tree_items.append({
        "path": fpath,
        "sha": blob["sha"],
        "mode": "100644",
        "type": "blob",
    })
    print(f"  [{len(tree_items)}/{len(FILES)}] {fpath} ({len(raw)}b)")

tree = gh_api("POST", "git/trees", {"base_tree": base_tree, "tree": tree_items})
print(f"Tree: {tree['sha'][:12]}")

commit = gh_api("POST", "git/commits", {
    "message": "seo: optimize titles and meta descriptions with keyword targeting (59 articles)",
    "tree": tree["sha"],
    "parents": [base_sha],
})
print(f"Commit: {commit['sha'][:12]}")

gh_api("PATCH", f"git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False})
print("\n=== PUSH SUCCESSFUL! 59 files deployed. ===")
