import streamlit  as st
import os
import dotenv
from openai import OpenAI
dotenv.load_dotenv()

st.title("AI Powered Fitness chatbot")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))