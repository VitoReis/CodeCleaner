from indexer import load_and_index_documents
from query_engine import create_query_engine


def send_code(code):
    index = load_and_index_documents()
    engine = create_query_engine(index)
    code = (
        "DADO O SEGUINTE CÓDIGO EM C, REFATORE APLICANDO OS PRINCIPIOS DE CLEAN CODE, RESPONDA EM PORTUGUÊS, RESPONDA APENAS COM O CODIGO PRONTO:\n"
        + code
    )
    reply = engine.query(code)
    return reply
