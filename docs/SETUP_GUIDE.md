# Seer v0 — Setup Guide

*For Paul. Plain English. No assumptions about terminal experience.*

---

## What you have

Everything in this `seer-v0` folder is ready to use. The schemas, scripts, docs, and folder structure are complete. What's missing is connecting this folder to a public GitHub repository so your forecasts become verifiable.

---

## Step 1: Open Terminal

On your Mac:
- Press **Cmd + Space** (opens Spotlight)
- Type **Terminal**
- Press Enter

You'll see a window with a text prompt. That's where you'll type commands.

---

## Step 2: Check that Git and Python work

Type each of these and press Enter:

```
git --version
```

You should see something like `git version 2.x.x`. If you get an error, macOS will prompt you to install Command Line Tools — say yes and wait for it to finish.

```
python3 --version
```

You should see `Python 3.x.x`. This should already be on your Mac.

---

## Step 3: Create the GitHub repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Settings:
   - **Repository name:** `seer-registry`
   - **Description:** `Public forecast registry — structural forecasting powered by Genesis Theory`
   - **Public** (this is your public ledger — it must be public)
   - Do NOT check "Add a README file" (we already have one)
   - Do NOT add .gitignore or license (we'll handle these)
4. Click **Create repository**
5. You'll see a page with setup instructions. Keep this page open — you'll need the URL it shows.

---

## Step 4: Connect your local folder to GitHub

In Terminal, navigate to the seer-v0 folder. The exact path depends on where your Seer workspace folder is. It's probably something like:

```
cd ~/Documents/Seer/seer-v0
```

If you're not sure where it is, open Finder, navigate to the seer-v0 folder, then drag the folder icon onto the Terminal window — it will paste the path for you. Then type `cd ` (with a space) before it and press Enter.

Now run these commands one at a time:

```
git init
```
This creates a new Git repository in the folder.

```
git add .
```
This stages all the files.

```
git commit -m "Initial commit: Seer v0 infrastructure"
```
This creates your first commit.

```
git branch -M main
```
This names your branch "main".

```
git remote add origin https://github.com/YOUR_USERNAME/seer-registry.git
```
**Replace YOUR_USERNAME with your actual GitHub username.** The exact URL is on the GitHub page you kept open.

```
git push -u origin main
```
This pushes everything to GitHub. It may ask for your GitHub credentials the first time.

**If it asks for a password:** GitHub no longer accepts passwords for terminal access. You'll need to create a Personal Access Token:
1. Go to github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "seer-terminal"
4. Check the "repo" scope
5. Click Generate token
6. **Copy the token immediately** (you won't see it again)
7. When Terminal asks for your password, paste the token instead

---

## Step 5: Verify it worked

Go to `https://github.com/YOUR_USERNAME/seer-registry` in your browser. You should see:
- The README rendering as a nice page with the Forecast Registry table
- The `forecasts/`, `schemas/`, `scripts/`, and `docs/` folders
- The scoring policy and operator checklist

If you see all that — you're live. The registry is public and the infrastructure is ready.

---

## Day-to-day usage

### Running a prediction

After completing a protocol run in Claude and exporting the JSON files:

```
cd ~/Documents/Seer/seer-v0
python3 scripts/lock.py spec my_spec.json
python3 scripts/lock.py evidence my_evidence.json --forecast-id SEER-2026-0001
python3 scripts/lock.py forecast my_forecast.json --forecast-id SEER-2026-0001
```

### Publishing to the registry

```
git add forecasts/SEER-2026-0001.json
git commit -m "Lock SEER-2026-0001: Tesla trajectory 18mo"
git push
```

### Scoring a resolved forecast

```
python3 scripts/score.py SEER-2026-0001 my_outcome.json
git add forecasts/SEER-2026-0001.json
git commit -m "Score SEER-2026-0001: 0.72 forecast, +0.12 differential"
git push
```

---

## If something goes wrong

- **"not a git repository"** — you're in the wrong folder. `cd` to the seer-v0 directory.
- **"Permission denied"** — your GitHub token may have expired. Generate a new one.
- **"merge conflict"** — this shouldn't happen since you're the only operator. If it does, ask me.
- **Any Python error** — copy the full error message and bring it here. I'll fix it.

---

## What NOT to worry about

- Branches, pull requests, issues, actions, CI/CD — none of that matters for v0.
- You don't need to understand Git internals. You need three commands: `git add`, `git commit`, `git push`.
- The folder structure and scripts handle everything else.

---

*This guide assumes macOS. If you're on a different system, the commands are nearly identical — let me know and I'll adjust.*
