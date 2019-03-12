# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from echopy.echoapi.ws.exceptions import RPCError
from lemoncheesecake.matching import check_that, is_not_none, this_dict, check_that_entry, is_integer, is_str, \
    has_entry

from common.base_test import BaseTest
from common.echo_operation import EchoOperations

SUITE = {
    "description": "Method 'get_required_fee'"
}


@lcc.prop("testing", "main")
@lcc.tags("get_required_fees")
@lcc.suite("Check work of method 'get_required_fees'", rank=3)
class GetRequiredFees(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.echo_operations = EchoOperations()
        self.asset = "1.3.0"

    @lcc.prop("type", "method")
    @lcc.test("Simple work of method 'get_required_fees'")
    # @lcc.depends_on("DatabaseApi.connection_to_database_api")  # todo: add with new release lcc
    def method_main_check(self):
        lcc.set_step("Get required fee for default 'transfer_operation'")
        response_id = self.send_request(self.get_request("get_required_fees", [
            [self.echo_operations.get_operation_json("transfer_operation", example=True),
             self.echo_operations.get_operation_json("transfer_operation", example=True)], self.asset]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)

        lcc.set_step("Check simple work of method 'get_required_fees'")
        for i in range(len(response["result"])):
            required_fee = response["result"][i]
            with this_dict(required_fee):
                check_that_entry("amount", is_integer())
                check_that_entry("asset_id", is_str(self.asset))


@lcc.prop("testing", "positive")
@lcc.tags("get_required_fees")
@lcc.suite("Positive testing of method 'get_required_fees'", rank=4)
class PositiveTesting(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.echo_operations = EchoOperations()
        self.amount = 1
        self.asset = "1.3.0"
        self.account_id1 = self.get_account_id("test-echo-1", self.__database_api_identifier,
                                               self.__registration_api_identifier)
        self.account_id2 = self.get_account_id("test-echo-2", self.__database_api_identifier,
                                               self.__registration_api_identifier)
        self.operation = None
        self.required_fee = None

    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.operation = self.echo_operations.get_transfer_operation(echo=self.echo, from_account_id=self.account_id1,
                                                                     to_account_id=self.account_id2, amount=self.amount)
        self.required_fee = self.get_required_fee(self.operation, self.__database_api_identifier)
        lcc.log_info("Required fee for transfer transaction: '{}'".format(self.required_fee))

    def teardown_suite(self):
        self._disconnect_to_echopy_lib()
        super().teardown_suite()

    @lcc.prop("type", "method")
    @lcc.test("Fee equal to get_required_fee in transfer operation")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def fee_equal_to_get_required_fee(self):
        lcc.set_step("Send transfer transaction with a fee equal to the 'get_required_fee'")
        self.add_fee_to_operation(self.operation, self.__database_api_identifier,
                                  fee_amount=(self.required_fee[0].get("amount")))
        broadcast_result = self.echo_operations.broadcast(echo=self.echo, list_operations=self.operation,
                                                          log_broadcast=False)
        check_that(
            "broadcast transaction complete successfully",
            broadcast_result["trx"], is_not_none(), quiet=True
        )

    @lcc.prop("type", "method")
    @lcc.test("Fee higher than get_required_fee in transfer operation")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def fee_higher_than_get_required_fee(self):
        lcc.set_step("Send transfer transaction with a higher fee than the 'get_required_fee'")
        self.add_fee_to_operation(self.operation, self.__database_api_identifier,
                                  fee_amount=(self.required_fee[0].get("amount") + 1))
        broadcast_result = self.echo_operations.broadcast(echo=self.echo, list_operations=self.operation,
                                                          log_broadcast=False)
        check_that(
            "broadcast transaction complete successfully",
            broadcast_result["trx"], is_not_none(), quiet=True
        )


@lcc.prop("testing", "negative")
@lcc.tags("get_required_fees")
@lcc.suite("Negative testing of method 'get_required_fees'", rank=4)
class NegativeTesting(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.echo_operations = EchoOperations()
        self.amount = 1
        self.asset = "1.3.0"
        self.account_id1 = self.get_account_id("test-echo-1", self.__database_api_identifier,
                                               self.__registration_api_identifier)
        self.account_id2 = self.get_account_id("test-echo-2", self.__database_api_identifier,
                                               self.__registration_api_identifier)
        self.operation = None
        self.contract = self.get_byte_code("piggy_code")
        self.valid_contract_id = None
        self.nonexistent_asset_id = None
        self.required_fee = None

    def get_nonexistent_asset_id(self):
        list_asset_ids = []
        response_id = self.send_request(self.get_request("list_assets", ["", 100]), self.__database_api_identifier)
        response = self.get_response(response_id)
        for i in range(len(response["result"])):
            list_asset_ids.append(response["result"][i]["id"])
        sorted_list_asset_ids = sorted(list_asset_ids, key=self.get_value_for_sorting_func)
        return "1.3.{}".format(str(int(sorted_list_asset_ids[-1][4:]) + 1))

    def get_valid_contract_id(self, registrar, contract):
        operation = self.echo_operations.get_create_contract_operation(echo=self.echo, registrar=registrar,
                                                                       bytecode=contract, fee_amount=500)
        broadcast_result = self.echo_operations.broadcast(echo=self.echo, list_operations=operation,
                                                          log_broadcast=False)
        contract_result = self.get_contract_result(broadcast_result)
        response_id = self.send_request(self.get_request("get_contract_result", contract_result),
                                        self.__database_api_identifier)
        contract_id_16 = self.get_trx_completed_response(response_id)
        return self.get_contract_id(contract_id_16)

    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.nonexistent_asset_id = self.get_nonexistent_asset_id()
        lcc.log_info("Nonexistent asset id: '{}'".format(self.nonexistent_asset_id))
        self.operation = self.echo_operations.get_transfer_operation(echo=self.echo, from_account_id=self.account_id1,
                                                                     to_account_id=self.account_id2, amount=self.amount)
        self.required_fee = self.get_required_fee(self.operation, self.__database_api_identifier)
        self.valid_contract_id = self.get_valid_contract_id(self.account_id1, self.contract)
        lcc.log_info("Valid contract id: '{}'".format(self.valid_contract_id))

    def teardown_suite(self):
        lcc.set_step("Teardown suite for {}".format(self.__class__.__name__))
        self._disconnect_to_echopy_lib()
        super().teardown_suite()

    @lcc.prop("type", "method")
    @lcc.test("Use in method call nonexistent asset_id")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def nonexistent_asset_id_in_method_call(self):
        lcc.set_step("Get required fee for default 'transfer_operation' but with nonexistent asset_id")
        response_id = self.send_request(self.get_request("get_required_fees", [
            [self.echo_operations.get_operation_json("transfer_operation", example=True)], self.nonexistent_asset_id]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id, negative=True)
        check_that(
            "'get_required_fees' return error message",
            response, has_entry("error"), quiet=True,
        )

    @lcc.prop("type", "method")
    @lcc.test("Fee lower than get_required_fee in transfer operation")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def fee_lower_than_get_required_fee(self):
        lcc.set_step("Send transfer transaction with a lower fee than the 'get_required_fee'")
        self.add_fee_to_operation(self.operation, self.__database_api_identifier,
                                  fee_amount=(self.required_fee[0].get("amount") - 1))
        try:
            self.echo_operations.broadcast(echo=self.echo, list_operations=self.operation)
            lcc.log_error("Error: broadcast transaction complete with insufficient.")
        except RPCError:
            lcc.log_info("Insufficient Fee Paid. Correct behavior.")

    @lcc.prop("type", "method")
    @lcc.test("Nonexistent contract byte code")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def nonexistent_contract_byte_code(self):
        # todo change on get_random_hex_string. Bug: "ECHO-653"
        not_valid_contract = "6e5964425a64326457664a44516474594a615878"

        lcc.set_step("Get required fee for 'create_contract_operation' with nonexistent byte code")
        operation = self.echo_operations.get_create_contract_operation(echo=self.echo, registrar=self.account_id1,
                                                                       bytecode=not_valid_contract)
        response_id = self.send_request(self.get_request("get_required_fees", [[operation], self.asset]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id, negative=True)
        check_that(
            "'get_required_fees' return error message",
            response, has_entry("error"), quiet=True
        )

    @lcc.prop("type", "method")
    @lcc.test("Nonexistent asset id")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def nonexistent_asset_id_in_operation(self):
        lcc.set_step("Get required fee for 'create_contract_operation' with nonexistent asset in operation")
        operation = self.echo_operations.get_create_contract_operation(echo=self.echo, registrar=self.account_id1,
                                                                       bytecode=self.contract, value_amount=self.amount,
                                                                       value_asset_id=self.nonexistent_asset_id)
        response_id = self.send_request(self.get_request("get_required_fees", [[operation], self.asset]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id, negative=True)
        check_that(
            "'get_required_fees' return error message",
            response, has_entry("error"), quiet=True
        )

    @lcc.prop("type", "method")
    @lcc.test("Nonexistent method byte code")
    # @lcc.depends_on("DatabaseApi.GetRequiredFees.GetRequiredFees.method_main_check")  # todo: add with new release lcc
    def nonexistent_method_byte_code(self, get_random_hex_string):
        lcc.set_step("Get required fee for 'call_contract_operation' with nonexistent method byte code")
        operation = self.echo_operations.get_call_contract_operation(echo=self.echo, registrar=self.account_id1,
                                                                     bytecode=get_random_hex_string,
                                                                     callee=self.get_valid_contract_id(self.account_id1,
                                                                                                       self.contract))
        response_id = self.send_request(self.get_request("get_required_fees", [[operation], self.asset]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id, negative=True, log_response=True)
        check_that(
            "'get_required_fees' return error message",
            response, has_entry("error"), quiet=True
        )
