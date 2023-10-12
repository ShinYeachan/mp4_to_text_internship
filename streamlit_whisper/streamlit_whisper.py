import subprocess
import streamlit as st
import whisper
import os
from docx import Document

# ------------------------ Constants ------------------------
MODEL_CHOICES = ["small", "base", "medium", "large"]


# ------------------------ Utility Functions ------------------------


def create_vtt_file(transcription_text, original_file_name):
    """Create a VTT file from the transcription."""
    base_name, _ = os.path.splitext(original_file_name)
    file_name = f"{base_name}_transcription.vtt"
    formatted_text = format_text(transcription_text, 80)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("WEBVTT\n\n")
        file.write(formatted_text)

    return file_name


def create_docx_file(transcription_text, original_file_name):
    """Create a DOCX file from the transcription."""
    base_name, _ = os.path.splitext(original_file_name)
    file_name = f"{base_name}_transcription.docx"
    formatted_text = format_text(transcription_text, 80)

    doc = Document()
    for line in formatted_text.split('\r\n'):
        doc.add_paragraph(line)
    doc.save(file_name)

    return file_name


def save_uploaded_file(uploaded_file):
    """Save the uploaded file to disk and return its path."""
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.abspath(uploaded_file.name)


def format_text(text, max_line_length):
    """Break the text into lines of specified length."""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_line_length:
            lines.append(' '.join(current_line))
            current_length = 0
            current_line = []
        current_line.append(word)
        current_length += len(word) + 1

    if current_line:  # Append any remaining words
        lines.append(' '.join(current_line))

    return '\r\n'.join(lines)  # Use '\r\n' for new lines


# ------------------------ Audio & Video Processing Functions ------------------------
def convert_video_to_mp3(input_file, output_file):
    """Convert a video file to MP3 audio."""
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        '-q:a', '0',
        '-map', 'a',
        output_file
    ]
    subprocess.run(ffmpeg_cmd)


def transcribe_audio(audio_path, model_choice):
    """Transcribe an audio using the specified Whisper model."""
    model = whisper.load_model(model_choice)
    return model.transcribe(audio_path)


def create_text_file(transcription_text, original_file_name):
    """Create a text file from the formatted transcription."""
    base_name, _ = os.path.splitext(original_file_name)
    file_name = f"{base_name}_transcription.txt"
    formatted_text = format_text(transcription_text, 80)

    with open(file_name, 'w') as file:
        file.write(formatted_text)

    return file_name


# ------------------------ Main Streamlit App ------------------------
def main():
    st.title("Whisper App")

    # Initialize session state variables if they don't exist
    if 'transcription_text' not in st.session_state:
        st.session_state.transcription_text = ""
    if 'download_file_name' not in st.session_state:
        st.session_state.download_file_name = ""

    # Upload handlers
    video_file = st.file_uploader("Upload Video (MP4)", type=["mp4"])
    audio_file = st.file_uploader("Upload Audio (if no video provided)", type=["wav", "mp3", "m4a"])

    # Model selection
    model_choice = st.sidebar.selectbox("Select Whisper Model", MODEL_CHOICES)
    st.text(f"Whisper Model Loaded: {model_choice}")

    if st.sidebar.button("Transcribe"):
        if video_file:
            video_path = save_uploaded_file(video_file)
            audio_path = video_path.replace(".mp4", ".mp3")
            convert_video_to_mp3(video_path, audio_path)
        elif audio_file:
            audio_path = save_uploaded_file(audio_file)
        else:
            st.sidebar.error("Please upload a video or audio file")
            return

        st.sidebar.text("Transcribing Audio...")
        transcription = transcribe_audio(audio_path, model_choice)
        st.sidebar.success("Transcription Complete")
        st.session_state.transcription_text = transcription["text"]  # Store in session state

        # Offer download option for transcription in text format
        original_file_name = video_file.name if video_file else audio_file.name
        txt_file_name = create_text_file(transcription["text"], original_file_name)

        # Offer download option for transcription in docx format
        docx_file_name = create_docx_file(transcription["text"], original_file_name)

        # Offer download option for transcription in VTT format
        vtt_file_name = create_vtt_file(transcription["text"], original_file_name)
        st.session_state.download_vtt_file_name = vtt_file_name  # Store in session state

        with open(txt_file_name, 'r') as file:
            txt_data = file.read()
        st.session_state.download_txt_file_name = f"{os.path.splitext(original_file_name)[0]}_transcription.txt"
        st.session_state.download_docx_file_name = docx_file_name  # Store in session state
    # Display transcription and download buttons if available
    if st.session_state.transcription_text:
        st.markdown(st.session_state.transcription_text)

        # Offer text file download
        st.sidebar.download_button(label="Download Transcription (TXT)", data=st.session_state.transcription_text,
                                   file_name=st.session_state.download_txt_file_name, mime="text/plain")

        # Offer DOCX file download
        with open(st.session_state.download_docx_file_name, 'rb') as file:
            docx_data = file.read()
        st.sidebar.download_button(label="Download Transcription (DOCX)", data=docx_data,
                                   file_name=st.session_state.download_docx_file_name,
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # Offer VTT file download
        with open(st.session_state.download_vtt_file_name, 'r', encoding='utf-8') as file:
            vtt_data = file.read()
        st.sidebar.download_button(label="Download Transcription (VTT)", data=vtt_data,
                                   file_name=st.session_state.download_vtt_file_name, mime="text/vtt")

    if audio_file:  # Allow the user to play the original audio
        st.sidebar.header("Play Original Audio File")
        st.sidebar.audio(audio_file)


if __name__ == "__main__":
    main()
