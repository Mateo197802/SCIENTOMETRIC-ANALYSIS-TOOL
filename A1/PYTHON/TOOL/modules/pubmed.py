import requests
import xml.etree.ElementTree as ET
import time
import logging

logger = logging.getLogger(__name__)

def process_pubmed(doi, current_authors, config):
    """
    Fetches PubMed metadata for a DOI, including MeSH terms, and identifies ghost authors 
    not found in the primary source.
    """
    if not config.get("pubmedActive"):
        for auth in current_authors:
            auth.update({
                "PMID_PM": "N/A",
                "MESH_PM": "No data",
                "FUNDING_PM": "No data",
                "AUTHOR_NAME_PM": "SKIP",
                "AFFILIATION_PM": "N/A"
            })
        return current_authors
        
    logger.info(f"[PubMed] Fetching data for {doi}...")
    
    pmid = "N/A"
    mesh_pm = "No data"
    funding_pm = "No data"
    authors_pm = []
    
    try:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": f"{doi}[LID]",
            "retmode": "json",
            "api_key": config.get("pubmedKey")
        }
        res_search = requests.get(search_url, params=search_params, timeout=10)
        res_search.raise_for_status()
        search_data = res_search.json()
        
        idlist = search_data.get("esearchresult", {}).get("idlist", [])
        
        if idlist:
            time.sleep(config.get("pubmedDelay", 0.1))
            pmid = idlist[0]
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "xml"
            }
            res_fetch = requests.get(fetch_url, params=fetch_params, timeout=10)
            res_fetch.raise_for_status()
            
            root = ET.fromstring(res_fetch.content)
            medline = root.find(".//MedlineCitation")
            if medline is not None:
                meshes = root.findall(".//MeshHeading/DescriptorName")
                if meshes:
                    mesh_pm = ", ".join([m.text for m in meshes[:5] if m.text])
                
                grants = root.findall(".//GrantList/Grant/Agency")
                if grants:
                    funding_pm = " | ".join([g.text for g in grants if g.text])
                    
                author_list = root.findall(".//AuthorList/Author")
                for idx, a in enumerate(author_list):
                    last_name = a.findtext("LastName", "")
                    fore_name = a.findtext("ForeName", "")
                    raw_name = f"{fore_name} {last_name}".strip()
                    name_lower = raw_name.lower()
                    
                    affil = "No affiliation"
                    affil_info = a.find(".//AffiliationInfo/Affiliation")
                    if affil_info is not None and affil_info.text:
                        affil = affil_info.text
                        
                    pos = "middle"
                    if idx == 0: pos = "first"
                    elif idx == len(author_list) - 1: pos = "last"
                    
                    authors_pm.append({
                        "name": name_lower,
                        "rawName": raw_name,
                        "affiliation": affil,
                        "pos": pos
                    })
    except Exception as e:
        logger.error(f"[PubMed] Error: {e}")
        
    final_rows = []
    # Match existing authors
    for oa in current_authors:
        oa_name_lower = oa.get("AUTHOR_NAME", "").lower()
        match_pm = None
        for pm in authors_pm:
            if pm["name"] in oa_name_lower or oa_name_lower in pm["name"]:
                match_pm = pm
                break
                
        oa.update({
            "PMID_PM": pmid,
            "MESH_PM": mesh_pm if mesh_pm else "No data",
            "FUNDING_PM": funding_pm if funding_pm else "No data",
            "AUTHOR_NAME_PM": match_pm["rawName"] if match_pm else "NOT_FOUND_IN_PM",
            "AFFILIATION_PM": match_pm["affiliation"] if match_pm else "N/A"
        })
        final_rows.append(oa)
        
    # Inject ghost authors
    base_data = current_authors[0] if current_authors else {}
    for pm in authors_pm:
        if not pm["name"]: continue
        exists = False
        for oa in current_authors:
            oa_name_lower = oa.get("AUTHOR_NAME", "").lower()
            if oa_name_lower in pm["name"] or pm["name"] in oa_name_lower:
                exists = True
                break
                
        if not exists:
            ghost = {
                "PAPER_TITLE": base_data.get("PAPER_TITLE", "No Title"),
                "DOI": base_data.get("DOI", doi),
                "YEAR": base_data.get("YEAR", "n/d"),
                "OPEN_ACCESS_OA": base_data.get("OPEN_ACCESS_OA", False),
                "FUNDING_OA": base_data.get("FUNDING_OA", "No data"),
                "AUTHOR_NAME": pm["rawName"],
                "AUTHOR_POS_OA": pm["pos"],
                "IS_CORRESPONDING_OA": False,
                "AFFILIATION_OA": "MISSING_IN_OA",
                "GEO_COUNTRY_OA": "UNKNOWN",
                "AUTHOR_ID_OA": "PubMed_Fallback",
                "ORCID": "NO_ORCID",
                "WORKS_COUNT_OA": 0,
                "CITATIONS_OA": 0,
                "HINDEX_OA": 0,
                "I10INDEX_OA": 0,
                "2YR_MEAN_OA": 0.0,
                "KEYWORDS_OA": "No data",
                "PMID_PM": pmid,
                "MESH_PM": mesh_pm if mesh_pm else "No data",
                "FUNDING_PM": funding_pm if funding_pm else "No data",
                "AUTHOR_NAME_PM": pm["rawName"],
                "AFFILIATION_PM": pm["affiliation"]
            }
            final_rows.append(ghost)
            
    return final_rows
