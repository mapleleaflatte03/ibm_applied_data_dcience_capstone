"""
SQL-based EDA for Automotive Sales Data
Uses pandasql to perform SQL queries on the dataset
"""

import pandas as pd
import pandasql as psql
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load the dataset"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'automotive_sales.csv')
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(Day=1))
    return df

def run_sql_queries(df):
    """Run various SQL queries for EDA"""
    
    print("=" * 80)
    print("SQL-BASED EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Query 1: Total sales by vehicle type
    print("\n[Query 1] Total Sales by Vehicle Type:")
    print("-" * 80)
    q1 = """
    SELECT 
        Vehicle_Type,
        COUNT(*) as Count,
        SUM(Sales) as Total_Sales,
        AVG(Sales) as Avg_Sales,
        SUM(Revenue) as Total_Revenue
    FROM df
    GROUP BY Vehicle_Type
    ORDER BY Total_Sales DESC
    """
    result1 = psql.sqldf(q1, locals())
    print(result1.to_string(index=False))
    
    # Query 2: Sales by year and recession status
    print("\n[Query 2] Sales by Year and Recession Status:")
    print("-" * 80)
    q2 = """
    SELECT 
        Year,
        SUM(CASE WHEN Recession = 1 THEN 1 ELSE 0 END) as Recession_Months,
        AVG(CASE WHEN Recession = 0 THEN Sales END) as Avg_Sales_Non_Recession,
        AVG(CASE WHEN Recession = 1 THEN Sales END) as Avg_Sales_Recession,
        (AVG(CASE WHEN Recession = 0 THEN Sales END) - 
         AVG(CASE WHEN Recession = 1 THEN Sales END)) as Sales_Difference
    FROM df
    GROUP BY Year
    ORDER BY Year
    """
    result2 = psql.sqldf(q2, locals())
    print(result2.to_string(index=False))
    
    # Query 3: Top 10 cities by revenue
    print("\n[Query 3] Top 10 Cities by Total Revenue:")
    print("-" * 80)
    q3 = """
    SELECT 
        City,
        Region,
        COUNT(*) as Transaction_Count,
        SUM(Sales) as Total_Sales,
        SUM(Revenue) as Total_Revenue,
        AVG(Sales) as Avg_Sales
    FROM df
    GROUP BY City, Region
    ORDER BY Total_Revenue DESC
    LIMIT 10
    """
    result3 = psql.sqldf(q3, locals())
    print(result3.to_string(index=False))
    
    # Query 4: Seasonal analysis
    print("\n[Query 4] Sales Analysis by Season:")
    print("-" * 80)
    q4 = """
    SELECT 
        Season,
        COUNT(*) as Count,
        AVG(Sales) as Avg_Sales,
        AVG(Price) as Avg_Price,
        SUM(Revenue) as Total_Revenue,
        AVG(GDP) as Avg_GDP,
        AVG(Unemployment_Rate) as Avg_Unemployment
    FROM df
    GROUP BY Season
    ORDER BY Avg_Sales DESC
    """
    result4 = psql.sqldf(q4, locals())
    print(result4.to_string(index=False))
    
    # Query 5: Vehicle type performance by region
    print("\n[Query 5] Vehicle Type Performance by Region:")
    print("-" * 80)
    q5 = """
    SELECT 
        Region,
        Vehicle_Type,
        COUNT(*) as Count,
        AVG(Sales) as Avg_Sales,
        AVG(Price) as Avg_Price
    FROM df
    GROUP BY Region, Vehicle_Type
    HAVING Count >= 10
    ORDER BY Region, Avg_Sales DESC
    """
    result5 = psql.sqldf(q5, locals())
    print(result5.to_string(index=False))
    
    # Query 6: Correlation between advertising and sales
    print("\n[Query 6] Advertising Impact Analysis:")
    print("-" * 80)
    q6 = """
    SELECT 
        CASE 
            WHEN Advertising_Expenditure < 30 THEN 'Low (<30)'
            WHEN Advertising_Expenditure < 50 THEN 'Medium (30-50)'
            WHEN Advertising_Expenditure < 70 THEN 'High (50-70)'
            ELSE 'Very High (>70)'
        END as Advertising_Category,
        COUNT(*) as Count,
        AVG(Sales) as Avg_Sales,
        AVG(Revenue) as Avg_Revenue,
        AVG(Price) as Avg_Price
    FROM df
    GROUP BY Advertising_Category
    ORDER BY Avg_Sales DESC
    """
    result6 = psql.sqldf(q6, locals())
    print(result6.to_string(index=False))
    
    # Query 7: Economic indicators impact
    print("\n[Query 7] Economic Indicators Impact on Sales:")
    print("-" * 80)
    q7 = """
    SELECT 
        CASE 
            WHEN GDP < 65 THEN 'Low GDP'
            WHEN GDP < 75 THEN 'Medium GDP'
            ELSE 'High GDP'
        END as GDP_Category,
        CASE 
            WHEN Unemployment_Rate < 5 THEN 'Low Unemployment'
            WHEN Unemployment_Rate < 8 THEN 'Medium Unemployment'
            ELSE 'High Unemployment'
        END as Unemployment_Category,
        COUNT(*) as Count,
        AVG(Sales) as Avg_Sales,
        SUM(Revenue) as Total_Revenue
    FROM df
    GROUP BY GDP_Category, Unemployment_Category
    ORDER BY Avg_Sales DESC
    """
    result7 = psql.sqldf(q7, locals())
    print(result7.to_string(index=False))
    
    # Query 8: Year-over-year growth
    print("\n[Query 8] Year-over-Year Sales Growth:")
    print("-" * 80)
    q8 = """
    WITH yearly_sales AS (
        SELECT 
            Year,
            AVG(Sales) as Avg_Sales,
            SUM(Revenue) as Total_Revenue
        FROM df
        GROUP BY Year
    )
    SELECT 
        a.Year,
        a.Avg_Sales as Avg_Sales_Current,
        b.Avg_Sales as Avg_Sales_Previous,
        ((a.Avg_Sales - b.Avg_Sales) / b.Avg_Sales * 100) as YoY_Growth_Pct,
        a.Total_Revenue
    FROM yearly_sales a
    LEFT JOIN yearly_sales b ON a.Year = b.Year + 1
    ORDER BY a.Year
    """
    result8 = psql.sqldf(q8, locals())
    print(result8.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("SQL EDA Analysis Complete!")
    print("=" * 80)
    
    # Save results to CSV
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    sql_results_dir = os.path.join(project_dir, 'data', 'sql_results')
    os.makedirs(sql_results_dir, exist_ok=True)
    
    result1.to_csv(os.path.join(sql_results_dir, 'sales_by_vehicle_type.csv'), index=False)
    result2.to_csv(os.path.join(sql_results_dir, 'sales_by_year_recession.csv'), index=False)
    result3.to_csv(os.path.join(sql_results_dir, 'top_cities.csv'), index=False)
    result4.to_csv(os.path.join(sql_results_dir, 'seasonal_analysis.csv'), index=False)
    
    print(f"\nSQL query results saved to {sql_results_dir}")

if __name__ == "__main__":
    df = load_data()
    run_sql_queries(df)

