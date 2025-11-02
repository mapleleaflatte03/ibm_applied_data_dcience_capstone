"""
Plotly Dash Dashboard for SpaceX Launch Analytics
Interactive dashboard for SpaceX launch data visualization and exploration

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
data_path = os.path.join(project_dir, 'data', 'spacex_launches.csv')
df = pd.read_csv(data_path)
df['Date'] = pd.to_datetime(df['Date_UTC'])
df['Landing_Success'] = (df['Core_Landing'] == 'Success').astype(int)
df['Launch_Success_Binary'] = df['Success'].astype(int)

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], 
                title="SpaceX Launch Analytics Dashboard")

# Define app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🚀 SpaceX Launch Analytics Dashboard", 
                   className="text-center mb-4", 
                   style={'color': '#1E88E5', 'font-weight': 'bold', 'font-size': '2.5em'}),
            html.P("Interactive dashboard for exploring SpaceX launch data (2006-2022)",
                   className="text-center text-muted mb-4"),
            html.Hr()
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Rocket Type:", style={'font-weight': 'bold', 'font-size': '1.1em'}),
            dcc.Dropdown(
                id='rocket-dropdown',
                options=[{'label': 'All Rockets', 'value': 'All'}] + 
                        [{'label': rocket, 'value': rocket} for rocket in sorted(df['Rocket_Name'].unique())],
                value='All',
                clearable=False,
                style={'font-size': '1.1em'}
            )
        ], md=6),
        dbc.Col([
            html.Label("Select Region:", style={'font-weight': 'bold', 'font-size': '1.1em'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All Regions', 'value': 'All'}] + 
                        [{'label': region, 'value': region} for region in sorted(df['Region'].unique())],
                value='All',
                clearable=False,
                style={'font-size': '1.1em'}
            )
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='launch-success-over-time')
        ], md=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='landing-success-by-rocket')
        ], md=6),
        dbc.Col([
            dcc.Graph(id='geographic-distribution')
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='payload-vs-landing')
        ], md=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='summary-stats', className="p-4 bg-light rounded shadow-sm")
        ], md=12)
    ])
    
], fluid=True, style={'padding': '20px'})

# Define callbacks
@app.callback(
    [Output('launch-success-over-time', 'figure'),
     Output('landing-success-by-rocket', 'figure'),
     Output('geographic-distribution', 'figure'),
     Output('payload-vs-landing', 'figure'),
     Output('summary-stats', 'children')],
    [Input('rocket-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_dashboard(rocket_type, region):
    # Filter data
    filtered_df = df.copy()
    
    if rocket_type != 'All':
        filtered_df = filtered_df[filtered_df['Rocket_Name'] == rocket_type]
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    
    # 1. Launch success over time
    df_time = filtered_df.groupby('Year').agg({
        'Launch_Success_Binary': ['mean', 'count'],
        'Landing_Success': 'mean'
    }).reset_index()
    df_time.columns = ['Year', 'Launch_Success_Rate', 'Total_Launches', 'Landing_Success_Rate']
    
    fig_time = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_time.add_trace(
        go.Scatter(x=df_time['Year'], y=df_time['Launch_Success_Rate'] * 100,
                  mode='lines+markers', name='Launch Success Rate',
                  line=dict(color='#1E88E5', width=3),
                  marker=dict(size=10)),
        secondary_y=False,
    )
    
    fig_time.add_trace(
        go.Scatter(x=df_time['Year'], y=df_time['Landing_Success_Rate'] * 100,
                  mode='lines+markers', name='Landing Success Rate',
                  line=dict(color='#D81B60', width=3),
                  marker=dict(size=10)),
        secondary_y=False,
    )
    
    fig_time.update_xaxes(title_text="Year")
    fig_time.update_yaxes(title_text="Success Rate (%)", secondary_y=False)
    fig_time.update_layout(
        title={'text': 'Launch & Landing Success Rates Over Time', 'font': {'size': 18, 'bold': True}},
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    # 2. Landing success by rocket type
    df_rocket = filtered_df.groupby('Rocket_Name').agg({
        'Landing_Success': ['mean', 'count', 'sum']
    }).reset_index()
    df_rocket.columns = ['Rocket_Name', 'Landing_Success_Rate', 'Total_Attempts', 'Successful_Landings']
    df_rocket = df_rocket.sort_values('Landing_Success_Rate', ascending=False)
    
    fig_rocket = go.Figure(data=[
        go.Bar(
            x=df_rocket['Rocket_Name'],
            y=df_rocket['Landing_Success_Rate'] * 100,
            text=[f"{val:.1f}%<br>({int(df_rocket.iloc[i]['Successful_Landings'])}/{int(df_rocket.iloc[i]['Total_Attempts'])})" 
                  for i, val in enumerate(df_rocket['Landing_Success_Rate'] * 100)],
            textposition='auto',
            marker=dict(color=['#1976D2', '#C2185B', '#F57C00'][:len(df_rocket)],
                       line=dict(color='black', width=2))
        )
    ])
    
    fig_rocket.update_layout(
        title={'text': 'Landing Success Rate by Rocket Type', 'font': {'size': 18, 'bold': True}},
        xaxis_title="Rocket Type",
        yaxis_title="Landing Success Rate (%)",
        yaxis=dict(range=[0, 105])
    )
    
    # 3. Geographic distribution
    df_geo = filtered_df.groupby('Region').agg({
        'Launch_Success_Binary': ['count', 'mean'],
        'Landing_Success': 'mean'
    }).reset_index()
    df_geo.columns = ['Region', 'Total_Launches', 'Launch_Success_Rate', 'Landing_Success_Rate']
    
    fig_geo = go.Figure(data=[
        go.Bar(
            name='Launch Success',
            x=df_geo['Region'],
            y=df_geo['Launch_Success_Rate'] * 100,
            marker_color='#1E88E5'
        ),
        go.Bar(
            name='Landing Success',
            x=df_geo['Region'],
            y=df_geo['Landing_Success_Rate'] * 100,
            marker_color='#D81B60'
        )
    ])
    
    fig_geo.update_layout(
        title={'text': 'Success Rates by Geographic Region', 'font': {'size': 18, 'bold': True}},
        xaxis_title="Region",
        yaxis_title="Success Rate (%)",
        barmode='group',
        yaxis=dict(range=[0, 105])
    )
    
    # 4. Payload vs Landing success
    landing_data = filtered_df[filtered_df['Core_Landing'] != 'No Attempt'].copy()
    
    fig_payload = px.scatter(
        landing_data, 
        x='Payload_Mass_kg', 
        y='Landing_Success',
        color='Rocket_Name',
        size='Payload_Count',
        hover_data=['Launch_Name', 'Year'],
        title='Payload Mass vs Landing Success',
        labels={'Payload_Mass_kg': 'Payload Mass (kg)', 'Landing_Success': 'Landing Success'},
        trendline='ols'
    )
    
    fig_payload.update_layout(
        title={'text': 'Payload Mass vs Landing Success', 'font': {'size': 18, 'bold': True}},
        yaxis=dict(range=[-0.1, 1.1], tickmode='linear', tick0=0, dtick=0.5)
    )
    
    # 5. Summary statistics
    total_launches = len(filtered_df)
    successful_launches = filtered_df['Launch_Success_Binary'].sum()
    launch_success_rate = filtered_df['Launch_Success_Binary'].mean() * 100
    
    landing_attempts = len(filtered_df[filtered_df['Core_Landing'] != 'No Attempt'])
    successful_landings = filtered_df['Landing_Success'].sum()
    landing_success_rate = (filtered_df['Landing_Success'].sum() / landing_attempts * 100) if landing_attempts > 0 else 0
    
    avg_payload = filtered_df['Payload_Mass_kg'].mean()
    
    stats_html = html.Div([
        html.H4("📊 Summary Statistics", className="mb-3", style={'color': '#1E88E5', 'font-weight': 'bold'}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Strong("Total Launches:", className="text-muted"),
                    html.H3(f"{total_launches:,}", style={'color': '#1E88E5', 'margin': '10px 0'})
                ], className="p-3 border rounded text-center")
            ], md=3),
            dbc.Col([
                html.Div([
                    html.Strong("Launch Success Rate:", className="text-muted"),
                    html.H3(f"{launch_success_rate:.1f}%", style={'color': '#28a745', 'margin': '10px 0'})
                ], className="p-3 border rounded text-center")
            ], md=3),
            dbc.Col([
                html.Div([
                    html.Strong("Landing Success Rate:", className="text-muted"),
                    html.H3(f"{landing_success_rate:.1f}%", style={'color': '#D81B60', 'margin': '10px 0'})
                ], className="p-3 border rounded text-center")
            ], md=3),
            dbc.Col([
                html.Div([
                    html.Strong("Avg Payload Mass:", className="text-muted"),
                    html.H3(f"{avg_payload:.0f} kg", style={'color': '#F57C00', 'margin': '10px 0'})
                ], className="p-3 border rounded text-center")
            ], md=3)
        ])
    ])
    
    return fig_time, fig_rocket, fig_geo, fig_payload, stats_html

if __name__ == '__main__':
    print("=" * 60)
    print("SpaceX Launch Analytics Dashboard")
    print("=" * 60)
    print("\nStarting dashboard server...")
    print("Open your browser and navigate to: http://localhost:8050")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    app.run_server(debug=True, port=8050)


