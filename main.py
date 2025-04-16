import streamlit as st
from parser import partitioner, separator
from local_store import save_file
import os
from embedding import embed
from dotenv import load_dotenv

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
                        embed(texts, tables, images)
                except Exception as e:
                    st.write(e)
        pass