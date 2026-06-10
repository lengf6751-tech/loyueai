import subprocess, os

token = open(os.path.expanduser("~/cf_token.txt")).read().strip()
env = os.environ.copy()
env["CLOUDFLARE_API_TOKEN"] = token

result = subprocess.run(
    ["npx.cmd", "wrangler", "pages", "deploy", ".", "--project-name=loyueai", "--branch=main"],
    cwd=r"D:\Hermes Agent\loyueai-pages-deploy",
    env=env,
    capture_output=True,
    text=True,
    timeout=120
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[-500:])
print("EXIT:", result.returncode)
