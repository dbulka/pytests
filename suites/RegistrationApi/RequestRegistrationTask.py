# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_integer, is_true

from common.validation import Validator
from common.base_test import BaseTest
from common.receiver import Receiver

SUITE = {
    "description": "Registration Api"
}


@lcc.prop("main", "type")
@lcc.tags("api", "notice", "registration_api", "request_registration_task")
@lcc.suite("Registration API", rank=1)
class RequestRegistrationTask(object):

    @lcc.tags("request_registration_task")
    @lcc.test("Check method request_registration_task of registration_api")
    def method_main_check(self):
        base = BaseTest()
        validator = Validator()
        base.ws = base.create_connection_to_echo()
        base.receiver = Receiver(web_socket=base.ws)
        lcc.set_step("Requesting Access to a Registration API")
        registration_api_identifier = base.get_identifier("registration")
        check_that("'registration api identifier'", registration_api_identifier, is_integer())

        lcc.set_step("Check request registration task params")
        response_id = base.send_request(base.get_request("request_registration_task"), registration_api_identifier)
        result = base.get_response(response_id)["result"]
        if not validator.is_hex(result["block_id"]):
            lcc.log_error("Wrong format of 'block_id', got: '{}'".format(result["block_id"]))
        else:
            lcc.log_info("Block_id '{}' has correct format: hex".format(result["block_id"]))
        check_that("rand_num is digit", result["rand_num"].isdigit(), is_true())
        check_that("difficulty", result["difficulty"], is_integer())
        base.ws.close()
