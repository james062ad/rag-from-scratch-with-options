from src.retrieval.db_utils import connect_db
from src.retrieval.chunk_utils import format_chunk

def retrieve_top_chunks(embedding, top_k=5, source_filter=None):
    conn = connect_db()
    cur = conn.cursor()

    where_clause = ""
    params = [embedding]

    if source_filter and source_filter != "all":
        where_clause = "WHERE source = %s"
        params = [embedding, source_filter]

    cur.execute(f"""
        SELECT chunk, source
        FROM papers
        {where_clause}
        ORDER BY embedding <-> %s::vector
        LIMIT {top_k};
    """, params[::-1] if where_clause else params)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [format_chunk(r) for r in rows]
