import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="TechBlog AI", layout="centered")

# App title
st.title("📝 AI for Content Generation")
st.subheader("TechBlog AI – Automated Blog Generator")

# -------- USER INPUTS --------

topic = st.text_input(
    "Enter Blog Topic",
    placeholder="e.g. What is Cloud Computing?"
)

tone = st.selectbox(
    "Select Writing Tone",
    [
        "Beginner Friendly",
        "Professional",
        "SEO Optimized",
        "Casual",
        "Formal"
    ]
)

length = st.slider(
    "Select Blog Length (Number of Words)",
    min_value=300,
    max_value=1500,
    value=600,
    step=100
)

extra_instructions = st.text_area(
    "Additional Instructions (Optional)",
    placeholder="e.g. Include examples, advantages, and real-world use cases"
)

# -------- GENERATE BUTTON --------

if st.button("Generate Blog"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a blog topic.")
    else:
        with st.spinner("Generating blog content..."):
            prompt = f"""
            Write a {length}-word blog article.

            Topic: {topic}
            Tone: {tone}

            Additional instructions:
            {extra_instructions}

            Structure:
            - Title
            - Introduction
            - Main content with headings
            - Conclusion
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert blog writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            blog_content = response.choices[0].message.content

            st.success("✅ Blog generated successfully!")
            st.text_area(
                "Generated Blog Content",
                blog_content,
                height=400
            )