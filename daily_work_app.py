import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re

# ---------------- FILE SETTINGS ---------------- #

DATA_FILE = "daily_thematic_log.csv"

# ---------------- THEMATIC DEFINITIONS ---------------- #

THEMATICS = [
    {"id": 1, "name": "AI-Driven Multilingual Content Localization & Accessible Digital Outreach through Integrated Multichannel Platforms",
     "keywords": ["vms","dissemination","campaign","outreach","osf","call log","calllog","whatsapp",
                  "what app","promo","promotional","csv","mustard","paddy","livestock",
                  "youtube","facebook","voice message","broadcast"]},

    {"id": 2, "name": "AI-Based Crop Health Detection App and WhatsApp Bot",
     "keywords": ["crop health","pest detection","plant disease","whatsapp bot","chatbot","ai bot"]},

    {"id": 3, "name": "Tele-Consultation Platform Enhancements – AI-integrated, multilingual, voice-enabled helpline",
     "keywords": ["helpline","ivr","ivrs","call center","call centre","teleconsult","tele consultation","voice call"]},

    {"id": 4, "name": "Development of Animal Digital Information System",
     "keywords": ["animal digital","adis","animal info"]},

    {"id": 5, "name": "FPO Management App – Development and Refinement",
     "keywords": ["fpo management","fpo app","fpo support"]},

    {"id": 6, "name": "24/7 Weather-Based Marine Fisheries Advisories (Machli App)",
     "keywords": ["machli","marine","fisheries"]},

    {"id": 7, "name": "Domain-Specific Data Management Tools (Web Scraping + GIS/ML)",
     "keywords": ["scraping","web scraping","crawler","data tool","gis ml"]},

    {"id": 8, "name": "Livelihood Advisory Podcasts via Internet Radio",
     "keywords": ["internet radio","podcast","audio","radio script"]},

    {"id": 9, "name": "RF Livelihood Video Learning App",
     "keywords": ["video","youtube live","shoot","editing"]},

    {"id": 10, "name": "Rural Yellow Pages App – Development & Scale",
     "keywords": ["yellow pages","service directory"]},

    {"id": 11, "name": "Digital Farm Management System (DFMS)",
     "keywords": ["dfms","farm management","plot advisory"]},

    {"id": 12, "name": "RF Super App – Scaling for Integrated Service Delivery",
     "keywords": ["super app"]},

    {"id": 13, "name": "E-Learning & Knowledge Dissemination",
     "keywords": ["training","workshop","webinar","orientation","session","meeting","power bi training"]},

    {"id": 14, "name": "Cloud Migration & Infrastructure Enhancements",
     "keywords": ["cloud","aws","azure","server migration"]},

    {"id": 15, "name": "Early Warning Systems & Disaster Resilience",
     "keywords": ["early warning","disaster","alert system"]},

    {"id": 16, "name": "Tech for Social Good & Knowledge Empowerment",
     "keywords": ["testing app","scan app","walkthrough","digital literacy"]},

    {"id": 17, "name": "Data-Driven Impact Analytics",
     "keywords": ["dashboard","analytics","impact","report","analysis","kpi"]},

    {"id": 18, "name": "WebKMS / CSDMS Knowledge Management",
     "keywords": ["kms","webkms","csdms","validate","verify","upload","approve"]},

    {"id": 19, "name": "Geo-Spatial Vulnerability Mapping",
     "keywords": ["vulnerability mapping","risk map"]},

    {"id": 20, "name": "Water Harvesting Mapping",
     "keywords": ["water harvesting","check dam","farm pond"]},

    {"id": 21, "name": "NDVI Crop Yield Computation",
     "keywords": ["ndvi","yield"]},

    {"id": 22, "name": "Multi Hazard Risk Mapping",
     "keywords": ["multi hazard","hazard map"]},

    {"id": 23, "name": "AGB Estimation",
     "keywords": ["agb","biomass"]},

    {"id": 24, "name": "Change Detection & Environmental Monitoring",
     "keywords": ["change detection","environment monitoring"]},

    {"id": 25, "name": "Climate Forecasting & Modelling",
     "keywords": ["climate modelling","forecast"]},

    {"id": 26, "name": "Mobile GIS Monitoring & Evaluation",
     "keywords": ["mobile gis","m&e app","survey app"]},

    {"id": 27, "name": "Spatial Decision Support",
     "keywords": ["spatial decision","risk intelligence"]},

    {"id": 28, "name": "IT Documentation & Other Support",
     "keywords": ["documentation","vba","excel","installation","support","help","troubleshoot","issue"]}
]

