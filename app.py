import streamlit as st
from google import genai
from google.genai import types
import os
import json
import time
import html


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CIVICLAW — Legal Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    os.environ.get("GEMINI_API_KEY", "")
)

if not api_key:
    st.error(
        "❌ GEMINI_API_KEY belum ditemukan. "
        "Tambahkan API key ke Streamlit Secrets."
    )
    st.stop()


# Gemini client
client = genai.Client(api_key=api_key)

# Stable Gemini model
MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# CUSTOM CSS
# ============================================================

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
    --yellow: #FBBF24;
    --text: #F8FAFC;
    --secondary: #94A3B8;
    --muted: #64748B;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(79,140,255,0.08),
            transparent 30%
        ),
        #070B14;

    color: var(--text);
    font-family: 'Inter', sans-serif;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}


/* TOP BAR */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0 25px 0;
}

.page-kicker {
    font-size: 11px;
    color: var(--cyan);
    letter-spacing: 2px;
    font-weight: 700;
}

.page-title {
    font-family: 'Space Grotesk';
    font-size: 36px;
    font-weight: 600;
    letter-spacing: -1.2px;
    margin-top: 5px;
}

.page-description {
    color: var(--secondary);
    font-size: 14px;
    max-width: 650px;
    line-height: 1.6;
}


/* AI STATUS */

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

.status-dot {
    width: 7px;
    height: 7px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(52,211,153,0.7);
}


/* HERO */

.hero-card {
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    background:
        linear-gradient(
            145deg,
            rgba(18,26,42,0.96),
            rgba(13,19,32,0.96)
        );
    box-shadow: 0 20px 60px rgba(0,0,0,0.20);
    margin-bottom: 15px;
}

.hero-label {
    font-family: 'Space Grotesk';
    font-size: 16px;
    font-weight: 600;
}

.hero-helper {
    color: var(--secondary);
    font-size: 12px;
    margin-top: 4px;
}


/* TEXT AREA */

.stTextArea textarea {
    background: #090F1B !important;
    color: #F8FAFC !important;
    border: 1px solid #263247 !important;
    border-radius: 12px !important;
    font-family: 'Inter' !important;
    font-size: 14px !important;
}


/* BUTTON */

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    border: none;
    border-radius: 11px;
    background: var(--blue);
    color: white;
    padding: 11px 20px;
    font-weight: 600;
    transition: all 180ms ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #669BFF;
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(79,140,255,0.25);
}


/* METRICS */

.metric-card {
    background: rgba(13,19,32,0.9);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 20px;
}

.metric-label {
    color: var(--secondary);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-family: 'Space Grotesk';
    font-size: 26px;
    font-weight: 700;
    margin-top: 10px;
}

.metric-description {
    color: var(--muted);
    font-size: 11px;
    margin-top: 3px;
}


/* SECTION */

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 32px;
    margin-bottom: 14px;
}

.section-title {
    font-family: 'Space Grotesk';
    font-size: 18px;
    font-weight: 600;
}

.section-label {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1.5px;
}


/* ISSUE */

.issue-card,
.risk-card {
    background: #0D1320;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
}

.issue-number {
    color: var(--blue);
    font-family: 'Space Grotesk';
    font-weight: 700;
    font-size: 12px;
}

.issue-title {
    font-family: 'Space Grotesk';
    font-weight: 600;
    margin-top: 6px;
}

.issue-description {
    color: var(--secondary);
    font-size: 12px;
    line-height: 1.5;
    margin-top: 6px;
}


/* ACTION */

.action-card {
    display: flex;
    gap: 18px;
    background: #0D1320;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
}

.action-number {
    min-width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(79,140,255,0.1);
    border: 1px solid rgba(79,140,255,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--blue);
    font-family: 'Space Grotesk';
    font-weight: 700;
}

.action-title {
    font-family: 'Space Grotesk';
    font-weight: 600;
}

.action-desc {
    color: var(--secondary);
    font-size: 12px;
    margin-top: 5px;
    line-height: 1.5;
}


/* DISCLAIMER */

