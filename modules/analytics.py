# modules/analytics.py

import streamlit as st
import plotly.express as px
import pandas as pd

def plot_segment_distribution(df: pd.DataFrame):
    """Bar chart of lead count by segment."""
    if "Segment" in df.columns and not df["Segment"].isnull().all():
        fig = px.histogram(df, x="Segment", title="Lead Count by Segment")
        st.plotly_chart(fig, use_container_width=True)

def plot_lead_score_distribution(df: pd.DataFrame):
    """Histogram of lead scores."""
    if "Lead Score" in df.columns:
        fig = px.histogram(df, x="Lead Score", nbins=20, title="Lead Score Distribution")
        st.plotly_chart(fig, use_container_width=True)

def plot_email_presence(df: pd.DataFrame):
    """Pie chart showing % of leads with valid emails."""
    if "Enriched Email" in df.columns:
        with_email = df["Enriched Email"].notna() & df["Enriched Email"].str.contains("@")
        counts = pd.Series({
            "With Email": with_email.sum(),
            "No Email": (~with_email).sum()
        })
        fig = px.pie(values=counts.values, names=counts.index, title="Email Enrichment Rate")
        st.plotly_chart(fig, use_container_width=True)
# Dashboard components for KPIs and metrics
