"""
Plotly Dash Dashboard for Automotive Sales Analytics
Interactive dashboard for data visualization and exploration

Author: Son Nguyen
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings('ignore')

# Load data
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'data', 'automotive_sales.csv')
df = pd.read_csv(data_path)
df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(Day=1))
df['Quarter'] = df['Month'].apply(lambda x: (x-1)//3 + 1)

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🚗 Automotive Sales Analytics Dashboard", 
                   className="text-center mb-4", 
                   style={'color': '#2c3e50', 'font-weight': 'bold'}),
            html.Hr()
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Vehicle Type:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='vehicle-type-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + 
                        [{'label': vt, 'value': vt} for vt in df['Vehicle_Type'].unique()],
                value='All',
                clearable=False
            )
        ], md=6),
        dbc.Col([
            html.Label("Select Region:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + 
                        [{'label': r, 'value': r} for r in df['Region'].unique()],
                value='All',
                clearable=False
            )
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sales-over-time')
        ], md=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sales-by-type')
        ], md=6),
        dbc.Col([
            dcc.Graph(id='sales-by-season')
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='price-sales-scatter')
        ], md=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='summary-stats', className="p-3 bg-light rounded")
        ], md=12)
    ])
    
], fluid=True)

# Define callbacks
@app.callback(
    [Output('sales-over-time', 'figure'),
     Output('sales-by-type', 'figure'),
     Output('sales-by-season', 'figure'),
     Output('price-sales-scatter', 'figure'),
     Output('summary-stats', 'children')],
    [Input('vehicle-type-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_dashboard(vehicle_type, region):
    # Filter data
    filtered_df = df.copy()
    
    if vehicle_type != 'All':
        filtered_df = filtered_df[filtered_df['Vehicle_Type'] == vehicle_type]
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    
    # 1. Sales over time
    df_time = filtered_df.groupby('Date')['Sales'].mean().reset_index()
    fig_time = px.line(df_time, x='Date', y='Sales',
                       title='Average Sales Over Time',
                       labels={'Sales': 'Average Sales', 'Date': 'Date'})
    fig_time.update_traces(line_color='steelblue', line_width=3)
    fig_time.update_layout(title_font_size=16, title_font_family='Arial')
    
    # 2. Sales by vehicle type
    df_type = filtered_df.groupby('Vehicle_Type')['Sales'].mean().sort_values(ascending=False)
    fig_type = px.bar(x=df_type.index, y=df_type.values,
                      title='Average Sales by Vehicle Type',
                      labels={'x': 'Vehicle Type', 'y': 'Average Sales'})
    fig_type.update_traces(marker_color='lightblue')
    fig_type.update_layout(title_font_size=16, title_font_family='Arial')
    
    # 3. Sales by season
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    df_season = filtered_df.groupby('Season')['Sales'].mean().reindex(season_order)
    fig_season = px.bar(x=df_season.index, y=df_season.values,
                        title='Average Sales by Season',
                        labels={'x': 'Season', 'y': 'Average Sales'},
                        color=df_season.index,
                        color_discrete_map={'Spring': 'green', 'Summer': 'orange', 
                                          'Fall': 'brown', 'Winter': 'blue'})
    fig_season.update_layout(title_font_size=16, title_font_family='Arial', showlegend=False)
    
    # 4. Price vs Sales scatter
    fig_scatter = px.scatter(filtered_df, x='Price', y='Sales',
                            title='Price vs Sales Relationship',
                            labels={'Price': 'Price (thousands)', 'Sales': 'Sales'},
                            trendline='ols',
                            hover_data=['Vehicle_Type', 'Region'])
    fig_scatter.update_layout(title_font_size=16, title_font_family='Arial')
    
    # 5. Summary statistics
    stats = {
        'Total Records': len(filtered_df),
        'Average Sales': f"{filtered_df['Sales'].mean():.2f}",
        'Total Revenue': f"${filtered_df['Revenue'].sum():,.2f}",
        'Average Price': f"${filtered_df['Price'].mean():.2f}K"
    }
    
    stats_html = html.Div([
        html.H4("📊 Summary Statistics", className="mb-3"),
        html.Div([
            html.Div([
                html.Strong(f"{k}:"), html.Br(),
                html.Span(f"{v}", style={'font-size': '1.2em', 'color': '#3498db'})
            ], className="p-2 m-2 border rounded", style={'display': 'inline-block', 'min-width': '150px'})
            for k, v in stats.items()
        ])
    ])
    
    return fig_time, fig_type, fig_season, fig_scatter, stats_html

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

