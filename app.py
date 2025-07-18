
import streamlit as st
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import os

# Load existing database
DATA_PATH = "cg_leads_database.csv"
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["Full Name", "Segment", "Platform", "Profile", "Company", "Role", "Location", "Public Email", "Notes", "Timestamp", "Enriched Email", "Title", "LinkedIn", "Company Logo"])

st.title("Christopher Guy Lead Intelligence App")
st.subheader("Review & Expand Lead Database")

# Show existing data
st.markdown("### 📋 Current Lead Database")
st.dataframe(df)

# Enrichment simulation function
@st.cache_data(show_spinner=False)
def enrich_contact(name, company):
    try:
        email = f"{name.split()[0].lower()}@{company.lower().replace(' ', '')}.com"
        title = "CEO" if "founder" in company.lower() else "Executive"
        linkedin = f"https://www.linkedin.com/in/{name.replace(' ', '').lower()}"
        logo = f"https://logo.clearbit.com/{company.lower().replace(' ', '')}.com"
        return email, title, linkedin, logo
    except:
        return "", "", "", ""

# Scrape name from public profile
@st.cache_data(show_spinner=False)
def scrape_name_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        if "instagram.com" in url or "twitter.com" in url:
            meta = soup.find('meta', property='og:title')
            return meta['content'].split("(@")[0].strip() if meta else ""
        else:
            title = soup.title.string.strip() if soup.title else ""
            return title.split("|")[0].strip()
    except:
        return ""

# Add new lead section
st.markdown("### ➕ Add New Lead")
with st.form("add_lead_form"):
    profile_url = st.text_input("Profile or Website URL")
    auto_name = scrape_name_from_url(profile_url) if profile_url else ""
    full_name = st.text_input("Full Name", value=auto_name)
    segment = st.selectbox("Segment", ["Lifestyle / HNW", "Old Money / HNW Individuals", "Diplomatic / Embassy", "School Trustee", "Political Family / Diplomat", "Crypto Millionaire / Influencer"])
    company = st.text_input("Company")
    role = st.text_input("Role")
    location = st.text_input("Location")
    public_email = st.text_input("Public Email")
    notes = st.text_area("Notes")
    add = st.form_submit_button("Add Lead")

    if add:
        enriched_email, enriched_title, linkedin_url, logo_url = enrich_contact(full_name, company)
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
            "Enriched Email": enriched_email,
            "Title": enriched_title,
            "LinkedIn": linkedin_url,
            "Company Logo": logo_url
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success(f"Added and enriched: {full_name}")

# Download updated database
st.markdown("### 📥 Download Updated Database")
st.download_button("Download CSV", df.to_csv(index=False), file_name="cg_leads_database.csv", mime="text/csv")
