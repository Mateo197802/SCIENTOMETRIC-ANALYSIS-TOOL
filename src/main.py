import pandas as pd
import time
import logging
import os
import json
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

# ─── CHECKPOINT SYSTEM ──────────────────────────────────────────────────────────
CHECKPOINT_FILE = None  # Set dynamically based on output path

def load_checkpoint(checkpoint_path):
    """
    Load the set of already-processed DOIs and their accumulated author records.
    Returns (processed_dois: set, master_table: list[dict]).
    """
    processed_dois = set()
    master_table = []
    
    if os.path.exists(checkpoint_path):
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)
            processed_dois = set(checkpoint_data.get("processed_dois", []))
            master_table = checkpoint_data.get("records", [])
            logger.info(f"[Checkpoint] Resuming from checkpoint: {len(processed_dois)} DOIs already processed, {len(master_table)} author records loaded.")
        except Exception as e:
            logger.warning(f"[Checkpoint] Could not load checkpoint file: {e}. Starting fresh.")
    
    return processed_dois, master_table

def save_checkpoint(checkpoint_path, processed_dois, master_table):
    """
    Save current progress: which DOIs have been processed and all accumulated records.
    """
    try:
        checkpoint_data = {
            "processed_dois": list(processed_dois),
            "records": master_table
        }
        # Write atomically: write to temp file then rename
        tmp_path = checkpoint_path + ".tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False)
        # Replace old checkpoint with new one
        if os.path.exists(checkpoint_path):
            os.remove(checkpoint_path)
        os.rename(tmp_path, checkpoint_path)
    except Exception as e:
        logger.error(f"[Checkpoint] Error saving checkpoint: {e}")

# ─── MAIN PIPELINE ──────────────────────────────────────────────────────────────

def export_master_table(master_table, output_csv, output_json):
    """
    Exports the current master table to CSV and JSON formats.
    Ensures all expected columns are present.
    """
    if not master_table:
        return
        
    final_df = pd.DataFrame(master_table)
    
    expected_columns = [
        "PAPER_TITLE", "DOI", "YEAR", "OPEN_ACCESS_OA", "FUNDING_OA",
        "AUTHOR_NAME", "AUTHOR_POS_OA", "IS_CORRESPONDING_OA", "AFFILIATION_OA",
        "GEO_COUNTRY_OA", "AUTHOR_ID_OA", "WORKS_COUNT_OA", "CITATIONS_OA",
        "HINDEX_OA", "I10INDEX_OA", "2YR_MEAN_OA", "TOPICS_OA", "PRIMARY_TOPIC_OA",
        "KEYWORDS_OA", "PMID_PM",
        "MESH_PM", "FUNDING_PM", "AUTHOR_NAME_PM", "AFFILIATION_PM",
        "INFLUENTIAL_CITATIONS_SS", "CITATION_CONTEXTS_SS",
        "AUTHOR_ID_SS", "AUTHOR_NAME_SS", "ORCID_SS",
        "HINDEX_SS", "CITATIONS_SS",
        "ORCID", "ORCID_EMPLOYMENT",
        "GENDER", "PROFILE_CLASSIFICATION"
    ]
        
    # Ensure all columns exist, fill missing ones with 'No data'
    for col in expected_columns:
        if col not in final_df.columns:
            final_df[col] = "No data"
                
    final_df = final_df[expected_columns]
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    
    final_df.to_csv(output_csv, index=False)
    final_df.to_json(output_json, orient='records', indent=4)

