import abc
from typing import Dict, List, Union

class Bank(abc.ABC):
    @abc.abstractmethod
    def create_account(self) -> str:
        pass
    
    @abc.abstractmethod
    def close_account(self, account_id: str) -> bool:
        pass
    
    @abc.abstractmethod
    def top_ranked(self, num_accounts: int) -> List[str]:
        pass

    @abc.abstractmethod
    def deposit(self, timestamp: int, account_id: str, amount: int) -> bool:
        pass

    @abc.abstractmethod
    def withdraw(self, timestamp: int, account_id: str, amount: int) -> bool:
        pass

    @abc.abstractmethod
    def transfer(self, timestamp: int, from_account_id: str, to_account_id: str, amount: int) -> bool:
        pass

    @abc.abstractmethod
    def schedule_deposit(self, timestamp: int, account_id: str, amount: int):
        pass

    @abc.abstractmethod
    def schedule_transfer(self, timestamp: int, from_account_id: str, to_account_id: str, amount: int) -> bool:
        pass
    
    @abc.abstractmethod
    def schedule_withdraw(self, timestamp: int, account_id: str, amount: int):
        pass
    
    @abc.abstractmethod
    def cancel_payment(self, timestamp: int, payment_id: str) -> bool:
        pass

    @abc.abstractmethod
    def check_balance(self, timestamp: int, account_id: str) -> float:
        pass

    @abc.abstractmethod
    def transaction_history(self, timestamp: int, account_id: str) -> List[Dict[str, Union[int, str, float]]]:
        pass
