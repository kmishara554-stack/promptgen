import streamlit as st
import requests
from deep_translator import GoogleTranslator

# Page Config
st.set_page_config(page_title="Ghee Family AI Designer", page_icon="🍲")

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def main():
    st.title("👨‍ූ Ghee Family AI Designer")
    st.write("දැන් අකුරු ලියන්න ඉඩ තියලා ලස්සන පෝස්ට් හදාගන්න.")

    # 1. Subject Input
    user_input = st.text_input("පෝස්ට් එක මොකක් ගැනද?", placeholder="උදා: රසවත් බුරියානි එකක්...")

    # 2. Template & Mood
    col1, col2 = st.columns(2)
    with col1:
        template = st.selectbox("Style එක තෝරන්න", ["Sri Lankan Food", "Business Promo", "Normal"])
    with col2:
        mood = st.selectbox("ස්වභාවය (Mood)", ["Vibrant", "Luxury", "Cinematic"])

    # --- අලුත් කොටස: TEXT PLACEMENT ---
    st.subheader("🛠️ Layout Settings")
    text_space = st.selectbox("අකුරු ලියන්න ඉඩ තියන්න ඕනේ කොහෙන්ද?", [
        "No Space (Full Image)", 
        "Left Side (වම් පැත්තෙන් ඉඩ තබන්න)", 
        "Right Side (දකුණු පැත්තෙන් ඉඩ තබන්න)", 
        "Bottom (යටින් ඉඩ තබන්න)"
    ])

    ratio = st.radio("ප්‍රමාණය", ["1:1", "4:5", "16:9"], horizontal=True)

    if st.button("Generate Post 🚀", use_container_width=True):
        if user_input:
            with st.spinner('වැඩේ කෙරෙනවා...'):
                english_subject = translate_to_english(user_input)
                
                # Text Space එක අනුව prompt එකට එකතු වන කොටස
                space_instruction = ""
                if "Left Side" in text_space:
                    space_instruction = "leave significant empty negative space on the left side for text overlay, subject positioned on the right,"
                elif "Right Side" in text_space:
                    space_instruction = "leave significant empty negative space on the right side for text overlay, subject positioned on the left,"
                elif "Bottom" in text_space:
                    space_instruction = "leave empty space at the bottom of the image for marketing text,"

                final_prompt = (
                    f"A professional photo of {english_subject}. {space_instruction} "
                    f"{template} style, {mood} lighting, high resolution, 8k, photorealistic --ar {ratio}"
                )

                # Image Generation
                encoded_prompt = requests.utils.quote(final_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

                st.divider()
                st.image(image_url, caption="Ghee Family Restaurant Post Preview", use_container_width=True)
                st.code(f"AI Prompt: {final_prompt}")
                st.markdown(f"[📥 පින්තූරය මෙතනින් Save කරගන්න]({image_url})")
        else:
            st.warning("කරුණාකර විස්තරයක් ඇතුළත් කරන්න.")

if __name__ == "__main__":
    main()
