
import streamlit as st
import pandas as pd
import datetime
import requests
import os
import sys
import plotly.express as px
import pydeck as pdk

# Fix for module imports on Streamlit Cloud
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))

from enrich import enrich_contact
from score import score_lead
from maps import geocode_location
from analytics import (
    plot_segment_distribution,
    plot_lead_score_distribution,
    plot_email_presence
)
from linkedin import infer_linkedin_url

# Load database
DATA_PATH = "data/cg_leads_database.csv"
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=[
        "Full Name", "Segment", "Platform", "Profile", "Company", "Role",
        "Location", "Public Email", "Notes", "Timestamp",
        "Enriched Email", "Title", "LinkedIn", "Company Logo",
        "Latitude", "Longitude", "Lead Score"
    ])

st.title("Christopher Guy Lead Intelligence App")

# Score leads
df["Lead Score"] = df.apply(score_lead, axis=1)

# Add new lead
st.markdown("### ➕ Add New Lead")
with st.form("add_lead_form"):
    profile_url = st.text_input("Profile or Website URL")
    full_name = st.text_input("Full Name")
    segment = st.selectbox("Segment", df['Segment'].unique().tolist() if not df.empty else ["Old Money / HNW Individuals", "Diplomatic / Embassy", "Lifestyle / HNW", "Crypto Millionaire / Influencer", "School Trustee", "Political Family / Diplomat"])
    company = st.text_input("Company")
    role = st.text_input("Role")
    location = st.text_input("Location")
    public_email = st.text_input("Public Email")
    notes = st.text_area("Notes")
    add = st.form_submit_button("Add Lead")

    if add:
        enrich = enrich_contact(full_name, company)
        linkedin = enrich.get("linkedin") or infer_linkedin_url(full_name, company)
        lat, lon = geocode_location(location, st.secrets["opencage"]["api_key"])
        new_entry = {
            "Full Name": full_name,
            "Segment": segment,
            "Platform": "Scraped",
            "Profile": profile_url,
            "Company": company,
            "Role": role,
            "Location": location,
            "Public Email": public_email,
            "Notes": notes,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Enriched Email": enrich.get("email"),
            "Title": enrich.get("title"),
            "LinkedIn": linkedin,
            "Company Logo": enrich.get("logo"),
            "Latitude": lat,
            "Longitude": lon,
            "Lead Score": score_lead({
                "Enriched Email": enrich.get("email"),
                "LinkedIn": linkedin,
                "Title": enrich.get("title"),
                "Segment": segment
            })
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success(f"Lead added and enriched: {full_name}")

# Dashboard
st.markdown("### 📊 Lead Analytics")
plot_segment_distribution(df)
plot_lead_score_distribution(df)
plot_email_presence(df)

# High-value leads
st.markdown("### 🎯 High-Scoring Leads")
top_leads = df[df["Lead Score"] >= 20]
st.dataframe(top_leads)
st.download_button("Download High Scoring Leads", top_leads.to_csv(index=False), file_name="high_score_leads.csv")

# Map View
st.markdown("### 🌍 Map of Lead Locations")
geo_df = df.dropna(subset=["Latitude", "Longitude"])
if not geo_df.empty:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=geo_df["Latitude"].mean(),
            longitude=geo_df["Longitude"].mean(),
            zoom=3,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=geo_df,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=50000,
            ),
        ],
    ))

# Download full database
st.markdown("### 📥 Full Database Export")
st.download_button("Download CSV", df.to_csv(index=False), file_name="cg_leads_database.csv")
