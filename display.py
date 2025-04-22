import base64
from io import BytesIO
from PIL import Image
import streamlit as st

def display_base64_image(base64_image):
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    st.image(image, caption=f"Source Image")

@st.dialog("sources")
def display_srcs(message):
    # Display text sources
    if message['context']['texts']:
        st.markdown("### Text Sources:")
        for element in message['context']['texts']:
            # Handle both string and object formats
            if isinstance(element, str):
                display_base64_image(element)
            else:
                # Display file name if available
                if hasattr(element, 'metadata') and hasattr(element.metadata, 'filename'):
                    st.markdown(f"**File:** {element.metadata.filename}")
                
                # Check if the element is a Table
                if "Table" in str(type(element)):
                    st.html(element.metadata.text_as_html)
                else:
                    # Handle regular text elements
                    if hasattr(element.metadata, 'page_number'):
                        st.markdown(f"Page number: {element.metadata.page_number}")
                    st.markdown(element.text)
            st.markdown("\n" + "-"*50 + "\n")
    
    # Display image sources
    if message['context']['images']:
        st.markdown("### Image Sources:")
        for image in message['context']['images']:
            if isinstance(image, dict):
                # Display file name if available
                if 'metadata' in image and 'filename' in image['metadata']:
                    st.markdown(f"**File:** {image['metadata']['filename']}")
                # Display the image
                if 'text' in image:
                    display_base64_image(image['text'])
            else:
                # Handle direct base64 strings
                display_base64_image(image)
            st.markdown("\n" + "-"*50 + "\n")