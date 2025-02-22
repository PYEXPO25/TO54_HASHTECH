import streamlit as st
import requests

# Function to get the user's location (latitude and longitude)
def get_location():
    """Fetch user's approximate latitude and longitude."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        location = data.get("loc", "").split(",")
        if len(location) == 2:
            return float(location[0]), float(location[1])
    except Exception:
        return None, None
    return None, None

# Function to find nearby clinics (using OpenStreetMap)
def find_nearby_clinics(lat, lon):
    """Generate a direct OpenStreetMap search link for clinics near the user."""
    if lat and lon:
        clinic_search_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}&q=clinic"
        return clinic_search_url
    return None

# Streamlit UI
st.title("🩺 Nearby Clinic Finder")

# Get the user's location
lat, lon = get_location()

if lat and lon:
    st.write(f"Your approximate location: Latitude: {lat}, Longitude: {lon}")
    
    # Find and display the clinic search link
    clinic_link = find_nearby_clinics(lat, lon)
    if clinic_link:
        st.markdown(f"[🏥 Find a Nearby Clinic Here]({clinic_link})", unsafe_allow_html=True)
    else:
        st.warning("Could not find nearby clinics. Please check your internet connection.")
else:
    st.warning("Could not detect your location. Please check your internet connection.")
