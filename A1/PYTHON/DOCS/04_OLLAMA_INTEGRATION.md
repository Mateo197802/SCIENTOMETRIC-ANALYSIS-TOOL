# Local LLM Integration (Ollama)

If you lack access to an Enterprise API like Azure OpenAI or need to process massive amounts of data under strict data-privacy security bounds, the LLM enrichment stage can be executed fully locally on your machine using Ollama.

## 1. Install Ollama

1. Download Ollama from [ollama.com](https://ollama.com/).
2. Install it on your machine.
3. Open a terminal and run a lightweight but competent model like Llama 3 or Mistral (make sure it fits within your machine's VRAM):

   ```bash
   ollama run llama3
   ```

   *( This will automatically download the model and serve it at `http://localhost:11434` )*

## 2. Install the Python Interface

While inside your Python virtual environment (`test_env`), install the official Ollama package:

```bash
pip install ollama
```

## 3. Modify the Enrichment Script

Open `modules/enrichment.py`. Locate the **"2. Azure OpenAI Logic"** section and swap the Azure OpenAI call with the local Ollama call.

### Change From (Azure OpenAI)

```python
from openai import AzureOpenAI
client = AzureOpenAI(
    api_key=api_key,  
    api_version="2024-02-15-preview",
    azure_endpoint=endpoint
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0
)
classification = response.choices[0].message.content.strip()
```

### Change To (Local Ollama)

```python
import ollama

response = ollama.chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

classification = response['message']['content'].strip()
```

*(You will no longer need `AZURE_OPENAI_KEY` or `AZURE_OPENAI_ENDPOINT` in your `.env` file.)*
