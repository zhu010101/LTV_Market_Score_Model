import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_regression
from scipy.stats import spearmanr

def analyze_correlations(data, target_col='MARKET_SCORE'):
    """
    Analyze correlations between features and the target column.
    """
    correlations = {}
    for col in data.select_dtypes(include='number').columns:
        if col != target_col:
            pearson_corr = data[col].corr(data[target_col])
            spearman_corr, _ = spearmanr(data[col], data[target_col])
            correlations[col] = {'Pearson': pearson_corr, 'Spearman': spearman_corr}
    return pd.DataFrame(correlations).T

def calculate_feature_importance(data, features, target):
    """
    Calculate feature importance using mutual information regression.
    """
    mi = mutual_info_regression(data[features], data[target])
    return pd.Series(mi, index=features).sort_values(ascending=False)

def plot_correlations(correlation_df, output_path="output/correlation_heatmap.png"):
    """
    Plot a heatmap of correlations and save it to the output folder.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_df, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Analysis")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Save the figure
    plt.close()  # Close the plot to avoid display in non-interactive environments