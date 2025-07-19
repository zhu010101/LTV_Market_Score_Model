import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class MarketScoreCalculator:
    def __init__(self, weights=None):
        """
        Initialize the Market Score Calculator with optional weights.
        """
        self.weights = {
                'SOLD_ABOVE_LIST': 0.3,
                'PENDING_SALES_YOY': 0.2,
                'AVG_SALE_TO_LIST': 0.3,
                'MEDIAN_DOM': 0.2
        }
        self.scaler = MinMaxScaler()

    def normalize_features(self, df):
        """
        Normalize the input features and invert necessary columns.
        """
        features_to_normalize = ['SOLD_ABOVE_LIST', 'PENDING_SALES_YOY', 'AVG_SALE_TO_LIST', 'MEDIAN_DOM']
        df[features_to_normalize] = self.scaler.fit_transform(df[features_to_normalize])
        df['MEDIAN_DOM'] = 1 - df['MEDIAN_DOM']  # Invert Days on Market
        return df

    def calculate_score(self, row):
        """
        Calculate the Compete Score for a single row.
        """
        score = (
            self.weights['SOLD_ABOVE_LIST'] * row['SOLD_ABOVE_LIST'] +
            self.weights['PENDING_SALES_YOY'] * row['PENDING_SALES_YOY'] +
            self.weights['AVG_SALE_TO_LIST'] * row['AVG_SALE_TO_LIST'] +
            self.weights['MEDIAN_DOM'] * row['MEDIAN_DOM']
        )
        return max(0, min(100, score * 110))  # Scale to 0–100

    def apply(self, df):
        """
        Normalize features and apply Market Score calculation to the DataFrame.
        """
        df = self.normalize_features(df)
        df['MARKET_SCORE'] = df.apply(self.calculate_score, axis=1)
        df['MARKET_SCORE'] = df['MARKET_SCORE'].round(0)
        return df

# Example Usage
def apply_scoring_and_ltv(data_path, output_path):
    """
    Apply Market Scoring and LTV adjustments to the dataset.
    """
    data = pd.read_csv(data_path)
    calculator = MarketScoreCalculator()
    data = calculator.apply(data)
    
    # Adjust LTV based on Market Score
    def adjust_ltv(score, base_ltv=70):
        if score >= 90:  # Extremely high score
            return base_ltv + 10
        elif score >= 80:  # Very high score
            return base_ltv + 7
        elif score >= 60:  # Medium-high score
            return base_ltv + 3
        elif score >= 40:  # Medium score
            return base_ltv
        elif score >= 20:  # Medium-low score
            return base_ltv - 5
        else:  # Low score
            return base_ltv - 10
    
    data['ADJUSTED_LTV'] = data['MARKET_SCORE'].apply(adjust_ltv)
    # Ensure ADJUSTED_LTV is numeric
    data['ADJUSTED_LTV'] = pd.to_numeric(data['ADJUSTED_LTV'], errors='coerce')  # Convert to numeric
    data['ADJUSTED_LTV'] = data['ADJUSTED_LTV'].fillna(0).round(0) # Replace NaN with 0
    data.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

# Uncomment to execute
# apply_scoring_and_ltv("data/real_estate_data_CA_2024.csv", "output/final_real_estate_data_with_ltv.csv")