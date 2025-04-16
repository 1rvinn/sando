import base64
from io import BytesIO
from PIL import Image
import streamlit as st

def display_base64_image(base64_image):
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    st.image(image, caption=f"Source Image")