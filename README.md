# Mini Todo — learn App Dev + DevOps + Cloud in one tiny project

```
 You write code ──► git push ──► GitHub Actions (CI/CD) ──► Render (cloud) ──► public URL
                                   1. run tests
                                   2. build Docker image + smoke test
                                   3. trigger deploy
```

## Project files

| File | What it teaches |
|------|-----------------|
| `app.py` | **App development**: a web page plus a REST API (GET/POST/PATCH/DELETE), a `/health` endpoint, config from env vars, logging |
| `test_app.py` | **Automated testing**: catch bugs before they reach users |
| `requirements.txt` | **Dependency management** |
| `Dockerfile` | **Containers**: package the app so it runs the same everywhere |
| `.github/workflows/ci.yml` | **CI/CD pipeline**: test → build → deploy on every push |

---

## Step 1 — Run it locally (Python only)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest -v            # run tests
python app.py        # open http://localhost:5000
```
Also try http://localhost:5000/health and http://localhost:5000/api/todos.

**Concepts:** virtual environment, dependencies, REST API, JSON, health check.
**Try:** add a todo, restart the app, and see the todo disappear. Memory is not storage, so real apps use a database.

## Step 2 — Containerize it (Docker)

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), then:
```powershell
docker build -t mini-todo .
docker run -p 8080:8080 mini-todo        # open http://localhost:8080
docker run -p 8080:8080 -e APP_VERSION=2.0 mini-todo   # config via env var
```
**Concepts:** image vs container, layers and caching, port mapping, env-var config, non-root user.

## Step 3 — Version control (Git + GitHub)

Install [Git](https://git-scm.com/download/win) and create a free GitHub account. Then create an **empty** repo named `mini-todo` and run:
```powershell
git init
git add .
git commit -m "Mini todo app"
git branch -M main
git remote add origin https://github.com/<you>/mini-todo.git
git push -u origin main
```
Open the **Actions** tab in your repo to watch the pipeline run. The deploy step is skipped until Step 5.

**Concepts:** commits, remote repos, CI runs automatically on push.
**Try:** break a test on purpose (e.g. change `"ok"` to `"okay"` in `app.py`), push, and watch CI go red. Fix it and watch it go green.

## Step 4 — Deploy to the cloud (Render, free tier)

1. Sign up at https://render.com with your GitHub account.
2. **New → Web Service**, pick your `mini-todo` repo.
3. Render detects the `Dockerfile` automatically. Choose the **Free** instance type.
4. Under **Environment**, add `APP_VERSION = 1.0.0`.
5. Set **Health Check Path** to `/health`.
6. Click **Create**. In a few minutes you get a public URL such as `https://mini-todo-xxxx.onrender.com` 🎉

**Concepts:** PaaS (Platform-as-a-Service), build logs, runtime logs, env vars and secrets in the cloud, health checks, HTTPS for free.
**Note:** free instances sleep when idle, so the first request after sleeping takes about 30 seconds.

## Step 5 — Full CD: deploy only when tests pass

1. In Render, open your service → **Settings** → set **Auto-Deploy = No**, then copy the **Deploy Hook URL**.
2. In GitHub, open the repo → **Settings → Secrets and variables → Actions** → add a secret named `RENDER_DEPLOY_HOOK_URL` with that URL.
3. Push a change. From now on, the pipeline runs tests → Docker build → deploy. Broken code never reaches production.

**Concepts:** continuous deployment, secrets management, pipeline gates.

---

## Next challenges (pick any)
- Change something visible (title, color), push, and watch it go live automatically.
- Add a `/version` endpoint and a test for it.
- Replace in-memory storage with SQLite, then a hosted Postgres database (Render offers one for free).
- Push the image to a registry (GitHub Container Registry) from CI.
- Deploy the same container to **AWS App Runner**, **Google Cloud Run** or **Azure Container Apps**. It's the same Dockerfile on a different cloud, which shows why containers matter.
- Add a free uptime monitor (e.g. UptimeRobot) that pings `/health`.
