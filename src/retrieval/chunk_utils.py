def format_chunk(row):
    if isinstance(row, tuple) and len(row) == 2:
        return {
            "text": row[0],
            "source": row[1]
        }
    else:
        return {"text": str(row), "source": "unknown"}
