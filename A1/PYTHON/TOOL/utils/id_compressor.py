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
        
        # Merge metrics safely keeping the best/found ones
        if item.get("AUTHOR_ID_SC") and item.get("AUTHOR_ID_SC") not in ["N/A", "NOT_FOUND_IN_SC"]:
            existing["AUTHOR_ID_SC"] = item["AUTHOR_ID_SC"]
            existing["HINDEX_SC"] = max(existing.get("HINDEX_SC", 0), item.get("HINDEX_SC", 0))
            existing["CITATIONS_SC"] = max(existing.get("CITATIONS_SC", 0), item.get("CITATIONS_SC", 0))
            if not existing.get("SUBJECT_AREAS_SC") or existing.get("SUBJECT_AREAS_SC") == "No data":
                existing["SUBJECT_AREAS_SC"] = item.get("SUBJECT_AREAS_SC")
            if not existing.get("SENIORITY_SC") or existing.get("SENIORITY_SC") == "Unknown":
                existing["SENIORITY_SC"] = item.get("SENIORITY_SC")
                
        if item.get("AUTHOR_ID_SS") and item.get("AUTHOR_ID_SS") not in ["N/A", "NOT_FOUND_IN_SS"]:
            existing["AUTHOR_ID_SS"] = item["AUTHOR_ID_SS"]
            existing["HINDEX_SS"] = max(existing.get("HINDEX_SS", 0), item.get("HINDEX_SS", 0))
            existing["CITATIONS_SS"] = max(existing.get("CITATIONS_SS", 0), item.get("CITATIONS_SS", 0))
            
        if item.get("AUTHOR_ID_GS") and item.get("AUTHOR_ID_GS") not in ["N/A", "N/A (Disabled)", "NOT_FOUND"]:
            existing["AUTHOR_ID_GS"] = item["AUTHOR_ID_GS"]
            existing["INTERESTS_GS"] = item.get("INTERESTS_GS", "N/A")
            
        if existing.get("ORCID") == "NO_ORCID" and item.get("ORCID") and item.get("ORCID") != "NO_ORCID":
            existing["ORCID"] = item["ORCID"]
            
    return merged_authors
