# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, equal_to

from common.base_test import BaseTest

SUITE = {
    "description": "Method 'get_registrar'"
}


@lcc.prop("main", "type")
@lcc.tags("api", "notice", "registration_api", "get_registrar")
@lcc.suite("Registration API", rank=1)
class GetRegistrar(BaseTest):

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

    @lcc.tags("get_registrar")
    @lcc.test("Check method get_registrar of registration_api")
    def method_main_check(self, get_random_valid_account_name):
        account_name = get_random_valid_account_name + "2"
        generate_keys = self.generate_keys()
        public_key = generate_keys[1]
        self._connect_to_echopy_lib()
        self.echo.register_account(1, account_name, public_key, public_key)
        response_id = self.send_request(self.get_request("get_account_by_name", [account_name]),
                                        self.__database_api_identifier)
        registrar = self.get_response(response_id)["result"]["registrar"]
        lcc.set_step("Check registrar account_id")
        response_id = self.send_request(self.get_request("get_registrar"),
                                        self.__registration_api_identifier)
        result = self.get_response(response_id)["result"]
        check_that("registrar", registrar, equal_to(result))
