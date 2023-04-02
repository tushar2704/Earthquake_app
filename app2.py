import streamlit as st
import requests
import time
import webbrowser
import folium
from streamlit_folium import folium_static

# Set page width and background color
st.set_page_config(page_title="Latest Earthquake Notifier", page_icon=":volcano:", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f2f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define function to get latest earthquake data
def get_latest_earthquake():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url).json()
    features = response["features"]
    latest = features[0]
    return latest

# Define function to display earthquake information and map
def display_earthquake_info(earthquake):
    # Create columns to display earthquake information and map
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display earthquake information
        st.image("https://www.shareicon.net/data/128x128/2015/08/06/80805_disaster_512x512.png", use_column_width=True)
        st.write(f"**Magnitude:** {earthquake['properties']['mag']}")
        st.write(f"**Location:** {earthquake['properties']['place']}")
        st.write(f"**Time:** {time.ctime(int(earthquake['properties']['time']/1000))}")
        
        # Add a button to open the USGS website with more information
        if st.button("View More Information"):
            webbrowser.open_new_tab(earthquake['properties']['url'])
        
    with col2:
        # Create a map centered on the earthquake location
        map_center = [earthquake['geometry']['coordinates'][1], earthquake['geometry']['coordinates'][0]]
        m = folium.Map(location=map_center, zoom_start=8, tiles='OpenStreetMap')
        folium.Marker(location=map_center, icon=folium.Icon(color="red")).add_to(m)
        # Convert the map to HTML and display it in a Streamlit column
        folium_static(m, width=700)

# Define main function to continuously check for new earthquakes
def main():
    st.title("Latest Earthquake Notifier")
    st.subheader("Get notified about the latest earthquake!")
    st.markdown("---")
    
    # Get latest earthquake data and display it
    latest_earthquake = get_latest_earthquake()
    display_earthquake_info(latest_earthquake)
    
    # Check for new earthquakes every minute
    while True:
        time.sleep(60)
        new_earthquake = get_latest_earthquake()
        if new_earthquake["id"] != latest_earthquake["id"]:
            latest_earthquake = new_earthquake
            display_earthquake_info(latest_earthquake)

if __name__ == "__main__":
    main()
