# 🚀 Jenkins HTML Deployment on AWS EC2 (Amazon Linux)

This guide documents the step-by-step process I followed to deploy a static HTML website using **Jenkins** on an **Amazon EC2 (Amazon Linux)** instance.

---

## ✅ Prerequisites

- AWS account with an EC2 instance (Amazon Linux 2023, `t3.micro`)
- Port `8080` (Jenkins) and `80` (NGINX) allowed in **EC2 Security Group**
- GitHub repo with HTML files (e.g. `index.html`, `README.md`)
- Basic knowledge of Linux, Git, and shell scripting

---

## 🧱 Project Structure

Example:
```
jenkins-demo-app/
├── index.html
└── README.md
```

---

## ⚙️ Step 1: Launch EC2 and Install Jenkins

SSH into your EC2 instance:

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### Install Java (required by Jenkins)

```bash
sudo dnf install java-17-amazon-corretto -y
```

### Add Jenkins repo and install Jenkins

```bash
sudo curl --silent --location https://pkg.jenkins.io/redhat-stable/jenkins.io.key | sudo tee /etc/pki/rpm-gpg/RPM-GPG-KEY-jenkins.io
sudo curl --silent --location https://pkg.jenkins.io/redhat-stable/jenkins.repo | sudo tee /etc/yum.repos.d/jenkins.repo
sudo dnf upgrade
sudo dnf install jenkins -y
```

### Start and enable Jenkins

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

---

## 🌐 Step 2: Access Jenkins Dashboard

- Visit: `http://<your-ec2-ip>:8080/`
- Get the initial password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

- Complete the web UI setup and install **recommended plugins**

---

## 🌍 Step 3: Install and Start NGINX

```bash
sudo dnf install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

Verify: `http://<your-ec2-ip>/` should show NGINX welcome page.

---

## ⚠️ Step 4: Fix Port Conflicts

Ensure:
- Jenkins stays on port **8080**
- NGINX stays on port **80**

If needed, adjust `/etc/nginx/nginx.conf` to `listen 80;`

---

## 📂 Step 5: Create GitHub Repo

- Create a new repo: `jenkins-demo-app`
- Add your `index.html` and `README.md`
- Push to GitHub:

```bash
git init
git remote add origin https://github.com/Yoganandha-S/jenkins-demo-app.git
git add .
git commit -m "Initial HTML app"
git push -u origin main
```

---

## 🔧 Step 6: Create Jenkins Freestyle Job

1. From Jenkins Dashboard → New Item → **Freestyle project**
2. Name: `deploy-frontend`
3. Under **Source Code Management → Git**:
   - Repo URL: `https://github.com/Yoganandha-S/jenkins-demo-app.git`
   - Branch: `*/main`
4. Under **Build Triggers**:
   - [✔] GitHub hook trigger for GITScm polling

5. Under **Build → Execute Shell**:

```bash
#!/bin/bash
echo "Deploying frontend..."
DEST="/usr/share/nginx/html"
rm -rf $DEST/*
cp -r * $DEST/
echo "✅ Deployment complete!"
```

6. Click **Save**

---

## 🔁 Step 7: Setup GitHub Webhook (Auto Trigger)

1. Go to GitHub → Repo → **Settings → Webhooks → Add Webhook**
2. Payload URL:  
   ```
   http://<your-ec2-ip>:8080/github-webhook/
   ```
3. Content type: `application/json`
4. Trigger: `Just the push event`

---

## 🚀 Step 8: Test the Pipeline

Make a change:

```bash
echo "<!-- test -->" >> index.html
git commit -am "Test webhook"
git push
```

→ Jenkins should build and deploy automatically  
→ Visit `http://<your-ec2-ip>/` to see the updated site

---

## ✅ Troubleshooting I Did

| Issue                                | Fix                                                                 |
|-------------------------------------|----------------------------------------------------------------------|
| Jenkins node stuck "Waiting"        | Increased executors, lowered disk space threshold                   |
| NGINX port conflict with Jenkins    | Kept Jenkins on `:8080` and NGINX on `:80`                          |
| Jenkins node marked offline         | Cleaned `/tmp`, reduced free space thresholds in node config        |
| Build not triggering from GitHub    | Enabled webhooks and `GitHub hook trigger` in Jenkins job           |

---

## 🧩 Tools Used

- **AWS EC2** (Amazon Linux 2023)
- **Jenkins 2.504**
- **NGINX**
- **GitHub Webhooks**
- **Shell scripting**

---

## 📌 To show in python 

-**  sudo dnf install python3-pip -y

-**  sudo pip3 install markdown
