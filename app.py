import streamlit as st
import google.generativeai as genai
import os
import json
import time

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-pro')

st.set_page_config(
    page_title="CIVICLAW — Legal Intelligence",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #070B14;
    --surface: #0D1320;
    --border: #1E293B;
    --blue: #4F8CFF;
    --cyan: #22D3EE;
    --green: #34D399;
    --red: #FB7185;
    --text: #F8FAFC;
    --secondary: #94A3B8;
    --muted: #64748B;
}

.stApp {
    background: radial-gradient(circle at 80% 10%, rgba(79,140,255,0.08), transparent 30%), #070B14;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0 25px 0;
}

.page-kicker { font-size: 11px; color: var(--cyan); letter-spacing: 2px; font-weight: 700; }
.page-title { font-family: 'Space Grotesk'; font-size: 36px; font-weight: 600; letter-spacing: -1.2px; margin-top: 5px; }
.page-description { color: var(--secondary); font-size: 14px; max-width: 650px; line-height: 1.6; }

.ai-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 13px;
    border: 1px solid rgba(52,211,153,0.2);
    background: rgba(52,211,153,0.06);
    border-radius: 999px;
    color: var(--green);
    font-size: 11px;
    font-weight: 600;
}

.status-dot { width: 7px; height: 7px; background: var(--green); border-radius: 50%; box-shadow: 0 0 10px rgba(52,211,153,0.7); }

.hero-card {
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(145deg, rgba(18,26,42,0.96), rgba(13,19,32,0.96));
    box-shadow: 0 20px 60px rgba(0,0,0,0.20);
    margin-bottom: 15px;
}

.hero-label { font-family: 'Space Grotesk'; font-size: 16px; font-weight: 600; }
.hero-helper { color: var(--secondary); font-size: 12px; margin-top: 4px; }

.stTextArea textarea {
    background: #090F1B !important;
    color: #F8FAFC !important;
    border: 1px solid #263247 !important;
    border-radius: 12px !important;
    font-family: 'Inter' !important;
    font-size: 14px !important;
}

.stButton > button, .stDownloadButton > button {
    width: 100%;
    border: none;
    border-radius: 11px;
    background: var(--blue);
    color: white;
    padding: 11px 20px;
    font-weight: 600;
    transition: all 180ms ease;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: #669BFF;
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(79,140,255,0.25);
}

