# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_none, is_true, equal_to

from common.base_test import BaseTest

SUITE = {
    "description": "Method 'broadcast_transaction'"
}


@lcc.prop("testing", "main")
@lcc.prop("testing", "positive")
@lcc.prop("testing", "negative")
@lcc.tags("network_broadcast_api", "broadcast_transaction")
@lcc.suite("Check work of method 'broadcast_transaction'", rank=1)
class BroadcastTransaction(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.__registration_api_identifier = None
        self.__network_broadcast_identifier = None
        self.echo_acc0 = None
        self.echo_acc1 = None
        self.state = None

    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.__network_broadcast_identifier = self.get_identifier("network_broadcast")
        lcc.log_info(
            "API identifiers are: database='{}', registration='{}', network_broadcast='{}'".format(
                self.__database_api_identifier, self.__registration_api_identifier,
                self.__network_broadcast_identifier))
        self.echo_acc0 = self.get_account_id(self.accounts[0], self.__database_api_identifier,
                                             self.__registration_api_identifier)
        self.echo_acc1 = self.get_account_id(self.accounts[1], self.__database_api_identifier,
                                             self.__registration_api_identifier)
        lcc.log_info("Echo accounts are: #1='{}', #2='{}'".format(self.echo_acc0, self.echo_acc1))

    def teardown_suite(self):
        self._disconnect_to_echopy_lib()
        super().teardown_suite()

    @lcc.prop("type", "method")
    @lcc.test("Simple work of method 'broadcast_transaction'")
    def method_main_check(self, get_random_integer_up_to_ten):
        transfer_amount = get_random_integer_up_to_ten

        lcc.set_step("Create signed transaction of transfer operation")
        transfer_operation = self.echo_ops.get_transfer_operation(echo=self.echo, from_account_id=self.echo_acc0,
                                                                  to_account_id=self.echo_acc1, amount=transfer_amount)
        collected_operation = self.collect_operations(transfer_operation, self.__database_api_identifier)
        signed_tx = self.echo_ops.broadcast(echo=self.echo, list_operations=collected_operation, no_broadcast=True)
        lcc.log_info("Signed transaction of transfer operation created successfully")

        lcc.set_step("Get account balance before transfer transaction broadcast")
        response_id = self.send_request(self.get_request("get_account_balances", [self.echo_acc1, [self.echo_asset]]),
                                        self.__database_api_identifier)
        account_balance = self.get_response(response_id)["result"][0]["amount"]
        lcc.log_info("'{}' account has '{}' in '{}' assets".format(self.echo_acc1, account_balance, self.echo_asset))

        lcc.set_step("Broadcast signed transfer transaction")
        response_id = self.send_request(self.get_request("broadcast_transaction", [signed_tx]),
                                        self.__network_broadcast_identifier)
        result = self.get_response(response_id)["result"]
        lcc.log_info("Call method 'broadcast_transaction'")

        lcc.set_step("Check that transaction broadcast")
        check_that("'broadcast_transaction' result", result, is_none(), quiet=True)

        lcc.set_step("Get account balance after transfer transaction broadcast")
        response_id = self.send_request(self.get_request("get_account_balances", [self.echo_acc1, [self.echo_asset]]),
                                        self.__database_api_identifier)
        updated_account_balance = self.get_response(response_id)["result"][0]["amount"]
        lcc.log_info(
            "'{}' account has '{}' in '{}' assets".format(self.echo_acc1, updated_account_balance, self.echo_asset))

        lcc.set_step("Check that transfer operation completed successfully")
        check_that("'account balance increased by transfer assets'",
                   (account_balance + transfer_amount) == updated_account_balance, is_true(), quiet=True)


@lcc.prop("suite_run_option_3", "negative")
@lcc.tags("network_broadcast_api", "broadcast_transaction")
@lcc.suite("Negative testing of method 'broadcast_transaction'", rank=2)
class NegativeTesting(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.__registration_api_identifier = None
        self.__network_broadcast_identifier = None
        self.echo_acc0 = None
        self.echo_acc1 = None

    @staticmethod
    def get_trx_without_sign_info_from_notice(notice):
        trx = deepcopy(notice["trx"])
        del trx["signed_with_echorand_key"]
        del trx["operation_results"]
        del trx["fees_collected"]
        return trx

    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.__network_broadcast_identifier = self.get_identifier("network_broadcast")
        lcc.log_info(
            "API identifiers are: database='{}', registration='{}', network_broadcast='{}'".format(
                self.__database_api_identifier, self.__registration_api_identifier,
                self.__network_broadcast_identifier))
        self.echo_acc0 = self.get_account_id(self.accounts[0], self.__database_api_identifier,
                                             self.__registration_api_identifier)
        self.echo_acc1 = self.get_account_id(self.accounts[1], self.__database_api_identifier,
                                             self.__registration_api_identifier)
        lcc.log_info("Echo accounts are: #1='{}', #2='{}'".format(self.echo_acc0, self.echo_acc1))

    def setup_test(self, test):
        lcc.set_step("Setup for '{}'".format(str(test).split(".")[-1]))
        self.utils.cancel_all_subscriptions(self, self.__database_api_identifier)
        lcc.log_info("Canceled all subscriptions successfully")

    def teardown_test(self, test, status):
        lcc.set_step("Teardown for '{}'".format(str(test).split(".")[-1]))
        self.utils.cancel_all_subscriptions(self, self.__database_api_identifier)
        lcc.log_info("Canceled all subscriptions successfully")
        lcc.log_info("Test {}".format(status))

    def teardown_suite(self):
        self._disconnect_to_echopy_lib()
        super().teardown_suite()

    @lcc.prop("type", "method")
    @lcc.test("Negative test 'broadcast_transaction' with wrong signature")
    @lcc.depends_on(
        "NetworkBroadcastApi.BroadcastTransaction.BroadcastTransaction.method_main_check")
    def check_broadcast_transaction_with_callback_with_wrong_signature(self, get_random_integer_up_to_ten):
        transfer_amount = get_random_integer_up_to_ten
        expected_message = "irrelevant signature included: Unnecessary signature(s) detected"
        transfer_operation = self.echo_ops.get_transfer_operation(echo=self.echo, from_account_id=self.echo_acc0,
                                                                  amount=transfer_amount, to_account_id=self.echo_acc1,
                                                                  signer=self.echo_acc1)
        collected_operation = self.collect_operations(transfer_operation, self.__database_api_identifier)

        lcc.set_step("Broadcast transfer transaction to get error message")
        try:
            self.echo_ops.broadcast(echo=self.echo, list_operations=collected_operation)
        except Exception as e:
            check_that("message", str(e), equal_to(expected_message))

    @lcc.prop("type", "method")
    @lcc.test("Negative test 'broadcast_transaction' with wrong expiration time")
    @lcc.depends_on(
        "NetworkBroadcastApi.BroadcastTransaction.BroadcastTransaction.method_main_check")
    def check_broadcast_transaction_with_callback_with_wrong_expiration_time(self, get_random_integer_up_to_ten):
        transfer_amount = get_random_integer_up_to_ten
        expiration_time_offset = 10
        expected_message = "Assert Exception: now <= trx.expiration: "
        transfer_operation = self.echo_ops.get_transfer_operation(echo=self.echo, from_account_id=self.echo_acc0,
                                                                  amount=transfer_amount, to_account_id=self.echo_acc1)
        collected_operation = self.collect_operations(transfer_operation, self.__database_api_identifier)
        datetime_str = self.get_datetime(global_datetime=True)
        datetime_str = self.subtract_from_datetime(datetime_str, seconds=expiration_time_offset)
        lcc.set_step("Broadcast transfer transaction to get error message")
        try:
            self.echo_ops.broadcast(echo=self.echo, list_operations=collected_operation, expiration=datetime_str)
        except Exception as e:
            check_that("message", str(e), equal_to(expected_message))
