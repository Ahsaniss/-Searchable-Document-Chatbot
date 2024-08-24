import os
import google.generativeai as genai
import PyPDF2
import streamlit as st

# Configure Gemini API
genai.configure(api_key="AIzaSyBFCRAdNSHw6894aq_56iBNfaDAhZgsIXI")

# Gemini model setup
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# PDF text extraction function
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# Streamlit UI setup
st.set_page_config(page_title="Searchable Document Chatbot", page_icon="🔍", layout="wide")

# Main heading and introduction
st.title("🔍 Searchable Document Chatbot")
st.write(
    "Welcome to our interactive document search chatbot! Feel free to upload your PDF document and start asking questions."
)

# Sidebar for PDF upload and status
with st.sidebar:
    st.subheader("📄 Upload PDF")
    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

    # PDF Preview Placeholder
    if uploaded_file:
        st.subheader("📄 PDF Preview")
        page_count = len(PyPDF2.PdfReader(uploaded_file).pages)
        st.write(f"Page 1 of {page_count}")
        st.image("https://via.placeholder.com/150", caption="PDF Preview")  # Online image placeholder

    # Status after upload
    if uploaded_file:
        st.success("✅ Ready to Chat!")
    else:
        st.warning("⚠️ Please upload a PDF document to start.")

# Main content for chat
if uploaded_file:
    # Extract the text from the uploaded PDF
    document_text = extract_text_from_pdf(uploaded_file)

    # Display a preview of the PDF's extracted text
    st.subheader("📜 PDF Document Preview")
    st.text_area("Document Content", document_text[:5000], height=300)  # Preview first 5000 chars

    # Input for the user's question and search button
    user_question = st.text_input("💬 Ask a question")
    if st.button("Search"):  # Add a "Search" button to submit the question
        if user_question:
            chat_session = model.start_chat(
                history=[]
            )
            response = chat_session.send_message(f"Document: {document_text}\n\nQuestion: {user_question}")

            # Display the AI's response
            st.subheader("🤖 Chatbot Response")
            st.markdown(f"""
            <div style='background-color:#f9f9f9; padding:10px; border-radius:5px;'>
                <strong>User Question:</strong> {user_question} <br><br>
                <strong>AI Response:</strong> {response.text}
            </div>
            """, unsafe_allow_html=True)

    # Button to clear chat
    if st.button("Clear Chat"):
        st.cache_data.clear()  # Updated to the new Streamlit caching mechanism
else:
    st.info("💡 Upload a PDF to start the chat!")

# Footer and additional info
st.markdown("---")
st.write(
    "Made with ❤️ by ahsani\n\n"
    "Connect with me: [LinkedIn](www.linkedin.com/in/muhammad-ahsan-raza-2a9b9828a) | [GitHub](https://github.com/Ahsaniss) | [Leet-code](https://leetcode.com/u/Ahsani/)"
)
