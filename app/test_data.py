from typing import Dict
from pydantic import BaseModel, Field
from .tools.wrapper import ToolWrapper

class AccountBalanceInput(BaseModel):
    account_number: str = Field(..., description="Номер счета")

class TransferMoneyInput(BaseModel):
    from_account: str = Field(..., description="Номер счета отправителя")
    to_account: str = Field(..., description="Номер счета получателя")
    amount: float = Field(..., description="Сумма перевода")

class ParkingInfoInput(BaseModel):
    parking_id: str = Field(..., description="ID парковки")

class ReserveParkingSpotInput(BaseModel):
    parking_id: str = Field(..., description="ID парковки")
    user_id: str = Field(..., description="ID пользователя")

def get_account_balance(account_number: str) -> Dict[str, float]:
    """
    Получает баланс счета по номеру счета.
    """
    balance = float(account_number) * 100  # Просто для примера
    return {"balance": balance}

def transfer_money(from_account: str, to_account: str, amount: float) -> Dict[str, str]:
    """
    Переводит деньги с одного счета на другой.
    """
    return {"status": "success", "message": f"Переведено {amount} с счета {from_account} на счет {to_account}"}

def get_parking_info(parking_id: str) -> Dict[str, str]:
    """
    Получает информацию о парковке по её ID.
    """
    return {"id": parking_id, "name": f"Парковка {parking_id}", "available_spots": "25"}

def reserve_parking_spot(parking_id: str, user_id: str) -> Dict[str, str]:
    """
    Резервирует место на парковке для пользователя.
    """
    return {"status": "success", "message": f"Место на парковке {parking_id} зарезервировано для пользователя {user_id}"}

# Словарь сервисов и их функций с соответствующими схемами ввода
test_services = {
    "accounts": [
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
    "parking": [
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
    ]
}

# Функция для инициализации тестовых данных в базе данных
async def init_test_data(db):
    from .database.crud import get_or_create_service, save_tool
    from .tools.wrapper import ToolWrapper

    for service_name, tools in test_services.items():
        service = await get_or_create_service(db, service_name, f"Это сервис {service_name}", f"Документация для сервиса {service_name}")
        
        for tool in tools:
            await save_tool(db, tool, service.id)

    print("Тестовые данные успешно инициализированы")
