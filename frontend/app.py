import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Set the backend URL
BACKEND_URL = "http://localhost:8000"  # Adjust if your backend is hosted elsewhere

# Set page configuration
st.set_page_config(page_title="Dating App Dashboard", page_icon=":heart:", layout="wide")

# Function to make requests
def make_request(method, endpoint, **kwargs):
    try:
        response = requests.request(method, f"{BACKEND_URL}{endpoint}", **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "User Operations", "Find Nearest Users"])

# Home Page
if page == "Home":
    st.title("Welcome to the Dating App Dashboard :heart:")
    st.write("""
        Interact with the backend server to manage and analyze user data:
        - Fetch and store users from an external API.
        - Generate random usernames.
        - Find the nearest users based on location.
    """)
    st.image("https://example.com/dating_app_image.png")  # Replace with your image URL or local file path

# User Operations Page
elif page == "User Operations":
    st.title("User Operations")

    num_users = st.number_input("Number of users to fetch", min_value=1, max_value=100, value=10)
    if st.button("Fetch Users"):
        result = make_request("POST", f"/fetch-users/?num_users={num_users}")
        print(result)
        if result:
            st.success( "Users fetched successfully")
            st.info(f"Run ID: {result[0].get('run_id', 'N/A')}")

    if st.button("Get Random User"):
        user = make_request("GET", "/random_user/")
        if user:
            st.write(f"**Name:** {user['first_name']} {user['last_name']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Gender:** {user['gender']}")
            st.write(f"**UID:** {user['uid']}")
            st.write(f"**Ingestion Date:** {user['created_at']}")
            m = folium.Map(location=[user['latitude'], user['longitude']], zoom_start=10)
            folium.Marker(
                [user['latitude'], user['longitude']],
                popup=f"{user['first_name']} {user['last_name']}",
                tooltip=user['email']
            ).add_to(m)
            folium_static(m)

# Find Nearest Users Page
elif page == "Find Nearest Users":
    st.title("Find Nearest Users")
    email = st.text_input("Enter user email")
    limit = st.number_input("Number of nearest users", min_value=1, max_value=100, value=10)
    if st.button("Find Nearest Users"):
        users = make_request("GET", f"/users/{email}/nearest", params={"limit": limit})
        if users:
            st.write(f"Found {len(users)} nearest users:")
            m = folium.Map(location=[users[0]['latitude'], users[0]['longitude']], zoom_start=10)
            for user in users:
                folium.Marker(
                    [user['latitude'], user['longitude']],
                    popup=f"{user['first_name']} {user['last_name']}",
                    tooltip=user['email']
                ).add_to(m)
            folium_static(m)
        else:
            st.write("No nearby users found.")
