import time
import logging
import requests

logger = logging.getLogger(__name__)

OPENALEX_WORKS_URL = "https://api.openalex.org/works"

def process_openalex(doi, config):
    """
    Fetches OpenAlex metadata for a DOI and extracts authors with their deep metrics.
    """
    if not config.get("openAlexActive"):
        logger.warning(f"OpenAlex module is disabled. Skipping DOI: {doi}")
        return []
        
    logger.info(f"[OpenAlex] Fetching data for {doi}...")
    
    doi_clean = doi.replace("https://doi.org/", "").strip()
    url = f"{OPENALEX_WORKS_URL}/doi:{doi_clean}"
    
    # It is recommended to use the polite pool by providing an email
    email = "mail@example.com"
    
    try:
        response = requests.get(url, params={"mailto": email}, timeout=20)
        
        if response.status_code == 404:
            logger.warning(f"[OpenAlex] DOI Not Found: {doi_clean}")
            return []
            
        response.raise_for_status()
        data = response.json()
        
        # --- 1. EXTRACT PAPER LEVEL METADATA ---
        paper_title = data.get("title", "No data")
        year = data.get("publication_year", "No data")
        open_access_oa = data.get("open_access", {}).get("is_oa", False)
        
        # Extract Funding (from crossref grants if available)
        funding_oa = "No data"
        grants = data.get("grants", [])
        if grants:
            funders = [g.get("funder_display_name") for g in grants if g.get("funder_display_name")]
            if funders:
                funding_oa = ", ".join(funders)
                
        # Extract Keywords
        keywords_list = data.get("concepts", [])
        # Get top 5 concepts as keywords
        keywords_oa = ", ".join([k.get("display_name") for k in keywords_list[:5] if k.get("display_name")]) or "No data"
        
        # --- 2. EXTRACT AUTHOR METADATA ---
        authorships = data.get("authorships", [])
        authors_meta = []
        
        for i, auth in enumerate(authorships):
            author_info = auth.get("author", {})
            auth_id = author_info.get("id", "No data")
            
            # Basic Author Info
            author_name = author_info.get("display_name", "No data")
            author_pos_oa = auth.get("author_position", "middle")
            is_corresponding_oa = auth.get("is_corresponding", False)
            orcid = author_info.get("orcid", "No data")
            
            # Affiliations
            affiliations = auth.get("institutions", [])
            affiliation_oa = "No data"
            geo_country_oa = "IN" # Default fallback
            
            if affiliations:
                # Top affiliation
                affiliation_oa = affiliations[0].get("display_name", "No data")
                geo_country_oa = affiliations[0].get("country_code", "No data")
                
            # Author Deep Metrics (Requires separate API call per author)
            works_count_oa = 0
            citations_oa = 0
            hindex_oa = 0
            i10index_oa = 0
            yr2_mean_oa = 0.0
            
            if auth_id != "No data":
                try:
                    logger.debug(f"[OpenAlex] Fetching deep metrics for author: {author_name}")
                    api_auth_id = auth_id.replace("https://openalex.org/", "https://api.openalex.org/authors/")
                    auth_resp = requests.get(api_auth_id, params={"mailto": email}, timeout=10)
                    
                    if auth_resp.status_code == 200:
                        a_data = auth_resp.json()
                        works_count_oa = a_data.get("works_count", 0)
                        citations_oa = a_data.get("cited_by_count", 0)
                        
                        stats = a_data.get("summary_stats", {})
                        hindex_oa = stats.get("h_index", 0)
                        i10index_oa = stats.get("i10_index", 0)
                        yr2_mean_oa = stats.get("2yr_mean_citedness", 0.0)
                        
                except Exception as e:
                    logger.debug(f"[OpenAlex] Could not fetch deep profile for {auth_id}: {e}")
                    
                time.sleep(config.get("openAlexDelay", 0.1))  # Polite delay
            
            # Clean auth_id for output
            clean_auth_id = auth_id.split("/")[-1] if auth_id != "No data" else "No data"
            clean_orcid = orcid.split("/")[-1] if orcid != "No data" else "No data"
            
            author_dict = {
                "PAPER_TITLE": paper_title,
                "DOI": doi_clean,
                "YEAR": year,
                "OPEN_ACCESS_OA": open_access_oa,
                "FUNDING_OA": funding_oa,
                "AUTHOR_NAME": author_name,
                "AUTHOR_POS_OA": author_pos_oa,
                "IS_CORRESPONDING_OA": is_corresponding_oa,
                "AFFILIATION_OA": affiliation_oa,
                "GEO_COUNTRY_OA": geo_country_oa,
                "AUTHOR_ID_OA": clean_auth_id,
                "ORCID": clean_orcid,
                "WORKS_COUNT_OA": works_count_oa,
                "CITATIONS_OA": citations_oa,
                "HINDEX_OA": hindex_oa,
                "I10INDEX_OA": i10index_oa,
                "2YR_MEAN_OA": yr2_mean_oa,
                "KEYWORDS_OA": keywords_oa
            }
            authors_meta.append(author_dict)
            
        return authors_meta

    except Exception as e:
        logger.error(f"[OpenAlex] Error fetching DOI {doi}: {e}")
        return []
