##This project creates the summary of the transcribed text using Youtubetranscriptapi

import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the environment variables
#importing os to interact with the os environment
import os

#importing genai from google.generative ai
import google.generativeai as genai

#this youtube_transcript_api contains the code for youtube content transcription
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        #video id is the id after "=" sign. so the youtube url is split into two parts based on the "=" sign
        video_id=youtube_video_url.split("=")[1]
        
        #taking the video id and transcribing it using get_transcript function
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        #As it will return the list of transcript texts to combining the text of each lists
        transcript = ""
        #for each list item in the lists are taken and converted to continuos text with by seperating space " "
        for i in transcript_text:
            transcript += " " + i["text"] #"text" refers to the text in the ith list
        return transcript

    except Exception as e:
        raise e #raise exception for non existing video id
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    #assigning model to "gemini-pro in generative ai models
    model=genai.GenerativeModel("gemini-pro")
    #generating response using prompt and transcribed text of the youtube video
    response=model.generate_content(prompt+transcript_text)
    return response.text #returning response text

#setting title for the streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    #for displaying thumbnail of the youtube video in the link that is extracted from video id
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)




