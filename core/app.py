import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from pipeline import process_notes, process_handwritten_notes


st.set_page_config(
    page_title="AI Notes Analyzer",
    page_icon="📘",
    layout="centered"
)


st.markdown(
    """
    <style>
    .stApp {
        background: #0b1120;
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #334155;
    }

    h1, h2, h3, p, label, span {
        color: #f8fafc;
    }

    .app-shell {
        max-width: 860px;
        margin: 0 auto;
        padding-top: 2.5rem;
    }

    .title {
        font-size: 2.7rem;
        line-height: 1.1;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.7rem;
    }

    .subtitle {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #cbd5e1;
        margin-bottom: 2rem;
    }

    .upload-panel {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
    }

    .uploaded {
        margin-top: 0.8rem;
        background: #172554;
        border: 1px solid #334155;
        color: #f8fafc;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        font-weight: 600;
    }

    .report {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1.2rem;
        color: #f8fafc;
    }

    div.stButton > button {
        width: 100%;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 700;
    }

    div.stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 700;
    }

    div[data-testid="stFileUploader"] section {
        background: transparent;
        border: 1px dashed #334155;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("Preferences")

    handwritten_mode = st.toggle(
        "Handwritten notes",
        help="Turn this on for photos of handwritten notes."
    )


st.markdown('<div class="app-shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="title">AI Notes Analyzer</div>
    <div class="subtitle">
        Upload notes and get a clean study report with explanations, definitions,
        questions, flashcards, and a revision plan.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="upload-panel">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a PDF or image",
    type=["pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    st.markdown(
        f'<div class="uploaded">Selected file: {uploaded_file.name}</div>',
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    suffix = Path(uploaded_file.name).suffix.lower()

    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    if handwritten_mode and suffix == ".pdf":
        st.warning("Handwritten mode works best with image files like JPG or PNG.")

    if st.button("Analyze Notes"):
        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Reading notes...")
            progress.progress(20)

            status.info("Extracting content...")
            progress.progress(45)

            status.info("Preparing study report...")
            progress.progress(75)

            if handwritten_mode and suffix != ".pdf":
                result = process_handwritten_notes(temp_file_path)
            else:
                result = process_notes(temp_file_path)

            progress.progress(100)
            status.success("Study report ready.")

            final_ai_analysis = result["final_ai_analysis"]

            st.markdown("### Study Report")

            if final_ai_analysis["status"] == "success":
                st.markdown(
                    f'<div class="report">{final_ai_analysis["final_analysis"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning(final_ai_analysis.get("message", "Analysis failed."))

                if "error" in final_ai_analysis:
                    st.code(final_ai_analysis["error"])

            st.download_button(
                label="Download Study Report",
                data=json.dumps(result["final_ai_analysis"], indent=2),
                file_name="study_report.json",
                mime="application/json"
            )

        except Exception as error:
            progress.empty()
            status.error("Something went wrong while analyzing the notes.")
            st.code(str(error))

else:
    st.info("Upload a file to begin.")

st.markdown("</div>", unsafe_allow_html=True)