import unittest
from unittest.mock import MagicMock
from typing import List

from bank_flask_app.bank_impl import BankImpl

class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = BankImpl()
    
    def test_account_creation(self):
        # create accounts
        account_id_1 = self.bank.create_account()
        self.assertEqual(account_id_1, "account1")
        account_id_2 = self.bank.create_account()
        self.assertEqual(account_id_2, "account2")
        account_ids = self.bank._get_account_ids()
        self.assertListEqual(account_ids, ["account1", "account2"], "Failed to create two accounts")
        
        # close accounts
        self.bank.close_account("account2")
        self.assertListEqual(account_ids, ["account1"], "Failed to delete one account")
        
    def test_top_rank(self):
        account_id_1 = self.bank.create_account()
        account_id_2 = self.bank.create_account()
        account_id_3 = self.bank.create_account()
        self.bank.transfer(1, account_id_1, account_id_2, 20)
        self.bank.transfer(1, account_id_2, account_id_3, 50)
        
        all_ranked = self.bank.top_ranked()
        self.assertListEqual(all_ranked, ["account2", "account1", "account3"], "Failed to rank all accounts")
        
        some_ranked = self.bank.top_ranked(2)
        self.assertListEqual(some_ranked, ["account2", "account1"], "Failed to rank subset of accounts")

if __name__ == '__main__':
    unittest.main()