def run_pipeline(input_csv, output_csv, output_json):
    """
    Orchestrates the entire data extraction pipeline.
    Features:
    - Checkpoint/resume: saves progress after each DOI so it can continue from where it left off
    - VPN Guard: pauses on Scopus HTTP 400 (institutional access error) and waits for user to reconnect VPN
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
    
    # 2. Load Checkpoint
    checkpoint_dir = os.path.dirname(output_csv)
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_path = os.path.join(checkpoint_dir, "pipeline_checkpoint.json")
    
    processed_dois, master_table = load_checkpoint(checkpoint_path)
    
    remaining_dois = [d for d in dois if d not in processed_dois]
    logger.info(f"Total DOIs: {len(dois)} | Already processed: {len(processed_dois)} | Remaining: {len(remaining_dois)}")
    
    # 3. Loop over remaining DOIs (Sequential Evaluation)
    for index, doi in enumerate(remaining_dois):
        global_index = len(processed_dois) + index + 1
        logger.info(f"\n=======================================================")
        logger.info(f" DOI {global_index}/{len(dois)}: {doi}")
        logger.info(f"=======================================================")
        
        try:
            # --- NODE 1: OPEN ALEX (The Foundation) ---
            logger.info("-> Executing Node: OpenAlex...")
            authors_list = process_openalex(doi, config)
            if not authors_list:
                logger.warning(f"DOI {doi} not found in OpenAlex. Skipping to the next.")
                processed_dois.add(doi)
                save_checkpoint(checkpoint_path, processed_dois, master_table)
                continue
                
            # --- NODE 2: PUBMED (Fallbacks & Ghost Authors) ---
            logger.info("-> Executing Node: PubMed...")
            authors_list = process_pubmed(doi, authors_list, config)
            
            # --- NODE 3: SCOPUS (Paper-level metadata) ---
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
            processed_dois.add(doi)
            
            # Save checkpoint after every DOI
            save_checkpoint(checkpoint_path, processed_dois, master_table)
            export_master_table(master_table, output_csv, output_json)
            logger.info(f"[Checkpoint] Progress saved and CSV updated. {len(processed_dois)}/{len(dois)} DOIs complete.")
            
        except ConnectionError as e:
            error_msg = str(e)
            if "SCOPUS_VPN_ERROR" in error_msg or "SCOPUS_AUTH_ERROR" in error_msg:
                logger.error("=" * 70)
                logger.error(" PIPELINE PAUSED — SCOPUS VPN/ACCESS ERROR")
                logger.error("=" * 70)
                logger.error(f" Error: {error_msg}")
                logger.error(f" DOI that failed: {doi}")
                logger.error(f" Progress saved: {len(processed_dois)}/{len(dois)} DOIs processed.")
                logger.error("")
                logger.error(" ACTION REQUIRED:")
                logger.error("   1. Reconnect the Yachay Tech FortiClient VPN")
                logger.error("   2. Re-run: python src/main.py")
                logger.error("   3. The pipeline will resume from DOI #{} automatically.".format(global_index))
                logger.error("=" * 70)
                # Save checkpoint before stopping
                save_checkpoint(checkpoint_path, processed_dois, master_table)
                return
            else:
                logger.error(f"Connection error for DOI {doi}: {e}. Skipping.")
                processed_dois.add(doi)
                save_checkpoint(checkpoint_path, processed_dois, master_table)
                
        except Exception as e:
            logger.error(f"Unexpected error processing DOI {doi}: {e}. Skipping to next.")
            processed_dois.add(doi)
            save_checkpoint(checkpoint_path, processed_dois, master_table)
        
        # Polite delay between iteration cycles
        time.sleep(1)
        
    # 4. Final Cleanup
    logger.info(f"Pipeline finished. Finalizing {len(master_table)} author records.")
    
    # Clean up checkpoint file on successful completion
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)
        logger.info("[Checkpoint] Pipeline completed successfully. Checkpoint file removed.")
    
    logger.info("=" * 70)
    logger.info(f" PIPELINE COMPLETE")
    logger.info(f" Total DOIs processed: {len(processed_dois)}")
    logger.info(f" Total author records: {len(master_table)}")
    logger.info(f" Output CSV: {output_csv}")
    logger.info(f" Output JSON: {output_json}")
    logger.info("=" * 70)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "input", "input_dois.csv")
    output_csv = os.path.join(base_dir, "data", "output", "csv", "MASTER_AUTHOR_TABLE.csv")
    output_json = os.path.join(base_dir, "data", "output", "json", "MASTER_AUTHOR_TABLE.json")
    
    # Ensure input directory exists to prevent errors on first run
    os.makedirs(os.path.dirname(input_file), exist_ok=True)
    
    run_pipeline(input_file, output_csv, output_json)
