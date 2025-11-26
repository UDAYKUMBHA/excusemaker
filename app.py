import streamlit as st
from openai import OpenAI
import os

# --- PAGE CONFIGURATION (Must be the first line) ---
st.set_page_config(
    page_title="ExecuseGen | AI Powered",
    page_icon="🕴️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (To remove 'Made with Streamlit' footer for a pro look) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stButton>button {
                width: 100%;
                background-color: #FF4B4B;
                color: white;
                font-weight: bold;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- SIDEBAR: CONFIG & DEVELOPER INFO ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    st.markdown("---")
    st.caption("👨‍💻 **Developer Mode**")
    
    # Feature: Download Source Code
    with open(__file__, "r") as f:
        source_code = f.read()
    st.download_button(
        label="📄 Download Source Code",
        data=source_code,
        file_name="app.py",
        mime="text/x-python",
        help="Review the clean code architecture."
    )
    
    st.info("Built with Python & GPT-4o.")

# --- MAIN INTERFACE ---
st.title("🕴️ Executive Excuse Generator")
st.markdown("""
<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
    <strong>The Problem:</strong> You have plans. You don't want to go.<br>
    <strong>The Solution:</strong> AI-crafted text messages optimized for social preservation.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    recipient = st.selectbox(
        "Who is the recipient?",
        ["My Boss", "My Partner", "My Mom/Dad", "A Friend", "A First Date"]
    )

with col2:
    vibe = st.select_slider(
        "Excuse Intensity",
        options=["Polite Refusal", "Standard Excuse", "Serious Emergency", "Total Chaos"]
    )

activity = st.text_input("What is the event?", placeholder="e.g., The quarterly budget meeting")

# --- LOGIC & GENERATION ---
if st.button("Generate Professional Excuse"):
    if not api_key:
        st.error("⚠️ API Key Missing. Please enter it in the sidebar.")
    elif not activity:
        st.warning("⚠️ Please specify the event you need to avoid.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            # Sophisticated Prompting
            system_prompt = f"""
            You are a social engineering expert. Draft a text message.
            TARGET: {recipient}
            EVENT: {activity}
            INTENSITY: {vibe}
            
            TONE GUIDE:
            - Polite Refusal: Professional, vague, firm.
            - Standard Excuse: Common ailments or scheduling conflicts.
            - Serious Emergency: Family crisis, car trouble, plumbing disaster.
            - Total Chaos: Wild, detailed, slightly unbelievable but hilarious.
            
            Do not include quotes. Just the raw text for the message.
            """

            with st.spinner('Consulting the excuse database...'):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_prompt}],
                    temperature=0.8
                )
                
                result = response.choices[0].message.content
                
                st.success("Draft Generated Successfully:")
                st.text_area("Copy this text:", value=result, height=100)
                st.balloons() # Fun visual effect for success
                
        except Exception as e:
            st.error(f"Connection Error: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 | Built for the Dynamic Project Interview</div>", unsafe_allow_html=True)