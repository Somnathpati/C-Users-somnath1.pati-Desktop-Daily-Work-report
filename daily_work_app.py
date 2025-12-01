import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "daily_work_log.csv"

# ---------- Helper functions ----------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "date",
                "employee_name",
                "department",
                "work_summary"
            ]
        )

def save_entry(employee_name, department, date, work_summary):
    df = load_data()
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": date.strftime("%Y-%m-%d"),
        "employee_name": employee_name,
        "department": department,
        "work_summary": work_summary.strip()
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ---------- Decide role from URL ----------
params = st.query_params  # new API
role = params.get("role", ["user"])
role = role[0] if isinstance(role, list) else role

# ---------- USER VIEW: Daily work submission ----------
if role != "admin":
    st.title("Daily Work Log – Submission")

    # You can replace these with your own master lists
    employee_name = st.selectbox(
        "Choose Your Name *",
        ["Select", "Somnath Pati", "Other"]
    )

    department = st.selectbox(
        "Select Your Department *",
        ["Select", "Information Services", "RT Team", "Other"]
    )

    date = st.date_input("Work Date *", datetime.today())

    st.markdown("### Describe today’s work *")
    work_example = (
        "Example:\n"
        "• Downloaded VMS call logs and WhatsApp call logs\n"
        "• Created 6 WhatsApp CSVs and disseminated 6 promotional messages\n"
        "• Organized and supported Power BI dashboard creation training for the team\n"
    )
    work_summary = st.text_area(
        "Enter all activities in detail",
        value="",
        placeholder=work_example,
        height=200
    )

    if st.button("Submit Today’s Work"):
        if employee_name == "Select" or department == "Select" or not work_summary.strip():
            st.error("Please select your name, department, and enter your work details.")
        else:
            save_entry(employee_name, department, date, work_summary)
            st.success("✅ Daily work saved successfully!")

    st.info(
        "Tip: At the end of the week, these daily entries can be used to auto-fill your weekly work report."
    )

# ---------- ADMIN VIEW: Review & export ----------
else:
    st.title("Daily Work Log – Admin View")

    df = load_data()
    if df.empty:
        st.warning("No daily work entries found yet.")
    else:
        # Filters
        with st.expander("Filter data"):
            selected_date = st.date_input(
                "Filter by date (optional)", value=None
            )
            selected_name = st.selectbox(
                "Filter by employee (optional)",
                ["All"] + sorted(df["employee_name"].dropna().unique().tolist())
            )

        filtered_df = df.copy()

        if selected_date:
            filtered_df = filtered_df[filtered_df["date"] == selected_date.strftime("%Y-%m-%d")]

        if selected_name != "All":
            filtered_df = filtered_df[filtered_df["employee_name"] == selected_name]

        st.subheader("Daily Work Entries")
        st.dataframe(filtered_df, use_container_width=True)

        # Download as CSV
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download filtered data as CSV",
            data=csv_data,
            file_name="daily_work_log_filtered.csv",
            mime="text/csv"
        )

        st.caption("You can connect this CSV to your weekly report app or Power BI dashboard.")
