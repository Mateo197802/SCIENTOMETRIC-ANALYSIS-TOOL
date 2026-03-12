import requests
import time
import logging
import datetime

logger = logging.getLogger(__name__)

def process_scopus(doi, current_authors, config):
    """
    Fetches Scopus metadata and author profiles for deep metrics like H-index and seniority.
    """
    if not config.get("scopusActive"):
        for auth in current_authors:
            auth.update({
                "AUTHOR_ID_SC": "N/A",
                "AUTHOR_NAME_SC": "SKIP",
                "AFFILIATION_SC": "N/A",
                "FUNDING_SC": "No data",
                "HINDEX_SC": 0,
                "CITATIONS_SC": 0,
                "DOC_COUNT_SC": 0,
                "SUBJECT_AREAS_SC": "No data",
                "SENIORITY_SC": "Unknown"
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
                    "affiliation": affil
                })
    except Exception as e:
        logger.error(f"[Scopus] Search Error: {e}")

    final_rows = []
    # Match authors
    for auth in current_authors:
        auth_name_lower = auth.get("AUTHOR_NAME", "").lower()
        match_sc = None
        for sc in scopus_authors:
            if sc["name"] in auth_name_lower or auth_name_lower in sc["name"]:
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

    # Author-level profile lookup
    for auth in final_rows:
        auth_id_sc = auth.get("AUTHOR_ID_SC")
        auth["HINDEX_SC"] = 0
        auth["CITATIONS_SC"] = 0
        auth["DOC_COUNT_SC"] = 0
        auth["SUBJECT_AREAS_SC"] = "No data"
        auth["SENIORITY_SC"] = "Unknown"
        
        if auth_id_sc and auth_id_sc not in ["NOT_FOUND_IN_SC", "SKIP", "N/A", "NO_ID_SC"]:
            try:
                time.sleep(config.get("scopusDelay", 0.5))
                url = f"https://api.elsevier.com/content/author/author_id/{auth_id_sc}"
                params = {"view": "ENHANCED"}
                
                res = requests.get(url, params=params, headers=headers, timeout=10)
                res.raise_for_status()
                profile_data = res.json().get("author-retrieval-response", [])
                
                if isinstance(profile_data, list) and len(profile_data) > 0:
                    profile_data = profile_data[0]
                elif not isinstance(profile_data, dict):
                    profile_data = {}
                    
                core = profile_data.get("coredata", {})
                auth["CITATIONS_SC"] = int(core.get("citation-count", 0))
                auth["DOC_COUNT_SC"] = int(core.get("document-ent-count", 0))
                
                h_data = profile_data.get("h-index", 0)
                if isinstance(h_data, dict):
                    auth["HINDEX_SC"] = int(h_data.get("$", h_data.get("value", 0)))
                else:
                    auth["HINDEX_SC"] = int(h_data) if h_data else 0
                    
                subjects = profile_data.get("subject-areas", {}).get("subject-area", [])
                if isinstance(subjects, dict): subjects = [subjects]
                if isinstance(subjects, list):
                    subj_names = [s.get("$", s.get("@abbrev", "")) for s in subjects if isinstance(s, dict)]
                    if subj_names:
                        auth["SUBJECT_AREAS_SC"] = " | ".join(filter(bool, subj_names))
                        
                pub_range = profile_data.get("author-profile", {}).get("publication-range", {})
                first_year = pub_range.get("@first")
                if first_year:
                    career_length = datetime.datetime.now().year - int(first_year)
                    if career_length >= 15: auth["SENIORITY_SC"] = f"Senior ({career_length} yrs)"
                    elif career_length >= 5: auth["SENIORITY_SC"] = f"Mid-level ({career_length} yrs)"
                    else: auth["SENIORITY_SC"] = f"Early-career ({career_length} yrs)"
                    
            except Exception as e:
                logger.debug(f"[Scopus] Author Profile Error for {auth_id_sc}: {e}")
                
    return final_rows