.disclaimer {
    color: #475569;
    font-size: 10px;
    text-align: center;
    margin: 35px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="topbar">

    <div>
        <div class="page-kicker">
            AUTONOMOUS LEGAL NAVIGATION
        </div>

        <div class="page-title">
            Navigate your legal situation.
        </div>

        <div class="page-description">
            Describe what happened. CIVICLAW identifies legal issues,
            maps relevant provisions, assesses risk, and builds
            your next tactical steps.
        </div>
    </div>

    <div class="ai-status">
        <div class="status-dot"></div>
        AI SYSTEM ONLINE
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("""
<div class="hero-card">

    <div class="hero-label">
        📝 Tell CIVICLAW what happened
    </div>

    <div class="hero-helper">
        Ceritakan kronologi kejadian secara bebas:
    </div>

</div>
""", unsafe_allow_html=True)


case_text = st.text_area(
    "",
    placeholder="Ceritakan kejadian hukum kamu di sini...",
    label_visibility="collapsed",
    height=180
)


col1, col2 = st.columns([1, 3])


with col1:
    analyze = st.button(
        "⚡ Analyze Situation →",
        use_container_width=True
    )


with col2:
    st.caption(
        "Supported analysis: legal issues · provisions · "
        "risks · evidence · action plan"
    )


# ============================================================
# SESSION STATE
# ============================================================

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    if not api_key:
        st.error("❌ API Key tidak ditemukan.")

    elif not case_text.strip():
        st.warning(
            "⚠️ Please describe your legal situation before proceeding."
        )

    else:

        try:

            # ------------------------------------------------
            # PROGRESS
            # ------------------------------------------------

            progress_box = st.empty()

            steps = [
                ("Understanding situation", 20),
                ("Detecting legal issues", 40),
                ("Mapping relevant law", 60),
                ("Assessing legal risk", 80),
                ("Building action plan", 100)
            ]

            for step, progress in steps:

                progress_box.markdown(
                    f"""
                    <div class="hero-card" style="margin-top:20px;">

                        <div style="
                            font-family:'Space Grotesk';
                            font-size:16px;
                            font-weight:600;
                        ">
                            ◌ AI INVESTIGATION
                        </div>

                        <div style="
                            color:#94A3B8;
                            font-size:12px;
                            margin-top:5px;
                        ">
                            {step}
                        </div>

                        <div style="
                            height:6px;
                            background:#1E293B;
                            border-radius:99px;
                            margin-top:16px;
                            overflow:hidden;
                        ">

                            <div style="
                                width:{progress}%;
                                height:100%;
                                background:#4F8CFF;
                            "></div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(0.08)


            # ------------------------------------------------
            # SYSTEM INSTRUCTION
            # ------------------------------------------------

            system_instruction = """
You are CIVICLAW, an AI Legal Intelligence Agent.

Your task is to analyze a user's legal situation and provide
structured legal navigation information.

IMPORTANT:
- Do not claim to be a lawyer.
- Do not provide definitive legal representation.
- Clearly distinguish facts from assumptions.
- Do not invent laws or statutory provisions.
- If the jurisdiction is unclear, state that the legal basis
  should be verified.
- Give practical and safe next steps.
- Consider evidence that may be relevant.

Return ONLY valid JSON.

Use exactly this structure:

{
    "legal_domain": "String",
    "risk_level": "HIGH, MEDIUM, or LOW",
    "confidence_score": "Percentage string such as 85%",
    "legal_issues": [
        {
            "number": "01",
            "title": "Short title",
            "description": "Detailed explanation"
        }
    ],
    "legal_bases": [
        "Relevant legal provision or legal concept"
    ],
    "action_plan": [
        {
            "number": "01",
            "title": "Action step",
            "description": "Detailed explanation"
        }
    ]
}
"""


            # ------------------------------------------------
            # PROMPT
            # ------------------------------------------------

            prompt_full = f"""
{system_instruction}

USER CASE:

{case_text}
"""


            # ------------------------------------------------
            # GEMINI API CALL
            # ------------------------------------------------

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt_full,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                ),
            )


            # ------------------------------------------------
            # PROCESS RESPONSE
            # ------------------------------------------------

            raw_text = response.text.strip()

            # Remove markdown fences if Gemini returns them
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]

            if raw_text.startswith("```"):
                raw_text = raw_text[3:]

            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            raw_text = raw_text.strip()


            # Parse JSON
            analysis_data = json.loads(raw_text)


            # Save result
            st.session_state.analysis_data = analysis_data
            st.session_state.analyzed = True

            progress_box.empty()

            st.rerun()


        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except json.JSONDecodeError:
            progress_box.empty()

            st.error(
                "❌ Gemini memberikan response yang bukan JSON valid."
            )

            with st.expander("Technical response"):
                st.code(raw_text if "raw_text" in locals() else "No response")


        except Exception as e:
            progress_box.empty()

            error_message = str(e)

            st.error(
                "❌ Analysis Failed"
            )

            with st.expander("Technical error"):
                st.code(error_message)

            # Helpful diagnosis
            if "404" in error_message:

                st.warning(
                    f"""
                    Model `{MODEL_NAME}` tidak dapat diakses oleh API key
                    atau project ini. Pastikan Gemini API aktif dan
                    package `google-genai` sudah diperbarui.
                    """
                )

            elif "401" in error_message or "403" in error_message:

                st.warning(
                    """
                    API key tidak valid atau tidak memiliki akses
                    ke Gemini API.
                    """
                )

            elif "429" in error_message:

                st.warning(
                    """
                    Request terkena rate limit. Tunggu beberapa saat
                    lalu coba lagi.
                    """
                )


# ============================================================
# DISPLAY RESULT
# ============================================================

if (
    st.session_state.analyzed
    and st.session_state.analysis_data
):

    data = st.session_state.analysis_data


    # --------------------------------------------------------
    # SAFE DATA EXTRACTION
    # --------------------------------------------------------

    legal_domain = data.get(
        "legal_domain",
        "Unknown"
    )

    risk_level = data.get(
        "risk_level",
        "UNKNOWN"
    )

    confidence_score = data.get(
        "confidence_score",
        "N/A"
    )

    legal_issues = data.get(
        "legal_issues",
        []
    )

    legal_bases = data.get(
        "legal_bases",
        []
    )

    action_plan = data.get(
        "action_plan",
        []
    )


    # --------------------------------------------------------
    # RISK COLOR
    # --------------------------------------------------------

    if risk_level == "HIGH":
        risk_color = "#FB7185"

    elif risk_level == "MEDIUM":
        risk_color = "#FBBF24"

    else:
        risk_color = "#34D399"


    # --------------------------------------------------------
    # REPORT TEXT
    # --------------------------------------------------------

    report_text = (
        "=== CIVICLAW LEGAL INTELLIGENCE REPORT ===\n\n"
    )

    report_text += (
        f"Domain Hukum  : {legal_domain}\n"
    )

    report_text += (
        f"Tingkat Risiko: {risk_level}\n"
    )

    report_text += (
        f"Confidence    : {confidence_score}\n\n"
    )


    report_text += (
        "--- IDENTIFIKASI ISU HUKUM ---\n"
    )

    for issue in legal_issues:

        report_text += (
            f"[{issue.get('number', '')}] "
            f"{issue.get('title', '')}\n"
        )

        report_text += (
            f"{issue.get('description', '')}\n\n"
        )


    report_text += (
        "--- DASAR HUKUM TERKAIT ---\n"
    )

    for statute in legal_bases:

        report_text += (
            f"- {statute}\n"
        )


    report_text += (
        "\n--- REKOMENDASI LANGKAH TAKTIS ---\n"
    )

    for action in action_plan:

        report_text += (
            f"[{action.get('number', '')}] "
            f"{action.get('title', '')}\n"
        )

        report_text += (
            f"{action.get('description', '')}\n\n"
        )


    # --------------------------------------------------------
    # ANALYSIS COMPLETE
    # --------------------------------------------------------

    st.markdown("""
    <div class="section-header">

        <div>

            <div class="section-label">
                CASE INTELLIGENCE
            </div>

            <div class="section-title">
                Analysis complete
            </div>

        </div>

        <div class="ai-status">

            <div class="status-dot"></div>

            ANALYSIS READY

        </div>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Legal Issues
                </div>

                <div class="metric-value">
                    {len(legal_issues):02d}
                </div>

                <div class="metric-description">
                    potential issues detected
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Risk Level
                </div>

                <div class="metric-value"
                     style="color:{risk_color};">

                    {html.escape(str(risk_level))}

                </div>

                <div class="metric-description">
                    requires attention
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Confidence
                </div>

                <div class="metric-value"
                     style="color:#22D3EE;">

                    {html.escape(str(confidence_score))}

                </div>

                <div class="metric-description">
                    analytical signal
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Actions
                </div>

                <div class="metric-value"
                     style="color:#34D399;">

                    {len(action_plan):02d}

                </div>

                <div class="metric-description">
                    recommended steps
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # ISSUE DETECTION
    # ========================================================

    st.markdown("""
    <div class="section-header">

        <div>

            <div class="section-label">
                01 · ISSUE DETECTION
            </div>

            <div class="section-title">
                Legal issues identified
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    for issue in legal_issues:

        issue_number = html.escape(
            str(issue.get("number", "01"))
        )

        issue_title = html.escape(
            str(issue.get("title", ""))
        )

        issue_description = html.escape(
            str(issue.get("description", ""))
        )


        st.markdown(
            f"""
            <div class="issue-card">

                <div class="issue-number">
                    {issue_number}
                </div>

                <div class="issue-title">
                    {issue_title}
                </div>

                <div class="issue-description">
                    {issue_description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # LEGAL CONTEXT + ACTION PLAN
    # ========================================================

    left, right = st.columns([1, 1.5])


    # --------------------------------------------------------
    # LEFT: LEGAL CONTEXT
    # --------------------------------------------------------

    with left:

        st.markdown("""
        <div class="section-header">

            <div>

                <div class="section-label">
                    02 · RISK & STATUTORY BASIS
                </div>

                <div class="section-title">
                    Legal context
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)


        st.markdown(
            f"""
            <div class="risk-card">

                <div style="
                    color:#94A3B8;
                    font-size:11px;
                ">
                    DOMAIN & STATUTES
                </div>

                <div style="
                    font-family:'Space Grotesk';
                    font-size:24px;
                    font-weight:700;
                    color:{risk_color};
                    margin-top:8px;
                ">
                    {html.escape(str(legal_domain))}
                </div>

                <div style="
                    margin-top:15px;
                    color:#F8FAFC;
                    font-size:13px;
                    font-weight:600;
                ">
                    Relevant Statutes:
                </div>

            """,
            unsafe_allow_html=True
        )


        for statute in legal_bases:

            st.info(
                f"⚖️ {statute}"
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # RIGHT: ACTION PLAN
    # --------------------------------------------------------

    with right:

        st.markdown("""
        <div class="section-header">

            <div>

                <div class="section-label">
                    03 · TACTICAL WORKFLOW
                </div>

                <div class="section-title">
                    Recommended action plan
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)


        for action in action_plan:

            action_number = html.escape(
                str(action.get("number", "01"))
            )

            action_title = html.escape(
                str(action.get("title", ""))
            )

            action_desc = html.escape(
                str(action.get("description", ""))
            )


            st.markdown(
                f"""
                <div class="action-card">

                    <div class="action-number">
                        {action_number}
                    </div>

                    <div>

                        <div class="action-title">
                            {action_title}
                        </div>

                        <div class="action-desc">
                            {action_desc}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.markdown("---")


    st.download_button(
        label="📥 Download Laporan Analisis (.txt)",
        data=report_text,
        file_name="CivicLaw_Legal_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.markdown("""
    <div class="disclaimer">

        CIVICLAW provides AI-assisted legal information
        and navigation, not legal representation or a
        substitute for qualified legal advice.

    </div>
    """, unsafe_allow_html=True)
