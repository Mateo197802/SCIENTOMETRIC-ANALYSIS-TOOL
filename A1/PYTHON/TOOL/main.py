import pandas as pd
import time
import logging
import os
from config import load_config
from modules.openalex import process_openalex
from modules.pubmed import process_pubmed
from modules.scopus import process_scopus
from modules.semantic_scholar import process_semantic_scholar
from modules.google_scholar import process_google_scholar
from modules.orcid import process_orcid
from modules.enrichment import process_gender_and_llm
from utils.id_compressor import compress_authors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline(input_csv, output_csv):
    """
    Orchestrates the entire data extraction pipeline.
    """
    logger.info(f"Starting pipeline with input: {input_csv}")
    
    # 1. Configuration & Input
    config = load_config()
    
    if not os.path.exists(input_csv):
        logger.error(f"Input file {input_csv} does not exist. Please provide a valid CSV file with a 'DOI' column.")
        return
        
    df = pd.read_csv(input_csv)
    if 'DOI' not in df.columns:
        logger.error("The input CSV must contain an explicit 'DOI' column.")
        return
        
    dois = df['DOI'].dropna().unique().tolist()
    
    master_table = []
    
    # 2. Loop over DOIs (Sequential Evaluation)
    for index, doi in enumerate(dois):
        logger.info(f"\n=======================================================")
        logger.info(f" STARTING COMPLETE FLOW FOR DOI {index + 1}/{len(dois)}: {doi}")
        logger.info(f"=======================================================")
        
        # --- NODE 1: OPEN ALEX (The Foundation) ---
        logger.info("-> Executing Node: OpenAlex...")
        authors_list = process_openalex(doi, config)
        if not authors_list:
            logger.warning(f"DOI {doi} not found in OpenAlex. Skipping to the next.")
            continue
            
        # --- NODE 2: PUBMED (Fallbacks & Ghost Authors) ---
        logger.info("-> Executing Node: PubMed...")
        authors_list = process_pubmed(doi, authors_list, config)
        
        # --- NODE 3: SCOPUS (Deep Metrics & Expertise) ---
        logger.info("-> Executing Node: Scopus...")
        authors_list = process_scopus(doi, authors_list, config)
        
        # --- NODE 4: SEMANTIC SCHOLAR (Influential Citations) ---
        logger.info("-> Executing Node: Semantic Scholar...")
        authors_list = process_semantic_scholar(doi, authors_list, config)
        
        # --- NODE 5: GOOGLE SCHOLAR (Interests via SerpApi) ---
        logger.info("-> Executing Node: Google Scholar...")
        authors_list = process_google_scholar(authors_list, config)
        
        # --- COMPRESSOR NODE ---
        logger.info("-> Executing Node: Id-Compressor (Deduplication)...")
        compressed_authors = compress_authors(authors_list)
        
        # --- NODE 6: ORCID (Employment Data) ---
        logger.info("-> Executing Node: ORCID...")
        compressed_authors = process_orcid(compressed_authors, config)
        
        # --- NODE 7: ENRICHMENT (Genderize & LLM Classification) ---
        logger.info("-> Executing Node: Enrichment (Genderize/Azure OpenAI)...")
        final_authors = process_gender_and_llm(compressed_authors, config)
        
        # Accumulate Result
        logger.info(f" Successful flow for DOI {doi}. {len(final_authors)} authors ready.")
        master_table.extend(final_authors)
        
        # Polite delay between iteration cycles
        time.sleep(1)
        
    # 3. Export Master Table
    logger.info(f"Pipeline finished. Saving {len(master_table)} author records to {output_csv}")
    final_df = pd.DataFrame(master_table)
    
    if final_df.empty:
        logger.warning("No data was retrieved. The Master Table is empty.")
        return
        
    # Reorder and restrict columns to match exact user expectations
    expected_columns = [
        "PAPER_TITLE", "DOI", "YEAR", "OPEN_ACCESS_OA", "FUNDING_OA",
        "AUTHOR_NAME", "AUTHOR_POS_OA", "IS_CORRESPONDING_OA", "AFFILIATION_OA",
        "GEO_COUNTRY_OA", "AUTHOR_ID_OA", "ORCID", "WORKS_COUNT_OA", "CITATIONS_OA",
        "HINDEX_OA", "I10INDEX_OA", "2YR_MEAN_OA", "KEYWORDS_OA", "PMID_PM",
        "MESH_PM", "FUNDING_PM", "AUTHOR_NAME_PM", "AFFILIATION_PM", "AUTHOR_ID_SC",
        "AUTHOR_NAME_SC", "AFFILIATION_SC", "FUNDING_SC", "INFLUENTIAL_CITATIONS_SS",
        "CITATION_CONTEXTS_SS", "AUTHOR_ID_SS", "AUTHOR_NAME_SS", "ORCID_SS",
        "HINDEX_SS", "CITATIONS_SS", "HINDEX_SC", "CITATIONS_SC", "DOC_COUNT_SC",
        "SUBJECT_AREAS_SC", "SENIORITY_SC", "AUTHOR_ID_GS", "INTERESTS_GS", 
        "ORCID_EMPLOYMENT", "GENDER", "PROFILE_CLASSIFICATION"
    ]
        
    # Ensure all columns exist, fill missing ones with 'No data'
    for col in expected_columns:
        if col not in final_df.columns:
            final_df[col] = "No data"
                
    final_df = final_df[expected_columns]
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    final_df.to_csv(output_csv, index=False)
    logger.info("Export completed successfully.")

if __name__ == "__main__":
    # Note: Adjust paths as needed. It's recommended to place input files in the 'data' directory.
    run_pipeline("data/input_dois.csv", "data/MASTER_AUTHOR_TABLE.csv")
