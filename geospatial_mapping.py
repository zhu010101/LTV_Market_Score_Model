import folium
from folium.plugins import MarkerCluster

def create_interactive_map(gdf, column, title, cmap='YlOrRd'):
    """
    Create an interactive map using Folium to visualize a specific column.
    """
    # Ensure GeoDataFrame uses EPSG:4326 (latitude/longitude)
    gdf = gdf.to_crs(epsg=4326)

    # Convert GeoDataFrame to GeoJSON
    geo_json = gdf.to_json()

    # Initialize the map centered on California
    m = folium.Map(location=[37.5, -119.5], zoom_start=6)

    # Add choropleth layer
    folium.Choropleth(
        geo_data=geo_json,
        data=gdf,
        columns=['ZIPCODE', column],
        key_on="feature.properties.ZIPCODE",
        fill_color=cmap,  # Use a valid ColorBrewer colormap
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=title
    ).add_to(m)

    # Add clustered markers
    marker_cluster = MarkerCluster()
    for _, row in gdf.iterrows():
        # Ensure the geometry is valid and has a centroid
        if row.geometry.is_valid:
            folium.Marker(
                location=[row.geometry.centroid.y, row.geometry.centroid.x],
                popup=f"{row['ZIPCODE']}: {row[column]}"
            ).add_to(marker_cluster)
    marker_cluster.add_to(m)

    return m