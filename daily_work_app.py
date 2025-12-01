import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "daily_thematic_log.csv"

# ---------------- THEMATIC DEFINITIONS ---------------- #

THEMATICS = [
    {
        "id": 1,
        "name": "AI-Driven Multilingual Content Localization & Accessible Digital Outreach through Integrated Multichannel Platforms",
        "keywords": [
            "vms", "dissemination", "whatsapp", "what app", "promo", "promotional",
            "campaign", "osf", "outreach", "content", "mustard", "paddy", "livestock",
            "csv create", "csv creation", "download call log", "call log", "calllog",
            "wli csv", "voice message", "bulk message", "broadcast", "youtube live",
            "fb live", "facebook live"
        ],
    },
    {
        "id": 2,
        "name": "AI-Based Crop Health Detection App and WhatsApp Bot",
        "keywords": [
            "crop health detection", "crop-health", "leaf disease", "pest detection",
            "whatsapp bot", "whatsapp chatbot", "chatbot", "ai bot", "crop doctor"
        ],
    },
    {
        "id": 3,
        "name": "Tele-Consultation Platform Enhancements – AI-integrated, multilingual, voice-enabled helpline and advisory services",
        "keywords": [
            "helpline", "ivr", "ivrs", "call centre", "call center",
            "tele consultation", "tele-consultation", "phone advisory",
            "inbound calls", "outbound calls", "voicebot"
        ],
    },
    {
        "id": 4,
        "name": "Development of Animal Digital Information System",
        "keywords": [
            "animal digital information system", "adis", "animal info", "livestock database"
        ],
    },
    {
        "id": 5,
        "name": "FPO Management App – Development and Refinement",
        "keywords": [
            "fpo management", "fpo app", "producer organisation", "producer organization"
        ],
    },
    {
        "id": 6,
        "name": "24/7 Weather-Based Marine Fisheries Advisories (Machli App)",
        "keywords": [
            "machli", "marine fisheries", "boat advisory", "fisheries advisory",
            "sea condition", "wave height", "fisher app"
        ],
    },
    {
        "id": 7,
        "name": "Domain-Specific Data Management Tools (Web Scraping + GIS/ML)",
        "keywords": [
            "web scraping", "scraping", "crawler", "api data pull",
            "gis/ml", "data pipeline", "data collection script"
        ],
    },
    {
        "id": 8,
        "name": "Livelihood Advisory Podcasts via Internet Radio",
        "keywords": [
            "internet radio", "podcast", "audio upload", "radio script",
            "livelihood advisory podcast", "radio content"
        ],
    },
    {
        "id": 9,
        "name": "RF Livelihood Video Learning App",
        "keywords": [
            "video learning app", "livelihood video app", "youtube video",
            "youtube live", "video shoot", "video editing", "create video",
            "support video"
        ],
    },
    {
        "id": 10,
        "name": "Rural Yellow Pages App – Development & Scale",
        "keywords": [
            "rural yellow pages", "yellow pages app", "service directory",
            "rural directory"
        ],
    },
    {
        "id": 11,
        "name": "Digital Farm Management System (DFMS) – Predictive and Mobile-Based Advisory",
        "keywords": [
            "dfms", "digital farm management", "farm management app",
            "plot advisory", "farm advisory app"
        ],
    },
    {
        "id": 12,
        "name": "RF Super App – Scaling for Integrated Service Delivery",
        "keywords": [
            "rf super app", "super app", "integrated service app"
        ],
    },
    {
        "id": 13,
        "name": "E-Learning & Knowledge Dissemination",
        "keywords": [
            "training", "orientation", "capacity building", "session",
            "workshop", "webinar", "demo", "knowledge sharing",
            "dashboard training", "power bi training", "team training",
            "meeting for training"
        ],
    },
    {
        "id": 14,
        "name": "Cloud Migration & Infrastructure Enhancements",
        "keywords": [
            "cloud migration", "azure", "aws", "gcp", "server migration",
            "infrastructure", "vm migration"
        ],
    },
    {
        "id": 15,
        "name": "Early Warning Systems & Disaster Resilience",
        "keywords": [
            "early warning", "disaster", "resilience", "alert system",
            "flood alert", "cyclone alert"
        ],
    },
    {
        "id": 16,
        "name": "Tech for Social Good & Knowledge Empowerment (toolkits, mobile apps, literacy, walkthroughs, etc.)",
        "keywords": [
            "toolkit", "digital literacy", "app walkthrough", "how to use app",
            "testing new app", "scan application", "pilot testing", "usability testing"
        ],
    },
    {
        "id": 17,
        "name": "Data-Driven Impact: Measuring Success in RF’s Tech-based Outreach",
        "keywords": [
            "analysis", "analytics", "impact", "dashboard", "reporting",
            "kpi", "metric", "power bi report", "data analysis", "weekly report",
            "monthly report", "quarterly report"
        ],
    },
    {
        "id": 18,
        "name": "Web-Based Knowledge Management System (WebKMS) + Multilingual AI Integration",
        "keywords": [
            "webkms", "web kms", "kms", "csdms", "knowledge management system",
            "upload in kms", "validate", "verify", "approve", "webkms portal"
        ],
    },
    {
        "id": 19,
        "name": "Geo-Spatial Vulnerability Mapping for Inclusive Development",
        "keywords": [
            "vulnerability mapping", "inclusive development map", "risk mapping"
        ],
    },
    {
        "id": 20,
        "name": "Monitoring & Mapping Water Harvesting Structures",
        "keywords": [
            "water harvesting", "check dam", "farm pond", "water structure mapping"
        ],
    },
    {
        "id": 21,
        "name": "NDVI-Based Crop Yield Computation",
        "keywords": [
            "ndvi", "yield computation", "vegetation index"
        ],
    },
    {
        "id": 22,
        "name": "Multi-Hazard Risk Mapping & Early Warning Systems",
        "keywords": [
            "multi-hazard", "risk map", "hazard map"
        ],
    },
    {
        "id": 23,
        "name": "Above Ground Biomass (AGB) Estimation",
        "keywords": [
            "agb", "biomass estimation", "above ground biomass"
        ],
    },
    {
        "id": 24,
        "name": "Change Detection & Environmental Monitoring",
        "keywords": [
            "change detection", "environmental monitoring", "land use change"
        ],
    },
    {
        "id": 25,
        "name": "Climate-Responsive Modelling & Forecasting",
        "keywords": [
            "climate model", "forecasting", "climate responsive", "weather model"
        ],
    },
    {
        "id": 26,
        "name": "Tech-Enabled Monitoring & Evaluation using Mobile-Based GIS",
        "keywords": [
            "mobile gis", "monitoring & evaluation", "m&e app", "survey app",
            "field monitoring", "gis survey"
        ],
    },
    {
        "id": 27,
        "name": "Spatial Decision Support & Risk Intelligence (WebKMS + GIS/RS)",
        "keywords": [
            "spatial decision support", "risk intelligence", "gis/rs", "geo portal"
        ],
    },
    {
        "id": 28,
        "name": "IT Documentation, Digital Infrastructure Support & Other Support",
        "keywords": [
            "documentation", "sop", "note", "minutes", "mom", "troubleshoot",
            "issue", "bug", "excel help", "vba code", "it support",
            "system support", "installation", "configuration"
        ],
    },
]


