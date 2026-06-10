import urllib.request, json, base64, os, subprocess

token = open(os.path.expanduser('C:/Users/Administrator/gh_token.txt')).read().strip()
API = 'https://api.github.com/repos/lengf6751-tech/loyueai'

def gh(m, p, d=None):
    url = API + p
    h = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'User-Agent': 'HA/1.0'}
    b = json.dumps(d).encode() if d else None
    if b: h['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=b, headers=h, method=m)
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return json.loads(op.open(req, timeout=20).read())

ref = gh('GET', '/git/refs/heads/main')
base = ref['object']['sha']
bt = gh('GET', '/git/commits/' + base)['tree']['sha']
print('Base:', base[:12], 'tree:', bt[:12])

out = subprocess.check_output(['git', '-C', r'D:\Hermes Agent\loyueai-pages-deploy', 'diff', '--name-only', 'HEAD~1']).decode().strip()
files = [f.strip() for f in out.split('\n') if f.strip()]
print(f'Files to push: {len(files)}')

items = []
for i, f in enumerate(files):
    full = os.path.join(r'D:\Hermes Agent\loyueai-pages-deploy', f)
    with open(full, 'rb') as fh:
        raw = fh.read()
    blob = gh('POST', '/git/blobs', {'content': base64.b64encode(raw).decode('ascii'), 'encoding': 'base64'})
    items.append({'path': f.replace('\\', '/'), 'sha': blob['sha'], 'mode': '100644', 'type': 'blob'})
    if (i+1) % 15 == 0:
        print(f'  {i+1}/{len(files)}')

tree = gh('POST', '/git/trees', {'base_tree': bt, 'tree': items})
print(f'Tree: {tree["sha"][:12]}')

commit = gh('POST', '/git/commits', {
    'message': 'seo: optimize titles and meta descriptions with keyword targeting (59 articles)',
    'tree': tree['sha'], 'parents': [base],
})
print(f'Commit: {commit["sha"][:12]}')

gh('PATCH', '/git/refs/heads/main', {'sha': commit['sha'], 'force': False})
print('\n=== PUSH SUCCESSFUL! 59 files deployed to Cloudflare Pages. ===')
