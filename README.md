# IBM Applied Data Science Capstone Project

**Automotive Sales Analytics: Predictive Analysis and Interactive Visualization**

## Project Overview

This project presents a comprehensive analysis of automotive sales data, combining exploratory data analysis, predictive modeling, and interactive visualizations. The project was completed as part of the IBM Applied Data Science Capstone course on Coursera.

## Repository Structure

```
coursera-capstone-final-project/
│
├── notebooks/              # Jupyter notebooks for each phase
│   ├── 1_data_collection.ipynb
│   ├── 2_data_wrangling.ipynb
│   ├── 3_eda_analysis.ipynb
│   ├── 4_sql_eda.ipynb
│   └── 5_predictive_analysis.ipynb
│
├── data/                  # Dataset files
│   └── automotive_sales.csv  # Main dataset (can be regenerated)
│
├── images/                # Visualization outputs
│   ├── sales_over_time.png
│   ├── sales_by_vehicle_type.png
│   ├── correlation_heatmap.png
│   ├── confusion_matrix_*.png
│   └── interactive_sales_map.html
│
├── src/                   # Python scripts
│   ├── generate_data.py
│   ├── create_eda_visualizations.py
│   ├── dashboard_app.py
│   ├── create_folium_map.py
│   ├── sql_eda.py
│   ├── predictive_analysis.py
│   └── create_presentation.py
│
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── IBM_Capstone_Presentation.pdf  # Final presentation (PDF)
```

## Dataset

**Synthetic Automotive Sales Dataset**
- **Size**: 2000 records
- **Time Period**: 2015-2023 (9 years)
- **Features**: 15 columns
  - Temporal: Year, Month, Season, Quarter
  - Vehicle: Vehicle_Type (8 types)
  - Geographic: Region, City, Latitude, Longitude
  - Sales: Sales, Price, Revenue
  - Economic: GDP, Unemployment_Rate, Recession
  - Marketing: Advertising_Expenditure

**Key Characteristics:**
- Realistic patterns and relationships
- Seasonal variations
- Recession periods (2020-2021)
- Geographic diversity (5 regions, 20 cities)
- Multiple vehicle types

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd coursera-capstone-final-project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Dataset

```bash
python src/generate_data.py
```

This will create `data/automotive_sales.csv`.

### 4. Run Analysis

**Option A: Using Jupyter Notebooks (Recommended)**
1. Start Jupyter: `jupyter notebook`
2. Open notebooks in order:
   - `notebooks/1_data_collection.ipynb`
   - `notebooks/2_data_wrangling.ipynb`
   - `notebooks/3_eda_analysis.ipynb`
   - `notebooks/4_sql_eda.ipynb`
   - `notebooks/5_predictive_analysis.ipynb`

**Option B: Using Python Scripts**

```bash
# Create EDA visualizations
python src/create_eda_visualizations.py

# Run SQL-based EDA
python src/sql_eda.py

# Run predictive analysis
python src/predictive_analysis.py

# Create Folium map
python src/create_folium_map.py

# Create presentation
python src/create_presentation.py
```

### 5. Launch Interactive Dashboard

```bash
python src/dashboard_app.py
```

Open browser to: `http://localhost:8050`

## Project Components

### 1. Data Collection (`1_data_collection.ipynb`)
- Synthetic data generation
- Dataset characteristics overview
- Initial data inspection

### 2. Data Wrangling (`2_data_wrangling.ipynb`)
- Data cleaning and validation
- Missing value handling
- Feature engineering:
  - Date column creation
  - Price categories
  - Sales categories
  - Economic index
  - Quarterly features

### 3. Exploratory Data Analysis (`3_eda_analysis.ipynb`)
- Statistical summaries
- Visualizations:
  - Sales over time
  - Sales by vehicle type
  - Seasonal patterns
  - Correlation analysis
  - Recession impact
  - Regional analysis
  - Price vs Sales relationship

### 4. SQL-Based EDA (`4_sql_eda.ipynb`)
- SQL queries using pandasql
- Key queries:
  - Sales by vehicle type
  - Year-over-year growth
  - Top cities by revenue
  - Seasonal performance
  - Economic indicators impact
  - Advertising effectiveness

