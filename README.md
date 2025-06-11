# AI Document Chatbot

An AI-powered chatbot built with Streamlit that allows you to upload documents (Word, PDF, Excel) and ask questions about their content using OpenAI's GPT-4o model.

## Features

- 📄 **Multiple File Support**: Upload Word (.docx, .doc), PDF, and Excel (.xlsx, .xls) files
- 🤖 **AI-Powered Responses**: Uses OpenAI's GPT-4o for intelligent document analysis
- 💬 **Interactive Chat**: Conversational interface with chat history
- 📊 **Smart Processing**: Automatically extracts text from documents and handles large files
- 🔄 **Real-time Processing**: Upload and start chatting immediately

## Prerequisites

Before running this application, you need:

1. **Python 3.11 or higher**
2. **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/)
3. **Required Python packages** (listed below)

## Installation

### 1. Clone or Download the Project

Download all the project files to your local directory:
- `app.py`
- `chat_handler.py`
- `document_processor.py`
- `pyproject.toml`
- `.streamlit/config.toml`

### 2. Install Dependencies

You can install the required packages using either pip or uv:

#### Option A: Using pip
```bash
pip install streamlit openai pandas PyPDF2 python-docx openpyxl docx
```

#### Option B: Using uv (recommended)
```bash
uv sync
```

### 3. Set Up OpenAI API Key

You need to set your OpenAI API key as an environment variable:

#### On Windows:
```bash
set OPENAI_API_KEY=your_api_key_here
```

#### On Mac/Linux:
```bash
export OPENAI_API_KEY=your_api_key_here
```

#### Or create a .env file:
Create a `.env` file in your project directory:
```
OPENAI_API_KEY=your_api_key_here
```

## Required Libraries

The application depends on these Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.45.1 | Web interface framework |
| openai | >=1.86.0 | OpenAI API integration |
| pandas | >=2.3.0 | Excel file processing |
| PyPDF2 | >=3.0.1 | PDF text extraction |
| python-docx | >=1.1.2 | Word document processing |
| openpyxl | >=3.1.5 | Excel file reading |
| docx | >=0.2.4 | Additional Word document support |

## How to Run

1. **Navigate to your project directory**:
   ```bash
   cd your-project-directory
   ```

2. **Run the Streamlit application**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage Guide

### Step 1: Upload Documents
1. Use the sidebar on the left to upload your documents
2. Click "Browse files" and select your Word, PDF, or Excel files
3. You can upload multiple files at once
4. Wait for the processing to complete

### Step 2: Start Chatting
1. Once your documents are processed, you'll see the chat interface
2. Type your question in the chat input box at the bottom
3. Press Enter or click Send
4. The AI will analyze your documents and provide answers

### Step 3: Ask Questions
You can ask various types of questions:
- **Summary questions**: "What is this document about?"
- **Specific information**: "What are the key findings?"
- **Data analysis**: "What are the sales figures for Q1?"
- **Comparisons**: "Compare the data between Sheet1 and Sheet2"

### Example Questions
- "Summarize the main points of this document"
- "What are the key recommendations?"
- "Find information about pricing"
- "What data is in the Excel spreadsheet?"
- "Explain the methodology section"

## File Structure

```
ai-document-chatbot/
├── app.py                 # Main Streamlit application
├── chat_handler.py        # OpenAI integration and response handling
├── document_processor.py  # Document parsing and text extraction
├── pyproject.toml         # Project dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## Configuration

### Streamlit Configuration
The `.streamlit/config.toml` file contains server settings:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### Token Limits
The application automatically handles large documents by:
- Truncating content to stay within OpenAI's token limits
- Limiting chat history to recent messages
- Smart truncation at sentence boundaries

## Troubleshooting

### Common Issues

1. **"OpenAI API key not found" error**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Verify your API key is correct and active

2. **"Request too large" error**
   - The application automatically handles this, but very large documents may still cause issues
   - Try uploading smaller documents or sections of large files

3. **File processing errors**
   - Ensure your files are not corrupted
   - Check that file formats are supported (.pdf, .docx, .doc, .xlsx, .xls)
   - Some password-protected files may not work

4. **Streamlit won't start**
   - Make sure all dependencies are installed
   - Check that port 5000 is not being used by another application
   - Try using a different port: `streamlit run app.py --server.port 8501`

### Getting Help

If you encounter issues:
1. Check the terminal/console for error messages
2. Verify all dependencies are installed correctly
3. Ensure your OpenAI API key is valid and has credits
4. Try with a smaller test document first

## Features Explained

### Document Processing
- **PDF**: Extracts text from all pages
- **Word**: Extracts text from paragraphs and tables
- **Excel**: Converts data to readable text format with statistics

### AI Capabilities
- Understands document context
- Provides specific citations when possible
- Maintains conversation history
- Handles follow-up questions

### Safety Features
- Automatic content truncation for large documents
- Error handling and user-friendly messages
- Secure API key handling

## Tips for Best Results

1. **Upload relevant documents**: Only upload files related to your questions
2. **Ask specific questions**: More specific questions get better answers
3. **Use follow-up questions**: Build on previous answers for deeper insights
4. **Check document quality**: Clear, well-formatted documents work best

## License

This project is open source. Feel free to modify and distribute as needed.

## Support

For questions or issues, please check the troubleshooting section above or refer to the documentation of the individual libraries used.