import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --------------- SETTINGS --------------- #

DATA_FILE = "daily_thematic_28.csv"

VERTICALS = ["Dissemination", "GIS", "IT", "KMS", "Platform"]

THEMATICS = {
    1: "AI Content Localization & Outreach",
    2: "Crop Health Detection App & WhatsApp Bot",
    3: "Tele-Consultation Platform / Helpline / IVRS",
    4: "Animal Digital Information System",
    5: "FPO Management App – Development and Refinement",
    6: "24/7 Weather-Based Marine Fisheries Advisories (Machli App)",
    7: "Domain-Specific Data Management Tools (Web Scraping + GIS/ML)",
    8: "Livelihood Advisory Podcasts via Internet Radio",
    9: "RF Livelihood Video Learning App",
    10: "Rural Yellow Pages App – Development & Scale",
    11: "Digital Farm Management System (DFMS) – Predictive and Mobile-Based Advisory",
    12: "RF Super App – Scaling for Integrated Service Delivery",
    13: "E-Learning & Knowledge Dissemination",
    14: "Cloud Migration & Infrastructure Enhancements",
    15: "Early Warning Systems & Disaster Resilience",
    16: "Tech for Social Good & Knowledge Empowerment",
    17: "Data-Driven Impact: Measuring Success in RF’s Tech-based Outreach",
    18: "Web-Based Knowledge Management System (WebKMS) + Multilingual AI Integration",
    19: "Geo-Spatial Vulnerability Mapping for Inclusive Development",
    20: "Monitoring & Mapping Water Harvesting Structures",
    21: "NDVI-Based Crop Yield Computation",
    22: "Multi-Hazard Risk Mapping & Early Warning Systems",
    23: "Above Ground Biomass (AGB) Estimation",
    24: "Change Detection & Environmental Monitoring",
    25: "Climate-Responsive Modelling & Forecasting",
    26: "Tech-Enabled Monitoring & Evaluation using Mobile-Based GIS",
    27: "Spatial Decision Support & Risk Intelligence (WebKMS + GIS/RS)",
    28: "IT Documentation, Digital Infrastructure Support & Other Support",
}


# --------------- DATA HELPERS --------------- #

def load_data():
    """Load existing CSV or create empty DataFrame with all columns."""
    columns = ["date", "name", "vertical"] + [f"T{i}" for i in range(1, 29)]
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Ensure all columns exist even if file older
        for c in columns:
            if c not in df.columns:
                df[c] = ""
        return df[columns]
    else:
        return pd.DataFrame(columns=columns)


def save_row(row: dict):
    """Append a single daily row (28 thematics) safely to CSV."""
    df = load_data()
    columns = df.columns.tolist()

    # Make sure all expected columns exist in row
    for c in columns:
        if c not in row:
            row[c] = ""

    # Append and save
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# --------------- ROUTING (USER / ADMIN) --------------- #

params = st.query_params
role = params.get("role", ["user"])
role = role[0] if isinstance(role, list) else role

# --------------- USER VIEW --------------- #

if role != "admin":
    st.title("📝 Daily Work Report – 28 Thematic Areas")

    name = st.text_input("Your Name", "Somnath Pati")
    vertical = st.selectbox("Vertical / Team", VERTICALS)
    work_date = st.date_input("Work Date", datetime.today())

    st.markdown("Fill only the thematics where you have work for the day. Others can be left blank.")

    theme_texts = {}

    # Use expanders so the page is not too long
    for tid in range(1, 29):
        label = f"{tid}. {THEMATICS[tid]}"
        with st.expander(label, expanded=(tid <= 3)):  # first few expanded
            txt = st.text_area(
                f"Work under Theme {tid}",
                key=f"theme_{tid}",
                height=80,
                placeholder=f"Enter work done for: {label}"
            )
            theme_texts[tid] = txt.strip()

    if st.button("💾 Save Today's Work"):
        if not name.strip():
            st.error("Please enter your name.")
        else:
            row = {
                "date": work_date.strftime("%Y-%m-%d"),
                "name": name.strip(),
                "vertical": vertical,
            }

            # Map T1..T28 from text areas
            for tid in range(1, 29):
                row[f"T{tid}"] = theme_texts[tid]

            save_row(row)
            st.success("✅ Daily thematic work saved successfully!")

            st.subheader("Preview of Saved Row")
            st.dataframe(
                pd.DataFrame([row]),
                use_container_width=True
            )

# --------------- ADMIN VIEW --------------- #

else:
    st.title("📊 Daily Work – 28 Thematic Report (Admin View)")

    df = load_data()
    if df.empty:
        st.warning("No data saved yet.")
    else:
        with st.expander("Filters"):
            # Date filter
            date_filter = st.date_input("Filter by date (optional)", None)

            # Name filter
            names = ["All"] + sorted(df["name"].dropna().unique().tolist())
            name_filter = st.selectbox("Filter by name", names)

            # Vertical filter
            verts = ["All"] + sorted(df["vertical"].dropna().unique().tolist())
            vert_filter = st.selectbox("Filter by vertical", verts)

        filtered = df.copy()

        if date_filter:
            filtered = filtered[filtered["date"] == date_filter.strftime("%Y-%m-%d")]

        if name_filter != "All":
            filtered = filtered[filtered["name"] == name_filter]

        if vert_filter != "All":
            filtered = filtered[filtered["vertical"] == vert_filter]

        st.subheader("Saved Daily Records")
        st.dataframe(filtered, use_container_width=True)

        st.download_button(
            "⬇ Download CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="daily_thematic_28_filtered.csv",
            mime="text/csv"
        )
