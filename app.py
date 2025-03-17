import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🚍 Calgary Bus Tracker")

# Load the data
url = "https://data.calgary.ca/resource/jkyn-p9x4.csv"
df = pd.read_csv(url)

# Clean the data - drop rows without lat/long
df = df.dropna(subset=['latitude', 'longitude'])

# Sidebar filter for vehicle_id
vehicle_ids = df['vehicle_id'].unique()
selected_vehicle_id = st.sidebar.selectbox("Select Vehicle ID:", vehicle_ids)

# Filter the dataframe by selected vehicle_id
filtered_df = df[df['vehicle_id'] == selected_vehicle_id]

# Sort by time for a proper trail (optional)
filtered_df = filtered_df.sort_values(by='vehicle_position_date_time')

st.subheader(f"Heatmap and Trail for Vehicle ID: {selected_vehicle_id}")

# Create a heatmap layer
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=filtered_df,
    get_position='[longitude, latitude]',
    radiusPixels=60,
)

# Create a line layer for the vehicle's trail
line_layer = pdk.Layer(
    "LineLayer",
    data=filtered_df,
    get_source_position='[longitude, latitude]',
    get_target_position='[longitude, latitude]',
    get_color=[0, 0, 255],
    get_width=4,
    pickable=True,
)

# Create a path layer (alternative to line layer)
path_data = [{
    'path': filtered_df[['longitude', 'latitude']].values.tolist(),
    'name': f'Vehicle {selected_vehicle_id}'
}]

path_layer = pdk.Layer(
    "PathLayer",
    data=path_data,
    get_path="path",
    get_width=4,
    get_color=[255, 0, 0],
    width_min_pixels=2,
)

# Set the viewport location and zoom level
view_state = pdk.ViewState(
    latitude=filtered_df['latitude'].mean(),
    longitude=filtered_df['longitude'].mean(),
    zoom=12,
    pitch=50,
)

# Render the deck.gl map with both heatmap and path layers
r = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[heatmap_layer, path_layer],  # Swap to line_layer if you prefer
    tooltip={"text": "Lat: {latitude}\nLon: {longitude}"}
)

st.pydeck_chart(r)

# Show raw data option
if st.checkbox("Show raw data"):
    st.write(filtered_df)
