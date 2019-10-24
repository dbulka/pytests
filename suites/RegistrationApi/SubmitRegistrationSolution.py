# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_integer, is_true, equal_to

from common.base_test import BaseTest

SUITE = {
    "description": "Registration Api"
}


@lcc.prop("main", "type")
@lcc.tags("api", "notice", "registration_api", "submit_registration_solution")
@lcc.suite("Registration API", rank=1)
class SubmitRegistrationSolution(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.__registration_api_identifier = None

    def setup_suite(self):
        super().setup_suite()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        lcc.log_info(
            "API identifiers are: database='{}', registration='{}'".format(self.__database_api_identifier,
                                                                           self.__registration_api_identifier))

    @lcc.tags("submit_registration_solution")
    @lcc.test("Check method submit_registration_solution of registration_api")
    def method_main_check(self, get_random_integer, get_random_valid_account_name):
        callback = get_random_integer
        account_name = get_random_valid_account_name
        generate_keys = self.generate_keys()
        public_key = generate_keys[1]

        lcc.set_step("Get 'request_registration_task' and solve")
        response_id = self.send_request(self.get_request("request_registration_task"),
                                        self.__registration_api_identifier)
        pow_algorithm_data = self.get_response(response_id)["result"]
        solution = self.solve_registration_task(pow_algorithm_data["block_id"],
                                                pow_algorithm_data["rand_num"],
                                                pow_algorithm_data["difficulty"])
        check_that("registration task solution", solution, is_integer())

        lcc.set_step("Check that 'submit_registration_solution' completed successfully")
        account_params = [callback, account_name, public_key, public_key, solution, pow_algorithm_data["rand_num"]]
        response_id = self.send_request(self.get_request("submit_registration_solution", account_params),
                                        self.__registration_api_identifier)
        result = self.get_response(response_id)["result"]
        check_that("'submit_registration_solution' result", result, is_true())
        response_id = self.send_request(self.get_request("get_account_by_name", [account_name]),
                                        self.__database_api_identifier)
        result = self.get_response(response_id)["result"]
        check_that("new account name", result["name"], equal_to(account_name))
        check_that("new account 'echorand_key'", result["echorand_key"], equal_to(public_key))
