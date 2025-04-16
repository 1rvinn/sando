from unstructured.partition.auto import partition

def partitioner(file_path):
    chunks=partition(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables
        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,
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

    images = get_images_base64(chunks)
    return texts,tables,images