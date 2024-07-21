import os
import sys
import pandas as pd
from bson.objectid import ObjectId

root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, root_folder)

import streamlit as st
from db.db_connector import DbConnector
conn = DbConnector("scraper", "jobs")
from config import config
from app.utils import *

# Set page configuration
st.set_page_config(page_title="Scraper", page_icon="🔍")

# Scraper page
st.markdown("# Scraper")
st.sidebar.header("Scraper")

# Function to add a new scraping job
def add_scraping_job(url, mode, partitions, source_type, pattern_mode, pattern):
    job = {
        "source": add_https(url),
        "mode": mode.lower(),
        "partitions": [partition.lower() for partition in partitions],
        "source_type": source_type.lower(),
        "pattern_mode": pattern_mode.lower(),
        "pattern": pattern
    }
    conn.collection.insert_one(job)
    return list(conn.collection.find())

# Function to delete a scraping job
def delete_scraping_job(job_id):
    conn.collection.delete_one({"_id": ObjectId(job_id)})
    return list(conn.collection.find())

# Function to get status color
def get_status_color(status):
    if status == "done":
        return "#36BA98"
    elif status == "failed":
        return "#e76f51"
    else:  # pending or no status field
        return "#F4A261"

# Initialize session state for scraper jobs
if 'scraper_jobs' not in st.session_state:
    st.session_state.scraper_jobs = list(conn.collection.find())

# Pop-up to add a new scraping job
with st.expander("Create a new scraping job"):
    url = st.text_input("Enter URL to scrape:", key="url_input")
    mode = st.selectbox("Mode", ["Recursive", "Single page", "Monitor"])
    country = st.multiselect("Region", ["France", "Germany", "Spain", "Italy"])
    source_type = st.selectbox("Source type", ["Government", "Independent", "Crowd-sourced"])
    pattern_mode = st.radio("Pattern Mode", ["Inclusionary", "Exclusionary"], key="pattern_mode")
    pattern_label = "URL include pattern:" if pattern_mode == "Inclusionary" else "URL exclude pattern:"
    pattern = st.text_input(pattern_label, key="url_pattern")

    if st.button("Scrape"):
        st.session_state.scraper_jobs = add_scraping_job(url, mode, country, source_type, pattern_mode, pattern)
        st.experimental_rerun()

# Display scraping jobs in a more compact layout
st.write("Current scraper jobs:")
for job in st.session_state.scraper_jobs:
    source = f"[{strip_https(job['source'])}]({job['source']})"
    mode = f"{job['mode'].capitalize()}"
    status = job.get("status", "pending")  # Default to pending if no status field
    status_color = get_status_color(status)
    
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # Adjust column widths
        col1.markdown(source, unsafe_allow_html=True)
        col2.write(mode)
        col3.markdown(
            f"<span style='background-color: {status_color}; color: white; padding: 5px 10px; border-radius: 5px;'>{status.capitalize()}</span>",
            unsafe_allow_html=True,
        )
        if col4.button("Delete", key=str(job["_id"])):
            st.session_state.scraper_jobs = delete_scraping_job(job["_id"])
            st.experimental_rerun()
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)  # Add separator line