.metric-card { background: rgba(13,19,32,0.9); border: 1px solid var(--border); border-radius: 15px; padding: 20px; }
.metric-label { color: var(--secondary); font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
.metric-value { font-family: 'Space Grotesk'; font-size: 26px; font-weight: 700; margin-top: 10px; }
.metric-description { color: var(--muted); font-size: 11px; margin-top: 3px; }

.section-header { display: flex; justify-content: space-between; align-items: center; margin-top: 32px; margin-bottom: 14px; }
.section-title { font-family: 'Space Grotesk'; font-size: 18px; font-weight: 600; }
.section-label { color: var(--muted); font-size: 10px; letter-spacing: 1.5px; }

.issue-card, .risk-card { background: #0D1320; border: 1px solid var(--border); border-radius: 14px; padding: 18px; margin-bottom: 10px; }
.issue-number { color: var(--blue); font-family: 'Space Grotesk'; font-weight: 700; font-size: 12px; }
.issue-title { font-family: 'Space Grotesk'; font-weight: 600; margin-top: 6px; }
.issue-description { color: var(--secondary); font-size: 12px; line-height: 1.5; margin-top: 6px; }

.action-card { display: flex; gap: 18px; background: #0D1320; border: 1px solid var(--border); border-radius: 14px; padding: 18px; margin-bottom: 10px; }
.action-number { min-width: 34px; height: 34px; border-radius: 50%; background: rgba(79,140,255,0.1); border: 1px solid rgba(79,140,255,0.3); display: flex; align-items: center; justify-content: center; color: var(--blue); font-family: 'Space Grotesk'; font-weight: 700; }
.action-title { font-family: 'Space Grotesk'; font-weight: 600; }
.action-desc { color: var(--secondary); font-size: 12px; margin-top: 5px; line-height: 1.5; }

.disclaimer { color: #475569; font-size: 10px; text-align: center; margin: 35px 0 10px; }
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

st.markdown("""
<div class="topbar">
<div>
    <div class="page-kicker">AUTONOMOUS LEGAL NAVIGATION</div>
    <div class="page-title">Navigate your legal situation.</div>
    <div class="page-description">
        Describe what happened. CIVICLAW identifies legal issues,
        maps relevant provisions, assesses risk, and builds your next tactical steps.
    </div>
</div>
<div class="ai-status">
    <div class="status-dot"></div>
    AI SYSTEM ONLINE
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
<div class="hero-label">📝 Tell CIVICLAW what happened</div>
<div class="hero-helper">Ceritakan kronologi kejadian secara bebas:</div>
</div>
""", unsafe_allow_html=True)

case_text = st.text_area(
    "",
    placeholder="Ceritakan kejadian hukum kamu di sini...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 3])

with col1:
    analyze = st.button("⚡ Analyze Situation →")

with col2:
    st.caption("Supported analysis: legal issues · provisions · risks · evidence · action plan")

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if analyze:
    if not api_key:
        st.error("API Key not found. Please set GEMINI_API_KEY environment variable or secret.")
    elif not case_text.strip():
        st.warning("Please describe your legal situation before proceeding.")
    else:
        try:
            progress_box = st.empty()
            steps = [
                ("Understanding situation", 20),
                ("Detecting legal issues", 40),
                ("Mapping relevant law", 60),
                ("Assessing legal risk", 80),
                ("Building action plan", 100)
            ]

            for step, progress in steps:
                progress_box.markdown(f"""
                <div class="hero-card" style="margin-top:20px;">
                    <div style="font-family:'Space Grotesk'; font-size:16px; font-weight:600;">
                        ◌ AI INVESTIGATION
                    </div>
                    <div style="color:#94A3B8; font-size:12px; margin-top:5px;">
                        {step}
                    </div>
                    <div style="height:6px; background:#1E293B; border-radius:99px; margin-top:16px; overflow:hidden;">
                        <div style="width:{progress}%; height:100%; background:#4F8CFF; transition:width 0.5s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.1)

            system_instruction = """
            You are CIVICLAW, an AI Legal Intelligence Agent. Analyze the user's legal situation and output valid JSON matching this schema:
            {
                "legal_domain": "String (e.g. Pidana / Perdata / Pertanahan)",
                "risk_level": "HIGH or MEDIUM or LOW",
                "confidence_score": "Percentage string (e.g. 95%)",
                "legal_issues": [
                    {"number": "01", "title": "Short Title", "description": "Detailed analysis text"}
                ],
                "legal_bases": ["Relevant statutory provision 1", "Provision 2"],
                "action_plan": [
                    {"number": "01", "title": "Action Step", "description": "Details of step"}
                ]
            }
            """
            
            prompt_full = f"{system_instruction}\n\nCase to analyze:\n{case_text}"
            
            response = model.generate_content(
                prompt_full,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2
                }
            )
            
            st.session_state.analysis_data = json.loads(response.text)
            st.session_state.analyzed = True
            progress_box.empty()

        except Exception as e:
            st.error(f"Analysis Failed: {str(e)}")

if st.session_state.analyzed and st.session_state.analysis_data:
    data = st.session_state.analysis_data

    report_text = f"=== CIVICLAW LEGAL INTELLIGENCE REPORT ===\n"
    report_text += f"Domain Hukum  : {data.get('legal_domain')}\n"
    report_text += f"Tingkat Risiko: {data.get('risk_level')}\n"
    report_text += f"Confidence    : {data.get('confidence_score')}\n\n"
    report_text += "--- IDENTIFIKASI ISU HUKUM ---\n"
    for issue in data.get("legal_issues", []):
        report_text += f"[{issue.get('number')}] {issue.get('title')}\n{issue.get('description')}\n\n"
    report_text += "--- DASAR HUKUM TERKAIT ---\n"
    for statute in data.get("legal_bases", []):
        report_text += f"- {statute}\n"
    report_text += "\n--- REKOMENDASI LANGKAH TAKTIS ---\n"
    for action in data.get("action_plan", []):
        report_text += f"[{action.get('number')}] {action.get('title')}\n{action.get('description')}\n\n"

    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-label">CASE INTELLIGENCE</div>
            <div class="section-title">Analysis complete</div>
        </div>
        <div class="ai-status">
            <div class="status-dot"></div>
            ANALYSIS READY
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    risk_color = "#FB7185" if data.get("risk_level") == "HIGH" else "#FBBF24" if data.get("risk_level") == "MEDIUM" else "#34D399"

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Legal Issues</div>
            <div class="metric-value">{len(data.get("legal_issues", [])):02d}</div>
            <div class="metric-description">potential issues detected</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Risk Level</div>
            <div class="metric-value" style="color:{risk_color};">{data.get("risk_level", "UNKNOWN")}</div>
            <div class="metric-description">requires attention</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Confidence</div>
            <div class="metric-value" style="color:#22D3EE;">{data.get("confidence_score", "90%")}</div>
            <div class="metric-description">analytical signal</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Actions</div>
            <div class="metric-value" style="color:#34D399;">{len(data.get("action_plan", [])):02d}</div>
            <div class="metric-description">recommended steps</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div>
            <div class="section-label">01 · ISSUE DETECTION</div>
            <div class="section-title">Legal issues identified</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for issue in data.get("legal_issues", []):
        st.markdown(f"""
        <div class="issue-card">
            <div class="issue-number">{issue.get('number', '01')}</div>
            <div class="issue-title">{issue.get('title', '')}</div>
            <div class="issue-description">{issue.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.5])

    with left:
        st.markdown("""
        <div class="section-header">
            <div>
                <div class="section-label">02 · RISK & STATUTORY BASIS</div>
                <div class="section-title">Legal context</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="risk-card">
            <div style="color:#94A3B8;font-size:11px;">DOMAIN & STATUTES</div>
            <div style="font-family:'Space Grotesk'; font-size:24px; font-weight:700; color:{risk_color}; margin-top:8px;">
                {data.get("legal_domain", "Legal Case")}
            </div>
            <div style="margin-top:15px; color:#F8FAFC; font-size:13px; font-weight:600;">Relevant Statutes:</div>
        """, unsafe_allow_html=True)
        
        for statute in data.get("legal_bases", []):
            st.info(f"⚖️ {statute}")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="section-header">
            <div>
                <div class="section-label">03 · TACTICAL WORKFLOW</div>
                <div class="section-title">Recommended action plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for action in data.get("action_plan", []):
            st.markdown(f"""
            <div class="action-card">
                <div class="action-number">{action.get('number', '01')}</div>
                <div>
                    <div class="action-title">{action.get('title', '')}</div>
                    <div class="action-desc">{action.get('description', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.download_button(
        label="📥 Download Laporan Analisis (.txt)",
        data=report_text,
        file_name="CivicLaw_Legal_Report.txt",
        mime="text/plain"
    )

    st.markdown("""
    <div class="disclaimer">
        CIVICLAW provides AI-assisted legal information and navigation,
        not legal representation or a substitute for qualified legal advice.
    </div>
    """, unsafe_allow_html=True)
