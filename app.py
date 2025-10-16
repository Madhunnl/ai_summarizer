import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")


st.set_page_config(page_title="AI Text Summarizer", page_icon="🧠")
st.title("🧠 AI Text Summarizer")
# Sidebar info
st.sidebar.header("About this App")
st.sidebar.info(
    """
    This app uses **OpenAI's GPT-4o-mini** model to generate concise summaries of any text.  
    Adjust the tone and target length for tailored results.  
    ---
    **Built by:** [Nikhil Madhunala](https://nikhilmadhunala.github.io/nikhil-ai-portfolio/)  
    💼 *AI Systems Engineer — Exploring LLMs, Agents, and MLOps*  
    📧 [Email me](mailto:nikhilmadhunala@gmail.com)
    """
)

if not api_key:
    st.warning("Add your OPENAI_API_KEY in the .env file to run this app.")
else:
    client = OpenAI(api_key=api_key)

text = st.text_area("Paste text to summarize:", height=200)
tone = st.selectbox("Tone", ["Neutral", "Casual", "Professional"])
length = st.slider("Target length (sentences)", 2, 8, 4)

if st.button("Summarize") and text.strip():
    prompt = f"Summarize the following text in a {tone.lower()} tone in about {length} sentences:\n\n{text}"
    with st.spinner("Summarizing…"):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
    st.subheader("Summary")
    st.write(resp.choices[0].message.content)
