# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that, is_integer, is_true, has_entry, is_list

from common.base_test import BaseTest

SUITE = {
    "description": "Method 'get_committee_frozen_balance'"
}


@lcc.prop("main", "type")
@lcc.prop("positive", "type")
@lcc.prop("negative", "type")
@lcc.tags("api", "database_api", "database_api_committee_members", "get_committee_frozen_balance")
@lcc.suite("Check work of method 'get_committee_frozen_balance'", rank=1)
class GetCommitteeFrozenBalance(BaseTest):
    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.echo_acc0 = None
        self.__registration_api_identifier = None
    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        lcc.log_info(
            "API identifiers are: database='{}'".format(self.__database_api_identifier))
        self.echo_acc0 = self.get_account_id(self.accounts[0], self.__database_api_identifier,
                                             self.__registration_api_identifier)
        lcc.log_info("Echo account is '{}'".format(self.echo_acc0))

    @lcc.test("Simple work of method 'get_committee_frozen_balance'")
    def method_main_check(self):
        response_id = self.send_request(self.get_request("get_global_properties"), self.__database_api_identifier)
        active_committee_members = self.get_response(response_id)["result"][
            "active_committee_members"]
        account_id = active_committee_members[0][0]
        response_id = self.send_request(self.get_request("get_committee_frozen_balance", [account_id]),
                                        self.__database_api_identifier)
        result = self.get_response(response_id)
        lcc.log_info("{}".format(result))
