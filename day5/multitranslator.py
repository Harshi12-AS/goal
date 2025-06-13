import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import Runnable

# 🔑 Gemini API Key
GOOGLE_API_KEY = "AIzaSyDS5C7ZwvX6hT2PAUkKN_JokleC6A6damA"  # Replace with your actual key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# 🌐 Streamlit UI setup
st.set_page_config(page_title="🌍 Language Translator", page_icon="🌐")
st.title("🌐 AI Language Translator")
st.markdown("Enter a sentence in English, select the target language, and click **Translate**.")

# Language options
languages = [
    "French", "Spanish", "German", "Tamil", "Hindi", "Chinese", "Japanese", "Korean", "Arabic", "Italian"
]

# 🧠 Initialize Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini: {e}")
    st.stop()

# 🧾 Translation prompt (with dynamic language)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates English into other languages."),
    ("user", "Translate this to {language}: {input}")
])

# 🔗 Create the chain
translation_chain: Runnable = prompt | llm

# 📝 Input form
with st.form("translation_form"):
    user_input = st.text_input("Enter English sentence:")
    target_language = st.selectbox("Choose the language to translate into:", languages)
    submitted = st.form_submit_button("Translate")

# 🚀 Perform translation
if submitted:
    if not user_input.strip():
        st.warning("⚠️ Please enter a sentence.")
    else:
        try:
            result = translation_chain.invoke({
                "input": user_input,
                "language": target_language
            })
            translated_text = result.content if hasattr(result, "content") else str(result)
            st.success("✅ Translation successful!")
            st.text_area(f"{target_language} Translation:", translated_text, height=100)
        except Exception as e:
            st.error(f"❌ Something went wrong during translation:\n{e}")
