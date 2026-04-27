import os
from dotenv import load_dotenv

def load_config():
    """
    Loads API Keys, Rate Limits, and Active Flags.
    Reads from the .env file and environment variables.
    """
    load_dotenv()
    
    config = {
        "openAlexKey": os.getenv("OPENALEX_KEY", ""),
        "openAlexDelay": float(os.getenv("OPENALEX_DELAY", 1.0)),
        "openAlexActive": os.getenv("OPENALEX_ACTIVE", "true").lower() == "true",
        
        "pubmedKey": os.getenv("PUBMED_KEY", ""),
        "pubmedDelay": float(os.getenv("PUBMED_DELAY", 1.0)),
        "pubmedActive": os.getenv("PUBMED_ACTIVE", "true").lower() == "true",
        
        "semanticKey": os.getenv("SEMANTIC_KEY", ""),
        "semanticDelay": float(os.getenv("SEMANTIC_DELAY", 1.0)),
        "semanticActive": os.getenv("SEMANTIC_ACTIVE", "true").lower() == "true",
        
        "scopusKey": os.getenv("SCOPUS_KEY", ""),
        "scopusDelay": float(os.getenv("SCOPUS_DELAY", 1.0)),
        "scopusActive": os.getenv("SCOPUS_ACTIVE", "true").lower() == "true",
        
        "scholarKey": os.getenv("SCHOLAR_KEY", ""),
        "scholarDelay": float(os.getenv("SCHOLAR_DELAY", 1.0)),
        "scholarActive": os.getenv("SCHOLAR_ACTIVE", "true").lower() == "true",
        
        "azureKey": os.getenv("AZURE_OPENAI_KEY", ""),
        "azureEndpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "")
    }    
    return config
