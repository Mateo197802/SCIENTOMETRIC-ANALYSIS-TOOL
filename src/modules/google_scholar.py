import requests
import logging
import time

logger = logging.getLogger(__name__)

# Basic dictionary to cache results in memory and save API calls
SCHOLAR_CACHE = {}

def process_google_scholar(current_authors, config):
    """
    Searches Google Scholar using SerpAPI to extract a researcher's academic defined interests.
    """
    if not config.get("scholarActive") or not current_authors:
        for auth in current_authors:
            auth.update({
                "AUTHOR_ID_GS": "N/A (Disabled)",
                "INTERESTS_GS": "N/A"
            })
        return current_authors

    logger.info("[GoogleScholar] Fetching Google Scholar Interests...")
    api_key = config.get("scholarKey")
    
    # 1. Search for the Paper by Title to find all GS Author IDs at once
    paper_title = current_authors[0].get("PAPER_TITLE", "")
    gs_author_ids = {}
    
    if paper_title:
        try:
            url = "https://serpapi.com/search.json"
            params = {
                "engine": "google_scholar",
                "q": paper_title,
                "api_key": api_key
            }
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            
            org_results = data.get("organic_results", [])
            if org_results:
                authors = org_results[0].get("publication_info", {}).get("authors", [])
                for a in authors:
                    gs_name = a.get("name", "").lower()
                    gs_id = a.get("author_id")
                    if gs_id:
                        gs_author_ids[gs_name] = gs_id
        except Exception as e:
            logger.debug(f"[GoogleScholar] Paper Search Error: {e}")
            
    # 2. Match current authors to GS IDs and fetch interests
    for author in current_authors:
        name = author.get("AUTHOR_NAME", "")
        
        if name in SCHOLAR_CACHE:
            author["AUTHOR_ID_GS"] = SCHOLAR_CACHE[name]["id"]
            author["INTERESTS_GS"] = SCHOLAR_CACHE[name]["interests"]
            continue
            
        interests_gs = "NOT_INDEXED_IN_GS"
        author_id_gs = "NOT_FOUND"
        
        # Try to match the author name with the GS authors retrieved
        name_lower = name.lower()
        name_parts = name_lower.split()
        last_name = name_parts[-1] if name_parts else name_lower
        
        matched_id = None
        for gs_name, gs_id in gs_author_ids.items():
            # If the last name matches, or the first letter of first name + last name matches
            if last_name in gs_name.split(): 
                matched_id = gs_id
                break
                
        if matched_id:
            author_id_gs = matched_id
            # Fetch Interests
            try:
                url = "https://serpapi.com/search.json"
                params = {
                    "engine": "google_scholar_author",
                    "author_id": matched_id,
                    "api_key": api_key
                }
                res = requests.get(url, params=params, timeout=10)
                res.raise_for_status()
                data = res.json()
                
                interests = data.get("author", {}).get("interests", [])
                if interests:
                    interests_gs = " | ".join([i.get("title", "") for i in interests])
                else:
                    interests_gs = "No explicit interests listed"
                    
            except Exception as e:
                logger.debug(f"[GoogleScholar] Author Profile Error for {name}: {e}")
        else:
            # Fallback: Search by Name + Affiliation using google_scholar_profiles
            try:
                url = "https://serpapi.com/search.json"
                affil = author.get("AFFILIATION_OA", "No data").split(',')[0][:15]
                q = f"{name} {affil}"
                params = {
                    "engine": "google_scholar_profiles",
                    "mauthors": q,
                    "api_key": api_key
                }
                res = requests.get(url, params=params, timeout=10)
                res.raise_for_status()
                data = res.json()
                
                profiles = data.get("profiles", [])
                if profiles:
                    author_id_gs = profiles[0].get("author_id", "NO_ID")
                    interests = profiles[0].get("interests", [])
                    if interests:
                        interests_gs = " | ".join([i.get("title", "") for i in interests])
                    else:
                        interests_gs = "No explicit interests listed"
            except Exception as e:
                logger.debug(f"[GoogleScholar] Fallback Profile Error for {name}: {e}")
                
        if interests_gs in ["NOT_INDEXED_IN_GS", "No explicit interests listed", ""]:
            topics_oa = author.get("TOPICS_OA", "")
            if topics_oa and topics_oa != "No data":
                interests_gs = f"{topics_oa} (via OpenAlex)"

        SCHOLAR_CACHE[name] = {"id": author_id_gs, "interests": interests_gs}
        author["AUTHOR_ID_GS"] = author_id_gs
        author["INTERESTS_GS"] = interests_gs
        
        time.sleep(config.get("scholarDelay", 1.0))

    return current_authors
