from unstructured.partition.pdf import partition_pdf
from unstructured.partition.doc import partition_doc
from unstructured.partition.docx import partition_docx
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.csv import partition_csv
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.text import partition_text
from unstructured.partition.html import partition_html
import re


def partitioner_pdf(file_path):
    chunks=partition_pdf(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    return chunks

def partitioner_docx(file_path):
    chunks=partition_docx(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    return chunks

def partitioner_doc(file_path):
    chunks=partition_doc(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    return chunks

def partitioner_pptx(file_path):
    chunks=partition_pptx(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    return chunks

def partitioner_ppt(file_path):
    chunks=partition_ppt(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    return chunks

def partitioner_csv(file_path):
    chunks=partition_csv(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000
    )
    return chunks

def partitioner_xlsx(file_path):
    chunks=partition_xlsx(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000
    )
    return chunks

def partitioner_txt(file_path):
    chunks=partition_text(
        filename=file_path,
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000
    )
    return chunks

def partitioner_html(url):
    chunks=partition_html(
        url=url,
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
        extract_images_in_pdf=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    return chunks

def get_images_base64(chunks):
        images_b64 = []
        for chunk in chunks:
            if "CompositeElement" in str(type(chunk)):
                chunk_els = chunk.metadata.orig_elements
                for el in chunk_els:
                    if "Image" in str(type(el)):
                        images_b64.append(el.metadata.image_base64)
        return images_b64

def separator(chunks):
    tables = []
    texts = []

    for chunk in chunks:
        if "Table" in str(type(chunk)):
            tables.append(chunk)

        if "CompositeElement" in str(type((chunk))):
            texts.append(chunk)
            # Extract and process URLs from text
            if hasattr(chunk, 'text'):
                # Common URL pattern
                url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*/?'
                found_urls = re.findall(url_pattern, chunk.text)
                for url in found_urls:
                    try:
                        # Get content from URL using partitioner_html
                        url_chunks = partitioner_html(url)
                        # Add the URL content to texts
                        texts.extend(url_chunks)
                    except Exception as e:
                        print(f"Error processing URL {url}: {e}")

    images = get_images_base64(chunks)
    return texts, tables, images

def separator_csv(chunks):
    tables=[]
    for chunk in chunks:
        if "Table" in str(type(chunk)):
            tables.append(chunk)
    return tables