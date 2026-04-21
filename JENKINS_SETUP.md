# Jenkins Job Setup Guide

## How to Create the Pipeline Job in Jenkins UI

Follow these steps to create your testforge-ai-pipeline job:

### Step 1: Create New Job
1. Go to **http://localhost:8080**
2. Click **New Item** (top left)
3. Enter job name: `testforge-ai-pipeline`
4. Select **Pipeline**
5. Click **OK**

### Step 2: Configure Pipeline
In the job configuration page:

1. **Description:** Add this:
   ```
   TestForge-AI CI/CD Pipeline with Ollama Error Analysis
   Automatically runs tests, analyzes errors with Ollama AI, and generates test cases
   ```

2. **Pipeline section** (scroll down to the bottom):
   - Select: **Pipeline script from SCM**
   - SCM: Select **Git**
   - Repository URL: `https://github.com/dayacode12/testforge-ai.git`
   - Credentials: Leave empty (public repo)
   - Branch: `*/master`
   - Script Path: `Jenkinsfile`

3. Click **Save**

### Step 3: Run the Job
1. Click **Build Now** on the job page
2. Watch the console output in real-time
3. The pipeline will:
   - Clone your repo
   - Build Docker image
   - Run tests
   - Send errors to Ollama
   - Generate test cases via TestForge-AI

### Step 4: View Results
- Click on the build number (e.g., #1)
- Click **Console Output** to see full logs
- Look for:
  - ✅ Build success/failure
  - 🤖 Ollama analysis
  - 📋 Test case generation results

## What the Pipeline Does

```
Checkout Code
    ↓
Build Docker Image
    ↓
Run Tests (with intentional errors)
    ↓
Send errors to Ollama for AI analysis
    ↓
Generate test cases via TestForge-AI
    ↓
Archive logs and results
```

## Troubleshooting

**Issue: "docker: command not found"**
- Jenkins needs Docker access
- Restart Jenkins or use the Docker socket mount

**Issue: "Connection refused to ollama:11434"**
- Make sure ollama container is running on shared-network
- Check: `docker network inspect shared-network`

**Issue: "Cannot pull from GitHub"**
- Repo is public, should work without credentials
- Check internet connection inside Jenkins container

---

That's it! Your CI/CD pipeline is ready to use.
