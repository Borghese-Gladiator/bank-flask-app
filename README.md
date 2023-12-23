# Bank Flask App
CodeSignal interview asked me to build a bank app and I struggled quite a bit, so I'm building a better implementation here.

Features
- Create accounts to track balances
- Ranking
- Scheduled payment

## Functionality
code signal methods
```python
def deposit(timestamp: int, account_id: str, amount: float) -> bool
def transfer(timestamp: int, from_account_id: str, to_account_id: str, amount: float) -> bool
def top_rank(num_accounts: int) -> List[str]
def schedule_payment(timestamp: int, from_account_id: str, to_account_id: str, amount: float) -> bool
def cancel_payment(timestamp: int, payment_id: str) -> bool
```

new methods
```python
def create_account(timestamp: int) -> str:
def close_account(timestamp: int, account_id: str) -> bool:
def withdraw(timestamp: int, account_id: str, amount: float) -> bool:
def schedule_withdraw(timestamp: int, account_id: str, amount: float) -> bool
def schedule_deposit(timestamp: int, account_id: str, amount: float) -> bool
def check_balance(timestamp: int, account_id: str) -> float:
def transaction_history(timestamp: int, account_id: str) -> List[Dict[str, Union[str, float, datetime]]]:
```

# Notes

## Steps to Build
- `mkdir bank-flask-app && cd ./bank-flask-app`
- `poetry new .`
- `poetry add flask`
- write app
  - `__init__.py`
  - `app.py`
  - `bank.py`
  - `bank_impl.py`
- `poetry shell`
- `python -m flask --app bank_flask_app run --port 8000 --debug`
- write tests
  - `test_bank_impl.py`
- `poetry run python -m unittest  # run at root (bank_flask_app) `

## References
- https://realpython.com/flask-project/