# ---------------- HELPER FUNCTIONS ---------------- #

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
                "activity_text",
                "thematic_ids",
                "thematic_names",
            ]
        )


def detect_thematics_for_text(text: str):
    text_l = text.lower()
    matched = []
    for th in THEMATICS:
        for kw in th["keywords"]:
            if kw in text_l:
                matched.append(th)
                break  # stop after first keyword match for that thematic
    # if nothing matched, put under thematic 28 (Other support)
    if not matched:
        matched = [t for t in THEMATICS if t["id"] == 28]
    return matched


def save_activities(employee_name, department, date, activities):
    """
    activities: list of dict with 'text', 'thematic_ids', 'thematic_names'
    """
    df = load_data()
    rows = []
    for act in activities:
        rows.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date": date.strftime("%Y-%m-%d"),
                "employee_name": employee_name,
                "department": department,
                "activity_text": act["text"],
                "thematic_ids": "|".join(str(i) for i in act["thematic_ids"]),
                "thematic_names": "|".join(act["thematic_names"]),
            }
        )
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# ---------------- ROLE FROM URL ---------------- #

params = st.query_params
role = params.get("role", ["user"])
role = role[0] if isinstance(role, list) else role

# ---------------- USER VIEW ---------------- #

if role != "admin":
    st.title("Daily Work – Thematic Logger")

    employee_name = st.text_input("Your Name *", value="Somnath Pati")
    department = st.text_input("Department *", value="Information Services")
    date = st.date_input("Work Date *", datetime.today())

    st.markdown("### Enter today’s work (one activity per line)")
    example_text = (
        "Download Call log, WhatsApp csv create-6 & disseminate promotional msg-6, "
        "OSF VMS Dissemination, Mustard, paddy, livestock content dissemination\n"
        "CSDMS WebKMS validate & verify 6 contents\n"
        "Organized Power BI dashboard creation training for RT team\n"
    )
    work_text = st.text_area(
        "Work details *",
        height=220,
        placeholder=example_text,
    )

    if st.button("Detect Thematics & Save"):
        if not employee_name.strip() or not department.strip() or not work_text.strip():
            st.error("Please fill name, department and work details.")
        else:
            lines = [l.strip() for l in work_text.split("\n") if l.strip()]
            activities = []
            preview_rows = []

            for line in lines:
                matched = detect_thematics_for_text(line)
                ids = [m["id"] for m in matched]
                names = [m["name"] for m in matched]
                activities.append(
                    {"text": line, "thematic_ids": ids, "thematic_names": names}
                )
                preview_rows.append(
                    {
                        "Activity": line,
                        "Detected Thematics": "; ".join(
                            f"{m['id']}. {m['name']}" for m in matched
                        ),
                    }
                )

            # Save to CSV
            save_activities(employee_name, department, date, activities)

            st.success("✅ Activities saved with thematic mapping.")
            st.markdown("#### Preview of thematic classification")
            st.dataframe(pd.DataFrame(preview_rows), use_container_width=True)

    st.info(
        "Tip: This file `daily_thematic_log.csv` can be used by your weekly-report app\n"
        "to calculate thematic-wise work for the AOP dashboard."
    )

