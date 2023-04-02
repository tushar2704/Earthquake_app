## Earthquake_Notification_App by Tushar Aggarwal, github.com/tushar2704

# Importing required libraries
import streamlit as st
import requests
import time
import winsound
from PIL import Image
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

# Load image and sound file
image = Image.open("earthquake.png")
notification_sound = "SystemExit"

def get_latest_earthquake():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url).json()
    features = response["features"]
    latest = features[0]
    return latest

def display_earthquake_info(earthquake):
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.image(image, use_column_width=True)
    with col2:
        st.write(f"**Magnitude:** {earthquake['properties']['mag']}")
        st.write(f"**Location:** {earthquake['properties']['place']}")
        st.write(f"**Time:** {time.ctime(int(earthquake['properties']['time']/1000))}")
    with col3:
        # Create a map centered on the earthquake location
        map_center = [earthquake['geometry']['coordinates'][1], earthquake['geometry']['coordinates'][0]]
        m = folium.Map(location=map_center, zoom_start=8, tiles='OpenStreetMap')
        folium.Marker(location=map_center, icon=folium.Icon(color="red")).add_to(m)
        # Convert the map to HTML and display it in a Streamlit column
        folium_static(m, width=700)

def play_notification_sound():
    winsound.PlaySound(notification_sound, winsound.SND_ALIAS)

def main():
    st.title("Latest Earthquake Notifier")
    st.subheader("Get notified about the latest earthquake!")
    st.markdown("---")
    
    latest_earthquake = get_latest_earthquake()
    display_earthquake_info(latest_earthquake)
    
    play_notification = st.checkbox("Enable notification for new earthquake?")

    while play_notification:
        time.sleep(60) # Check every minute
        new_earthquake = get_latest_earthquake()
        if new_earthquake["id"] != latest_earthquake["id"]:
            latest_earthquake = new_earthquake
            display_earthquake_info(latest_earthquake)
            play_notification_sound()

if __name__ == "__main__":
    main()
##########Tushar Aggarwal

#################################################################################################