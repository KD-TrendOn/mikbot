import os
from typing import List, Dict
from langchain.document_loaders import (
    CSVLoader,
    JSONLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
    NotebookLoader,
    BSHTMLLoader,
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
        self.type = filename.split(".")[-1]
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
            "html": BSHTMLLoader,
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
    documentation: str,
):
    # Create or get the service
    service = await get_or_create_service(db, service_name, prompt, documentation)

    # Process documents
    # all_docs = []
    # for file_path in file_paths:
    #     data = DataAbstraction(file_path)
    #     docs = data.get_loader()
    #     all_docs.extend(docs)

    # # Split documents
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    # splits = text_splitter.split_documents(all_docs)

    # # Prepare documents for vector store
    # vector_docs = [
    #     Document(
    #         page_content=split.page_content,
    #         metadata={**split.metadata, "service": service_name},
    #     )
    #     for split in splits
    # ]

    # Add documents to vector store
    # await add_documents_to_vectorstore(vector_docs)

    # Save tools
    for tool in tools:
        await save_tool(db, tool, service.id)
    await update_router_parser(db)

    return service


# Делаем анализатора финансов, автокнопку, техподдержку
async def init_real_services(db: AsyncSession):
    from ..tools.wrapper import ToolWrapper
    from ..test_data import (
        EmptyInput,
        SupportInput,
        PieChartInput,
        LineChartInput,
        card_info_button,
        kindergarten_button,
        library_card_button,
        taxes_payment_button,
        home_gas_payment_button,
        transfer_payment_button,
        communal_services_button,
        traffic_fine_payment_button,
        balance_replenishment_button,
        internet_replenishment_button,
        educational_card_replenishment_button,
        public_transport_card_replenishment_button,
        pie_chart,
        line_chart,
        contact_tech_support,
    )

    # Accounts service
    await create_service(
        db,
        "Анализ доходов и расходов и советы по финансовому плану",
        [],
        [
            ToolWrapper(
                name="pie_chart",
                description="Генерирует удобный pie график по какому то срезу транзакций пользователя",
                function=pie_chart,
                input_schema=PieChartInput,
            ),
            ToolWrapper(
                name="line_chart",
                description="Генерирует удобный линейный график баланса пользователя. Помогает отследить тенденцию баланса пользователя.",
                function=line_chart,
                input_schema=LineChartInput,
            ),
        ],
        prompt="""Ты - помощник пользователя по финансам. Ты работаешь с двумя таблицами - таблицей расходов и таблицей доходов пользователя.
        Схема таблиц выглядит так: date, amount, category.
        Категории расходов и сумма затрат за весь учетный период:
        Перевод 27955
        Оплата Продуктовый 42044
        Оплата Ресторан 23511
        Оплата Аптека 12862
        Онлайн оплата 7877
        Оплата Развлечения 8755
        Оплата Ювелирный 11230
        Категории дохождов и сумма доходов за весь учетный период:
        Перевод 93170
        Заработная плата 450000
        Кэшбек 77073
        Стипендия 45000
        Дивиденды 49474
        Тебе даны функции для показа специальной статистики финансах пользователя.
        
        Твоя задача ответить на запрос пользователя.

        Если пользователь требует график - используй инструменты, но только когда требуется.
        

        Если используешь инструменты: поле description каждой функции будет показано пользователю после выполнения функции.
        Если используешь инструменты, используй это поле, чтобы продолжить диалог с пользователем, объяснить результаты и предложить дальнейшие действия. Например указать крупнейшую по сумме категорию, сделать вывод из тенденции или баланса счета пользователя.
        Ответь на вопрос пользователя или вызови инструмент, если требуются графики""",
        documentation="""Сервис для помощи пользователю с финансовым учетом и финансовыми целями и накоплениями.
        Этот сервис НЕ выполняет операции по переводу денег или оплате услуг.
        Он занимается анализом доходов и расходов, предоставлением статистики и советами по финансовому планированию.

        Примеры запросов, которые обрабатывает этот сервис:
        - Покажи мои расходы за последний месяц
        - Сколько я потратил на продукты в этом году?
        - Какая категория расходов у меня самая большая?
        - Помоги составить финансовый план на следующий месяц
        - Как мне сократить расходы?
        - Сколько я могу откладывать ежемесячно?
        - Покажи динамику моего баланса за последние полгода""",
    )
    # Parking service
    await create_service(
        db,
        "Бот навигатор по приложению",
        [],
        [
            ToolWrapper(
                name="contact_tech_support",
                description="Отправляет запрос на который тебе сложно было ответить в обращение в техподдержку",
                function=contact_tech_support,
                input_schema=SupportInput,
            ),
            ToolWrapper(
                name="card_info_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с информацией по банковской карте",
                function=card_info_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="kindergarten_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой детского сада",
                function=kindergarten_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="library_card_button",
                description="Отправляет пользователю быструю кн опку отсылающую его на страницу с читательским билетом",
                function=library_card_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="taxes_payment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой налогов и штрафов",
                function=taxes_payment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="home_gas_payment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой Газа по штрих коду",
                function=home_gas_payment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="transfer_payment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с Переводом на другую карту",
                function=transfer_payment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="communal_services_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой ЖКХ",
                function=communal_services_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="traffic_fine_payment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой штрафов ГИБДД",
                function=traffic_fine_payment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="balance_replenishment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с пополнением баланса карты",
                function=balance_replenishment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="internet_replenishment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с пополнением интернет провайдера",
                function=internet_replenishment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="educational_card_replenishment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой образовательной карты",
                function=educational_card_replenishment_button,
                input_schema=EmptyInput,
            ),
            ToolWrapper(
                name="public_transport_card_replenishment_button",
                description="Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой транспортной карты",
                function=public_transport_card_replenishment_button,
                input_schema=EmptyInput,
            ),
        ],
        prompt="""Ты помощник пользователя по навигации в приложении.
        Ты находишься в мобильном приложении для Android и IOS Карты жителя Республики Татарстан.
        Карта жителя Татарстана - банковские и социальные сервисы в одном приложении
        • Выпустите цифровую Карту жителя или закажите пластиковую карту с курьерской доставкой
        • Получайте бонусы за рекомендацию карты жителя
        • Выпустите карту жителя для себя и ребенка
        • Отслеживайте операции по карте жителя и детской карте жителя
        • Узнайте об акциях и специальных предложениях от наших партнёров в разделе "Акции"
        • Узнайте, какие льготы вам положены, и подайте заявку на их получение
        • Сохраните читательский билет Национальной библиотеки РТ в электронном формате
        • Совершайте платежи без комиссии
        • Сохраняйте образовательную карту ребенка в мобильном приложении и отслеживайте баланс по карте, а также расходы на питание в школьной столовой. Пополняйте образовательную карту в пару кликов с вашей карты жителя
        • Объединяйте детскую карту жителя вашего ребенка с образовательной картой, ваш ребенок сможет использовать детскую карту жителя как в школе так и в торговых сетях
        • Подключайте автопополнение образовательной карт и управляйте им прямо из приложения

        Интерфейс приложения Карты жителя татарстан:
        - Кнопка на нижней панели "Главное" cодержит в себе:
            - Банковская карта
            - Другие карты
            - Портал "Забота". Социальные льготы и начисления
            - Читательский билет. Сохранение читательского билета в электронном формате
        - Кнопка на нижней панели "Платежи" содержит ссылки на оплату данных услуг:
            - Детский сад
            - Транспортная карта
            - Обркарта
            - ЖКХ
            - Газ по штрих-коду
            - Штрафы ГИБДД
            - Налоги, штрафы, госплатежи
            - Интернет
            - Телевидение
            - Домашний телефон
        - Кнопка на нижней панели "Акции" содержит в себе:
            - Список акций партнеров
            - Карта с точками, магазинами партнеров и их акциями
        - Кнопка на нижней панели "Новости" содержит в себе:
            - Новости
        Важно: поле description каждой функции будет показано пользователю после показанного виджета.
        Используй это поле, чтобы продолжить диалог с пользователем, объяснить результаты и предложить дальнейшие действия или предупредить о возможных рисках.
        """,
        documentation="""Сервис помогающий с навигацией и основными вопросами по приложению.
        Также может обрабатывать запросы в техподдержку и предоставлять быстрые кнопки для перехода к различным функциям приложения.

        Примеры запросов, которые обрабатывает этот сервис:
        - Как пополнить баланс карты?
        - Где найти информацию о моей карте?
        - Как оплатить детский сад?
        - Где посмотреть мой читательский билет?
        - Как оплатить коммунальные услуги?
        - Где найти акции партнеров?
        - Как связаться с техподдержкой?
        - Как перевести деньги на другую карту?
        - Где посмотреть мои льготы?""",
    )
    #
    await create_service(
        db=db,
        service_name="Всё остальное",
        file_paths=[],
        tools=[],  # Быть осторожнее. Тут записаны текстом доступные сервисы
        prompt="Твоя задача отвечать в доброй манере о том, что к сожалению ты не можешь ответить на текущий запрос пользователя, но обязательно уведомишь его, как только появиться возможность исполнить данный пользователем запрос.",
        documentation="Сервис, который вызывается если другие сервисы не подходят под запрос пользователя.",
    )
    print("Реальные сервисы успешно инициализированы")
