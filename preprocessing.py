import pandas as pd

def preprocess_data(input_path, output_path):
    # Load Data
    data = pd.read_csv("data/real_estate_data.tsv", sep='\t')  # Replace with your file path

    # Filter Data for Jan 2024 – Dec 2024
    data['PERIOD_BEGIN'] = pd.to_datetime(data['PERIOD_BEGIN'])
    data['PERIOD_END'] = pd.to_datetime(data['PERIOD_END'])
    data = data[(data['PERIOD_BEGIN'] >= '2024-01-01') & (data['PERIOD_END'] <= '2024-12-31')]

    # Keep Only California (State Code: CA)
    data = data[data['STATE_CODE'] == 'CA']

    # Select Useful Columns
    useful_cols = [
        'REGION', 'MEDIAN_SALE_PRICE', 'HOMES_SOLD', 'HOMES_SOLD_YOY','MEDIAN_SALE_PRICE_YOY',
        'PENDING_SALES', 'PENDING_SALES_YOY', 'MEDIAN_DOM', 'INVENTORY', 'INVENTORY_YOY', 'AVG_SALE_TO_LIST', 'SOLD_ABOVE_LIST'
    ]
    data = data[useful_cols]

    # Handle Missing Values

    # For continuous variables like MEDIAN_SALE_PRICE_YOY or INVENTORY_YOY, replace missing values with the median for avoiding outliers.
    continuous_cols = ['MEDIAN_SALE_PRICE_YOY', 'HOMES_SOLD_YOY', 'PENDING_SALES_YOY', 'INVENTORY',
                    'INVENTORY_YOY', 'MEDIAN_DOM', 'AVG_SALE_TO_LIST']
    for col in continuous_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce') 
        data[col] = data[col].fillna(data[col].median())

    # For variables like PENDING_SALES and HOMES_SOLD, where missing values may indicate no activity, replace missing values with 0.
    zero_fill_cols = ['PENDING_SALES', 'HOMES_SOLD']
    for col in zero_fill_cols:
        data[col].fillna(0)
    
    data['REGION'] = data['REGION'].str.replace("Zip Code: ", "")

    # Convert all columns to numeric where possible
    numerical_columns = data.select_dtypes(include=['object', 'float64', 'int64']).columns
    data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric, errors='coerce')

    data.to_csv('data/real_estate_data_CA_2024.csv', index=False)