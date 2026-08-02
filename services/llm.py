import os
import streamlit as st

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("Current Key:", GROQ_API_KEY[:15]) 

client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt):

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        st.error(f"❌ LLM Error: {e}")

        return None