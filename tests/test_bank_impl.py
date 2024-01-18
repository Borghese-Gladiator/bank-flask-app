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


import unittest

class TestAccountManager(unittest.TestCase):
    def setUp(self):
        # Assuming AccountManager is the class under test
        self.account_manager = AccountManager()

    # Existing tests...

    def test_withdraw(self):
        # Test withdraw method
        self.account_manager.bank = {"acc1": 100}
        result = self.account_manager.withdraw(123456, "acc1", 50)
        self.assertEqual(result, "acc1")
        self.assertEqual(self.account_manager.bank["acc1"], 50)

        # Test withdraw for non-existent account
        result = self.account_manager.withdraw(123456, "acc2", 50)
        self.assertIsNone(result)  # Assert None for non-existent account

    def test_schedule_deposit(self):
        # Test schedule_deposit method
        result = self.account_manager.schedule_deposit(123456, "acc1", 50)
        self.assertTrue(result)  # Assert True for successful deposit scheduling
        self.assertIsInstance(self.account_manager.scheduled[-1], Deposit)  # Assuming Deposit is the payment type

    def test_schedule_transfer(self):
        # Test schedule_transfer method
        result = self.account_manager.schedule_transfer(123456, "from_acc", "to_acc", 30)
        self.assertTrue(result)  # Assert True for successful transfer scheduling
        self.assertIsInstance(self.account_manager.scheduled[-1], Transfer)  # Assuming Transfer is the payment type

    def test_schedule_withdraw(self):
        # Test schedule_withdraw method
        self.account_manager.bank = {"acc1": 100}
        result = self.account_manager.schedule_withdraw(123456, "acc1", 50)
        self.assertTrue(result)  # Assert True for successful withdrawal scheduling
        self.assertIsInstance(self.account_manager.scheduled[-1], Withdraw)  # Assuming Withdraw is the payment type

    def test_cancel_payment(self):
        # Test cancel_payment method
        payment = Deposit("payment1", 123456, "acc1", 50)  # Mock payment
        self.account_manager.transactions.append(payment)
        result = self.account_manager.cancel_payment(123456, "payment1")
        self.assertTrue(result)  # Assert True for successful payment cancellation
        self.assertIsInstance(self.account_manager.scheduled[-1], InversePayment)  # Assuming InversePayment is the inverse payment type

if __name__ == '__main__':
    unittest.main()
