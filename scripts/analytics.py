import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def generate_analytics():
    # Set the style to look like a professional scientific journal
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    plt.rcParams['font.family'] = 'sans-serif'
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_dir, "data", "output", "csv", "MASTER_AUTHOR_TABLE.csv")
    output_dir = os.path.join(base_dir, "assets", "figures", "analytics")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading Master Author Table...")
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Data Cleaning and Preparation
    # 1. Clean H-Index and Citations
    df['HINDEX_OA'] = pd.to_numeric(df['HINDEX_OA'], errors='coerce').fillna(0)
    df['CITATIONS_OA'] = pd.to_numeric(df['CITATIONS_OA'], errors='coerce').fillna(0)
    
    # 2. Clean Profiles
    def extract_base_profile(prof):
        if pd.isna(prof) or prof == "No data" or prof == "Unknown":
            return "UNKNOWN"
        return str(prof).split(" | ")[0].strip()
    
    df['BASE_PROFILE'] = df['PROFILE_CLASSIFICATION'].apply(extract_base_profile)
    
    # 3. Clean Countries (Exclude missing)
    df_country = df[~df['GEO_COUNTRY_OA'].isin(['No data', 'Unknown', np.nan])].copy()
    
    print("Generating Figure 1: Global H-Index Disparity...")
    # ==========================================
    # FIGURE 1: GLOBAL H-INDEX DISPARITY
    # ==========================================
    # Limit to top 25 countries by number of authors for readability
    top_countries = df_country['GEO_COUNTRY_OA'].value_counts().head(25).index.tolist()
    df_country_top = df_country[df_country['GEO_COUNTRY_OA'].isin(top_countries)].copy()
    
    # Sort by median H-Index
    order = df_country_top.groupby('GEO_COUNTRY_OA')['HINDEX_OA'].median().sort_values(ascending=False).index
    
    fig1, ax1 = plt.subplots(figsize=(16, 7))
    
    sns.boxplot(x='GEO_COUNTRY_OA', y='HINDEX_OA', data=df_country_top, order=order,
                palette="viridis", ax=ax1, fliersize=3)
    
    ax1.set_title('Global H-Index Disparity by Country of Origin\n(Scientometric Impact Gap — Top 25 Countries by Author Count)',
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Country (ISO Code)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('H-Index (OpenAlex)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=90, ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_global_hindex_disparity.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generating Figure 2: Clinical vs. Technical Impact Matrix...")
    # ==========================================
    # FIGURE 2: CLINICAL VS TECHNICAL IMPACT
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    # Filter out UNKNOWN for a cleaner chart
    df_profile = df[df['BASE_PROFILE'] != 'UNKNOWN'].copy()
    
    # Use violin plot to show distribution density
    ax2 = sns.violinplot(x='BASE_PROFILE', y='HINDEX_OA', data=df_profile, palette="mako", inner="quartile")
    # Use stripplot instead of swarmplot — swarmplot hangs with 7k+ points
    sns.stripplot(x='BASE_PROFILE', y='HINDEX_OA', data=df_profile, color="black", alpha=0.15, jitter=True, size=2)
    
    plt.title('Clinical vs. Technical Representation and Impact\n(H-Index Distribution by LLM-Classified Role)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Research Profile Classification', fontsize=12, fontweight='bold')
    plt.ylabel('H-Index (OpenAlex)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_clinical_vs_technical_impact.png"), dpi=300)
    plt.close()

    print("Generating Figure 3: Parachute Research Index...")
    # ==========================================
    # FIGURE 3: PARACHUTE RESEARCH INDEX
    # ==========================================
    # We want to see the proportion of First, Middle, and Last authors per country.
    # High-Income Countries usually dominate First/Last. LMICs usually dominate Middle.
    
    df_para = df_country[~df_country['AUTHOR_POS_OA'].isin(['No data', 'Unknown', np.nan])].copy()
    
    # Normalize author positions
    df_para['AUTHOR_POS_OA'] = df_para['AUTHOR_POS_OA'].str.lower()
    
    # Create crosstab for 100% stacked bar
    ct = pd.crosstab(df_para['GEO_COUNTRY_OA'], df_para['AUTHOR_POS_OA'], normalize='index') * 100
    
    # Ensure correct column order if they exist
    cols_order = []
    for col in ['first', 'middle', 'last']:
        if col in ct.columns:
            cols_order.append(col)
    ct = ct[cols_order]
    
    # Sort by percentage of 'middle' authorship (highest middle authorship = higher risk of being parachute researchers)
    if 'middle' in ct.columns:
        ct = ct.sort_values(by='middle', ascending=False)
        
    ax3 = ct.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='coolwarm', edgecolor='black')
    
    plt.title('The "Parachute Research" Matrix\n(Authorship Hierarchy by Country of Origin)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Country (ISO Code)', fontsize=12, fontweight='bold')
    plt.ylabel('Percentage of Authorship Position (%)', fontsize=12, fontweight='bold')
    
    # Legend
    plt.legend(title='Author Position', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_parachute_research_index.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Analytics generation complete! Check the assets/figures/analytics directory.")

if __name__ == "__main__":
    generate_analytics()
