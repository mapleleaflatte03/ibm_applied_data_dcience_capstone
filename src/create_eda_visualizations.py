"""
Create EDA Visualizations for Capstone Project
Generates all necessary plots for the presentation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')

def load_data():
    """Load the cleaned dataset"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'automotive_sales.csv')
    
    df = pd.read_csv(data_path)
    
    # Create Date column
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(Day=1))
    
    # Create additional features
    df['Quarter'] = df['Month'].apply(lambda x: (x-1)//3 + 1)
    df['Price_Category'] = pd.cut(
        df['Price'],
        bins=[0, 20, 30, 40, 100],
        labels=['Budget', 'Mid-range', 'Premium', 'Luxury']
    )
    sales_median = df['Sales'].median()
    df['Sales_Category'] = (df['Sales'] > sales_median).astype(int)
    
    return df

def create_all_visualizations():
    """Create all EDA visualizations"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(project_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    df = load_data()
    
    print("Creating EDA visualizations...")
    
    # 1. Sales over time
    plt.figure(figsize=(14, 6))
    df_time = df.groupby('Date')['Sales'].mean()
    plt.plot(df_time.index, df_time.values, linewidth=2, color='steelblue')
    plt.title('Average Sales Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Average Sales', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'sales_over_time.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Sales by Vehicle Type
    plt.figure(figsize=(12, 6))
    vehicle_sales = df.groupby('Vehicle_Type')['Sales'].mean().sort_values(ascending=False)
    colors = plt.cm.viridis(np.linspace(0, 1, len(vehicle_sales)))
    plt.bar(vehicle_sales.index, vehicle_sales.values, color=colors)
    plt.title('Average Sales by Vehicle Type', fontsize=16, fontweight='bold')
    plt.xlabel('Vehicle Type', fontsize=12)
    plt.ylabel('Average Sales', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'sales_by_vehicle_type.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Sales by Season
    plt.figure(figsize=(10, 6))
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_sales = df.groupby('Season')['Sales'].mean().reindex(season_order)
    plt.bar(season_sales.index, season_sales.values, color=['green', 'orange', 'brown', 'blue'])
    plt.title('Average Sales by Season', fontsize=16, fontweight='bold')
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Average Sales', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'sales_by_season.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    numeric_cols = ['Sales', 'Price', 'Advertising_Expenditure', 'Unemployment_Rate', 'GDP', 'Revenue']
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Heatmap of Numerical Variables', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Sales Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(df['Sales'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    axes[0].set_title('Sales Distribution (Histogram)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Sales', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    
    axes[1].boxplot(df['Sales'], vert=True)
    axes[1].set_title('Sales Distribution (Boxplot)', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Sales', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'sales_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Recession Impact
    plt.figure(figsize=(12, 6))
    recession_impact = df.groupby(['Year', 'Recession'])['Sales'].mean().reset_index()
    recession_years = recession_impact[recession_impact['Recession']==1]['Year'].values
    non_recession_years = recession_impact[recession_impact['Recession']==0]['Year'].values
    
    plt.bar(non_recession_years, 
            recession_impact[recession_impact['Recession']==0]['Sales'].values,
            color='green', alpha=0.7, label='Non-Recession')
    plt.bar(recession_years,
            recession_impact[recession_impact['Recession']==1]['Sales'].values,
            color='red', alpha=0.7, label='Recession')
    plt.title('Impact of Recession on Sales', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Sales', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'recession_impact.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Sales by Region
    plt.figure(figsize=(12, 6))
    region_sales = df.groupby('Region')['Sales'].mean().sort_values(ascending=False)
    colors = plt.cm.Set3(np.linspace(0, 1, len(region_sales)))
    plt.bar(region_sales.index, region_sales.values, color=colors)
    plt.title('Average Sales by Region', fontsize=16, fontweight='bold')
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Average Sales', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'sales_by_region.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. Price vs Sales Scatter
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Price'], df['Sales'], alpha=0.5, s=50)
    plt.title('Price vs Sales Relationship', fontsize=16, fontweight='bold')
    plt.xlabel('Price (thousands)', fontsize=12)
    plt.ylabel('Sales', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(df['Price'], df['Sales'], 1)
    p = np.poly1d(z)
    plt.plot(df['Price'].sort_values(), p(df['Price'].sort_values()), 
             "r--", alpha=0.8, linewidth=2, label='Trend Line')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'price_vs_sales.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("All visualizations created successfully!")
    print(f"Images saved to: {images_dir}")

if __name__ == "__main__":
    create_all_visualizations()

