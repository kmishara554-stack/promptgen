import streamlit as st

# Page Config
st.set_page_config(page_title="Pro FB AI Designer", page_icon="🎨", layout="centered")

# Custom CSS - iPhone එකට ගැලපෙන ලස්සන UI එකක්
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

def main():
    st.title("🎯 Pro FB AI Prompt Maker")
    st.write("වෘත්තීය මට්ටමේ Facebook Post එකක් සඳහා අවශ්‍ය සියල්ල මෙතනින්.")

    # 1. Category Selection
    category = st.selectbox("මොන වගේ Post එකක්ද? (Category)", 
                            ["General", "Food & Restaurant", "Real Estate", "Tech & Gadgets", "Fashion & Beauty", "Education"])

    # 2. Basic Inputs
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Post එකේ ප්‍රධාන දේ", placeholder="උදා: Burger, New House")
        mood = st.selectbox("Mood", ["Luxury", "Energetic", "Cozy", "Professional", "Minimalist"])
    
    with col2:
        colors = st.text_input("වර්ණ (Colors)", placeholder="Gold, White, Black")
        aspect_ratio = st.selectbox("ප්‍රමාණය", ["1:1 (Square)", "4:5 (Portrait)", "16:9 (Landscape)"])

    # 3. Advanced Features
    with st.expander("🛠️ තව විස්තර එකතු කරන්න (Advanced)"):
        lighting = st.select_slider("Lighting", options=["Natural", "Studio", "Cinematic", "Neon", "Soft"])
        negative_prompt = st.text_area("අයින් කරන්න ඕනේ දේවල් (Negative Prompt)", 
                                       value="blurry, distorted, low resolution, ugly, messy text, extra fingers")

    # Prompt එක හදන Logic එක
    if st.button("Generate Pro Prompt 🚀"):
        if subject:
            # Category එක අනුව අමතර විස්තර එකතු කිරීම
            extra_details = {
                "Food & Restaurant": "high-end food photography, macro shot, steam, appetizing colors, depth of field",
                "Real Estate": "architectural photography, wide angle, bright interiors, blue sky background",
                "Fashion & Beauty": "high fashion editorial, professional model, sharp focus, magazine style",
                "Tech & Gadgets": "clean tech product shot, futuristic lighting, sleek surfaces",
                "General": ""
            }

            ar_val = aspect_ratio.split(" ")[0]
            
            final_prompt = (
                f"A professional {category} Facebook post design of {subject}. "
                f"Style: {mood}. Lighting: {lighting}. Colors: {colors if colors else 'natural'}. "
                f"{extra_details.get(category, '')}. High resolution, 8k, social media optimized. "
                f"--ar {ar_val}"
            )

            # Save to History
            st.session_state.history.append(final_prompt)

            # Display Result
            st.success("මෙන්න ඔයාගේ Prompt එක:")
            st.code(final_prompt)
            
            st.write("**Negative Prompt:**")
            st.info(negative_prompt)
        else:
            st.error("කරුණාකර මොකක් ගැනද කියලා ටයිප් කරන්න.")

    # History Section
    if st.session_state.history:
        st.divider()
        st.subheader("📜 කලින් හැදූ Prompt")
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Prompt {len(st.session_state.history)-i}"):
                st.code(item)

if __name__ == "__main__":
    main()
