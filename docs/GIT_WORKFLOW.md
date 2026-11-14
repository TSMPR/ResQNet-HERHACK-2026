# Git and GitHub workflow (VS Code)

## 1. Install and configure Git
Install Git for Windows from https://git-scm.com/download/win. Restart VS Code after installation. In the VS Code terminal:

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

Use the email associated with your GitHub account (or GitHub's noreply email). Never put passwords or tokens in source files.

## 2. Initialize the project
Open the extracted `ResQNet` folder in VS Code, then run:

```bash
git init
git branch -M main
git status
git add .
git commit -m "chore: initialize ResQNet for HERHACK 2026"
```

Review `.gitignore` before `git add .`. Do not commit `.venv/`, `__pycache__/`, SQLite databases, uploads, secrets, or model weights.

## 3. Create a GitHub repository and connect it
Create an empty repository on GitHub (do not initialize it with another README if this local project already has one). Copy its HTTPS URL, then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/ResQNet.git
git push -u origin main
```

Replace the example URL with your repository URL. Authenticate through Git Credential Manager/browser prompt; never paste a personal access token into code or chat.

## 4. Work safely with teammates
Each teammate creates a branch:

```bash
git switch -c feature/api
# or feature/dashboard, feature/ml-evaluation, feature/docs
```

After making changes:

```bash
git status
git add path/to/changed-file
git commit -m "feat: describe the change"
git push -u origin feature/api
```

Open a Pull Request on GitHub, request review, run tests, then merge. Avoid multiple teammates editing the same file simultaneously.

## 5. Pull the latest team changes

```bash
git switch main
git pull origin main
git switch feature/api
git merge main
```

Resolve conflicts carefully, run tests again, then push the branch.

## 6. Useful inspection commands

```bash
git status
git log --oneline --graph --decorate -10
git diff
git diff --staged
git branch
 git remote -v
```

If a secret or personal data was committed, deleting it in a later commit is not enough: revoke/rotate the secret and follow GitHub's sensitive-data removal guidance.
