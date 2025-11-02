"""
Data Generation Script for IBM Applied Data Science Capstone Project
Generates synthetic automotive sales dataset with realistic patterns

Author: Son Nguyen
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def generate_automotive_sales_data(n_records=2000, random_seed=42):
    """
    Generate synthetic automotive sales data with realistic patterns
    
    Parameters:
    -----------
    n_records : int
        Number of records to generate
    random_seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pd.DataFrame
        Generated dataset with columns:
        - Year, Month, Vehicle_Type, Sales, Price, 
        - Advertising_Expenditure, Unemployment_Rate, GDP, 
        - Season, Recession, Region, City, Latitude, Longitude
    """
    np.random.seed(random_seed)
    
    # Define base ranges
    years = list(range(2015, 2024))
    months = list(range(1, 13))
    vehicle_types = ['Sedan', 'SUV', 'Truck', 'Coupe', 'Hatchback', 'Van', 'Hybrid', 'Electric']
    regions = ['North', 'South', 'East', 'West', 'Central']
    cities_by_region = {
        'North': ['Boston', 'New York', 'Chicago', 'Detroit'],
        'South': ['Atlanta', 'Houston', 'Miami', 'Dallas'],
        'East': ['Philadelphia', 'Washington', 'Baltimore', 'Charlotte'],
        'West': ['Los Angeles', 'San Francisco', 'Seattle', 'Phoenix'],
        'Central': ['Denver', 'Kansas City', 'Minneapolis', 'St. Louis']
    }
    
    # Coordinates for cities
    city_coords = {
        'Boston': (42.3601, -71.0589),
        'New York': (40.7128, -74.0060),
        'Chicago': (41.8781, -87.6298),
        'Detroit': (42.3314, -83.0458),
        'Atlanta': (33.7490, -84.3880),
        'Houston': (29.7604, -95.3698),
        'Miami': (25.7617, -80.1918),
        'Dallas': (32.7767, -96.7970),
        'Philadelphia': (39.9526, -75.1652),
        'Washington': (38.9072, -77.0369),
        'Baltimore': (39.2904, -76.6122),
        'Charlotte': (35.2271, -80.8431),
        'Los Angeles': (34.0522, -118.2437),
        'San Francisco': (37.7749, -122.4194),
        'Seattle': (47.6062, -122.3321),
        'Phoenix': (33.4484, -112.0740),
        'Denver': (39.7392, -104.9903),
        'Kansas City': (39.0997, -94.5786),
        'Minneapolis': (44.9778, -93.2650),
        'St. Louis': (38.6270, -90.1994)
    }
    
    # Recession periods
    recession_years = [2020, 2021]
    recession_months_2020 = list(range(3, 13))  # March-December 2020
    recession_months_2021 = list(range(1, 7))   # January-June 2021
    
    data = []
    
    for i in range(n_records):
        year = np.random.choice(years)
        month = np.random.choice(months)
        
        # Determine recession status
        is_recession = (year in recession_years and 
                       ((year == 2020 and month in recession_months_2020) or
                        (year == 2021 and month in recession_months_2021)))
        
        # Season mapping
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'Fall'
        
        # Select region and city
        region = np.random.choice(regions)
        city = np.random.choice(cities_by_region[region])
        lat, lon = city_coords[city]
        
        # Vehicle type selection (some types more popular)
        vehicle_type = np.random.choice(
            vehicle_types,
            p=[0.20, 0.25, 0.15, 0.10, 0.10, 0.05, 0.08, 0.07]
        )
        
        # Base price by vehicle type (in thousands)
        base_prices = {
            'Sedan': 25, 'SUV': 35, 'Truck': 40, 'Coupe': 30,
            'Hatchback': 20, 'Van': 32, 'Hybrid': 28, 'Electric': 45
        }
        
        # Generate features with realistic relationships
        base_price = base_prices[vehicle_type]
        price = np.random.normal(base_price, base_price * 0.15)
        price = max(15, price)  # Minimum price
        
        # GDP (normalized, 0-100 scale)
        base_gdp = 70 + (year - 2015) * 1.5  # Gradual growth
        if is_recession:
            gdp = np.random.normal(base_gdp - 10, 5)
        else:
            gdp = np.random.normal(base_gdp, 3)
        gdp = max(50, min(100, gdp))
        
        # Unemployment rate (lower is better)
        base_unemployment = 5.0
        if is_recession:
            unemployment = np.random.normal(base_unemployment + 4, 1.5)
        else:
            unemployment = np.random.normal(base_unemployment, 1.0)
        unemployment = max(3.0, min(15.0, unemployment))
        
        # Advertising expenditure (in thousands)
        advertising = np.random.normal(50, 15)
        advertising = max(10, advertising)
        
        # Sales calculation with multiple factors
        base_sales = 100
        
        # Seasonality effect
        seasonal_multiplier = {
            'Spring': 1.1, 'Summer': 1.2, 'Fall': 1.0, 'Winter': 0.9
        }
        
        # Vehicle type popularity
        type_multiplier = {
            'SUV': 1.3, 'Sedan': 1.1, 'Truck': 1.2, 'Electric': 1.4,
            'Hybrid': 1.25, 'Coupe': 0.9, 'Hatchback': 0.95, 'Van': 1.0
        }
        
        # Recession impact
        recession_multiplier = 0.6 if is_recession else 1.0
        
        # Advertising effect (diminishing returns)
        ad_effect = 1 + (advertising / 200) * 0.3
        
        # GDP and unemployment effects
        gdp_effect = gdp / 70
        unemployment_effect = 1 - (unemployment - 5) / 20
        
        sales = (base_sales * 
                seasonal_multiplier[season] * 
                type_multiplier[vehicle_type] * 
                recession_multiplier * 
                ad_effect * 
                gdp_effect * 
                unemployment_effect)
        
        # Add some randomness
        sales = np.random.normal(sales, sales * 0.1)
        sales = max(10, sales)  # Minimum sales
        
        data.append({
            'Year': year,
            'Month': month,
            'Season': season,
            'Vehicle_Type': vehicle_type,
            'Region': region,
            'City': city,
            'Latitude': lat,
            'Longitude': lon,
            'Sales': round(sales, 2),
            'Price': round(price, 2),
            'Advertising_Expenditure': round(advertising, 2),
            'Unemployment_Rate': round(unemployment, 2),
            'GDP': round(gdp, 2),
            'Recession': 1 if is_recession else 0,
            'Revenue': round(sales * price, 2)
        })
    
    df = pd.DataFrame(data)
    
    # Add some outliers (5% of data)
    n_outliers = int(n_records * 0.05)
    outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
    
    for idx in outlier_indices:
        if np.random.random() > 0.5:
            # High sales outlier
            df.loc[idx, 'Sales'] = df.loc[idx, 'Sales'] * np.random.uniform(2, 4)
        else:
            # Low sales outlier
            df.loc[idx, 'Sales'] = df.loc[idx, 'Sales'] * np.random.uniform(0.2, 0.5)
    
    return df

if __name__ == "__main__":
    import os
    
    print("Generating automotive sales dataset...")
    df = generate_automotive_sales_data(n_records=2000, random_seed=42)
    
    # Save to CSV - use absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_path = os.path.join(project_dir, 'data', 'automotive_sales.csv')
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset generated successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nBasic statistics:")
    print(df.describe())
    print(f"\nMissing values:")
    print(df.isnull().sum())
    print(f"\nDataset saved to: {output_path}")

