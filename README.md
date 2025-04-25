# sando

A powerful document analysis and Q&A application built with Streamlit and Google's Gemini AI. Sando enables intelligent document processing and interactive querying across multiple file formats.

## Key Features

- **Multi-Format Document Support**: Process and analyze various file formats:
  - PDF documents
  - Word documents (DOC, DOCX)
  - PowerPoint presentations (PPT, PPTX)
  - Spreadsheets (CSV, XLSX)
  - Text files (TXT)
  - Images (JPG, JPEG, PNG)

- **Intelligent Content Extraction**:
  - Automatic text extraction and structuring
  - Table detection and parsing
  - Image extraction and analysis
  - URL detection and web content processing

- **Advanced Document Analysis**:
  - Semantic search capabilities
  - Multi-vector retrieval system
  - Context-aware responses
  - Source attribution for answers

- **Interactive Chat Interface**:
  - Real-time Q&A with uploaded documents
  - Source verification for responses
  - Support for both text and image queries
  - Clean and modern UI

## Technical Pipeline

![pipeline](https://github.com/1rvinn/sando/blob/main/pipeline.jpg?raw=true)

## Installation Guide

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd sando
   ```

2. **Set Up Python Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **System Dependencies**:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install poppler-utils
   
   # On macOS
   brew install poppler
   
   # On Windows
   # Download and install poppler from: http://blog.alivate.com.au/poppler-windows/
   ```

5. **Environment Setup**:
   - Create a `.streamlit/secrets.toml` file
   - Add your Google API key:
     ```toml
     GEMINI_API_KEY="your-api-key-here"
     ```

6. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

## Usage

1. Upload your documents using the sidebar file uploader
2. Click "ask ai" to initialize the document processing
3. Use the chat interface to ask questions about your documents
4. Click "sources" on any response to verify the source content

## Requirements

- Python 3.8+
- Google API key with access to Gemini models
- Poppler utils for PDF processing
- Sufficient RAM for document processing (recommended: 8GB+)

## Note

Ensure you have appropriate permissions and licenses for the documents you process. The application processes documents locally but uses Google's API for embeddings and response generation.
