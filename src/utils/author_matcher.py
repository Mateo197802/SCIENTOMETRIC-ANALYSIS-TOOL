import logging

logger = logging.getLogger(__name__)

def is_same_author(auth_oa, api_author, api_type="scopus"):
    """
    Strictly checks if two author objects represent the same person using PIDs.
    auth_oa: dictionary containing 'ORCID', 'RAW_SCOPUS_ID_OA'
    api_author: dictionary containing 'orcid', 'scopusId', etc. depending on api_type
    Returns True if IDs match, False otherwise.
    NO FUZZY MATCHING ALLOWED.
    """
    oa_orcid = auth_oa.get("ORCID", "No data")
    oa_scopus = auth_oa.get("RAW_SCOPUS_ID_OA", "No data")
    
    if oa_orcid != "No data":
        oa_orcid = oa_orcid.replace("https://orcid.org/", "").strip()
        
    if api_type == "scopus":
        api_scopus = api_author.get("scopusId", "NO_ID_SC")
        if oa_scopus != "No data" and api_scopus != "NO_ID_SC":
            if str(oa_scopus) == str(api_scopus):
                return True
                
        api_orcid = api_author.get("orcid")
        if api_orcid and oa_orcid != "No data":
            api_orcid = api_orcid.replace("https://orcid.org/", "").strip()
            if api_orcid == oa_orcid:
                return True
                
        return False

    elif api_type == "semantic_scholar":
        external_ids = api_author.get("externalIds") or {}
        api_orcid = external_ids.get("ORCID")
        if api_orcid and oa_orcid != "No data":
            api_orcid = api_orcid.replace("https://orcid.org/", "").strip()
            if api_orcid == oa_orcid:
                return True
                
        # SS might return a Scopus ID as well, though usually we just match ORCID
        # Just in case:
        ss_scopus = external_ids.get("Scopus")
        if ss_scopus and oa_scopus != "No data":
            if str(ss_scopus) == str(oa_scopus):
                return True
                
        return False
        
    elif api_type == "pubmed":
        # PubMed xml parser will need to extract 'orcid' if present
        api_orcid = api_author.get("orcid")
        if api_orcid and oa_orcid != "No data":
            api_orcid = api_orcid.replace("https://orcid.org/", "").replace("http://orcid.org/", "").strip()
            if api_orcid == oa_orcid:
                return True
        return False
        
    return False
