import streamlit as st
import pandas as pd

from utils.data_loader import load_and_prepare_data
from utils.filters import filter_by_recency
from utils.pitch import assign_pitch_angle
from utils.personas import assign_persona

from components.sidebar import render_sidebar
from components.metrics import render_metrics

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Selling Signals – Rep View",
    layout="wide"
)

st.title("📍 Selling Signals – Rep View")
st.caption(
    "Targets are generated dynamically based on geography and current market signals."
)

# --------------------------------------------------
# Load Data (schema-only CSV is valid)
# --------------------------------------------------
df = load_and_prepare_data("data/selling_targets.csv")

# Handle empty dataset explicitly (normal starting state)
if df.empty:
    st.warning("No selling targets have been generated yet.")
    st.info(
        "Select a geographic area and generate targets to begin. "
        "This app displays dynamically generated selling targets."
    )
    st.stop()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
filters = render_sidebar(df)
filtered_df = filters["geo_df"]

# Business filters
filtered_df = filtered_df[
    (filtered_df["Buying Likelihood"].isin(filters["likelihoods"])) &
    (filtered_df["Selling Trigger Source"].isin(filters["sources"])) &
    (filtered_df["Employee Count"]
     .between(filters["emp_range"][0], filters["emp_range"][1], inclusive="both"))
]

# Trigger recency
filtered_df = filter_by_recency(filtered_df, filters["recency"])

# --------------------------------------------------
# Derived Rep Fields
# --------------------------------------------------
filtered_df["Suggested Pitch Angle"] = filtered_df.apply(
    lambda row: assign_pitch_angle(
        row["Selling Trigger"],
        row["Sector / Domain"]
    ),
    axis=1
)

filtered_df["Target Persona"] = filtered_df["Sector / Domain"].apply(assign_persona)

# --------------------------------------------------
# Metrics
# --------------------------------------------------
st.subheader("📊 Overview")
render_metrics(filtered_df)

# --------------------------------------------------
# Calendar-Aligned View
# --------------------------------------------------
st.subheader("📅 Call Priority")

calendar_filter = st.radio(
    "Show accounts triggered:",
    ["All", "This Week", "Last 2 Weeks", "This Month"],
    horizontal=True
)

if calendar_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Call Timing"] == calendar_filter
    ]

# --------------------------------------------------
# Results Table
# --------------------------------------------------
st.subheader("📋 Accounts to Call")

display_cols = [
    "Call Timing",
    "Company Name",
    "HQ State",
    "Suggested Pitch Angle",
    "Selling Trigger",
    "Buying Likelihood"
]

st.dataframe(
    filtered_df[display_cols].sort_values(
        by=["Call Timing", "Buying Likelihood"],
        ascending=[True, False]
    ),
    use_container_width=True
)

# --------------------------------------------------
# Company Detail View
# --------------------------------------------------
st.subheader("🔎 Account Detail")

selected_company = st.selectbox(
    "Select an account",
    filtered_df["Company Name"].unique()
)

row = filtered_df[
    filtered_df["Company Name"] == selected_company
].iloc[0]

st.markdown("### 🎯 Recommended Pitch")
st.success(row["Suggested Pitch Angle"])

st.markdown("**Why now:**")
st.write(row["Selling Trigger"])

st.markdown("---")

st.markdown(f"""
**Location:** {row['HQ City']}, {row['HQ State']}  
**Employees:** {row['Employee Count']}  
**Sector:** {row['Sector / Domain']}  
**Buying Likelihood:** {row['Buying Likelihood']}  

**Where this signal came from:**  
{row['Selling Trigger Source']}  

**Equipment Implications:**  
{row['Equipment Types']}  

**Notes:**  
{row['Notes']}
""")
