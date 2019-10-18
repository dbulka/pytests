# -*- coding: utf-8 -*-

import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_true, is_false

from common.base_test import BaseTest

SUITE = {
    "description": "Method 'is_public_key_registered'"
}


@lcc.prop("main", "type")
@lcc.prop("positive", "type")
@lcc.prop("negative", "type")
@lcc.tags("api", "database_api", "database_api_keys", "is_public_key_registered")
@lcc.suite("Check work of method 'is_public_key_registered'", rank=1)
class IsPublicKeyRegistered(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.nathan_name = "nathan"

    def setup_suite(self):
        super().setup_suite()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        lcc.log_info("Database API identifier is '{}'".format(self.__database_api_identifier))

    @lcc.test("Simple work of method 'is_public_key_registered'")
    def method_main_check(self):
        lcc.set_step("Get the account by name and store his echorand_key")
        account_info = self.get_account_by_name(self.nathan_name, self.__database_api_identifier)
        echorand_key = account_info["result"]["echorand_key"]
        lcc.set_step("Check that nathan public key registered")
        response_id = self.send_request(self.get_request("is_public_key_registered", [echorand_key]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)["result"]
        check_that("public key registration state", response, is_true())


@lcc.prop("positive", "type")
@lcc.tags("api", "database_api", "database_api_keys", "is_public_key_registered")
@lcc.suite("Positive testing of method 'is_public_key_registered'", rank=2)
class PositiveTesting(BaseTest):

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

    @lcc.test("Check method 'is_public_key_registered'")
    @lcc.depends_on("DatabaseApi.Keys.IsPublicKeyRegistered.IsPublicKeyRegistered.method_main_check")
    def check_method_with_is_public_key_registered(self, get_random_integer, get_random_valid_account_name):
        new_account_name = get_random_valid_account_name
        callback = get_random_integer

        lcc.set_step("Generate public key")
        generate_keys = self.generate_keys()
        echorand_key = generate_keys[1]
        lcc.log_info("New public key: {} generated successfully".format(echorand_key))

        lcc.set_step("Check if public key is registered before its registration")
        response_id = self.send_request(self.get_request("is_public_key_registered", [echorand_key]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)["result"]
        check_that("public key registration state", response, is_false())

        lcc.set_step("Register account with {} public key".format(echorand_key))
        account_params = [callback, new_account_name, echorand_key, echorand_key]
        response_id = self.send_request(self.get_request("register_account", account_params),
                                        self.__registration_api_identifier)
        self.get_response(response_id)

        lcc.set_step("Check public key state after registration")
        response_id = self.send_request(self.get_request("is_public_key_registered", [echorand_key]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id)["result"]
        check_that("public key registration state", response, is_true())
