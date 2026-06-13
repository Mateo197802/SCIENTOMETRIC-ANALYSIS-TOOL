import unicodedata
import re

def compress_authors(authors_list):
    """
    Deduplicates authors across the multiple sources using their names.
    Merges their metrics safely to retain the best or successfully found ones.
    """
    merged_authors = []
    
    def get_parts(name):
        if not name: return {"clean": "", "lastName": "", "firstInitial": ""}
        no_accents = unicodedata.normalize('NFD', name)
        no_accents = re.sub(r'[\u0300-\u036f]', '', no_accents).lower()
        no_accents = re.sub(r'[^a-z\s]', '', no_accents).strip()
        parts = re.split(r'\s+', no_accents)
        return {
            "clean": no_accents.replace(' ', ''),
            "lastName": parts[-1] if len(parts) > 0 else "",
            "firstInitial": parts[0][0] if len(parts) > 0 and parts[0] else ""
        }
        
    for item in authors_list:
        curr = get_parts(item.get("AUTHOR_NAME"))
        if not curr["clean"]: continue
        
        match_idx = -1
        for i, existing in enumerate(merged_authors):
            ex = get_parts(existing.get("AUTHOR_NAME"))
            # Match by identical full clean string, or partial inclusion
            if curr["clean"] == ex["clean"] or curr["clean"] in ex["clean"] or ex["clean"] in curr["clean"]:
                match_idx = i
                break
            # Fallback match: identical last name and identical first initial
            if curr["lastName"] != "" and curr["lastName"] == ex["lastName"] and curr["firstInitial"] == ex["firstInitial"]:
                match_idx = i
                break
                
        if match_idx == -1:
            merged_authors.append(item.copy())
            match_idx = len(merged_authors) - 1
            
        existing = merged_authors[match_idx]
        
        # Merge Scopus paper-level IDs (kept)
        if item.get("AUTHOR_ID_SC") and item.get("AUTHOR_ID_SC") not in ["N/A", "NOT_FOUND_IN_SC"]:
            existing["AUTHOR_ID_SC"] = item["AUTHOR_ID_SC"]
        
        # Merge Semantic Scholar IDs and metrics
        if item.get("AUTHOR_ID_SS") and item.get("AUTHOR_ID_SS") not in ["N/A", "NOT_FOUND_IN_SS"]:
            existing["AUTHOR_ID_SS"] = item["AUTHOR_ID_SS"]
            existing["HINDEX_SS"] = max(existing.get("HINDEX_SS", 0), item.get("HINDEX_SS", 0))
            existing["CITATIONS_SS"] = max(existing.get("CITATIONS_SS", 0), item.get("CITATIONS_SS", 0))
            
            # Carry over Name and ORCID if existing is missing them
            if existing.get("AUTHOR_NAME_SS") in ["NOT_FOUND_IN_SS", "SKIP", "", None]:
                existing["AUTHOR_NAME_SS"] = item.get("AUTHOR_NAME_SS", "NOT_FOUND_IN_SS")
            if existing.get("ORCID_SS") in ["NO_ORCID_SS", "", None]:
                existing["ORCID_SS"] = item.get("ORCID_SS", "NO_ORCID_SS")
            
        # Update primary ORCID if missing
        if existing.get("ORCID") in ["NO_ORCID", "", None]:
            if item.get("ORCID") and item.get("ORCID") != "NO_ORCID":
                existing["ORCID"] = item["ORCID"]
            elif item.get("ORCID_SS") and item.get("ORCID_SS") != "NO_ORCID_SS":
                existing["ORCID"] = item["ORCID_SS"]
            
    return merged_authors
