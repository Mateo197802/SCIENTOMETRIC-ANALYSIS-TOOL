import requests
import time
import logging

logger = logging.getLogger(__name__)

def process_scopus(doi, current_authors, config):
    """
    Fetches Scopus paper-level metadata: author IDs, names, affiliations, and funding.
    NOTE: Deep metrics (H-index, citations, seniority) removed — requires institutional
    API subscription tier (view=ENHANCED) which is not available with standard access.
    """
    if not config.get("scopusActive"):
        for auth in current_authors:
            auth.update({
                "AUTHOR_ID_SC": "N/A",
                "AUTHOR_NAME_SC": "SKIP",
                "AFFILIATION_SC": "N/A",
                "FUNDING_SC": "No data",
            })
        return current_authors

    logger.info(f"[Scopus] Fetching data for {doi}...")
    api_key = config.get("scopusKey")
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }
    
    funding_sc = "No data"
    scopus_authors = []
    
    # Paper-level fetch
    try:
        url = "https://api.elsevier.com/content/search/scopus"
        params = {
            "query": f'DOI("{doi}")',
            "view": "COMPLETE"
        }
        res = requests.get(url, params=params, headers=headers, timeout=10)
        
        # --- VPN GUARD: Detect institutional access issues ---
        if res.status_code == 400:
            logger.error("=" * 60)
            logger.error("[Scopus] HTTP 400 — VPN/Institutional access error!")
            logger.error("[Scopus] Please reconnect the Yachay Tech VPN and restart.")
            logger.error("=" * 60)
            raise ConnectionError("SCOPUS_VPN_ERROR: HTTP 400 — VPN is disconnected or institutional access denied. Reconnect VPN and retry.")
        
        if res.status_code == 401 or res.status_code == 403:
            logger.error(f"[Scopus] HTTP {res.status_code} — API key or access issue.")
            raise ConnectionError(f"SCOPUS_AUTH_ERROR: HTTP {res.status_code} — Check API key and VPN.")
        
        res.raise_for_status()
        data = res.json()
        
        results = data.get("search-results", {})
        total = int(results.get("opensearch:totalResults", 0))
        
        if total > 0:
            entry = results.get("entry", [])[0]
            funding_sc = entry.get("fund-sponsor", "No data")
            
            authors = entry.get("author", [])
            for a in authors:
                given = a.get("given-name", "")
                surname = a.get("surname", "")
                raw_name = f"{given} {surname}".strip()
                name_lower = raw_name.lower()
                
                authid = a.get("authid", "NO_ID_SC")
                sc_orcid = a.get("orcid")
                
                afid = a.get("afid", [])
                if isinstance(afid, list) and len(afid) > 0:
                    affil = afid[0].get("$", "No affiliation")
                elif isinstance(afid, dict):
                    affil = afid.get("$", "No affiliation")
                else:
                    affil = "No affiliation"
                    
                scopus_authors.append({
                    "name": name_lower,
                    "rawName": raw_name,
                    "scopusId": authid,
                    "orcid": sc_orcid,
                    "affiliation": affil
                })
    except ConnectionError:
        # Re-raise VPN/auth errors so main.py can handle them
        raise
    except Exception as e:
        logger.error(f"[Scopus] Search Error: {e}")

    final_rows = []
    
    from utils.author_matcher import is_same_author
    
    # Match authors
    for auth in current_authors:
        match_sc = None
        for sc in scopus_authors:
            if is_same_author(auth, sc, api_type="scopus"):
                match_sc = sc
                break
                
        auth.update({
            "AUTHOR_ID_SC": match_sc["scopusId"] if match_sc else "NOT_FOUND_IN_SC",
            "AUTHOR_NAME_SC": match_sc["rawName"] if match_sc else "SKIP",
            "AFFILIATION_SC": match_sc["affiliation"] if match_sc else "N/A",
            "FUNDING_SC": funding_sc
        })
        final_rows.append(auth)
        
    # Inject Scopus Ghost Authors
    base_data = current_authors[0] if current_authors else {}
    for sc in scopus_authors:
        if not sc["name"]: continue
        exists = False
        for auth in current_authors:
            auth_name_lower = auth.get("AUTHOR_NAME", "").lower()
            if auth_name_lower in sc["name"] or sc["name"] in auth_name_lower:
                exists = True
                break
        
        if not exists:
            ghost = {
                "PAPER_TITLE": base_data.get("PAPER_TITLE", "No Title"),
                "DOI": base_data.get("DOI", doi),
                "YEAR": base_data.get("YEAR", "n/d"),
                "AUTHOR_NAME": sc["rawName"],
                "AUTHOR_POS_OA": "Unknown",
                "IS_CORRESPONDING_OA": False,
                "AUTHOR_ID_OA": "Scopus_Fallback",
                "ORCID": "NO_ORCID",
                "OPEN_ACCESS_OA": False,
                "FUNDING_OA": "No data",
                "AFFILIATION_OA": "MISSING_IN_OA",
                "GEO_COUNTRY_OA": "UNKNOWN",
                "WORKS_COUNT_OA": 0,
                "CITATIONS_OA": 0,
                "HINDEX_OA": 0,
                "I10INDEX_OA": 0,
                "2YR_MEAN_OA": 0.0,
                "KEYWORDS_OA": "No data",
                "PMID_PM": "N/A",
                "MESH_PM": "No data",
                "FUNDING_PM": "No data",
                "AUTHOR_NAME_PM": "SKIP",
                "AFFILIATION_PM": "N/A",
                "AUTHOR_ID_SC": sc["scopusId"],
                "AUTHOR_NAME_SC": sc["rawName"],
                "AFFILIATION_SC": sc["affiliation"],
                "FUNDING_SC": funding_sc
            }
            final_rows.append(ghost)

    return final_rows
