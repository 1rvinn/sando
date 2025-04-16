import uuid
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from summarizer import summarize_tables, summarize_images

def embed(texts, tables, images):
    # The vectorstore to use to index the child chunks
    tables_summ=summarize_tables(tables)
    images_summ=summarize_images(images)
    vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"))

    # The storage layer for the parent documents
    store = InMemoryStore()
    id_key = "doc_id"

    # The retriever (empty to start)
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )

    # Add texts
    text_ids = [str(uuid.uuid4()) for _ in texts]
    summary_texts = [
        Document(page_content=str(summary), metadata={id_key: text_ids[i]}) for i, summary in enumerate(texts) if str(summary).strip()
    ]
    retriever.vectorstore.add_documents(summary_texts)
    retriever.docstore.mset(list(zip(text_ids, texts)))

    if tables:
        table_ids = [str(uuid.uuid4()) for _ in tables]
        summary_tables = [
            Document(page_content=summary, metadata={id_key: text_ids[i]}) for i, summary in enumerate(tables_summ) if summary.strip()
        ]
        retriever.vectorstore.add_documents(summary_tables)
        retriever.docstore.mset(list(zip(table_ids, tables)))

    image_ids = [str(uuid.uuid4()) for _ in images]
    summary_images = [
        Document(page_content=summary, metadata={id_key: image_ids[i]}) for i, summary in enumerate(images_summ) if summary.strip()
    ]
    retriever.vectorstore.add_documents(summary_images)
    retriever.docstore.mset(list(zip(image_ids, images)))
    return retriever