import os
from openai import OpenAI
import streamlit as st

class ChatHandler:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        
        # Get API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            st.stop()
        
        self.client = OpenAI(api_key=api_key)
    
    def truncate_content(self, content, max_chars=200000):
        """Truncate content to fit within token limits using character count"""
        if len(content) <= max_chars:
            return content
        
        # Truncate content
        truncated_content = content[:max_chars]
        
        # Try to end at a complete sentence or paragraph
        last_period = truncated_content.rfind('.')
        last_newline = truncated_content.rfind('\n')
        
        if last_period > max_chars - 1000:  # If period is near the end
            truncated_content = truncated_content[:last_period + 1]
        elif last_newline > max_chars - 1000:  # If newline is near the end
            truncated_content = truncated_content[:last_newline]
        
        # Add a note about truncation
        return truncated_content + "\n\n[Note: Document content was truncated due to length limits]"
    
    def get_response(self, user_question, document_content, chat_history):
        """Generate response based on user question and document content"""
        try:
            # Truncate document content to prevent token limit issues
            truncated_content = self.truncate_content(document_content, max_chars=200000)
            
            # Prepare the system message with truncated document content
            system_message = f"""You are an AI assistant that helps users understand and analyze their documents. 
            You have access to the following document content:

            {truncated_content}

            Please answer questions based on this content. If the question cannot be answered from the provided documents, 
            please say so clearly. Be helpful, accurate, and cite specific parts of the documents when relevant.
            Keep your responses concise but informative."""
            
            # Prepare conversation messages
            messages = [{"role": "system", "content": system_message}]
            
            # Add limited chat history to avoid token limits
            recent_history = chat_history[-3:] if len(chat_history) > 3 else chat_history
            for msg in recent_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Add current user question
            messages.append({"role": "user", "content": user_question})
            
            # Estimate total characters to ensure we're within limits
            total_chars = sum(len(msg["content"]) for msg in messages)
            
            # If still too many characters, further reduce content
            if total_chars > 250000:
                truncated_content = self.truncate_content(document_content, max_chars=120000)
                messages[0]["content"] = f"""You are an AI assistant that helps users understand and analyze their documents. 
                You have access to the following document content:

                {truncated_content}

                Please answer questions based on this content. If the question cannot be answered from the provided documents, 
                please say so clearly. Be helpful, accurate, and cite specific parts of the documents when relevant.
                Keep your responses concise but informative."""
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def summarize_document(self, document_content):
        """Generate a summary of the document content"""
        try:
            # Truncate content for summary to avoid token limits
            content_for_summary = self.truncate_content(document_content, max_chars=15000)
            
            prompt = f"""Please provide a concise summary of the following document content, 
            highlighting the main topics, key points, and structure:

            {content_for_summary}
            
            Keep the summary under 200 words."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")