# Technical Guide: Local LLM Integration with Ollama

In the provided n8n workflow, an Artificial Intelligence node (specifically tasked via **Azure OpenAI gpt-4o-mini**) is utilized to analyze author affiliations and extract a standardized 2-letter ISO Country Code.

However, depending on proprietary APIs incurs recurring costs. This guide details how to implement **Ollama locally** on your workstation. Ollama is a framework that executes powerful Large Language Models (LLMs) such as *Llama 3* or *Mistral* entirely on local hardware, offering a secure, offline, and cost-free alternative that integrates directly with n8n.

---

## Phase 1: Installing Ollama

Ollama is a highly optimized framework that abstracts the complexity of running local inference models using native CPU and GPU resources.

1. **Download:** Navigate to [ollama.com/download](https://ollama.com/download) and acquire the Windows installer.
2. **Install:** Execute the installer (`OllamaSetup.exe`). Upon completion, the service runs implicitly in the system tray.
3. **Verify:** Open a PowerShell or Command Prompt terminal and input:

   ```bash
   ollama --version
   ```

   A returned version number confirms a successful installation and an active background service.

---

## Phase 2: Downloading an LLM

To reliably extract spatial data from unstructured text, a fast model capable of strict instruction adherence is required. **Llama 3.2** is highly recommended for semantic extraction pipelines.

1. Keep your terminal active.
2. Execute the following command to download and initialize the *Llama 3.2* model:

   ```bash
   ollama run llama3.2
   ```

3. A progress bar will track the download (approximately 2-3 GB of weights).
4. Once downloaded, the terminal will display a `>>>` execution prompt. You may input a test query, and then press `Ctrl + D` or type `/bye` to exit. The model is now permanently cached locally.

---

## Phase 3: Exposing Ollama to n8n (Docker bridging)

When hosting n8n via Docker (as outlined in the Local Deployment Guide), n8n operates within an isolated virtual network. Consequently, it cannot natively resolve `localhost:11434` (Ollama's default port) because traversing `localhost` within Docker points back to the container itself, not the Windows host.

### Solution: Route configuration

We must instruct n8n to direct standard traffic to the host Windows machine.

1. Open the n8n `docker-compose.yml` file.
2. Append the `extra_hosts` parameter to the `n8n` service block. The configuration should mirror this structure:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n_local
    restart: always
    ports:
      - "5678:5678"
    extra_hosts:               # Ensure this directive is added
      - "host.docker.internal:host-gateway" 
    environment:
      - N8N_HOST=localhost
      # ... (include preceding environmental flags)
```

3. Restart the n8n container to apply the changes by executing:

   ```bash
   docker-compose down
   docker-compose up -d
   ```

*(Note: If n8n was installed directly onto Windows via npm, bypassing Docker entirely, this network bridging phase is unnecessary).*

---

## Phase 4: Replacing Azure OpenAI with Ollama in n8n

With the local inference server active, proceed to exchange the cloud-based AI node for the local model within the n8n JSON architecture.

1. Open the n8n workflow editor.
2. Locate the **Information Extractor** node currently tethered to the **Azure OpenAI Chat Model** node.
3. Select the input connector on the **Information Extractor** node or utilize the node search panel to find the **Ollama Chat Model**.
4. Drag and drop the **Ollama Chat Model** onto the canvas.
5. Connect it to the AI input parameter of the **Information Extractor** node, replacing the Azure linkage.
6. Double-click the **Ollama Chat Model** node to access its properties:
   - **Base URL:** Input `http://host.docker.internal:11434` *(If operating via Docker)* OR `http://localhost:11434` *(If running n8n directly on Windows).*
   - **Model:** Specify the exact model string deployed earlier (e.g., `llama3.2`).
   - **Temperature:** Configure statically as `0`. *(This parameter enforces maximum determinism and logic, suppressing the probability of hallucinated outputs).*
7. Safely delete the defunct `Azure OpenAI Chat Model` node.

> [!TIP]
> **Performance Note:** When n8n triggers the LLM extraction protocol, computational demand will temporarily spike. Standard hardware may exhibit increased thermal thresholds (fan noise). If processing latency is substantial, close tertiary heavy applications or deploy a leaner model variant, such as `phi3`.

---

### Provisioning Azure OpenAI Alternatively

Should the speed and benchmark accuracy of a commercial AI be preferred (aligned with the original JSON design), retain the Azure node logic:

- Access the n8n **Credentials** menu.
- Configure a new **Azure OpenAI API** credential suite.
- Provide the Azure Resource Name, Deployment Name (`gpt-4o-mini`), and the designated API Key from your Azure tenant.

This modular architecture permits zero-cost local iteration via Ollama or enterprise-grade acceleration via Azure.
