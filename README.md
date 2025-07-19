# LTV_Model
# LTV_Model: Real Estate Market Analysis and Visualization

## **Overview**
The `LTV_Model` project provides tools to analyze real estate market dynamics at the ZIP-code level. It calculates **Market Scores**, adjusts Loan-to-Value (LTV) ratios, and generates interactive geospatial maps and visual reports to uncover trends and patterns in the real estate market.

### **Features**
- **Data Preprocessing**: Cleans and processes raw real estate data.
- **Market Score Calculation**: Computes ZIP-code-level competition scores based on key market metrics.
- **Adjusted LTV Calculation**: Adjusts LTV values based on Market Scores.
- **Geospatial Mapping**: Creates interactive maps to visualize Market Scores and LTV distributions.
- **Statistical Analysis**: Generates correlation heatmaps and feature importance scores.
- **Zip-Level Reports**: Produces visual distributions and charts for Market Score and LTV.

---

## **Project Structure**
```plaintext
LTV_model/
│
├── preprocessing.py            # Preprocess raw data (filter, clean, and format)
├── rule_based_scoring.py        # Apply scoring rules and adjust LTV
├── geospatial_mapping.py        # Generate interactive maps with Folium
├── statistical_analysis.py      # Perform statistical analysis and feature importance
├── zip_level_report.py          # Generate ZIP-level visual reports
├── main.py                      # Main pipeline for executing the entire workflow
│
├── data/                        # Input data folder
│   ├── real_estate_data.tsv     # Raw real estate data
│   └── USA_ZIP_Code_Areas/      # Shapefiles for ZIP code geospatial data
│
├── output/                      # Output folder for results
│   ├── final_real_estate_data_with_ltv.csv  # Processed data with scores and LTV
│   ├── market_score_map.html                 # Interactive Market Score map
│   ├── ltv_map.html                          # Interactive LTV map
│   └── reports/                              # Visual reports (plots)
│       ├── MARKET_SCORE_distribution_histogram.png
│       ├── ADJUSTED_LTV_boxplot.png
│       └── ... (other charts for patterns)
│
└── README.md                    # Project documentation
```
## **Setup**

### **1. Prerequisites**

Ensure you have Python 3.7+ installed along with the following libraries:

pandas
numpy
matplotlib
seaborn
folium
geopandas
scikit-learn

**Install the dependencies using pip:**

pip install pandas numpy matplotlib seaborn folium geopandas scikit-learn

### **2. File Setup**

Ensure the following files are present in the correct directories:

Place the raw data file (real_estate_data.tsv) in the data/ folder.
Place the shapefiles for ZIP code geospatial data in the data/USA_ZIP_Code_Areas/ folder.

## **Usage**

### **1. Run the Main Pipeline**

The main pipeline handles the entire workflow:

Preprocesses the data.
Calculates Market Scores and adjusts LTV.
Generates interactive geospatial maps.
Outputs statistical analysis and visual reports.

### **2. Outputs**

After running the scripts, you will find:

**1. Processed Data:**
output/final_real_estate_data_with_ltv.csv: Contains Market Score and LTV values for each ZIP code.

**2. Interactive Maps:**
output/market_score_map.html: Visualizes Market Scores by ZIP code.
output/ltv_map.html: Visualizes Adjusted LTV by ZIP code.

**3. Visual Reports:**
Located in output/reports/, including histograms, boxplots, and bar charts.

## **Future Enhancements**
1. Add support for additional metrics like price growth trends.
2. Enhance the visualization of interactive maps with more layers.
3. Allow filtering maps by specific ZIP code ranges or thresholds.
