from preprocessing import preprocess_data
from rule_based_scoring import apply_scoring_and_ltv
from geospatial_mapping import create_interactive_map
from statistical_analysis import analyze_correlations, calculate_feature_importance, plot_correlations
import geopandas as gpd
import pandas as pd

# Step 1: Preprocess Data
# preprocess_data("data/real_estate_data.tsv", "data/real_estate_data_CA_2024.csv")

# Step 2: Apply Scoring and Adjust LTV
apply_scoring_and_ltv("data/real_estate_data_CA_2024.csv", "output/final_real_estate_data_with_ltv.csv")

# Step 3: Statistical Analysis
processed_data = pd.read_csv("output/final_real_estate_data_with_ltv.csv")

# Debugging: Check processed data
print("\n--- Processed Data Sample ---")
print(processed_data.head())
print("\n--- MARKET_SCORE Summary ---")
print(processed_data['MARKET_SCORE'].describe())

# Analyze correlations
correlation_df = analyze_correlations(processed_data, target_col='MARKET_SCORE')
correlation_df.to_csv("output/correlation_analysis.csv", index=True)

# Plot correlations heatmap
plot_correlations(correlation_df, "output/correlation_heatmap.png")

# Step 4: Generate Geospatial Maps
geo_data = gpd.read_file("USA_ZIP_Code_Areas_anaylsis_2177383641487863978/zip_poly.shp")
processed_data = pd.read_csv("output/final_real_estate_data_with_ltv.csv")

# Standardize column names for merging
geo_data = geo_data.rename(columns={'ZIP_CODE': 'ZIPCODE'})
processed_data = processed_data.rename(columns={'REGION': 'ZIPCODE'})

# Convert ZIPCODE to string in both DataFrames
geo_data['ZIPCODE'] = geo_data['ZIPCODE'].astype(str)
processed_data['ZIPCODE'] = processed_data['ZIPCODE'].astype(str)

# Merge the data
geo_data = geo_data.merge(processed_data, on="ZIPCODE", how="inner")

# Debugging: Check CRS and invalid geometries
print("\n--- CRS Check ---")
print(geo_data.crs)
geo_data = geo_data.to_crs(epsg=4326)

print("\n--- Invalid Geometries ---")
invalid_geometries = geo_data[~geo_data.is_valid]
print(f"Number of invalid geometries: {invalid_geometries.shape[0]}")

# Simplify geometries to reduce size
geo_data['geometry'] = geo_data['geometry'].simplify(tolerance=0.001, preserve_topology=True)

# Debugging: Check GeoDataFrame sample
print("\n--- GeoDataFrame Sample ---")
print(geo_data.head())

# Generate and save the maps
market_score_map = create_interactive_map(geo_data, 'MARKET_SCORE', "Market Score by Zip Code", cmap='YlOrRd')
ltv_map = create_interactive_map(geo_data, 'ADJUSTED_LTV', "Adjusted LTV by Zip Code", cmap='RdYlGn')

market_score_map.save("output/market_score_map.html")
ltv_map.save("output/ltv_map.html")