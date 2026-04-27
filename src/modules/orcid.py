import requests
import logging

logger = logging.getLogger(__name__)

def process_orcid(current_authors, config):
    """
    Fetches the author's deepest known organizational employment layout using the ORCID API.
    """
    logger.info("[ORCID] Fetching ORCID Employment Data...")
    
    headers = {"Accept": "application/json"}
    
    for author in current_authors:
        orcid = author.get("ORCID", "NO_ORCID")
        
        if orcid in ["NO_ORCID", "ORCID_SS", "", None, "No data"]:
            author["ORCID_EMPLOYMENT"] = "No ORCID ID"
            continue
            
        employment = "No employment data listed in ORCID"
        try:
            url = f"https://pub.orcid.org/v3.0/{orcid}/employments"
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            
            employments = data.get("employment-summary", [])
            # Read the latest employment record
            if employments and len(employments) > 0:
                latest = employments[0]
                org_name = latest.get("organization", {}).get("name", "Unknown organization")
                dept_name = latest.get("department-name", "No department")
                if not dept_name: dept_name = "No department"
                employment = f"{org_name} ({dept_name})"
                
        except Exception as e:
            logger.debug(f"[ORCID] Error for {orcid}: {e}")
            
        author["ORCID_EMPLOYMENT"] = employment
        
    return current_authors
