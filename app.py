import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- Page Config ---
st.set_page_config(page_title="Textile Cert Tracker", layout="wide")
st.title("🛡️ Client Certificate Compliance Manager")

# --- Data Initialization ---
# In a real app, you'd link this to a database or Google Sheets.
# For now, we use session_state to keep data during the current session.
if 'client_db' not in st.session_state:
    st.session_state.client_db = pd.DataFrame(columns=[
        "Client Name", "Standards", "Issue Date", "Expiry Date", "Status"
    ])

# --- Sidebar: Data Entry ---
st.sidebar.header("Add New Client")
with st.sidebar.form("client_form", clear_on_submit=True):
    name = st.text_input("Client Name")
    
    # Checklist for Standards
    selected_standards = st.multiselect(
        "Select Standards", 
        ["GOTS", "OCS", "GRS", "RCS", "BCI"]
    )
    
    col1, col2 = st.columns(2)
    issue_date = col1.date_input("Issue Date", value=date.today())
    expiry_date = col2.date_input("Expiry Date", value=date.today())
    
    submitted = st.form_submit_button("Add to Database")

    if submitted:
        if name and selected_standards:
            # Logic for Status
            today = date.today()
            days_to_expiry = (expiry_date - today).days
            
            if days_to_expiry < 0:
                status = "🔴 Expired"
            elif days_to_expiry <= 30:
                status = "🟠 Near Expiry"
            else:
                status = "🟢 Active"
            
            # Update DataFrame
            new_data = {
                "Client Name": name,
                "Standards": ", ".join(selected_standards),
                "Issue Date": issue_date,
                "Expiry Date": expiry_date,
                "Status": status
            }
            st.session_state.client_db = pd.concat([st.session_state.client_db, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"Added {name}")
        else:
            st.error("Please fill in all fields")

# --- Main Dashboard ---
if not st.session_state.client_db.empty:
    # 1. Metrics
    total = len(st.session_state.client_db)
    expired = len(st.session_state.client_db[st.session_state.client_db['Status'] == "🔴 Expired"])
    
    m1, m2 = st.columns(2)
    m1.metric("Total Clients", total)
    m2.metric("Critical (Expired)", expired, delta_color="inverse")

    # 2. Visuals
    st.subheader("Compliance Visuals")
    fig = px.bar(
        st.session_state.client_db, 
        x="Status", 
        color="Status",
        color_discrete_map={"🟢 Active": "green", "🟠 Near Expiry": "orange", "🔴 Expired": "red"},
        title="Certificate Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 3. Data Table
    st.subheader("Client Registry")
    st.dataframe(st.session_state.client_db, use_container_width=True)
else:
    st.info("No data added yet. Use the sidebar to enter client details.")
