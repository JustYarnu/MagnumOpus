# Overview
[![Style: Over-Engineered](https://img.shields.io/badge/code%20style-over--engineered-blueviolet)](#)
[![Efficiency: No](https://img.shields.io/badge/efficiency-no-red)](#)


In the contemporary landscape of digitized collaboration ecosystems, the performance metrics of an engineering asset are tragically reduced to a single, monolithic indicator: **The GitHub Contribution Graph**. 

MagnumOpus is a state-of-the-art Python program to simulate commit history via a line-to-line destructive pipeline to automate commits and pushes. Want to send the entiry bible in commits? You can do that.


## System Requirements
- Docker Engine
- Python 3.11+ 
- Git
- A willingness to accept that everything is technically a pipeline if you think about it long enough

## Installation Guide
### Step 1: Clone repository
```bash
git clone https://example.com/mocof.git
cd mocof
```

### Step 2: Initialize environment
```bash
cp .env.example .env
```

Fill in:
GITHUB_TOKEN=your_personal_access_token
GITHUB_REPO=https://github.com/your-user/your-repo.git

### Step 3: Put a .txt file in the project root
Can be any text file. Remember that commits are made on a line-to-line basis.

### Step 4: Configure
See configuration.

### Step 5: Deploy container
```bash
docker compose up --build
```

## Configuration

### Overview
```yaml
repo:
  path: "./" # Project root
  branch: "main" # Branch name

file:
  input_path: "./bibel.txt" #Path to the .txt file

commit:
  limit: 20 # Hard limit for commits
  push_interval: 10 # How many commits are made before a push
  delay_seconds: 3 # Timeout after a push
```
