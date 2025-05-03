from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from base64 import b64decode


def parse_docs(docs):
    """Split base64-encoded images and texts"""
    b64 = []
    text = []
    for doc in docs:
        # Check if the doc is an image object (dict with 'text' field)
        if isinstance(doc, dict) and 'text' in doc:
            # Preserve the entire image object with metadata
            b64.append(doc)
        else:
            text.append(doc)
    return {"images": b64, "texts": text}


def build_prompt(kwargs):
    docs_by_type = kwargs["context"]
    user_question = kwargs["question"]

    context_text = ""
    if len(docs_by_type["texts"]) > 0:
        for text_element in docs_by_type["texts"]:
            # Handle both string and object text formats
            if hasattr(text_element, 'text'):
                context_text += text_element.text
            else:
                context_text += str(text_element)

    # construct prompt with context (including images)
    prompt_template = f"""
    You are an AI assistant that can analyze both text and images. 
    Answer the question based on the following context and images.
    
    Context: {context_text}
    Question: {user_question}
    
    If the question is about an image, carefully analyze the image and provide a detailed answer.
    If the context includes both text and images, consider both when answering.
    """

    prompt_content = [{"type": "text", "text": prompt_template}]

    if len(docs_by_type["images"]) > 0:
        for image in docs_by_type["images"]:
            # Handle both dictionary and string image formats
            image_base64 = image['text'] if isinstance(image, dict) and 'text' in image else image
            prompt_content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            )

    return ChatPromptTemplate.from_messages(
        [
            HumanMessage(content=prompt_content),
        ]
    )


# chain = (
#     {
#         "context": retriever | RunnableLambda(parse_docs),
#         "question": RunnablePassthrough(),
#     }
#     | RunnableLambda(build_prompt)
#     | ChatOpenAI(model="gpt-4o-mini")
#     | StrOutputParser()
# )

# chain_with_sources = {
#     "context": retriever | RunnableLambda(parse_docs),
#     "question": RunnablePassthrough(),
# } | RunnablePassthrough().assign(
#     response=(
#         RunnableLambda(build_prompt)
#         | ChatOpenAI(model="gpt-4o-mini")
#         | StrOutputParser()
#     )
# )