import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("Audit Dashboard & Tracking System")

file = "data.csv"

# Load data
if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=[
        "Client Name","Standard","Audit Start","Audit End",
        "Report Uploaded","Report Reviewed",
        "Certificate Issued","Major NC","Minor NC"
    ])

# ---------------- FORM ----------------
st.sidebar.header("Add New Audit")

with st.sidebar.form("form"):
    client = st.text_input("Client Name")
    standard = st.multiselect("Standard", ["GOTS","OCS","GRS","BCI"])
    
    audit_start = st.date_input("Audit Start")
    audit_end = st.date_input("Audit End")
    
    upload = st.date_input("Report Uploaded")
    review = st.date_input("Report Reviewed")
    cert = st.date_input("Certificate Issued")
    
    major = st.number_input("Major NC", 0)
    minor = st.number_input("Minor NC", 0)

    submit = st.form_submit_button("Save")

    if submit:
        new = {
            "Client Name": client,
            "Standard": ", ".join(standard),
            "Audit Start": audit_start,
            "Audit End": audit_end,
            "Report Uploaded": upload,
            "Report Reviewed": review,
            "Certificate Issued": cert,
            "Major NC": major,
            "Minor NC": minor
        }

        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(file, index=False)
        st.success("Saved!")

# ---------------- CALCULATIONS ----------------
if not df.empty:
    df["Audit End"] = pd.to_datetime(df["Audit End"], errors="coerce")
    df["Report Uploaded"] = pd.to_datetime(df["Report Uploaded"], errors="coerce")
    df["Report Reviewed"] = pd.to_datetime(df["Report Reviewed"], errors="coerce")
    df["Certificate Issued"] = pd.to_datetime(df["Certificate Issued"], errors="coerce")

    df["Upload TAT"] = (df["Report Uploaded"] - df["Audit End"]).dt.days
    df["Review TAT"] = (df["Report Reviewed"] - df["Report Uploaded"]).dt.days
    df["Certification TAT"] = (df["Certificate Issued"] - df["Report Reviewed"]).dt.days

    def status(row):
        if pd.isna(row["Report Uploaded"]):
            return "Pending Upload"
        elif pd.isna(row["Report Reviewed"]):
            return "Pending Review"
        elif pd.isna(row["Certificate Issued"]):
            return "Pending Certification"
        else:
            return "Completed"

    df["Status"] = df.apply(status, axis=1)

# ---------------- FILTERS ----------------
st.sidebar.header("Filters")

client_filter = st.sidebar.multiselect("Client", df["Client Name"].dropna().unique())
status_filter = st.sidebar.multiselect("Status", df["Status"].dropna().unique())

filtered_df = df.copy()

if client_filter:
    filtered_df = filtered_df[filtered_df["Client Name"].isin(client_filter)]

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

# ---------------- DASHBOARD ----------------
st.subheader("Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Audits", len(filtered_df))
col2.metric("Completed", len(filtered_df[filtered_df["Status"]=="Completed"]))
col3.metric("Pending", len(filtered_df[filtered_df["Status"]!="Completed"]))
col4.metric("Avg Upload TAT", round(filtered_df["Upload TAT"].mean(),1) if not filtered_df.empty else 0)

# ---------------- CHARTS ----------------
st.subheader("Insights")

st.bar_chart(filtered_df["Status"].value_counts())

st.bar_chart(filtered_df.groupby("Client Name")["Major NC"].sum())

# ---------------- TABLE ----------------
st.subheader("Audit Records")
st.dataframe(filtered_df)

# ---------------- DOWNLOAD ----------------
st.download_button(
    "Download Data",
    filtered_df.to_csv(index=False),
    "audit_data.csv"
)
