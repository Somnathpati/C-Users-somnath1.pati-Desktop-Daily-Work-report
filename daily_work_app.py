import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------- SETTINGS ----------

DATA_FILE = "daily_work_master.csv"

VERTICALS = [
    "Dissemination",
    "GIS",
    "IT",
    "KMS",
    "Platform"
]

THEMATICS = [
    (1, "AI Content Localization & Outreach"),
    (2, "Crop Health Detection App & WhatsApp Bot"),
    (3, "Tele-Consultation / Helpline / IVRS"),
    (4, "Animal Digital Information System"),
    (5, "FPO Management App"),
    (6, "Machli Fisheries App"),
    (7, "Domain Data Tools (GIS/ML/Web Scraping)"),
    (8, "Internet Radio Podcasts"),
    (9, "Video Learning App"),
    (10, "Rural Yellow Pages"),
    (11, "DFMS – Farm Management"),
    (12, "RF Super App"),
    (13, "E-Learning / Training"),
    (14, "Cloud & Infrastructure"),
    (15, "Early Warning Systems"),
    (16, "Tech for Social Good"),
    (17, "Impact Analytics & Reporting"),
    (18, "WebKMS / CSDMS"),
    (19, "Geo-Spatial Vulnerability Mapping"),
    (20, "Water Harvesting Mapping"),
    (21, "NDVI & Yield Computation"),
    (22, "Multi-Hazard Mapping"),
    (23, "AGB Estimation"),
    (24, "Change Detection"),
    (25, "Climate Forecasting"),
    (26, "Mobile GIS Monitoring"),
    (27, "Spatial Risk Decision Support"),
    (28, "IT Support & Documentation")
]

THEME_LOOKUP = {t[0]: t[1] for t in THEMATICS}

# ---------- DATA LAYER ----------

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)

    return pd.DataFrame(columns=[
        "date",
        "name",
        "vertical",
        "thematic_id",
        "thematic_name",
        "work_details",
        "quantity"
    ])

def save_entry(row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ---------- ROUTING ----------

params = st.query_params
role = params.get("role", ["user"])
role = role[0] if isinstance(role, list) else role

# ======================================================
# ================= USER ENTRY VIEW ===================
# ======================================================

if role != "admin":

    st.title("📝 Daily Work Report")

    name = st.text_input("Your Name", "Somnath Pati")

    vertical = st.selectbox("Vertical / Team", VERTICALS)

    work_date = st.date_input("Work Date", datetime.today())

    thematic_id = st.selectbox(
        "Select Thematic",
        options=[t[0] for t in THEMATICS],
        format_func=lambda x: f"{x}. {THEME_LOOKUP[x]}"
    )

    details = st.text_area(
        "Work Details",
        height=150,
        placeholder="Example: Downloaded call logs, created WhatsApp CSV, disseminated mustard VMS"
    )

    qty = st.text_input("Quantity / Count (optional)", "")

    if st.button("✅ Save Daily Work"):
        if not details.strip():
            st.warning("Please enter your work details.")
        else:
            save_entry({
                "date": work_date.strftime("%Y-%m-%d"),
                "name": name,
                "vertical": vertical,
                "thematic_id": thematic_id,
                "thematic_name": THEME_LOOKUP[thematic_id],
                "work_details": details,
                "quantity": qty
            })

            st.success("✅ Daily work saved successfully!")

# ======================================================
# ================= ADMIN DASHBOARD ===================
# ======================================================

else:

    st.title("📊 Daily Work – Admin Dashboard")

    df = load_data()

    with st.expander("Filters"):

        date_filter = st.date_input("Filter by date", None)

        staff = ["All"] + sorted(df["name"].dropna().unique().tolist())
        emp = st.selectbox("Employee", staff)

        team = st.selectbox(
            "Vertical",
            ["All"] + VERTICALS
        )

        theme = st.selectbox(
            "Thematic",
            ["All"] + [f"{t[0]}. {t[1]}" for t in THEMATICS]
        )

    filtered = df.copy()

    if date_filter:
        filtered = filtered[filtered["date"] == date_filter.strftime("%Y-%m-%d")]

    if emp != "All":
        filtered = filtered[filtered["name"] == emp]

    if team != "All":
        filtered = filtered[filtered["vertical"] == team]

    if theme != "All":
        filtered = filtered[
            filtered["thematic_name"] == theme.split(". ",1)[1]
        ]

    st.subheader("✅ Daily Submitted Work")
    st.dataframe(filtered, use_container_width=True)

    # ---------------- THEMATIC SUMMARY ----------------

    st.subheader("📊 Summary: Entries per Thematic")

    if not filtered.empty:

        summary = (
            filtered.groupby(["thematic_id", "thematic_name"])
            .size()
            .reset_index(name="total_entries")
            .sort_values("total_entries", ascending=False)
        )

        st.dataframe(summary, use_container_width=True)

    # ---------------- DOWNLOAD ----------------

    st.download_button(
        "⬇ Download CSV",
        data=df.to_csv(index=False).encode(),
        file_name="daily_work_master.csv",
        mime="text/csv"
    )
