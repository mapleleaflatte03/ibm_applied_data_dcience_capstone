"""
Create Interactive Folium Map for Automotive Sales Data
Shows sales by city location on an interactive map
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import warnings
warnings.filterwarnings('ignore')

def create_sales_map():
    """Create interactive Folium map with sales data"""
    import os
    
    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'automotive_sales.csv')
    df = pd.read_csv(data_path)
    
    # Aggregate sales by city
    city_sales = df.groupby(['City', 'Latitude', 'Longitude']).agg({
        'Sales': 'mean',
        'Revenue': 'sum',
        'Vehicle_Type': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Mixed'
    }).reset_index()
    
    # Create base map centered on USA
    m = folium.Map(
        location=[39.8283, -98.5795],  # Center of USA
        zoom_start=4,
        tiles='OpenStreetMap'
    )
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each city
    for idx, row in city_sales.iterrows():
        popup_html = f"""
        <div style='width: 200px;'>
            <h4>{row['City']}</h4>
            <hr>
            <p><strong>Average Sales:</strong> {row['Sales']:.2f}</p>
            <p><strong>Total Revenue:</strong> ${row['Revenue']:,.2f}</p>
            <p><strong>Popular Type:</strong> {row['Vehicle_Type']}</p>
        </div>
        """
        
        # Color based on sales volume
        if row['Sales'] > 150:
            color = 'green'
        elif row['Sales'] > 100:
            color = 'blue'
        elif row['Sales'] > 70:
            color = 'orange'
        else:
            color = 'red'
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color, icon='car', prefix='fa'),
            tooltip=f"{row['City']}: Avg Sales = {row['Sales']:.2f}"
        ).add_to(marker_cluster)
    
    # Add heatmap layer
    heat_data = [[row['Latitude'], row['Longitude'], row['Sales']] 
                 for idx, row in city_sales.iterrows()]
    
    HeatMap(heat_data, name='Sales Heatmap', 
            radius=15, blur=10, max_zoom=1, 
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save map
    images_dir = os.path.join(project_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    output_path = os.path.join(images_dir, 'interactive_sales_map.html')
    m.save(output_path)
    
    print(f"Interactive map created and saved to: {output_path}")
    print(f"Map shows {len(city_sales)} cities with sales data")
    
    return m

if __name__ == "__main__":
    create_sales_map()

