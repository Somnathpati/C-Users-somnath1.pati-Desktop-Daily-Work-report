import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# ================= SETTINGS =================

DATA_FILE = "daily_work_log_simple.csv"

TEAMS = [
    "Dissemination",
    "GIS",
    "IT",
    "KMS",
    "Platform"
]

# ================= DATA FUNCTIONS =================

def load_data():
    """Load CSV or create empty structure."""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["date", "name", "team", "work_details"])
    return df


def save_entry(row):
    """Append new row to CSV safely."""
    df = load_data()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# ================= ROUTING =================

params = st.query_params
role = params.get("role", ["user"])
role = role[0] if isinstance(role, list) else role


# ====================================================
# ===================== USER VIEW ====================
# ====================================================

if role != "admin":

    st.title("📝 Daily Work Log")

    name = st.text_input("Your Name", "Somnath Pati")

    team = st.selectbox("Your Team / Department", TEAMS)

    work_date = st.date_input("Work Date", date.today())

    work = st.text_area(
        "Daily Work Details",
        height=180,
        placeholder="Write everything you worked on today..."
    )

    if st.button("✅ Save Today's Work"):

        if not name.strip():
            st.warning("Please enter your name.")
        elif not work.strip():
            st.warning("Please enter your work details.")
        else:
            save_entry({
                "date": work_date.strftime("%Y-%m-%d"),
                "name": name.strip(),
                "team": team,
                "work_details": work.strip()
            })

            st.success("✅ Daily work saved successfully!")


# ====================================================
# ===================== ADMIN VIEW ===================
# ====================================================

else:

    st.title("📊 Daily Work Reports")

    df = load_data()

    if df.empty:
        st.info("No data available yet.")
        st.stop()

    # ✅ Convert date safely
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ----------- FILTERS -----------

    with st.expander("Filters"):

        min_date = df["date"].min()
        max_date = df["date"].max()

        if pd.isna(min_date) or pd.isna(max_date):
            min_date = datetime.today()
            max_date = datetime.today()

        start_date = st.date_input("Start Date", min_date.date())
        end_date = st.date_input("End Date", max_date.date())

        people = ["All"] + sorted(df["name"].dropna().unique().tolist())
        selected_person = st.selectbox("Person", people)

        teams = ["All"] + sorted(df["team"].dropna().unique().tolist())
        selected_team = st.selectbox("Team", teams)

    # ----------- APPLY FILTERS -----------

    filtered = df.copy()

    filtered = filtered[
        (filtered["date"] >= pd.to_datetime(start_date))
        & (filtered["date"] <= pd.to_datetime(end_date))
    ]

    if selected_person != "All":
        filtered = filtered[filtered["name"] == selected_person]

    if selected_team != "All":
        filtered = filtered[filtered["team"] == selected_team]

    filtered["date"] = filtered["date"].dt.strftime("%Y-%m-%d")

    # ----------- DISPLAY -----------

    st.subheader("🗂 Filtered Records")

    st.dataframe(filtered, use_container_width=True)

    # ----------- DOWNLOAD -----------

    st.download_button(
        label="📥 Download CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="daily_work_report_filtered.csv",
        mime="text/csv"
    )

    # ----------- HELP -----------

    st.info(
        """
### ✅ How to generate reports

- **Weekly report:** select last 7 days  
- **Monthly report:** select full month  
- **Quarterly report:** select 3-month range  
- **Half-yearly report:** select 6-month range  
- **Yearly report:** select full year  

Then click **Download CSV**.
"""
    )
