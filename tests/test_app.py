import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import load_data, filter_by_vehicle, calculate_view_state

def test_load_data():
    url = "https://data.calgary.ca/resource/jkyn-p9x4.csv"
    df = load_data(url)

    assert not df.empty, "Dataframe is empty!"
    assert 'vehicle_id' in df.columns
    assert 'latitude' in df.columns
    assert 'longitude' in df.columns
    assert df['latitude'].isnull().sum() == 0
    assert df['longitude'].isnull().sum() == 0

def test_filter_by_vehicle():
    data = {
        'vehicle_id': [1, 2, 1],
        'latitude': [51.0, 51.2, 51.4],
        'longitude': [-114.0, -114.2, -114.4]
    }
    df = pd.DataFrame(data)

    filtered_df = filter_by_vehicle(df, 1)

    assert len(filtered_df) == 2
    assert all(filtered_df['vehicle_id'] == 1)

def test_calculate_view_state():
    data = {
        'latitude': [51.0, 51.5],
        'longitude': [-114.0, -114.5]
    }
    df = pd.DataFrame(data)

    view_state = calculate_view_state(df)

    assert view_state.latitude == 51.25
    assert view_state.longitude == -114.25
    assert view_state.zoom == 12
    assert view_state.pitch == 50
