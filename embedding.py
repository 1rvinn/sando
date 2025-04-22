import uuid
from langchain.schema.document import Document

def embed(content, summaries, retriever, id_key):
    if content:
        content_ids = [str(uuid.uuid4()) for _ in content]
        summary_content = [
            Document(page_content=summary, metadata={id_key: content_ids[i]}) for i, summary in enumerate(summaries) if summary.strip()
        ]
        retriever.vectorstore.add_documents(summary_content)
        retriever.docstore.mset(list(zip(content_ids, content)))
    return retriever