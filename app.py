import streamlit as st
import requests
import time

# -----------------------------
# Page Settings
# -----------------------------
st.set_page_config(
    page_title="Mistral AI Text Summarizer",
    page_icon="📝",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("📝 Mistral AI Text Summarizer")
st.write("Enter your text below and get a simple summary.")

# -----------------------------
# Get API Key from Secrets
# -----------------------------
try:
     MY_API_KEY = st.secrets["MY_API_KEY"]
except Exception:
    st.error("MY_API_KEY is not configured in Streamlit Secrets.")
    st.stop()

# -----------------------------
# Text Input
# -----------------------------
text = st.text_area(
    "Enter your huge text",
    height=300,
    placeholder="Paste your text here..."
)

# -----------------------------
# Summarization Prompt
# -----------------------------
prompt = st.text_input(
    "Enter your summarization prompt",
    value="Summarize this text in 5 simple bullet points."
)

# -----------------------------
# Summarize Button
# -----------------------------
if st.button("✨ Summarize"):

    if not text.strip():
        st.warning("Please enter some text first.")

    else:

        url = "https://api.mistral.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer { MY_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": f"{prompt}\n\n{text}"
                }
            ],
            "max_tokens": 500
        }

        with st.spinner("Generating summary..."):

            try:

                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=60
                )

                # -----------------------------
                # Success
                # -----------------------------
                if response.status_code == 200:

                    result = response.json()

                    summary = result["choices"][0]["message"]["content"]

                    st.subheader("📌 Summary")
                    st.write(summary)

                # -----------------------------
                # Rate Limit
                # -----------------------------
                elif response.status_code == 429:

                    st.error(
                        "Mistral API rate limit exceeded. "
                        "Please wait and try again later."
                    )

                    st.info(
                        "This is an API usage/rate-limit issue, "
                        "not a problem with your text."
                    )

                # -----------------------------
                # Invalid API Key
                # -----------------------------
                elif response.status_code == 401:

                    st.error(
                        "Invalid Mistral API key. "
                        "Please check Streamlit Secrets."
                    )

                # -----------------------------
                # Other Errors
                # -----------------------------
                else:

                    st.error(
                        f"MY API Error: {response.status_code}"
                    )

                    st.write(response.text)

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. Please try again."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )