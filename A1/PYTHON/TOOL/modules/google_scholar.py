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
    if not config.get("scholarActive"):
        for auth in current_authors:
            auth.update({
                "AUTHOR_ID_GS": "N/A (Disabled)",
                "INTERESTS_GS": "N/A"
            })
        return current_authors

    logger.info("[GoogleScholar] Fetching Google Scholar Interests...")
    api_key = config.get("scholarKey")
    
    for author in current_authors:
        name = author.get("AUTHOR_NAME", "")
        
        if name in SCHOLAR_CACHE:
            author["AUTHOR_ID_GS"] = SCHOLAR_CACHE[name]["id"]
            author["INTERESTS_GS"] = SCHOLAR_CACHE[name]["interests"]
            continue
            
        interests_gs = "NOT_INDEXED_IN_GS"
        author_id_gs = "NOT_FOUND"
        
        try:
            url = "https://serpapi.com/search.json"
            # Limit affiliation to 15 chars to generate better heuristic searches
            affil = author.get("AFFILIATION_OA", "No data").split(',')[0][:15]
            q = f"{name} {affil}"
            params = {
                "engine": "google_scholar",
                "q": q,
                "api_key": api_key
            }
            
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            
            profiles = data.get("profiles", [])
            # Priority 1: Exact author profile match
            if len(profiles) > 0:
                p = profiles[0]
                author_id_gs = p.get("author_id", "NO_ID")
                interests = p.get("interests", [])
                if interests:
                    interests_gs = " | ".join([i.get("title", "") for i in interests])
            else:
                # Priority 2: Try to find author link in organic search results
                org_results = data.get("organic_results", [])
                if len(org_results) > 0:
                    paper = org_results[0]
                    authors = paper.get("publication_info", {}).get("authors", [])
                    for a in authors:
                        if name.split()[0].lower() in a.get("name", "").lower():
                            if a.get("author_id"):
                                author_id_gs = a.get("author_id")
                                interests_gs = "Extracted from papers"
                                break
        except Exception as e:
            logger.debug(f"[GoogleScholar] Search Error for {name}: {e}")
            
        SCHOLAR_CACHE[name] = {"id": author_id_gs, "interests": interests_gs}
        author["AUTHOR_ID_GS"] = author_id_gs
        author["INTERESTS_GS"] = interests_gs
        
        time.sleep(config.get("scholarDelay", 1.0))

    return current_authors
