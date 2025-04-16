import streamlit as st
from parser import partitioner, separator
from local_store import save_file
import os
from embedding import embed
from dotenv import load_dotenv
from unstructured_utils import parse_docs, build_prompt
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from display import display_base64_image

st.set_page_config(page_title="sando", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.header("sando")

load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

#file uploader
files=st.file_uploader('label', type=["csv","pdf","jpg","jpeg","png"], accept_multiple_files=True, help=None, disabled=False, label_visibility="visible")


if files:
    if st.button("ask ai"):
        with st.spinner("preparing ai system", show_time=False):
            for file in files:
                try:
                    file_path=save_file(file)
                    chunks=partitioner(file_path)
                    set([str(type(el)) for el in chunks])
                    texts,tables,images=separator(chunks)
                    st.write(f"texts: {len(texts)}, tables: {len(tables)}, images: {len(images)}")
                    with st.spinner("generating embeddings"):
                        retriever=embed(texts, tables, images)
                    chain_with_sources = {
                        "context": retriever | RunnableLambda(parse_docs),
                        "question": RunnablePassthrough(),
                    } | RunnablePassthrough().assign(
                        response=(
                            RunnableLambda(build_prompt)
                            | ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.8)
                            | StrOutputParser()
                        )
                    )
                    response = chain_with_sources.invoke(
                        "What is a transformer?"
                    )

                    st.write("Response:", response['response'])

                    st.write("\n\nContext:")
                    for text in response['context']['texts']:
                        st.write(text.text)
                        st.write("Page number: ", text.metadata.page_number)
                        st.write("\n" + "-"*50 + "\n")
                    for image in response['context']['images']:
                        display_base64_image(image)
                except Exception as e:
                    st.write(e)
        pass