"""
Create Interactive Folium Map for SpaceX Launch Data
Shows launch sites and launch performance on an interactive map

Author: Son Nguyen
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import warnings
warnings.filterwarnings('ignore')

def create_spacex_map():
    """Create interactive Folium map with SpaceX launch data"""
    import os
    
    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'spacex_launches.csv')
    df = pd.read_csv(data_path)
    
    # Add derived features
    df['Landing_Success'] = (df['Core_Landing'] == 'Success').astype(int)
    df['Launch_Success_Binary'] = df['Success'].fillna(0).astype(int)
    
    # Filter data with valid coordinates
    df_valid = df[df['Latitude'].notna() & df['Longitude'].notna()].copy()
    
    # Aggregate by launchpad
    launchpad_stats = df_valid.groupby(['Launchpad_Name', 'Location', 'Latitude', 'Longitude']).agg({
        'Launch_Success_Binary': ['count', 'sum', 'mean'],
        'Landing_Success': ['sum', 'mean'],
        'Rocket_Name': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
    }).reset_index()
    
    launchpad_stats.columns = ['Launchpad_Name', 'Location', 'Latitude', 'Longitude', 
                               'Total_Launches', 'Successful_Launches', 'Launch_Success_Rate',
                               'Successful_Landings', 'Landing_Success_Rate', 'Popular_Rocket']
    
    # Calculate center of all launch sites
    center_lat = df_valid['Latitude'].mean()
    center_lon = df_valid['Longitude'].mean()
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each launchpad
    for idx, row in launchpad_stats.iterrows():
        # Create popup HTML
        popup_html = f"""
        <div style='width: 250px;'>
            <h4 style='color: #1E88E5;'>{row['Launchpad_Name']}</h4>
            <hr>
            <p><strong>Location:</strong> {row['Location']}</p>
            <p><strong>Total Launches:</strong> {int(row['Total_Launches'])}</p>
            <p><strong>Launch Success Rate:</strong> {row['Launch_Success_Rate']*100:.1f}%</p>
            <p><strong>Landing Success Rate:</strong> {row['Landing_Success_Rate']*100:.1f}%</p>
            <p><strong>Successful Landings:</strong> {int(row['Successful_Landings'])}</p>
            <p><strong>Popular Rocket:</strong> {row['Popular_Rocket']}</p>
        </div>
        """
        
        # Color based on launch success rate
        success_rate = row['Launch_Success_Rate']
        if success_rate >= 0.95:
            color = 'green'
            icon = 'rocket'
        elif success_rate >= 0.85:
            color = 'blue'
            icon = 'rocket'
        elif success_rate >= 0.70:
            color = 'orange'
            icon = 'rocket'
        else:
            color = 'red'
            icon = 'rocket'
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
            tooltip=f"{row['Launchpad_Name']}: {row['Launch_Success_Rate']*100:.1f}% success"
        ).add_to(marker_cluster)
    
    # Add individual launch markers
    for idx, row in df_valid.iterrows():
        # Color based on launch success
        if row['Launch_Success_Binary'] == 1:
            launch_color = 'green'
            landing_color = 'green' if row['Landing_Success'] == 1 else 'red'
        else:
            launch_color = 'red'
            landing_color = 'gray'
        
        # Create popup for individual launch
        popup_html = f"""
        <div style='width: 200px;'>
            <h5>{row['Launch_Name']}</h5>
            <hr>
            <p><strong>Date:</strong> {row['Date_UTC'][:10] if pd.notna(row['Date_UTC']) else 'N/A'}</p>
            <p><strong>Rocket:</strong> {row['Rocket_Name']}</p>
            <p><strong>Launch:</strong> {'✓ Success' if row['Launch_Success_Binary'] == 1 else '✗ Failed'}</p>
            <p><strong>Landing:</strong> {'✓ Success' if row['Landing_Success'] == 1 else '✗ Failed' if row['Core_Landing'] == 'Failed' else 'No Attempt'}</p>
            <p><strong>Payload:</strong> {row['Payload_Mass_kg']:.0f} kg</p>
        </div>
        """
        
        # Use CircleMarker for individual launches
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            popup=folium.Popup(popup_html, max_width=250),
            color=launch_color,
            fillColor=landing_color,
            fillOpacity=0.7,
            weight=2,
            tooltip=f"{row['Launch_Name']}: Launch {'Success' if row['Launch_Success_Binary'] == 1 else 'Failed'}"
        ).add_to(m)
    
    # Add heatmap layer for launch frequency
    heat_data = [[row['Latitude'], row['Longitude'], 1] 
                 for idx, row in df_valid.iterrows()]
    
    HeatMap(heat_data, name='Launch Frequency Heatmap', 
            radius=20, blur=15, max_zoom=1, 
            gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'lime', 0.8: 'yellow', 1: 'red'},
            min_opacity=0.5).add_to(m)
    
    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Add title
    title_html = '''
                 <h3 align="center" style="font-size:20px"><b>SpaceX Launch Sites & Performance Map</b></h3>
                 <p align="center" style="font-size:14px">Interactive map showing launch sites, individual launches, and performance metrics</p>
                 '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    images_dir = os.path.join(project_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    output_path = os.path.join(images_dir, 'spacex_interactive_map.html')
    m.save(output_path)
    
    print(f"[OK] Interactive SpaceX map created successfully!")
    print(f"  Saved to: {output_path}")
    print(f"  Launchpads: {len(launchpad_stats)}")
    print(f"  Total launches: {len(df_valid)}")
    
    return m

if __name__ == "__main__":
    create_spacex_map()