# ---------------- ADMIN VIEW ---------------- #

else:
    st.title("Daily Work – Thematic Log (Admin View)")

    df = load_data()
    if df.empty:
        st.warning("No data saved yet.")
    else:
        # Filters
        with st.expander("Filters"):
            date_filter = st.date_input(
                "Filter by date (optional)", value=None
            )
            name_options = ["All"] + sorted(
                df["employee_name"].dropna().unique().tolist()
            )
            name_filter = st.selectbox("Filter by employee", name_options)

        filtered = df.copy()
        if date_filter:
            filtered = filtered[filtered["date"] == date_filter.strftime("%Y-%m-%d")]
        if name_filter != "All":
            filtered = filtered[filtered["employee_name"] == name_filter]

        st.subheader("Saved Activities")
        st.dataframe(filtered, use_container_width=True)

        # Thematic summary
        st.subheader("Summary: Number of activities per thematic")
        # explode thematic_ids into rows
        temp = filtered.copy()
        temp["thematic_ids"] = temp["thematic_ids"].fillna("")
        temp = temp[temp["thematic_ids"] != ""]
        temp = temp.assign(thematic_id=temp["thematic_ids"].str.split("|")).explode(
            "thematic_id"
        )
        temp["thematic_id"] = temp["thematic_id"].astype(int)

        if not temp.empty:
            # map id -> name
            id_to_name = {t["id"]: t["name"] for t in THEMATICS}
            summary = (
                temp.groupby("thematic_id")
                .size()
                .reset_index(name="activity_count")
                .sort_values("activity_count", ascending=False)
            )
            summary["thematic_name"] = summary["thematic_id"].map(id_to_name)
            summary = summary[["thematic_id", "thematic_name", "activity_count"]]
            st.dataframe(summary, use_container_width=True)
        else:
            st.info("No thematic data found for the current filter.")

        # Download
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download filtered data as CSV",
            data=csv_bytes,
            file_name="daily_thematic_log_filtered.csv",
            mime="text/csv",
        )
