# Technical Guide: Hosting n8n Locally (Docker Compose)

Running n8n locally ensures data privacy, removes execution limits, and avoids any cloud-hosting costs while securely containing your API keys locally. We use Docker Compose for an industry-standard containerized deployment.

---

## Prerequisites

1. **Operating System:** Windows 10/11 (Pro/Enterprise/Education with Hyper-V or Home with WSL2 enabled), macOS, or Linux.
2. **Software:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running.

---

## Step 1: Initialize Docker

1. Open the Docker Desktop application and wait until the indicator shows "Engine Running".

---

## Step 2: Launching n8n via Docker Compose

Included in this `A1\N8N` directory is a pre-configured `docker-compose.yml` file. This file contains the architecture to deploy n8n permanently, persist your sensitive data across reboots, and establish an internal network bridge (via `extra_hosts`) to allow n8n to communicate with local LLMs (like Ollama).

1. Open a terminal (Command Prompt or PowerShell).
2. Navigate to the `A1\N8N` directory where the `docker-compose.yml` file resides:

   ```bash
   cd "C:\Users\intel\OneDrive - yachaytech.edu.ec\Escritorio\Scientometric Analysis Tool\SCIENTOMETRIC ANALYSIS TOOL\A1\N8N"
   ```

   *(Adjust the path if you moved the folder).*
3. Run the following command to download the n8n image and start the container in detached mode:

   ```bash
   docker-compose up -d
   ```

4. Docker will download the n8n image automatically.

---

## Step 3: Initial Setup and Configuration

1. Open your specific web browser.
2. Navigate to the local URL: **`http://localhost:5678`**
3. The n8n setup screen will appear.
4. **Create the Owner Account:** Enter your email address and a secure password. *(As this is a local deployment, these credentials are kept strictly on your machine).*

---

## Step 4: Maintenance Commands

### Stopping the Server

To halt the n8n instance and conserve RAM:

```bash
docker-compose down
```

### Updating n8n

To keep n8n current with the latest updates:

```bash
docker-compose pull
docker-compose up -d
```

---
**Success:** You have established a robust, local deployment of n8n. You are now ready to import the `A1 SCIENTOMETRIC ANALYSIS TOOL .json` workflow file into the canvas.
