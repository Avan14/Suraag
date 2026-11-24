# Deploying Suraag on Streamlit Community Cloud

The app is one file (`app.py`) and needs no database. Cases are pre-generated in `cases/`, so the demo works
even when the Gemini API is down or out of quota (the app falls back to cached replies and stub filler).

## Steps (about 10 minutes)

1. Push `main` to GitHub (`git push origin main`). The repository must be public for a free deploy.
2. Go to https://share.streamlit.io and sign in with GitHub. Click **Create app**, then **Deploy a public app from GitHub**.
3. Repository `Avan14/Suraag`, branch `main`, main file path `app.py`.
4. Open **Advanced settings**:
   - Python version: **3.12**.
   - Secrets (paste as TOML):
     ```toml
     GEMINI_API_KEY = "paste a key from a project that has the free tier"
     SURAAG_MODEL_FILLER = "gemini-3.5-flash"
     SURAAG_MODEL_SOLVER = "gemini-3.6-flash"
     ```
5. Click **Deploy**. The first build takes a few minutes.

## Before you share the link

- Open the URL in a private window on a phone. It must load with no login.
- Sample case: generate, plant a defect, watch it get flagged, repaired and turn green.
- Student tab: cite a wrong line and read the explanation. Switch to Hindi and repeat.
- Download the case ZIP and recompute one SHA-256 against `manifest.json`.
- Switch the key off (delete the secret, reboot the app) and confirm the sample cases still open.

## Limits and safety

- `DAILY_CAP = 20` generations a day per app instance (`app.py`). The free key allows about 20 requests per model per day,
  so the cap protects the demo from running dry during judging. Plan for that by using pre-generated cases in the video.
- Never commit `.env` or `.streamlit/secrets.toml` (both are gitignored). Secrets live only in the Streamlit dashboard.
- Every case, file and screen is labelled SYNTHETIC. Hashes show a file has not changed since sealing; they do not show who made it.

## If the deploy fails

- "Module not found": check `requirements.txt` was pushed (versions are pinned to the tested set).
- Python version error: set 3.12 in Advanced settings (redeploy the app to change it).
- Blank page with a component error: confirm `suraag/components/canvas` and `suraag/components/speak` are in the repo.
