import asyncio
import os
import tempfile
import edge_tts
import streamlit as st

st.set_page_config(
    page_title="Mobile TTS Studio", page_icon="🎙️", layout="centered"
)

VOICES = {
    "🇺🇸 English (US) - Ava (Neural) [Warm/Popular]": "en-US-AvaNeural",
    "🇺🇸 English (US) - Andrew (Neural) [Professional/Deep]": (
        "en-US-AndrewNeural"
    ),
    "🇺🇸 English (US) - Jenny (Neural) [Friendly/Clear]": "en-US-JennyNeural",
    "🇬🇧 English (UK) - Sonia (Neural) [British Accent]": "en-GB-SoniaNeural",
    "🇮🇳 English (India) - Neha (Neural) [Clear Indian English]": (
        "en-IN-NehaNeural"
    ),
    "🇮🇳 Hindi (India) - Swara (Neural) [Natural Hindi]": "hi-IN-SwaraNeural",
}


async def generate_speech(
    text, voice_key, rate_offset, pitch_offset, volume_offset
):
    if not text.strip():
        return None
    voice_id = VOICES.get(voice_key, "en-US-AvaNeural")
    rate_str = f"{rate_offset:+d}%" if rate_offset != 0 else "+0%"
    pitch_str = f"{pitch_offset:+d}Hz" if pitch_offset != 0 else "+0Hz"
    volume_str = f"{volume_offset:+d}%" if volume_offset != 0 else "+0%"

    fd, output_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        communicate = edge_tts.Communicate(
            text,
            voice_id,
            rate=rate_str,
            pitch=pitch_str,
            volume=volume_str,
        )
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None


st.title("🎙️ Mobile YouTube Voice Studio")
st.write(
    "Generate natural Microsoft neural voiceovers instantly on your phone."
)

text_input = st.text_area(
    "Script Input", placeholder="Type or paste your video script paragraph here..."
)
voice_choice = st.selectbox("Select Voice", list(VOICES.keys()))

with st.expander("Advanced Voice Controls (Speed / Pitch / Volume)"):
    rate = st.slider("Speed Rate (%)", -50, 50, 0, 5)
    pitch = st.slider("Pitch (Hz)", -20, 20, 0, 1)
    volume = st.slider("Volume (%)", -50, 50, 0, 5)

    if st.button("🚀 Generate Voiceover", type="primary"):
        if text_input:
            with st.spinner("Synthesizing audio..."):
                audio_file = asyncio.run(
                    generate_speech(
                        text_input, voice_choice, rate, pitch, volume
                    )
                )
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
                with open(audio_file, "rb") as f:
                    st.download_button(
                        "📥 Download MP3 File",
                        f,
                        file_name="voiceover.mp3",
                        mime="audio/mp3",
                    )
        else:
            st.warning("Please enter some text first.")
                                                                                                                                                                                                                                                                                                                                                                                            