import unittest

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
        self.assertListEqual(self.bank._get_account_ids(), ["account1", "account2"], "Failed to create two accounts")
        
        # close accounts
        self.bank.close_account("account2")
        self.assertListEqual(self.bank._get_account_ids(), ["account1"], "Failed to delete one account")
        
    def test_top_rank(self):
        account_id_1 = self.bank.create_account()
        account_id_2 = self.bank.create_account()
        account_id_3 = self.bank.create_account()
        self.bank.transfer(1, account_id_1, account_id_2, 20)
        self.bank.transfer(1, account_id_2, account_id_3, 50)
        
        all_ranked = self.bank.top_ranked()
        self.assertListEqual(all_ranked, ["<account2:50>", "<account1:20>", "<account3:0>"], "Failed to rank all accounts")
        
        some_ranked = self.bank.top_ranked(2)
        self.assertListEqual(some_ranked, ["<account2:50>", "<account1:20>"], "Failed to rank subset of accounts")

if __name__ == '__main__':
    unittest.main()
