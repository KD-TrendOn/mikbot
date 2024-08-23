import os
from typing import List, Dict
from langchain.document_loaders import (
    CSVLoader, JSONLoader, Docx2txtLoader, UnstructuredExcelLoader,
    PyMuPDFLoader, TextLoader, UnstructuredPowerPointLoader, NotebookLoader, BSHTMLLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pandas as pd
from ..tools.wrapper import ToolWrapper
from ..database.crud import get_or_create_service, save_tool
from ..services.vector_store import add_documents_to_vectorstore
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.router import update_router_parser
class DataAbstraction:
    def __init__(self, filename: str):
        self.type = filename.split('.')[-1]
        self.filename = filename
        self.sql_like = self.type in ["csv", "json", "xlsx"]

    def get_loader(self):
        loaders = {
            "csv": CSVLoader,
            "json": JSONLoader,
            "docx": Docx2txtLoader,
            "xlsx": UnstructuredExcelLoader,
            "pdf": PyMuPDFLoader,
            "txt": TextLoader,
            "pptx": UnstructuredPowerPointLoader,
            "ipynb": NotebookLoader,
            "html": BSHTMLLoader
        }
        loader_class = loaders.get(self.type, TextLoader)
        if self.type == "json":
            return loader_class(file_path=self.filename, text_content=False).load()
        elif self.type == "xlsx":
            return loader_class(self.filename, mode="elements").load()
        else:
            return loader_class(self.filename).load()

    def get_df(self):
        if self.type in ["csv", "json", "xlsx"]:
            return pd.read_csv(self.filename)
        return None

async def create_service(
    db: AsyncSession,
    service_name: str,
    file_paths: List[str],
    tools: List[ToolWrapper],
    prompt: str,
    documentation: str
):
    # Create or get the service
    service = await get_or_create_service(db, service_name, prompt, documentation)

    # Process documents
    all_docs = []
    for file_path in file_paths:
        data = DataAbstraction(file_path)
        docs = data.get_loader()
        all_docs.extend(docs)

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)

    # Prepare documents for vector store
    vector_docs = [
        Document(
            page_content=split.page_content,
            metadata={**split.metadata, "service": service_name}
        )
        for split in splits
    ]

    # Add documents to vector store
    await add_documents_to_vectorstore(vector_docs, service_name)

    # Save tools
    for tool in tools:
        await save_tool(db, tool, service.id)
    await update_router_parser(db)

    return service

# Делаем анализатора финансов, автокнопку, техподдержку
async def init_real_services(db: AsyncSession):
    from ..tools.wrapper import ToolWrapper
    from ..test_data import (
        get_account_balance, transfer_money,
        get_parking_info, reserve_parking_spot,
        AccountBalanceInput, TransferMoneyInput,
        ParkingInfoInput, ReserveParkingSpotInput
    )

    # Accounts service
    await create_service(
        db,
        "Finance analyzer",
        [],
        [
            ToolWrapper(
                name="get_account_balance",
                description="Получает баланс счета по номеру счета",
                function=get_account_balance,
                input_schema=AccountBalanceInput
            ),
            ToolWrapper(
                name="transfer_money",
                description="Переводит деньги с одного счета на другой",
                function=transfer_money,
                input_schema=TransferMoneyInput
            )
        ],
        prompt="Вы ассистент по банковским счетам. Помогите пользователю с вопросами о балансе и переводах.",
        documentation="Подробная документация о работе с банковскими счетами..."
    )

    # Parking service
    await create_service(
        db,
        "parking",
        [],
        [
            ToolWrapper(
                name="get_parking_info",
                description="Получает информацию о парковке по её ID",
                function=get_parking_info,
                input_schema=ParkingInfoInput
            ),
            ToolWrapper(
                name="reserve_parking_spot",
                description="Резервирует место на парковке для пользователя",
                function=reserve_parking_spot,
                input_schema=ReserveParkingSpotInput
            )
        ],
        prompt="Вы ассистент по парковкам. Помогите пользователю найти информацию о парковках и зарезервировать место.",
        documentation="Подробная документация о системе парковок..."
    )

    print("Реальные сервисы успешно инициализированы")
