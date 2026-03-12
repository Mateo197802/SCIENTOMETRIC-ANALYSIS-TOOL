# Technical Guide: Importing the Workflow JSON into n8n

n8n offers a highly efficient method for saving and sharing comprehensive automations via **JSON objects**. A large block of JSON code associated with n8n represents the precise nodes, parameters, and connections of an entire pipeline.

This guide details the procedure for deploying raw JSON code—specifically formatted for the A1 Scientometric Tool—directly into your n8n interface.

---

## Step 1: Prepare the JSON Code

Ensure the complete JSON file (`A1 SCIENTOMETRIC ANALYSIS TOOL .json`) is ready and accessible on your local machine.

> [!WARNING]
> Do not manually modify the raw JSON unless you possess an advanced understanding of the n8n schema formatting. A single structural error, such as a missing brace `}`, will corrupt the import process.

---

## Step 2: Access n8n

1. Open your designated web browser.
2. Navigate to your n8n instance (For local Docker deployments, the address is `http://localhost:5678`).
3. If prompted, authenticate using the Owner Account credentials.

---

## Step 3: Create a New Blank Workflow

To prevent overwriting existing configurations, the JSON must be imported into a blank workspace.

1. On the left sidebar menu, locate and select the **Workflows** tab.
2. In the top-right corner, click the **+ Add workflow** button.
3. The canvas editor will open with a blank grid.

---

## Step 4: Import Deployment

1. Within the blank n8n canvas, navigate to the top-right menu.
2. Click the `...` (More options) button adjacent to the "Save" function.
3. Select **Import from File...**
4. A standard file browser dialog will appear. Locate and select the target `A1 SCIENTOMETRIC ANALYSIS TOOL .json` file.
5. All predefined nodes, Code logic, switch architectures, and mapping frameworks will subsequently populate the canvas automatically.

> [!NOTE]
> Upon importing a workflow, certain nodes may display orange exclamation warnings. This is expected behavior; it indicates the absence of active **Credentials** tied to your personal n8n instance (e.g., your specific Google OAuth connection or Azure API keys).

---

## Step 5: Connecting the Workflow Credentials

With the structural blueprint established, the workflow must be authorized to interact with external services.

1. Identify nodes displaying missing credential warnings (such as the Google Drive Trigger node, the Google Sheets Read/Write nodes, or the Azure OpenAI interface node).
2. Double-click the initial unassigned node.
3. Locate the **Credential for [Service Name]** dropdown menu.
4. Select your corresponding accounts previously configured. If none exist, click **- Create New Credential -** and execute standard OAuth login setups directly in the n8n browser UI.
5. Repeat this authorization process for all nodes showing orange icons.

Once all warnings are resolved, click the prominent **Save** button in the top right corner to commit the workflow to your local database securely.

You are now fully ready to execute the A1 pipeline.
