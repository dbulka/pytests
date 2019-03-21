# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_, is_integer, is_str, check_that_in, is_true

from common.base_test import BaseTest
from common.echo_operation import EchoOperations

SUITE = {
    "description": "Testing contract creation and calling its methods"
}


@lcc.prop("testing", "main")
@lcc.tags("hello_world")
@lcc.suite("Check scenario 'Hello World'")
class HelloWorld(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.echo_operations = EchoOperations()
        self.registrar = "test-echo-1"
        self.contract = self.get_byte_code("piggy_code")
        self.greet = self.get_byte_code("piggy_greet")
        self.get_pennie = self.get_byte_code("piggy_getPennie")
        self.break_piggy = self.get_byte_code("piggy_breakPiggy")
        self.asset = "1.3.0"
        self.value_amount = 10

    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.registrar = self.get_account_id(self.registrar, self.__database_api_identifier,
                                             self.__registration_api_identifier)

    def teardown_suite(self):
        self._disconnect_to_echopy_lib()
        super().teardown_suite()

    @lcc.prop("type", "scenario")
    @lcc.test("The scenario describes the mechanism of creating, deploying, "
              "and invoking a contract on the Echo network, written in Solidity.")
    def hello_world_scenario(self):
        lcc.set_step("Create 'Piggy' contract in the Echo network")
        operation = self.echo_operations.get_create_contract_operation(echo=self.echo, registrar=self.registrar,
                                                                       bytecode=self.contract,
                                                                       value_amount=self.value_amount,
                                                                       value_asset_id=self.asset)
        collected_operation = self.collect_operations(operation, self.__database_api_identifier)
        broadcast_result = self.echo_operations.broadcast(echo=self.echo, list_operations=collected_operation)
        contract_result = self.get_contract_result(broadcast_result, self.__database_api_identifier)
        contract_id = self.get_contract_id(contract_result)

        lcc.set_step("Call 'greet' method")
        operation = self.echo_operations.get_call_contract_operation(echo=self.echo, registrar=self.registrar,
                                                                     bytecode=self.greet, callee=contract_id)
        collected_operation = self.collect_operations(operation, self.__database_api_identifier)
        broadcast_result = self.echo_operations.broadcast(echo=self.echo, list_operations=collected_operation)
        contract_result = self.get_contract_result(broadcast_result, self.__database_api_identifier)

        lcc.set_step("Check get 'Hello World!!!'")
        contract_output = self.get_contract_output(contract_result, in_hex=False)[1:]
        check_that(
            "return of method 'greet'",
            contract_output,
            is_("Hello World!!!"),
        )

        lcc.set_step("Get contract balance and store")
        response_id = self.send_request(self.get_request("get_contract_balances", [contract_id]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)
        check_that_in(
            response["result"][0],
            "amount", is_integer(self.value_amount),
            "asset_id", is_str(self.asset)
        )
        contract_balance = response["result"][0]["amount"]

        lcc.set_step("Get owner balance and store")
        params = [self.registrar, [self.asset]]
        response_id = self.send_request(self.get_request("get_account_balances", params),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)
        check_that_in(
            response["result"][0],
            "amount", is_integer(),
            "asset_id", is_str(self.asset)
        )
        owner_balance = response["result"][0]["amount"]

        lcc.set_step("Call 'getPennie' method")
        operation = self.echo_operations.get_call_contract_operation(echo=self.echo, registrar=self.registrar,
                                                                     bytecode=self.get_pennie, callee=contract_id)
        fee = self.get_required_fee(operation, self.__database_api_identifier)
        collected_operation = self.collect_operations(operation, self.__database_api_identifier)
        self.echo_operations.broadcast(echo=self.echo, list_operations=collected_operation)

        lcc.set_step("Get contract. Amount should be reduced by one.")
        response_id = self.send_request(self.get_request("get_contract_balances", [contract_id]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)
        check_that_in(
            response.get("result")[0],
            "amount", is_integer(contract_balance - 1),
            "asset_id", is_str(self.asset)
        )

        lcc.set_step("Get owner balance. Amount should be reduced by fee and increase by one.")
        params = [self.registrar, [self.asset]]
        response_id = self.send_request(self.get_request("get_account_balances", params),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)
        check_that(
            "'owner balance'",
            response.get("result")[0].get("amount"),
            is_integer(owner_balance - fee[0].get("amount") + 1)
        )

        lcc.set_step("Destroy the contract. Call 'breakPiggy' method")
        operation = self.echo_operations.get_call_contract_operation(echo=self.echo, registrar=self.registrar,
                                                                     bytecode=self.break_piggy, callee=contract_id)
        collected_operation = self.collect_operations(operation, self.__database_api_identifier)
        self.echo_operations.broadcast(echo=self.echo, list_operations=collected_operation)

        lcc.set_step("Get contract balance, must be 0 (zero)")
        response_id = self.send_request(self.get_request("get_contract_balances", [contract_id]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)
        check_that(
            "'contract balance'",
            response["result"][0]["amount"],
            is_integer(0)
        )

        lcc.set_step("Check that contract to be 'suicided=True'")
        response_id = self.send_request(self.get_request("get_objects", [[contract_id]]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)
        check_that(
            "contract deleted and 'destroyed'",
            response["result"][0]["destroyed"],
            is_true()
        )