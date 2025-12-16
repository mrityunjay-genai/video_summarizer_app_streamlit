import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file,get_file
import google.generativeai as genai
import time
import os
from pathlib import Path
import tempfile
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Page Config
st.set_page_config(
    page_title="Video Summarizer",
    page_icon="📽️",
    layout="wide"
)
st.title("Video Sumarizer Agent 📽️")
st.header("This app is powered by Gemini")

# Agent
def initialize_agent():
    return Agent(
        name="Video Summarizer Agent",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True
    )
multimodel_agent = initialize_agent()

# File Uploader
video_file = st.file_uploader(
    "Upload a Video file here", type=['mp4','mov','avi'], help="Upload a video for AI Analysis"
)

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        video_path= temp_video.name  #   video_path = /tmp/tmpeuo041ei.mp4
    
    st.video(video_path, format="video/mp4", start_time=0, width=300)

    # Text Area
    user_query = st.text_area(
        "What insights you are seeking from video?",
        placeholder="Ask anything about video content. The AI agent will analyze and gather additional context if needed.",
        help="Provide specific questions or insights you want from the video."
    )
    if st.button("🔍Anallyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    processed_video = upload_file(video_path)
                    while processed_video.state.name=="PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)
                        # print("processed_video-->", processed_video)

                    # Prompt generation
                    analysis_prompt=(
                        f"""
                        Analyze the uploaded video for content and context.
                        Respond to the following query using video insights and supplementary web research:
                        {user_query}
                        Provide a detailed, user-friendly, and actionable response.
                        """
                    )
                    # AI Agent processing
                    response = multimodel_agent.run(analysis_prompt, videos=[processed_video])
                # Display the result
                st.subheader("Analysis Result")
                st.markdown(response.content)
            
            except Exception as error:
                st.error(f"An error occured during the analysis: {error}")
            finally:
                # Clean up temporary video file
                Path(video_path).unlink(missing_ok=True)
    else:
        st.info("Upload a video file to begin analysis.")

# Customize text are height
st.markdown(
    """
    <style>
    .stTextArea textarea{
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)




       


