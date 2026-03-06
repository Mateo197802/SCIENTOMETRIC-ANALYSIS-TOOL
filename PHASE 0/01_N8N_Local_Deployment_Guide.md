# Technical Guide: Hosting n8n Locally (Step-by-Step)

This guide provides a professional, detailed walkthrough on deploying and hosting n8n (Node-based Workflow Automation) locally on your machine. Running n8n locally ensures data privacy, removes execution limits, and avoids cloud-hosting costs.

We will use Docker for the deployment. In a professional environment, Docker is the industry standard as it provides process isolation, facilitates dependency management, and operates securely in the background.

---

## Prerequisites

Before proceeding, ensure your system meets the following requirements:

1. **Operating System:** Windows 10/11 (Pro/Enterprise/Education with Hyper-V or Home with WSL2 enabled).
2. **Hardware:** At least 4GB of RAM and a modern multi-core CPU.
3. **Software:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running.

---

## Step 1: Install Docker Desktop

1. Download the Docker Desktop for Windows installer from the official website.
2. Run the installer. Leave the default options checked (especially "Use WSL 2 instead of Hyper-V" if prompted).
3. Once the installation is complete, restart your computer if required.
4. Open the Docker Desktop application. Wait until the application indicates "Engine Running".

> [!TIP]
> **WSL2 Verification:** On Windows, Docker relies on the Windows Subsystem for Linux (WSL2). If Docker prompts you to update the WSL kernel, follow the provided link, run the installer, and restart Docker.

---

## Step 2: Set Up the n8n Project Directory

To ensure configurations, credentials, and workflows are securely persisted (even if the container restarts), a dedicated directory must be established.

1. Create a new folder on your computer to store n8n data.
   - *Example:* `C:\n8n-local`
2. Inside this folder, create a new plain text file and name it `docker-compose.yml`.
   > **Note:** Ensure Windows is not hiding file extensions, to prevent the file from accidentally being named `docker-compose.yml.txt`.

---

## Step 3: Configure the Docker Compose File

Open the `docker-compose.yml` file using a professional text editor (such as Visual Studio Code) and paste the following configuration:

```yaml
version: '3.8'

volumes:
  n8n_data:

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n_local
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=America/Guayaquil
    volumes:
      - n8n_data:/home/node/.n8n
```

### Configuration Breakdown

- **`restart: always`**: Ensures the service runs continuously in the background and starts on boot.
- **`ports`**: Maps the internal container port (5678) to your local machine (5678).
- **`volumes`**: Creates a persistent storage volume (`n8n_data`) to safeguard workflows and settings.
- **`GENERIC_TIMEZONE`**: Essential for the proper functioning of scheduled triggers (e.g., cron jobs).

---

## Step 4: Launching n8n

With the configuration ready, proceed to deploy the application.

1. Open a terminal (Command Prompt or PowerShell).
2. Navigate to the project directory created in Step 2:

   ```bash
   cd C:\n8n-local
   ```

3. Run the following command to download the n8n image and start the container in detached mode:

   ```bash
   docker-compose up -d
   ```

4. Docker will download the n8n image. This process may take several minutes depending on network bandwidth.

Upon completion, the terminal will output `Started n8n_local`.

---

## Step 5: Initial Setup and Configuration

1. Open your preferred web browser.
2. Navigate to the local URL: **`http://localhost:5678`**
3. The n8n setup screen will appear.
4. **Create the Owner Account:**
   - Enter your email address, first and last name, and a secure password.
   - *Note: As this is a local deployment, these credentials are kept strictly on your machine.*

> [!IMPORTANT]
> Secure your password carefully. This account protects your API keys and workflows from unauthorized local access.

---

## How to Stop or Update n8n

### Stopping the Server

To halt the n8n instance and conserve system resources, open PowerShell in the `C:\n8n-local` directory and execute:

```bash
docker-compose down
```

### Updating n8n to the Latest Version

To keep n8n current with the latest updates and security patches, execute the following commands in your project directory:

```bash
docker-compose pull
docker-compose up -d
```

This process downloads the updated version and restarts the application while preserving your persistent volumes.

---

**Success:** You have established a robust, production-grade local deployment of n8n. The system is now ready for workflow importation and configuration.
