import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# ---------------- FILE ---------------- #

DATA_FILE = "daily_work_log_simple.csv"

TEAMS = ["Dissemination", "GIS", "IT", "KMS", "Platform"]

# ---------------- DATA ---------------- #

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["date","name","team","work_details"])

def save_entry(row):
    df = load_data()
    df = pd.concat([df,pd.DataFrame([row])],ignore_index=True)
    df.to_csv(DATA_FILE,index=False)

# ---------------- ROUTING ---------------- #

params = st.query_params
role = params.get("role",["user"])
role = role[0] if isinstance(role,list) else role

# ===============================================================
# ======================= USER VIEW =============================
# ===============================================================

if role != "admin":

    st.title("📝 Simple Daily Work Log")

    name = st.text_input("Your Name","Somnath Pati")
    team = st.selectbox("Your Team / Department", TEAMS)
    work_date = st.date_input("Work Date", date.today())

    work = st.text_area(
        "Daily Work Details",
        height=180,
        placeholder="Write everything you worked on today..."
    )

    if st.button("💾 Save Today's Work"):

        if not name.strip() or not work.strip():
            st.warning("Name and work details are required.")
        else:
            save_entry({
                "date": work_date.strftime("%Y-%m-%d"),
                "name": name.strip(),
                "team": team,
                "work_details": work.strip()
            })

            st.success("✅ Daily work saved successfully!")

# ===============================================================
# ====================== ADMIN VIEW =============================
# ===============================================================

else:

    st.title("📊 Daily Work Reports Dashboard")

    df = load_data()

    if df.empty:
        st.info("No data found yet.")
        st.stop()

    # -------- Filters -------- #

    with st.expander("Filters"):

        start_date = st.date_input("Start Date", min(df["date"]).astype("datetime64[D]").astype(date))
        end_date = st.date_input("End Date", max(df["date"]).astype("datetime64[D]").astype(date))

        person_list = ["All"] + sorted(df["name"].unique().tolist())
        person = st.selectbox("Select Person", person_list)

        team_list = ["All"] + sorted(df["team"].unique().tolist())
        team = st.selectbox("Select Team", team_list)

    df["date"] = pd.to_datetime(df["date"])

    filtered = df.copy()

    filtered = filtered[
        (filtered["date"] >= pd.to_datetime(start_date)) &
        (filtered["date"] <= pd.to_datetime(end_date))
    ]

    if person != "All":
        filtered = filtered[filtered["name"] == person]

    if team != "All":
        filtered = filtered[filtered["team"] == team]

    # -------- OUTPUT -------- #

    st.subheader("🗂 Filtered Records")

    filtered["date"] = filtered["date"].dt.strftime("%Y-%m-%d")

    st.dataframe(filtered,use_container_width=True)

    st.markdown("### 📥 Download Reports")

    st.download_button(
        "Download Filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="daily_work_report_filtered.csv",
        mime="text/csv"
    )

    # -------- PERIOD SELECT HELP -------- #

    st.info(
        """
Use Start Date → End Date to generate:

Weekly report → last 7 days  
Monthly report → select full month  
Quarterly report → 3 months range  
Half yearly → 6 months range  
Yearly report → 12 months range  
"""
    )
