import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_zip_level_report(input_file, output_folder, column="MARKET_SCORE"):
    """
    Generate zip-level reports with visuals for Market Score or Adjusted LTV.
    
    Args:
        input_file (str): Path to the CSV file containing processed data.
        output_folder (str): Path to save the generated plots.
        column (str): Column to analyze ("MARKET_SCORE" or "ADJUSTED_LTV").
    """
    # Load data
    data = pd.read_csv(input_file)

    # Ensure column is numeric
    data[column] = pd.to_numeric(data[column], errors='coerce')

    # Distribution Histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], bins=30, kde=True, color="skyblue")
    plt.title(f"{column} Distribution Across ZIP Codes", fontsize=16)
    plt.xlabel(column, fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(axis='y')
    plt.savefig(f"{output_folder}/{column}_distribution_histogram.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=data[column], color="lightcoral")
    plt.title(f"{column} Boxplot", fontsize=16)
    plt.xlabel(column, fontsize=12)
    plt.savefig(f"{output_folder}/{column}_boxplot.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Top 10 ZIP Codes
    top_10 = data.nlargest(10, column)[["REGION", column]]
    plt.figure(figsize=(10, 6))
    sns.barplot(x=column, y="REGION", data=top_10, palette="viridis")
    plt.title(f"Top 10 ZIP Codes by {column}", fontsize=16)
    plt.xlabel(column, fontsize=12)
    plt.ylabel("ZIP Code", fontsize=12)
    plt.savefig(f"{output_folder}/top_10_{column}_zipcodes.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Bottom 10 ZIP Codes
    bottom_10 = data.nsmallest(10, column)[["REGION", column]]
    plt.figure(figsize=(10, 6))
    sns.barplot(x=column, y="REGION", data=bottom_10, palette="mako")
    plt.title(f"Bottom 10 ZIP Codes by {column}", fontsize=16)
    plt.xlabel(column, fontsize=12)
    plt.ylabel("ZIP Code", fontsize=12)
    plt.savefig(f"{output_folder}/bottom_10_{column}_zipcodes.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Scatter Plot: Market Score vs. Adjusted LTV (if both columns exist)
    if "MARKET_SCORE" in data.columns and "ADJUSTED_LTV" in data.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="MARKET_SCORE", y="ADJUSTED_LTV", data=data, color="teal")
        plt.title("Market Score vs Adjusted LTV", fontsize=16)
        plt.xlabel("Market Score", fontsize=12)
        plt.ylabel("Adjusted LTV", fontsize=12)
        plt.grid()
        plt.savefig(f"{output_folder}/market_score_vs_ltv_scatter.png", dpi=300, bbox_inches='tight')
        plt.close()

    print(f"All visuals for {column} have been saved in {output_folder}.")

# Example Usage
if __name__ == "__main__":
    # Input and output paths
    input_file = "output/final_real_estate_data_with_ltv.csv"
    output_folder = "output/reports"

    # Create reports for Market Score
    generate_zip_level_report(input_file, output_folder, column="MARKET_SCORE")

    # Create reports for Adjusted LTV
    generate_zip_level_report(input_file, output_folder, column="ADJUSTED_LTV")