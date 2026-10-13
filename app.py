
import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables from the project folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

st.set_page_config(
    page_title="CloudBuddy AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 CloudBuddy AI")
st.write("Your AI assistant powered by Google Gemini.")

# Load API key
api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    st.error(
        "Gemini API key not found. "
        "Check that GEMINI_API_KEY is set in your .env file."
    )
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# User input
prompt = st.text_area(
    "What would you like help with?",
    placeholder="Ask CloudBuddy AI anything...",
    height=120,
)

if st.button("Ask AI", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a question.")
    else:
        start_time = time.time()

        try:
            with st.spinner("CloudBuddy AI is thinking..."):
                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt.strip(),
                )

            answer = getattr(response, "output_text", None)

            if answer:
                st.subheader("Answer")
                st.markdown(answer)
                st.caption(
                    f"Response time: {time.time() - start_time:.1f} seconds"
                )
            else:
                st.warning(
                    "Gemini returned no text. Please try another prompt."
                )

        except Exception as e:
            st.error(f"Gemini request failed: {e}")
            st.info(
                "Check your internet connection, API key, model availability, "
                "and installed google-genai package."
            )

