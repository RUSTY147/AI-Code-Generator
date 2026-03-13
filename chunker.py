import re

def chunk_code(file_path, content, chunk_size=1000):

    chunks = []

    # split by functions/classes (works for most languages)
    parts = re.split(r'\n(?=(def |class |function ))', content)

    current_chunk = ""

    for part in parts:

        if len(current_chunk) + len(part) > chunk_size:
            chunks.append({
                "file": file_path,
                "content": current_chunk
            })
            current_chunk = part
        else:
            current_chunk += part

    if current_chunk:
        chunks.append({
            "file": file_path,
            "content": current_chunk
        })

    return chunks