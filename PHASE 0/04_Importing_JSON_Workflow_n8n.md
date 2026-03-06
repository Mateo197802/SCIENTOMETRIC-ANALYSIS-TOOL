# Technical Guide: Importing the Workflow JSON into n8n

n8n offers a highly efficient and declarative method for saving and sharing comprehensive automation networks via **JSON objects**. A large block of JSON code associated with n8n represents the precise nodes, parameters, and connections of a workflow.

This guide details the procedure for deploying raw JSON code—specifically formatted for the Scientometric Tool—directly into your n8n interface.

---

## Step 1: Prepare the JSON Code

Prior to accessing the interface, ensure the complete JSON file is ready.

1. Depending on the delivery method, you will possess either a `.json` file downloaded to your local machine, or raw text beginning with `{ "meta": { ... } , "nodes": [ ... ] , "connections": { ... } }`.
2. Open the file in a standard text editor (e.g., Notepad, VS Code) if direct copying is required, or simply locate the file if preparing for a direct upload.

> [!WARNING]
> Do not manually modify the raw JSON unless you possess an advanced understanding of the n8n schema formatting. A single structural error, such as a missing brace `}`, will corrupt the import process.

---

## Step 2: Accessing n8n

1. Open your designated web browser.
2. Navigate to your n8n instance (For local deployments, the default address is `http://localhost:5678`).
3. If prompted, authenticate using the Owner Account credentials established during installation.

---

## Step 3: Create a New Blank Workflow

To prevent overwriting existing configurations, the JSON must be imported into a new workspace.

1. On the left sidebar menu, locate and select the **Workflows** tab.
2. In the top-right corner, click the **+ Add workflow** button.
3. The canvas editor will open. By default, a "Start" or "Webhook" node may appear in the center.

---

## Step 4: Method A - Clipboard Injection (Rapid Deployment)

n8n natively supports direct clipboard injection for rapid workflow instantiation.

1. Open the file containing the JSON data.
2. **Select all text** (`Ctrl + A` on Windows).
3. **Copy to your clipboard** (`Ctrl + C`).
4. Return to the browser containing the blank n8n canvas.
5. Click anywhere within the blank grid to ensure the canvas is actively focused.
6. **Paste the data directly via keyboard command** (`Ctrl + V`).

**Result:** Instantly, all nodes, annotations, code blocks, and execution pathways will render onto the canvas. Complex workflows, such as this scraper, may require a brief moment to visualize.

---

## Step 4: Method B - Direct File Import (Alternative Deployment)

Should the JSON exceed clipboard limits or manual pasting fail, a strict file import provides a reliable alternative.

1. Within the blank n8n canvas, navigate to the top-right menu.
2. Click the `...` (More options) button adjacent to the "Save" function.
3. Select **Import from File...**
4. A standard file browser dialog will appear. Locate and select the target `.json` workflow file.
5. The predefined nodes will subsequently populate the canvas.

> [!NOTE]
> Upon importing a workflow, certain nodes may display orange exclamation warnings. This is expected behavior; it indicates the absence of active **Credentials** (e.g., specific API keys or OAuth connections).

---

## Step 5: Connecting the Workflow Credentials

With the structural blueprint established, the workflow must be authorized to interact with external services.

1. Identify nodes displaying missing credential warnings (such as Google Drive, Google Sheets, or Azure/OpenAI interface nodes).
2. Double-click the initial unassigned node.
3. Locate the **Credential for [Service Name]** dropdown menu.
4. Select the corresponding credentials previously configured. If none exist, click **- Create New Credential -** and execute the procedures outlined in the GCP or local LLM setup guides.
5. Repeat this authorization process for:
   - Google Sheets Input Nodes
   - Google Drive Upload Nodes

Once all warnings are resolved, click the prominent **Save** button in the top right corner to commit the workflow to the database.

---

## Step 6: Test Execution

The final phase involves verifying the operational integrity of the ecosystem.

1. Ensure the `DeepSearch .xlsx` control file is correctly populated within Google Sheets.
2. At the bottom of the interface, execute the process by clicking **Execute Workflow**.
3. Monitor the visualizer. Successful node operations are denoted by green execution paths. By selecting the pin icon on any active node, system operators can inspect the arrays of JSON data actively traversing the pipeline.
