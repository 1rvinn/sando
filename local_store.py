import streamlit as st
import os

def save_file(file):
    save_dir="session_uploads"
    os.makedirs(save_dir, exist_ok=True)
    try:
        file_path = os.path.join(save_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return(file_path)
    except Exception as e:
        st.error(e)