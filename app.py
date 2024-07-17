import os
import streamlit as st
from langchain_mistralai import ChatMistralAI

def main():
    st.title("Code Assistant with Mistral AI")

    # Set API key
    os.environ["MISTRAL_API_KEY"] = "4FRt1cK7cHt5MfFqTmiyxkQwOl9oN21F"
    api_key = os.environ["MISTRAL_API_KEY"]

    # Navigation
    pages = ["Code Translation", "Code Generation", "Code Snippet Completion", "Code Documentation Generation"]
    choice = st.sidebar.selectbox("Select Feature", pages)

    if choice == "Code Translation":
        code_translation(api_key)
    elif choice == "Code Generation":
        code_generation(api_key)
    elif choice == "Code Snippet Completion":
        code_snippet_completion(api_key)
    elif choice == "Code Documentation Generation":
        code_docs_generation(api_key)

def code_translation(api_key):
    st.subheader("Code Translation")
    source_code = st.text_area("Enter your source code")
    languages = ["Python", "Java", "C++", "JavaScript", "Swift", "Ruby", "Kotlin"]
    target_language = st.selectbox("Select target language", languages)

    if st.button("Translate Code"):
        llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)
        prompt = f"Translate the following code to {target_language}:\n{source_code}"
        response = llm.invoke([("user", prompt)])
        content = response.content
        translated_code = extract_code_block(content)
        if translated_code:
            st.code(translated_code)
        else:
            st.error("No translated code found in the response.")

def code_generation(api_key):
    st.subheader("Code Generation")
    code_description = st.text_area("Enter code description")
    languages = ["Python", "Java", "C++", "JavaScript", "Swift", "Ruby", "Kotlin"]
    target_language = st.selectbox("Select programming language", languages)

    if st.button("Generate Code"):
        llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)
        prompt = f"{code_description} in {target_language}"
        response = llm.invoke([("user", prompt)])
        content = response.content
        generated_code = extract_code_block(content)
        if generated_code:
            st.code(generated_code)
        else:
            st.error("No generated code found in the response.")

def code_snippet_completion(api_key):
    st.subheader("Code Snippet Completion")
    incomplete_code = st.text_area("Enter your incomplete code")
    if st.button("Complete Code"):
        llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)
        prompt = f"Complete the following code snippet:\n{incomplete_code}"
        response = llm.invoke([("user", prompt)])
        content = response.content
        completed_code = extract_code_block(content)
        if completed_code:
            st.code(completed_code)
        else:
            st.error("No completed code found in the response.")

def code_docs_generation(api_key):
    st.subheader("Code Documentation Generation")
    uploaded_file = st.file_uploader("Upload your code file", type=["py", "java", "cpp", "js", "swift", "rb", "kt"])
    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")
        if st.button("Generate Documentation"):
            llm = ChatMistralAI(model="codestral-latest", temperature=0, api_key=api_key)
            prompt = f"Generate documentation for the following code:\n{code}"
            response = llm.invoke([("user", prompt)])
            content = response.content
            st.markdown(content)
            st.download_button("Download Documentation", content)

def extract_code_block(content):
    import re
    code_blocks = re.findall(r"```(.*?)```", content, re.DOTALL)
    return code_blocks[0].strip() if code_blocks else None

if __name__ == "__main__":
    main()
