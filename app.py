
import streamlit as st
import requests

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 Language Translation Tool")
st.write("Translate text from one language to another.")

languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "French": "fr",
    "Arabic": "ar"
}

col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

input_text = st.text_area(
    "Enter Text",
    placeholder="Write your text here..."
)

if st.button("Translate Text", type="primary"):

    if not input_text.strip():
        st.warning("Please enter some text.")

    elif source_language == target_language:
        st.warning("Please select different languages.")

    else:
        try:
            response = requests.get(
                "https://api.mymemory.translated.net/get",
                params={
                    "q": input_text,
                    "langpair": (
                        f"{languages[source_language]}|"
                        f"{languages[target_language]}"
                    )
                },
                timeout=20
            )

            response.raise_for_status()
            data = response.json()

            if data.get("responseStatus") == 200:
                translated_text = data.get(
                    "responseData", {}
                ).get("translatedText", "")

                if translated_text:
                    st.subheader("Translated Text")

                    st.text_area(
                        "Translation Result",
                        value=translated_text,
                        height=150
                    )

                    st.code(translated_text, language=None)
                    st.caption(
                        "Use the copy icon to copy the translated text."
                    )

                else:
                    st.error("No translation was returned.")

            else:
                st.error(
                    data.get(
                        "responseDetails",
                        "Translation failed."
                    )
                )

        except requests.RequestException:
            st.error(
                "API connection failed. Check your internet "
                "connection and try again."
            )

        except (ValueError, TypeError):
            st.error(
                "Invalid response received from the API."
            )
