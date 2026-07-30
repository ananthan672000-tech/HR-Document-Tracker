import streamlit as st
import pandas as pd

# -----------------------------
# Page Settings
# -----------------------------
st.set_page_config(
    page_title="HR Document Management System",
    page_icon="📁",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("documents.csv")

# -----------------------------
# Header
# -----------------------------
st.title("📁 HR Document Management System")
st.caption("Demo Prototype")

# -----------------------------
# Dashboard
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Documents", len(df))
col2.metric("Custodians", df["Custodian"].nunique())
col3.metric("Categories", df["Category"].nunique())

st.divider()

# -----------------------------
# Sidebar
# -----------------------------
option = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Search by Document",
        "Search by Custodian",
        "Browse Category"
    ]
)

# -----------------------------
# Dashboard
# -----------------------------
if option == "Dashboard":

    st.subheader("All Documents")

    st.dataframe(df, use_container_width=True)

# -----------------------------
# Search by Document
# -----------------------------
elif option == "Search by Document":

    search = st.text_input("Enter Document Name")

    if search:

        result = df[
            df["Document Name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

        if len(result) == 0:
            st.error("No document found.")
        else:
            st.success(f"{len(result)} document(s) found")
            st.dataframe(result, use_container_width=True)

# -----------------------------
# Search by Custodian
# -----------------------------
elif option == "Search by Custodian":

    custodian = st.selectbox(
        "Select Custodian",
        sorted(df["Custodian"].unique())
    )

    result = df[df["Custodian"] == custodian]

    st.subheader(f"Documents under {custodian}")

    st.success(f"Total Documents : {len(result)}")

    st.dataframe(result, use_container_width=True)

# -----------------------------
# Browse Category
# -----------------------------
elif option == "Browse Category":

    category = st.selectbox(
        "Select Category",
        sorted(df["Category"].unique())
    )

    result = df[df["Category"] == category]

    st.dataframe(result, use_container_width=True)