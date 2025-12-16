# Expense Tracker Monorepo

This repo contains three Python/FastAPI microservices:
- `auth`: credential and JWT issuance
- `users`: profile management (auth-protected)
- `expenses`: expense CRUD (auth-protected)

The scheduler folder currently holds a sample Airflow DAG and is not part of the deployment pipeline below.

## Local development
1. Create virtualenv and install for a service, e.g.:
   ```bash
   cd auth
   python -m venv .venv
   . .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   ```
2. Copy the sample env and fill in values:
   ```bash
   cp .env.example .env
   ```
3. Run the service:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   Health endpoints live at `/auth/health`, `/users/health`, `/expenses/health`.

## GitHub setup
1. Initialize and push:
   ```bash
   git init
   git add .
   git commit -m "chore: bootstrap infra for render/vercel deployments"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
2. Set the GitHub Action secrets listed under **CI/CD secrets**.

## CI (GitHub Actions)
- `.github/workflows/ci.yml` runs per-service installs, a quick import check, and `pytest` (if tests exist) on every push/PR.

## Deploy to Render
- `render.yaml` defines three Python web services (`auth`, `users`, `expenses`) with `rootDir` pointing at each folder and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- One-time setup:
  1. In Render, create three Web Services from this repo using the matching `rootDir` and choose Python runtime.
  2. Set env vars for each service (`AUTH_DATABASE_URL`, `USERS_DATABASE_URL`, `EXPENSES_DATABASE_URL`, `AUTH_JWT_*`). The blueprint marks them as `sync: false` so you provide the values in Render.
  3. Note each Render Service ID for CI/CD.
- To deploy manually: `render.yaml` can be used as a Blueprint, or trigger a deploy via `curl -X POST https://api.render.com/v1/services/<SERVICE_ID>/deploys`.

## Deploy to Vercel
Each service includes:
- `vercel.json` routing all traffic to a serverless function.
- `api/index.py` exposing `handler = Mangum(app)` so FastAPI runs on Vercel's Python runtime.

One-time setup per service:
1. Create a Vercel project and set **Root Directory** to the service folder (`auth`, `users`, `expenses`).
2. Add env vars matching the `.env.example` files.
3. Record the Project ID and your Org ID.
4. First deploy from the repo root:
   ```bash
   cd auth && vercel --prod
   cd ../users && vercel --prod
   cd ../expenses && vercel --prod
   ```

## CD (Render + Vercel)
- `.github/workflows/deploy.yml` deploys on pushes to `main` (or manual `workflow_dispatch`) to:
  - Render: triggers deploys via API per service.
  - Vercel: uses Vercel CLI per service with `--cwd`.

### CI/CD secrets to add in GitHub
- Render: `RENDER_API_KEY`, `RENDER_SERVICE_ID_AUTH`, `RENDER_SERVICE_ID_USERS`, `RENDER_SERVICE_ID_EXPENSES`
- Vercel: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID_AUTH`, `VERCEL_PROJECT_ID_USERS`, `VERCEL_PROJECT_ID_EXPENSES`

## Notes
- Do not commit real `.env` files or local databases (`*.db`). Use the `.env.example` files to share configuration keys.
- Rotate the secrets currently present in local `.env` files before pushing public code.
