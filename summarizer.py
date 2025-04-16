from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY=os.getenv("API_KEY")

def summarize_tables(tables):
    prompt_text = """
    You are an assistant tasked with summarizing tables and text.
    Give a concise summary of the table or text.

    Respond only with the summary, no additionnal comment.
    Do not start your message by saying "Here is a summary" or anything like that.
    Just give the summary as it is.

    Table or text chunk: {element}
    """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Summary chain
    model = ChatGoogleGenerativeAI(temperature=0.5, model="gemini-2.0-flash")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Summarize tables
    tables_html = [table.metadata.text_as_html for table in tables]
    table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})
    return table_summaries

def summarize_images(images):
    summaries=[]
    genai.configure(api_key=GOOGLE_API_KEY)
    model=genai.GenerativeModel("gemini-2.0-flash")
    prompt = """You are an automotive assistant tasked with summarizing images for retrieval. \
                These summaries will be embedded and used to retrieve the raw image. \
                Describe the image in detail. Be specific about graphs, such as bar plots."""
    for image in images:
        image_data=base64.b64decode(image)
        img=Image.open(BytesIO(image_data))
        response=model.generate_content([prompt, img])
        summaries.append(response.text)
    return summaries
