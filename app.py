import streamlit as st
import pandas as pd
import pydeck as pdk

DATA_URL = "https://data.calgary.ca/resource/jkyn-p9x4.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df = df.dropna(subset=['latitude', 'longitude'])
    return df

def filter_by_vehicle(df, vehicle_id):
    return df[df['vehicle_id'] == vehicle_id]

def calculate_view_state(df):
    return pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=12,
        pitch=50,
    )

def create_layers(filtered_df):
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_df,
        get_position='[longitude, latitude]',
        radiusPixels=60,
    )

    path_data = [{
        'path': filtered_df[['longitude', 'latitude']].values.tolist(),
        'name': f'Vehicle {filtered_df.iloc[0]["vehicle_id"]}' if not filtered_df.empty else 'Vehicle'
    }]

    path_layer = pdk.Layer(
        "PathLayer",
        data=path_data,
        get_path="path",
        get_width=4,
        get_color=[255, 0, 0],
        width_min_pixels=2,
    )

    return heatmap_layer, path_layer

def main():
    st.title("🚍 Calgary Bus Tracker")

    df = load_data(DATA_URL)

    # Sidebar filter
    vehicle_ids = df['vehicle_id'].unique()
    selected_vehicle_id = st.sidebar.selectbox("Select Vehicle ID:", vehicle_ids)

    filtered_df = filter_by_vehicle(df, selected_vehicle_id)

    if filtered_df.empty:
        st.warning("No data found for this vehicle.")
        return

    view_state = calculate_view_state(filtered_df)

    heatmap_layer, path_layer = create_layers(filtered_df)

    r = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[heatmap_layer, path_layer],
        tooltip={"text": "Lat: {latitude}\nLon: {longitude}"}
    )

    st.subheader(f"Heatmap and Trail for Vehicle ID: {selected_vehicle_id}")
    st.pydeck_chart(r)

    if st.checkbox("Show raw data"):
        st.write(filtered_df)

if __name__ == "__main__":
    main()
