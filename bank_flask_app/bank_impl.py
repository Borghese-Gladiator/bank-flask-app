import abc
import math
from typing import Deque, Dict, List, Optional, Union

from bank_flask_app.bank import Bank


#=================
#  UTILS
#=================
class Account:
    def __init__(self, account_id, amount=100, outgoing=0):
        self.account_id = account_id
        self.amount = amount
        self.outgoing = outgoing

    def __repr__(self):
        return f"<Account at {self.account_id}>"
class Payment(abc.ABC):
    def __init__(self, payment_id: str, timestamp: int, amount=0):
        self.payment_id = payment_id
        self.timestamp = timestamp
    
    def get_inverse(self, payment_id, timestamp):
        return Payment(payment_id, timestamp, -self.amount)

    def execute(self, bank: Dict[str, Account]) -> Optional[bool]:
        pass

class Transfer(Payment):
    def __init__(self, payment_id: str, timestamp: int, from_account_id: str, to_account_id: str, amount=0):
        super().__init__(payment_id, timestamp, amount)
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
    
    def execute(self, bank: Dict[str, Account]) -> Optional[bool]:
        if self.from_account_id not in bank\
            or self.to_account_id not in bank\
            or bank[self.from_account_id].amount < self.amount:
            return None
        bank[self.from_account_id].amount -= self.amount
        bank[self.from_account_id].outgoing += self.amount
        bank[self.to_account_id].amount += self.amount
        return True

class Deposit(Payment):
    def __init__(self, payment_id: str, timestamp: int, account_id: str, amount=0):
        super().__init__(payment_id, timestamp, amount)
        self.account_id = account_id
    
    def execute(self, bank: Dict[str, Account]) -> Optional[bool]:
        if self.account_id not in bank:
            return None
        bank[self.account_id].amount += self.amount
        return True

class Withdraw(Payment):
    def __init__(self, payment_id: str, timestamp: int, account_id: str, amount=0):
        super().__init__(payment_id, timestamp, amount)
        self.account_id = account_id
    
    def execute(self, bank: Dict[str, Account]) -> Optional[bool]:
        if self.account_id not in bank:
            return None
        bank[self.account_id].amount -= self.amount
        return True

"""
from collections import namedtuple
Account = namedtuple('Account', ['account_id', 'amount', 'outgoing'])
Payment = namedtuple('Payment', ['payment_id', 'amount', 'from_account_id', 'to_account_id'])
"""

class BankImpl(Bank):
    def __init__(self):
        # Maps account_id to Account
        self.bank: Dict[str, Account] = {}
        self.bank_count: int = 0
        
        # Maps timestamp to Payment
        self.scheduled: Dict[int, List[Payment]] = {}

        # Lists executed payments (deque enables O(1) insert at end since implemented as an LL)
        self.transactions: Deque[Payment] = []
    
    def create_account(self) -> str:
        self.bank_count += 1
        account_id = f"account{self.bank_count}"
        self.bank[account_id] = Account(account_id)
        return account_id

    def close_account(self, account_id: str) -> bool:
        if account_id not in self.bank:
            return False
        del self.bank[account_id]
        return True
    
    def top_ranked(self, num_accounts=math.inf) -> List[str]:
        def account_sort(account: Account):
            return -account.outgoing, account.account_id
        def stringify(account_list: List[Account]) -> List[str]:
            return [f"<{account.account_id}:{account.outgoing}>" for account in account_list]
        sorted_accounts = sorted([account for account in self.bank.values()], key=account_sort)
        if len(sorted_accounts) < num_accounts:
            return stringify(sorted_accounts)
        return stringify(sorted_accounts[:num_accounts])

    def _execute_scheduled(self, timestamp: int):
        if timestamp in self.scheduled:
            payment_list: List[Payment] = self.scheduled[timestamp]
            del self.scheduled[timestamp]
            for payment in payment_list:
                payment.execute()

    def deposit(self, timestamp: int, account_id: str, amount: int) -> str:
        self._execute_scheduled(timestamp)
        
        if account_id not in self.bank:
            return None
        self.bank[account_id] += amount
        return account_id

    def transfer(self, timestamp: int, from_account_id: str, to_account_id: str, amount: int) -> str:
        self._execute_scheduled(timestamp)
        
        if from_account_id not in self.bank\
            or to_account_id not in self.bank\
            or self.bank[from_account_id].amount < amount:
            return None
        self.bank[from_account_id].amount -= amount
        self.bank[from_account_id].outgoing += amount
        self.bank[to_account_id].amount += amount
        return f"${amount} from {from_account_id} to {to_account_id}"

    def withdraw(self, timestamp: int, account_id: str, amount: int) -> bool:
        self._execute_scheduled(timestamp)

        if account_id not in self.bank:
            return None
        self.bank[account_id] -= amount
        self.bank[account_id].outgoing += amount
        return account_id

    def schedule_deposit(self, timestamp: int, account_id: str, amount: int) -> bool:
        payment: Payment = Deposit(f"payment{len(self.transactions)}", timestamp, account_id, amount)
        self.scheduled.append(payment)
        self.transactions.append(payment)
        return True
    
    def schedule_transfer(self, timestamp: int, from_account_id: str, to_account_id: str, amount: int) -> bool:
        payment: Payment = Transfer(f"payment{len(self.transactions)}", timestamp, from_account_id, to_account_id, amount)
        self.scheduled.append(payment)
        self.transactions.append(payment)
        return True
    
    def schedule_withdraw(self, timestamp: int, account_id: str, amount: int):
        payment: Payment = Withdraw(f"payment{len(self.transactions)}", timestamp, account_id, amount)
        self.scheduled.append(payment)
        self.transactions.append(payment)
        return True

    def cancel_payment(self, timestamp: int, payment_id: str) -> bool:
        payment: Payment = next((payment_id == payment.id for payment in self.transactions))
        if not payment:
            return False
        inverse_payment = payment.get_inverse(f"payment{len(self.transactions)}", timestamp)
        self.scheduled.append(inverse_payment)
        self.transactions.append(inverse_payment)
        return True

    def check_balance(self, timestamp: int, account_id: str) -> float:
        pass

    def transaction_history(self, account_id: str) -> List[Dict[str, Union[int, str, float]]]:
        pass

    # TESTING UTILS
    def _get_accounts(self):
        return self.bank.values()
    def _get_account_ids(self):
        return [account.account_id for account in self.bank.values()]

