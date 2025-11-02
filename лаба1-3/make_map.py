import pandas as pd
from geopy.geocoders import Nominatim
import folium
import time

def plot_clusters_on_map(df, clusters, filename="clusters_map.html"):

    clusters_df = pd.concat([df['City'], clusters['cluster']], axis=1)

    geolocator = Nominatim(user_agent="cluster_mapper")
    city_coords = {}

    for city in clusters_df['City'].unique():
        try:
            query = f"{city}, Greece" if city.lower() in ["athens", "athína"] else city
            location = geolocator.geocode(query, timeout=10)
            if location:
                city_coords[city] = (location.latitude, location.longitude)
            time.sleep(1)
        except Exception as e:
            print(f"Ошибка при геокодировании {city}: {e}")
            continue

    clusters_df['coords'] = clusters_df['City'].map(city_coords)
    clusters_df.dropna(subset=['coords'], inplace=True)
    clusters_df[['lat', 'lon']] = pd.DataFrame(clusters_df['coords'].tolist(), index=clusters_df.index)

    base_colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'brown', 'gray']
    unique_clusters = sorted(clusters_df['cluster'].unique())
    colors = {c: base_colors[i % len(base_colors)] for i, c in enumerate(unique_clusters)}

    world_map = folium.Map(location=[20, 0], zoom_start=2)

    for _, row in clusters_df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            popup=f"City: {row['City']}<br>Cluster: {row['cluster']}",
            color=colors[row['cluster']],
            fill=True,
            fill_color=colors[row['cluster']],
            fill_opacity=0.7
        ).add_to(world_map)

    world_map.save(filename)