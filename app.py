import streamlit as st
import os
from document_processor import DocumentProcessor
from chat_handler import ChatHandler

# Initialize processors
@st.cache_resource
def get_processors():
    doc_processor = DocumentProcessor()
    chat_handler = ChatHandler()
    return doc_processor, chat_handler

def main():
    st.set_page_config(
        page_title="PLM Smart Self Service",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title(" PLM Smart Self Service")
    st.markdown("Upload your documents (Word, PDF, Excel) and ask questions about their content!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processed_content" not in st.session_state:
        st.session_state.processed_content = ""
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    # Get processors
    doc_processor, chat_handler = get_processors()
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'docx', 'doc', 'xlsx', 'xls'],
            accept_multiple_files=True,
            help="Supported formats: PDF, Word (.docx, .doc), Excel (.xlsx, .xls)"
        )
        
        if uploaded_files:
            if uploaded_files != st.session_state.uploaded_files:
                st.session_state.uploaded_files = uploaded_files
                st.session_state.processed_content = ""
                st.session_state.messages = []
                
                with st.spinner("Processing documents..."):
                    try:
                        all_content = []
                        for uploaded_file in uploaded_files:
                            content = doc_processor.process_file(uploaded_file)
                            if content:
                                all_content.append(f"--- Content from {uploaded_file.name} ---\n{content}\n")
                        
                        if all_content:
                            st.session_state.processed_content = "\n".join(all_content)
                            st.success(f"Successfully processed {len(uploaded_files)} file(s)!")
                        else:
                            st.error("No content could be extracted from the uploaded files.")
                    except Exception as e:
                        st.error(f"Error processing files: {str(e)}")
        
        # Display uploaded files info
        if st.session_state.uploaded_files:
            st.subheader("📄 Uploaded Files")
            for file in st.session_state.uploaded_files:
                st.write(f"• {file.name} ({file.size} bytes)")
    
    # Main chat interface
    if not st.session_state.processed_content:
        st.info("👆 Please upload some documents to start chatting!")
        return
    
    # Display chat messages
    st.subheader("💬 Chat with your documents")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = chat_handler.get_response(
                        prompt, 
                        st.session_state.processed_content,
                        st.session_state.messages[:-1]  # Exclude the current user message
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
