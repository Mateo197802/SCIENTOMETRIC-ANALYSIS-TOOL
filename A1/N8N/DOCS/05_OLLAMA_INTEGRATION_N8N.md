# Technical Guide: Local LLM Integration with Ollama for n8n

The A1 pipeline uses **Azure OpenAI** by default to read the collected academic metrics (affiliations, interests, keywords) and rigidly classify the author into specific scientific domains. To avoid commercial API usage costs, you can completely replace Azure OpenAI with a local language model utilizing **Ollama**.

---

## Phase 1: Installing Ollama and the Model

1. **Download:** Navigate to [ollama.com](https://ollama.com/) and acquire the installer for your OS.
2. **Install:** Execute the installer.
3. **Verify and Download Model:** Open a terminal (PowerShell or CMD) and initialize the download of a fast, instruction-following model like Llama 3:

   ```bash
   ollama run llama3
   ```

4. A progress bar will track the download. Once downloaded, you'll see a `>>>` prompt. Use `Ctrl + D` to exit. The model is now running permanently in the background at `localhost:11434`.

---

## Phase 2: Docker Network Bridging (Pre-configured)

When n8n is hosted via Docker, it operates in an isolated virtual network and cannot read `localhost` directly.

Our provided `docker-compose.yml` file already handles this natively via the `host.docker.internal:host-gateway` parameter. No further manual docker configuration is required.

---

## Phase 3: Swapping Nodes in the n8n Canvas

With Ollama active, proceed to exchange the cloud-based AI node for the local LLM inside your imported n8n workflow.

1. Open your n8n canvas (`http://localhost:5678`).
2. Locate the **"Profile Classification"** node (The Information Extractor node tied to Azure OpenAI).
3. Open the **Node Search** panel (`+` button) and find the **"Ollama Chat Model"** node.
4. Drag and drop the **Ollama Chat Model** onto the canvas.
5. Disconnect the input link from the *Azure OpenAI Chat Model* and reconnect it to the *Ollama Chat Model*.
6. Double-click your new **Ollama Chat Model** node to configure it:
   - **Base URL:** Input `http://host.docker.internal:11434` *(If running n8n via Docker)* or `http://localhost:11434` *(If running n8n directly on Windows via npm)*.
   - **Model:** Type the exact string you downloaded (e.g., `llama3`).
   - **Temperature:** Configure statically as `0` to enforce maximum determinism based purely on the prompt taxonomy.
7. You may now delete the defunct `Azure OpenAI Chat Model` node and its Credentials.

Save the workflow. Your entire pipeline is now running 100% locally and free of charge.
