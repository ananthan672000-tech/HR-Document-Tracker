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
        "Browse Category",
        "Add New Document"
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
    st.success(f"Total Documents: {len(result)}")

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

# -----------------------------
# Add New Document
# -----------------------------
elif option == "Add New Document":

    st.subheader("➕ Add New Document")

    with st.form("add_document"):

        doc_id = st.text_input("Document ID")
        doc_name = st.text_input("Document Name")
        category = st.text_input("Category")
        custodian = st.text_input("Custodian")
        location = st.text_input("Storage Location")
        retention = st.text_input("Retention")
        status = st.selectbox(
            "Status",
            ["Active", "Archived"]
        )

        submitted = st.form_submit_button("Save Document")

        if submitted:

            if (
                doc_id == "" or
                doc_name == "" or
                category == "" or
                custodian == "" or
                location == "" or
                retention == ""
            ):
                st.error("Please fill all fields.")

            else:

                new_row = pd.DataFrame([{
                    "Document ID": doc_id,
                    "Document Name": doc_name,
                    "Category": category,
                    "Custodian": custodian,
                    "Storage Location": location,
                    "Retention": retention,
                    "Status": status
                }])

                df = pd.concat([df, new_row], ignore_index=True)

                df.to_csv("documents.csv", index=False)

                st.success("✅ Document added successfully!")

                st.rerun()
