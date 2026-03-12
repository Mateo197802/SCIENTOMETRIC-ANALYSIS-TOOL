import requests
import re
import logging
import copy
import urllib.parse

logger = logging.getLogger(__name__)

GENDER_CACHE = {}

def process_gender_and_llm(current_authors, config):
    """
    Enriches authors data with a gender prediction (based on their first name and country)
    and an LLM-powered domain classification based strictly on their academic lifetime record.
    """
    logger.info("[Enrichment] Running Genderize and LLM Profiling...")
    
    inst_regex = re.compile(r'(group|network|study|collaborators|team|consortium|committee)', re.IGNORECASE)
    final_authors = []
    
    for original_author in current_authors:
        author = copy.deepcopy(original_author)
        author_name = author.get("AUTHOR_NAME", "")
        
        # 1. Genderize Logic
        gender = "Unknown"
        
        # Avoid genderizing institutional authors
        if inst_regex.search(author_name):
            gender = "N/A"
        else:
            first_name = re.sub(r'[^a-z]', '', author_name.split(" ")[0].lower())
            if first_name in GENDER_CACHE:
                gender = GENDER_CACHE[first_name]
            else:
                try:
                    url = f"https://api.genderize.io/?name={urllib.parse.quote(first_name)}"
                    country = author.get("GEO_COUNTRY_OA")
                    if country and len(country) == 2 and country != "NO":
                        url += f"&country_id={country.lower()}"
                        
                    res = requests.get(url, timeout=10)
                    if res.status_code == 200:
                        data = res.json()
                        prob = data.get("probability", 0)
                        raw_gender = data.get("gender")
                        # Trust predictions with high probability
                        if raw_gender and float(prob) >= 0.8:
                            gender = raw_gender.capitalize()
                            GENDER_CACHE[first_name] = gender
                except Exception as e:
                    logger.debug(f"[Enrichment] Genderize error for {first_name}: {e}")
                    
        author["GENDER"] = gender
        
        # 2. Azure OpenAI Logic (Taxonomy Classification)
        api_key = config.get("azureKey")
        endpoint = config.get("azureEndpoint")
        
        classification = f"UNKNOWN_DOMAIN | {gender}"
        
        if api_key and endpoint:
            try:
                from openai import AzureOpenAI
                client = AzureOpenAI(
                    api_key=api_key,  
                    api_version="2024-02-15-preview",
                    azure_endpoint=endpoint
                )
                
                # Rigid prompt ensuring exact matching logic from previous visual nodes
                prompt = f"""==You are an expert scientometric data analyst. Your strict task is to profile the INDIVIDUAL AUTHOR, not the specific paper they co-authored. 

ANTI-HALLUCINATION PROTOCOL: If any variable below says "No data", "N/A", "NOT_FOUND", "UNKNOWN" or is empty, you must ignore it. DO NOT invent, assume, or infer affiliations, interests, or areas that are not explicitly listed in the valid data.

AUTHOR LEVEL DATA (Primary Weight - Use this to define the core expertise of the author):
- Name: {author.get('AUTHOR_NAME', 'No data')}
- Affiliation (OpenAlex): {author.get('AFFILIATION_OA', 'No data')}
- Affiliation (PubMed): {author.get('AFFILIATION_PM', 'No data')}
- Affiliation (Scopus): {author.get('AFFILIATION_SC', 'No data')}
- Department (ORCID): {author.get('ORCID_EMPLOYMENT', 'No data')}
- Lifetime Keywords (OpenAlex): {author.get('KEYWORDS_OA', 'No data')}
- Lifetime Subject Areas (Scopus): {author.get('SUBJECT_AREAS_SC', 'No data')}
- Lifetime Interests (Google Scholar): {author.get('INTERESTS_GS', 'No data')}

PAPER LEVEL DATA (Secondary Context only - Do not let this override their lifetime profile):
- Current Paper MeSH: {author.get('MESH_PM', 'No data')}

Current Gender Status: {gender}

TASK 1 (BACKGROUND): Based STRICTLY on the AUTHOR LEVEL DATA, classify the author into EXACTLY ONE category from this comprehensive taxonomy:

[Core Domains for the Study]
- CLINICAL: Affiliated with hospitals/clinics. Focus on patient care, surgery, clinical trials, healthcare.
- COMPUTER_SCIENCE: Affiliated with CS/IT faculties. Focus on algorithms, software, AI, hardware.
- BIOINFORMATICS: Focus on genetics, molecular biology, or drug discovery heavily combined with data/coding.
- HYBRID_MED_TECH: Cross-disciplinary. Blends clinical hospital data/records/imaging with Machine Learning/AI.

[Purists & Broad Domains]
- BASIC_LIFE_SCIENCES: Pure biology, pure biochemistry, neuroscience, zoology, botany. No explicit tech/computational focus.
- PHYSICAL_SCIENCES: Pure chemistry, physics, astronomy, materials science.
- ENGINEERING_MATH: Non-CS engineering (civil, mechanical, electrical, chemical), pure mathematics, statistics.
- SOCIAL_SCIENCES_HUMANITIES: Psychology, sociology, economics, arts, food science/gastronomy, public policy, linguistics.
- OTHER_SCIENCES: Agriculture, environmental science, earth sciences, ecology.
- UNKNOWN: Insufficient valid data to make a confident classification.

TASK 2 (GENDER): If "Current Gender Status" is "Unknown", guess the gender strictly based on the cultural origin of the First Name (Male, Female, or Unknown). If it is already Male, Female, or N/A, keep the current status exactly as it is.

STRICT OUTPUT FORMAT:
CATEGORY | GENDER
(Example: PHYSICAL_SCIENCES | Female)
Do not add any other text, explanation, or intro."""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0
                )
                
                classification = response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"[Enrichment] Azure OpenAI error for {author_name}: {e}")
                classification = f"ERROR_LLM | {gender}"
                
        author["PROFILE_CLASSIFICATION"] = classification
        final_authors.append(author)
        
    return final_authors
