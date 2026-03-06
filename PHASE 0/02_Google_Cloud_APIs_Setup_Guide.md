# Technical Guide: Connecting n8n to Google Cloud APIs (Drive & Sheets)

To enable n8n to autonomously read queries from Google Sheets and save CSV outputs to Google Drive, the system must be authenticated with the **Google Cloud Platform (GCP)**. We will employ the **OAuth2** standard, which is the most secure and scalable method for authenticate local automation workflows.

---

## Phase 1: Create a Project in Google Cloud Console

1. **Log into Google Cloud:** Navigate to the [Google Cloud Console](https://console.cloud.google.com/) and authenticate with your primary Google account.
2. **Create a New Project:**
   - In the top-left corner, access the **Project Dropdown** (adjacent to the Google Cloud logo).
   - In the modal window, click **New Project** in the upper-right corner.
   - **Project Name:** Use a descriptive identifier. *Example:* `n8n-Scientometric-Scraper`.
   - Leave the `Location` field as "No organization" unless operating under a corporate domain.
   - Click **Create**.
3. Allow a few seconds for provisioning. Subsequently, ensure the new project is selected from the top dropdown menu.

---

## Phase 2: Enable Google Drive and Google Sheets APIs

Google Cloud requires explicit authorization for each API you intend to consume. Given that the n8n workflow demands downloading queries and uploading results, both Sheets and Drive APIs must be enabled.

1. Open the left sidebar menu (the hamburger icon) and navigate to **APIs & Services > Library**.
2. **Enable Google Drive API:**
   - Search for "Google Drive API".
   - Select the respective result.
   - Click the **Enable** button.
3. Return to the Library interface.
4. **Enable Google Sheets API:**
   - Search for "Google Sheets API".
   - Select the respective result.
   - Click the **Enable** button.

The GCP project is now authorized to perform Drive and Sheets operations.

---

## Phase 3: Configure the OAuth Consent Screen

Google requires a formal Consent Screen to inform users of the permissions being requested.

1. In the sidebar, navigate to **APIs & Services > OAuth consent screen**.
2. **User Type:** Select **External** (unless operating within a corporate Google Workspace, wherein Internal applies). Click **Create**.
3. **App Information:**
   - **App name:** `n8n Local Workflow`
   - **User support email:** Provide your email address.
   - **Developer contact information:** Provide your email address.
   - Logo and domains can be bypassed for internal testing.
4. Click **Save and Continue**.
5. **Scopes:** For internal testing, explicit scope definition here is unnecessary. n8n manages this dynamically during the connection phase. Click **Save and Continue**.
6. **Test Users:** **[CRITICAL STEP]** Since the application is in "Testing" mode, only explicitly whitelisted accounts can issue tokens.
   - Click **+ Add Users**.
   - Input the exact Google email address associated with the intended Sheets and Drive accounts.
   - Click **Save and Continue**.
7. Validate the inputs on the **Summary** screen and click **Back to Dashboard**.

---

## Phase 4: Generate OAuth Client ID Credentials

This phase involves acquiring the exact credentials required for n8n to connect.

1. In the sidebar, navigate to **APIs & Services > Credentials**.
2. Click **+ Create Credentials** at the top of the page and select **OAuth client ID**.
3. **Application Type:** Select **Web application**.
4. **Name:** `n8n Credentials`
5. **Authorized JavaScript origins:**
   - This prevents unauthorized domains from utilizing your API.
   - Add URI: `http://localhost:5678` (Or the precise URL of your n8n host).
6. **Authorized redirect URIs:**
   - **[CRITICAL STEP]** This determines where Google routes the authentication token post-login.
   - Add URI: `http://localhost:5678/rest/oauth2-credential/callback`
7. Click **Create**.

A dialog box will present your **Client ID** and **Client Secret**.

> [!CAUTION]
> **Keep the Client Secret strictly confidential.** Treat it with the same security protocols as an administrative password. Never hardcode it in public repositories.

---

## Phase 5: Linking credentials inside the n8n Interface

The final step is securely injecting these credentials into the n8n environment.

1. Open the n8n interface at `http://localhost:5678`.
2. On the left sidebar menu, access **Credentials** and click the `+ Add Credential` button located in the top right.
3. Search for the **Google Drive OAuth2 API** block and select it.
4. Input the keys generated in Phase 4:
   - **OAuth Client ID:** `[paste Client ID]`
   - **OAuth Client Secret:** `[paste Client Secret]`
5. Click **Sign in with Google**.
6. A Google Login window will prompt authentication. Select the specific account whitelisted as a Test User in Phase 3.
   > **Note:** Because the application remains in testing mode, Google will present an unverified app warning. Click **Advanced**, and then select **Go to n8n Local Workflow (unsafe)** to bypass.
7. Click **Continue/Allow** to grant the requested Drive permissions.
8. The window will close, validating and storing the credential within n8n.

**Repeat Steps 3 to 8**, this time searching for **Google Sheets OAuth2 API**. Utilize the identical Client ID and Secret.

Your n8n local instance is now fully certified to manipulate data autonomously and securely across your Google infrastructure.
