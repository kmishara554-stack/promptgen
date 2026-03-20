import streamlit as st

# iPhone එකට ගැලපෙන විදිහට Page එක සැකසීම
st.set_page_config(page_title="AI Prompt Gen", page_icon="🎨")

# කලින් හදපු Prompt මතක තබා ගැනීමට (History)
if 'prompt_history' not in st.session_state:
    st.session_state['prompt_history'] = []

def main():
    st.title("🚀 AI Prompt Generator")
    st.write("ඔයාගේ Facebook Post එකට අවශ්‍ය AI Prompt එක මෙතනින් හදාගන්න.")

    # විස්තර ඇතුළත් කරන තැන්
    subject = st.text_input("Post එක මොකක් ගැනද? (Subject)", placeholder="උදා: Coffee Shop, Gaming PC Sale")
    
    style = st.selectbox("නිර්මාණ විලාසය (Style)", [
        "Modern Minimalist", "3D Isometric", "Cyberpunk", 
        "Vintage Retro", "Professional Corporate", "Photorealistic"
    ])

    colors = st.text_input("වර්ණ (Colors)", placeholder="උදා: Blue and White, Gold and Black")
    
    mood = st.selectbox("ස්වභාවය (Mood)", [
        "Energetic", "Calm & Relaxing", "Luxury", "Urgent (Sales)", "Friendly"
    ])

    aspect_ratio = st.radio("ප්‍රමාණය (Aspect Ratio)", ["1:1", "4:5", "16:9"], horizontal=True)

    # Prompt එක Generate කරන Button එක
    if st.button("Generate Prompt ✨", use_container_width=True):
        if subject:
            final_prompt = (
                f"A high-end Facebook post design featuring {subject}. "
                f"Style: {style}. Colors: {colors if colors else 'balanced'}. "
                f"Mood: {mood}. Optimized for social media, 8k, professional lighting. "
                f"--ar {aspect_ratio}"
            )
            
            # History එකට එකතු කිරීම
            st.session_state['prompt_history'].append(final_prompt)
            
            st.divider()
            st.subheader("ඔයාගේ AI Prompt එක:")
            st.code(final_prompt, language="text")

            # Download Button එක
            st.download_button(
                label="මෙම Prompt එක Download කරන්න",
                data=final_prompt,
                file_name="ai_prompt.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.error("කරුණාකර Subject එක ඇතුළත් කරන්න!")

    # කලින් හදපු Prompt බලන්න (History)
    if st.session_state['prompt_history']:
        with st.expander("📜 පරණ Prompt බලන්න (History)"):
            for i, old_prompt in enumerate(reversed(st.session_state['prompt_history'])):
                st.code(old_prompt)

if __name__ == "__main__":
    main()