# ---------------- UTILITIES ---------------- #

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        "timestamp","date","employee","department",
        "activity","thematic_ids","thematic_names"
    ])

def detect_thematic(text):
    text = text.lower()
    hits = []
    for t in THEMATICS:
        for k in t["keywords"]:
            if k in text:
                hits.append(t)
                break
    if not hits:
        hits = [t for t in THEMATICS if t["id"] == 28]
    return hits

def save_activities(name, dept, date, lines):
    df = load_data()
    rows = []

    for line in lines:
        matches = detect_thematic(line)
        ids = "|".join(str(t["id"]) for t in matches)
        names = "|".join(t["name"] for t in matches)

        rows.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date": date.strftime("%Y-%m-%d"),
            "employee": name,
            "department": dept,
            "activity": line,
            "thematic_ids": ids,
            "thematic_names": names
        })

    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ---------------- APP ---------------- #

params = st.query_params
role = params.get("role",["user"])
role = role[0] if isinstance(role,list) else role

# ---------------- USER PAGE ---------------- #

if role != "admin":

    st.title("📋 Daily Work Logger")

    name = st.text_input("Your Name", "Somnath Pati")
    dept = st.text_input("Department", "Information Services")
    date = st.date_input("Date", datetime.today())

    st.markdown("### Enter work (one point per line)")
    text = st.text_area("Activities")

    if st.button("Save Daily Work"):
        if not text.strip():
            st.warning("Please enter work.")
        else:
            lines = [i.strip() for i in text.split("\n") if i.strip()]
            save_activities(name, dept, date, lines)
            st.success("✅ Work saved with thematic mapping!")

            st.markdown("### Detected Thematics")
            for ln in lines:
                th = detect_thematic(ln)
                st.write("•", ln)
                for t in th:
                    st.caption(f"   → {t['id']} - {t['name']}")

# ---------------- ADMIN PAGE ---------------- #

else:

    st.title("📊 Admin Dashboard")

    df = load_data()

    with st.expander("Filter"):
        date_filter = st.date_input("Date filter (optional)", None)

        employees = ["All"] + sorted(df["employee"].dropna().unique().tolist())
        emp = st.selectbox("Employee", employees)

    filtered = df.copy()

    if date_filter:
        filtered = filtered[filtered["date"] == date_filter.strftime("%Y-%m-%d")]

    if emp != "All":
        filtered = filtered[filtered["employee"] == emp]

    st.subheader("Daily Entries")
    st.dataframe(filtered, use_container_width=True)

    # ---------------- THEMATIC SUMMARY SAFE ---------------- #

    st.subheader("Thematic Summary")

    temp = filtered.copy()

    temp["thematic_ids"] = (
        temp["thematic_ids"]
        .fillna("")
        .apply(lambda x:str(x))
        .str.replace(r"[^0-9|]","",regex=True)
    )

    temp = temp[temp["thematic_ids"] != ""]

    if temp.empty:
        st.info("No thematic data found.")
    else:
        temp = temp.assign(
            thematic_id=temp["thematic_ids"].str.split("|")
        ).explode("thematic_id")

        temp["thematic_id"] = pd.to_numeric(
            temp["thematic_id"], errors="coerce"
        )

        temp = temp.dropna(subset=["thematic_id"])
        temp["thematic_id"] = temp["thematic_id"].astype(int)

        id_map = {t["id"]: t["name"] for t in THEMATICS}

        summary = (
            temp.groupby("thematic_id")
            .size()
            .reset_index(name="activity_count")
            .sort_values("activity_count",ascending=False)
        )

        summary["thematic_name"] = summary["thematic_id"].map(id_map)

        st.dataframe(
            summary[["thematic_id","thematic_name","activity_count"]],
            use_container_width=True
        )

    # Download filtered data
    st.download_button(
        "Download CSV",
        data=filtered.to_csv(index=False).encode(),
        file_name="daily_thematic_log_filtered.csv",
        mime="text/csv"
    )
