# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_integer, is_true

from common.validation import Validator
from common.base_test import BaseTest

SUITE = {
    "description": "Registration Api"
}


@lcc.prop("main", "type")
@lcc.tags("api", "notice", "registration_api", "request_registration_task")
@lcc.suite("Registration API", rank=1)
class RequestRegistrationTask(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.__registration_api_identifier = None
        self.validator = Validator()

    def setup_suite(self):
        super().setup_suite()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        lcc.log_info(
            "API identifiers are: database='{}', registration='{}'".format(self.__database_api_identifier,
                                                                           self.__registration_api_identifier))

    @lcc.tags("request_registration_task")
    @lcc.test("Check method request_registration_task of registration_api")
    def method_main_check(self):
        lcc.set_step("Check request registration task params")
        response_id = self.send_request(self.get_request("request_registration_task"),
                                        self.__registration_api_identifier)
        result = self.get_response(response_id)["result"]
        if not self.validator.is_hex(result["block_id"]):
            lcc.log_error("Wrong format of 'block_id', got: '{}'".format(result["block_id"]))
        else:
            lcc.log_info("Block_id '{}' has correct format: hex".format(result["block_id"]))
        check_that("rand_num is digit", result["rand_num"].isdigit(), is_true())
        check_that("difficulty", result["difficulty"], is_integer())