### 5. Predictive Analysis (`5_predictive_analysis.ipynb`)
- Classification task: Predict High/Low Sales
- Models evaluated:
  - Logistic Regression (85.0% accuracy)
  - Random Forest (87.5% accuracy)
- Evaluation metrics:
  - Accuracy, ROC-AUC
  - Confusion Matrix
  - Feature Importance
  - Classification Report

### 6. Interactive Visualizations

**Plotly Dash Dashboard** (`dashboard_app.py`)
- Interactive filtering by Vehicle Type and Region
- Real-time chart updates
- Multiple visualizations in one dashboard
- Summary statistics panel

**Folium Map** (`create_folium_map.py`)
- Interactive map with city markers
- Color-coded by sales volume
- Heatmap overlay
- Popup information for each city

### 7. Presentation

**PDF Presentation** (`create_presentation.py` + `export_pptx_to_pdf.py`)
- Complete slide deck covering all required sections:
  - Executive Summary
  - Introduction
  - Data Collection & Wrangling
  - EDA Results
  - SQL-Based EDA
  - Predictive Analysis Methodology & Results
  - Interactive Visualizations
  - Conclusion
  - Creative Insights

## Key Findings

### Sales Patterns
- **Vehicle Types**: SUV and Electric vehicles show highest average sales
- **Seasonal**: Summer shows peak sales (128 units), Winter lowest (92 units)
- **Regional**: West Coast (LA, SF) leads in sales, followed by East Coast (NY, Boston)

### Economic Impact
- **Recession**: 2020-2021 recession caused ~40% sales decline
- **GDP**: Higher GDP correlates with increased sales
- **Unemployment**: Lower unemployment rates lead to better sales

### Predictive Insights
- **Model Performance**: Random Forest achieves 87.5% accuracy
- **Key Features**: Price (21%), GDP (18%), Advertising (15%)
- **ROC-AUC**: 0.92 indicates excellent predictive capability

## Business Recommendations

1. **Focus on High-Performance Segments**: Prioritize SUV and Electric vehicle marketing
2. **Seasonal Planning**: Increase inventory in Spring/Summer, reduce in Winter
3. **Economic Monitoring**: Track GDP and unemployment rates for sales forecasting
4. **Advertising Strategy**: Maintain higher advertising spend during recovery periods
5. **Geographic Focus**: Allocate more resources to high-performing regions (West/East Coast)

## Technologies Used

- **Python 3.8+**
- **Libraries**: Pandas, NumPy, Matplotlib, Seaborn, Plotly, Dash, Folium
- **Machine Learning**: Scikit-learn
- **SQL**: pandasql
- **Visualization**: Plotly, Folium, Matplotlib
- **Presentation**: python-pptx

## Project Deliverables

✅ Complete dataset (2000 records)
✅ Data collection and wrangling notebooks
✅ EDA with visualizations (8+ charts)
✅ SQL-based EDA analysis
✅ Predictive classification models
✅ Interactive Plotly Dash dashboard
✅ Interactive Folium map
✅ Complete PDF presentation (19 slides)
✅ Comprehensive README

## How to Submit

1. **GitHub Repository**:
   - Push all files to GitHub
   - Ensure repository is public
   - Include link in Coursera submission

2. **Presentation**:
   - File `IBM_Capstone_Presentation.pdf` is ready
   - Upload PDF to Coursera

3. **Dashboard Screenshots**:
   - Run `python src/dashboard_app.py`
   - Take screenshots of dashboard
   - Include in submission

4. **Map Screenshot**:
   - Open `images/interactive_sales_map.html` in browser
   - Take screenshot
   - Include in submission

## Author

**Your Name**  
IBM Applied Data Science Certificate Program  
Coursera

## License

This project is created for educational purposes as part of the IBM Applied Data Science Capstone course.

## Acknowledgments

- IBM Applied Data Science Certificate Program
- Coursera for providing the platform
- Open-source Python community for excellent libraries

---

**Note**: This project uses synthetic data generated for educational purposes. For production use, real-world data should be obtained and validated.

