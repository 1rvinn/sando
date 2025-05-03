import streamlit as st
from parser import partitioner_pdf, partitioner_docx, partitioner_doc, partitioner_ppt, partitioner_pptx, partitioner_csv, separator, separator_csv, partitioner_xlsx, partitioner_txt
from local_store import save_file
import os
from embedding import embed
from dotenv import load_dotenv
from prompt import parse_docs, build_prompt
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from display import display_srcs, display_base64_image
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from summarizer import summarize_images, summarize_tables, summarize_text
import shutil
import base64

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "processed_data" not in st.session_state:
    st.session_state.processed_data = []

# Create vectorstore directory with proper permissions
vectorstore_dir = os.path.abspath("vectorstore")
if os.path.exists(vectorstore_dir):
    shutil.rmtree(vectorstore_dir)
os.makedirs(vectorstore_dir, exist_ok=True)

st.set_page_config(page_title="sando", page_icon="icon.png", layout="wide", initial_sidebar_state="auto", menu_items=None)
st.logo("logo.png",size="large")

load_dotenv()
GOOGLE_API_KEY=st.secrets["GEMINI_API_KEY"]
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

#file uploader
files=st.sidebar.file_uploader(label="upload your documents", type=["csv","pdf","jpg","jpeg","png","txt", "docx", "doc", "ppt","pptx", "xlsx"], accept_multiple_files=True, help=None, disabled=False, label_visibility="visible")

if files:
    if st.sidebar.button("ask ai", type="primary"):
        try:
            # Process files first
            processed_data = []
            for file in files:
                texts = []
                tables = []
                images = []
                if file.name.lower().endswith(".pdf"):
                    with st.spinner(f"processing {file.name}"):
                        file_path = save_file(file)
                        chunks = partitioner_pdf(file_path)
                        shutil.rmtree("session_uploads")
                        texts,tables,images = separator(chunks)
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".docx"):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_docx(file_path)
                        shutil.rmtree("session_uploads")
                        texts,tables,images=separator(chunks)
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".doc"):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_doc(file_path)
                        shutil.rmtree("session_uploads")
                        texts,tables,images=separator(chunks)
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".ppt"):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_ppt(file_path)
                        shutil.rmtree("session_uploads")
                        texts,tables,images=separator(chunks)
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".pptx"):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_pptx(file_path)
                        shutil.rmtree("session_uploads")
                        texts,tables,images=separator(chunks)
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".csv"):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_csv(file_path)
                        shutil.rmtree("session_uploads")
                        tables=separator_csv(chunks)
                        texts = []
                        images = []
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".xlsx"):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_xlsx(file_path)
                        shutil.rmtree("session_uploads")
                        tables=separator_csv(chunks)
                        texts = []
                        images = []
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith((".jpg", ".jpeg", ".png")):
                    with st.spinner(f"processing {file.name}", show_time=False):
                        image_bytes = file.read()
                        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                        # Create a simple object with the base64 string
                        image_obj = {
                            'text': image_base64,
                            'metadata': {
                                'filename': file.name
                            }
                        }
                        images = [image_obj]
                        texts = []
                        tables = []
                    processed_data.append((texts, tables, images))
                elif file.name.lower().endswith(".txt"):
                    with st.spinner("analysing files", show_time=False):
                        file_path=save_file(file)
                        chunks=partitioner_txt(file_path)
                        shutil.rmtree("session_uploads")
                        texts,tables,images=separator(chunks)
                    processed_data.append((texts, tables, images))

            # Initialize FAISS and add data
            with st.spinner("initializing vector store"):
                embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
                vectorstore = FAISS.from_texts(
                    ["initial document"],  # Create with a dummy document
                    embedding_function
                )
                store = InMemoryStore()
                id_key = "doc_id"
                st.session_state.retriever = MultiVectorRetriever(
                    vectorstore=vectorstore,
                    docstore=store,
                    id_key=id_key
                )

                # Add processed data to the vectorstore
            for texts, tables, images in processed_data:                  
                with st.spinner("generating embeddings"):
                    texts_summ = summarize_text(texts)
                    embed(texts, texts_summ, st.session_state.retriever, id_key)
                    tables_summ = summarize_tables(tables)
                    embed(tables, tables_summ, st.session_state.retriever, id_key)
                    images_summ = summarize_images(images)
                    embed(images, images_summ, st.session_state.retriever, id_key)

            # Save the vectorstore
            vectorstore.save_local(vectorstore_dir)
                
            # Store processed data in session state
            st.session_state.processed_data = processed_data

        except Exception as e:
            st.error(f"Error: {e}")

# Display extracted contents if available
if st.session_state.processed_data:
    with st.expander("extracted contents"):
        for i, data in enumerate(st.session_state.processed_data):
            # Get the file name from the first available source
            file_name = None
            if data[0]:  # Check texts
                if hasattr(data[0][0].metadata, 'filename'):
                    file_name = data[0][0].metadata.filename
            elif data[1]:  # Check tables
                if hasattr(data[1][0].metadata, 'filename'):
                    file_name = data[1][0].metadata.filename
            elif data[2]:  # Check images
                if isinstance(data[2][0], dict) and 'metadata' in data[2][0] and 'filename' in data[2][0]['metadata']:
                    file_name = data[2][0]['metadata']['filename']
            
            st.markdown(f"### File: {file_name if file_name else f'Document {i+1}'}")
            st.write(f"texts: {len(data[0])}, tables: {len(data[1])}, images: {len(data[2])}")
            for text in data[0]:
                st.markdown(text.text)
            for table in data[1]:
                st.html(table.metadata.text_as_html)
            st.markdown("## images:")
            for image in data[2]:
                if isinstance(image, dict):
                    display_base64_image(image['text'])
                else:
                    display_base64_image(image)
            st.markdown("---")  # Add a separator between files

if st.session_state.retriever:
    chain_with_sources = {
        "context": st.session_state.retriever | RunnableLambda(parse_docs),
        "question": RunnablePassthrough(),
    } | RunnablePassthrough().assign(
        response=(
            RunnableLambda(build_prompt)
            | ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.8)
            | StrOutputParser()
        )
    )

    # Create a container for the chat interface
    chat_container = st.container()
    with chat_container:
        # Create two columns: one for the chat messages and one for the input
        col1, col2 = st.columns([1, 0.1])
        
        with col1:
            # Chat messages container with scrollable area
            messages_container = st.container()
            with messages_container:
                for i, message in enumerate(st.session_state.messages):
                    if isinstance(message, HumanMessage):
                        with st.chat_message("user", avatar="user_icon.png"):
                            st.markdown(message.content)
                    else:
                        with st.chat_message("assistant", avatar="icon_.png"):
                            st.markdown(message['response'])
                            if st.button("sources", key=f"sources_button_{i}"):
                                display_srcs(message)

    # Chat input at the bottom
    prompt = st.chat_input("ask a question")
    if prompt:
        with chat_container:
            with st.chat_message("user", avatar="user_icon.png"):
                st.markdown(prompt)
            st.session_state.messages.append(HumanMessage(prompt))
            with st.chat_message("assistant", avatar="icon_.png"):
                with st.spinner("thinking"):
                    response = chain_with_sources.invoke(prompt)
                    st.session_state.messages.append(response)
                st.markdown(response['response'])
                if st.button("sources", key=f"sources_button_{len(st.session_state.messages)-1}"):
                    display_srcs(response)