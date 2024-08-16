from .vector_store import add_documents_to_vectorstore

async def add_service_documents(documents, service_name):
    await add_documents_to_vectorstore(documents, service_name)

# Добавьте другие функции для управления документами, если необходимо