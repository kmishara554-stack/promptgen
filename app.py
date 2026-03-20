import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator

# Page Config
st.set_page_config(page_title="Ghee Family AI Designer", page_icon="🍲")

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def main():
    st.title("👨‍🍳 Pro AI Designer with Logo")
    st.write("ලෝගෝ එකත් එක්කම Facebook පෝස්ට් එක දැන්ම හදාගන්න.")

    # 1. Inputs
    user_input = st.text_input("පෝස්ට් එක ගැන කෙටියෙන්", placeholder="උදා: රසවත් බුරියානි එකක්...")
    
    # 2. Logo URL (මෙතනට ඔයාගේ ලෝගෝ එකේ ලින්ක් එක දෙන්න පුළුවන්)
    logo_url = st.text_input("Logo එකේ Link එක (Optional)", placeholder="https://your-logo-link.com/logo.png")

    col1, col2 = st.columns(2)
    with col1:
        template = st.selectbox("Style", ["Sri Lankan Food", "Business Promo", "Modern"])
        mood = st.selectbox("Mood", ["Vibrant", "Luxury", "Cinematic"])
    with col2:
        text_space = st.selectbox("අකුරු වලට ඉඩ", ["No Space", "Left Side", "Right Side", "Bottom"])
        ratio = st.radio("ප්‍රමාණය", ["1:1", "4:5", "16:9"], horizontal=True)

    if st.button("Generate & Add Logo 🚀", use_container_width=True):
        if user_input:
            with st.spinner('වැඩේ කෙරෙනවා...'):
                # 1. Translation & Prompt Building
                english_subject = translate_to_english(user_input)
                
                space_instruction = ""
                if "Left Side" in text_space: space_instruction = "leave empty space on left,"
                elif "Right Side" in text_space: space_instruction = "leave empty space on right,"
                elif "Bottom" in text_space: space_instruction = "leave empty space at bottom,"

                final_prompt = f"Professional photo of {english_subject}. {space_instruction} {template} style, {mood} lighting, 8k --ar {ratio}"

                # 2. Fetch AI Image
                encoded_prompt = requests.utils.quote(final_prompt)
                img_api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                response = requests.get(img_api_url)
                main_img = Image.open(BytesIO(response.content)).convert("RGBA")

                # 3. Logo Overlay Logic (ලෝගෝ එක තිබේ නම් පමණක්)
                if logo_url:
                    try:
                        logo_res = requests.get(logo_url)
                        logo_img = Image.open(BytesIO(logo_res.content)).convert("RGBA")
                        
                        # ලෝගෝ එකේ size එක adjust කිරීම (උදා: පින්තූරයෙන් 15% ක් විතර)
                        logo_img.thumbnail((200, 200)) 
                        
                        # දකුණු පැත්තේ යටට ලෝගෝ එක දැමීම
                        main_img.paste(logo_img, (main_img.width - logo_img.width - 20, main_img.height - logo_img.height - 20), logo_img)
                    except:
                        st.error("Logo එකේ link එකේ ප්‍රශ්නයක් තියෙනවා!")

                # 4. Show & Download
                st.divider()
                st.image(main_img, caption="Ghee Family Final Post", use_container_width=True)
                
                # Save image to bytes for download button
                buf = BytesIO()
                main_img.convert("RGB").save(buf, format="JPEG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="📥 Final පෝස්ට් එක Download කරන්න",
                    data=byte_im,
                    file_name="ghee_family_post.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
        else:
            st.warning("විස්තරයක් ඇතුළත් කරන්න.")

if __name__ == "__main__":
    main()
