# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc

from common.base_test import BaseTest

SUITE = {
    "description": "Perform 'update_asset_operation' without field 'new_options'"
}


@lcc.prop("main", "type")
@lcc.tags("scenarios", "update_asset")
@lcc.suite("Check scenario 'Update asset'")
class UpdateAsset(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None
        self.__registration_api_identifier = None
        self.__history_api_identifier = None
        self.echo_acc0 = None

    def setup_suite(self):
        super().setup_suite()
        self._connect_to_echopy_lib()
        self.__database_api_identifier = self.get_identifier("database")
        self.__registration_api_identifier = self.get_identifier("registration")
        self.__history_api_identifier = self.get_identifier("history")
        lcc.log_info(
            "API identifiers are: database='{}', registration='{}', "
            "history='{}'".format(self.__database_api_identifier, self.__registration_api_identifier,
                                  self.__history_api_identifier))
        self.echo_acc0 = self.get_account_id(self.accounts[0], self.__database_api_identifier,
                                             self.__registration_api_identifier)
        lcc.log_info("Echo account is '{}'".format(self.echo_acc0))

    @lcc.test("Perform update new asset without field 'new_options'")
    def update_asset(self, get_random_valid_account_name, get_random_valid_asset_name):
        new_account = get_random_valid_account_name
        new_asset_name = get_random_valid_asset_name
        operation_count = 1

        lcc.set_step("Create and get new account. Add balance to pay for asset_create_operation fee")
        new_account = self.get_account_id(new_account, self.__database_api_identifier,
                                          self.__registration_api_identifier)
        asset_create_operation = self.echo_ops.get_asset_create_operation(echo=self.echo, issuer=new_account,
                                                                          symbol=new_asset_name)
        self.utils.add_balance_for_operations(self, new_account, asset_create_operation,
                                              self.__database_api_identifier,
                                              operation_count=operation_count)
        lcc.log_info("New Echo account created, account_id='{}, balance added".format(new_account))

        lcc.set_step("Perform asset create operation using a new account")
        collected_operation = self.collect_operations(asset_create_operation, self.__database_api_identifier)
        broadcast_result = \
            self.echo_ops.broadcast(echo=self.echo, list_operations=collected_operation)
        new_asset_id = str(broadcast_result["trx"]["operation_results"][0][1])
        lcc.log_info("New asset created, new_asset_id='{}'".format(new_asset_id))

        lcc.set_step("Get new asset info")
        param = [new_asset_id]
        response_id = self.send_request(self.get_request("get_assets", [param]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id, log_response=True)

        lcc.set_step("Perform new asset update operation without 'new_options'")
        asset_update_operation = self.echo_ops.get_asset_update_operation(echo=self.echo, issuer=new_account,
                                                                          asset_to_update=new_asset_id,
                                                                          new_options=True)
        self.utils.add_balance_for_operations(self, new_account, asset_create_operation,
                                              self.__database_api_identifier,
                                              operation_count=operation_count)
        collected_operation = self.collect_operations(asset_update_operation, self.__database_api_identifier)
        broadcast_result = \
            self.echo_ops.broadcast(echo=self.echo, list_operations=collected_operation, debug_mode=True,
                                    log_broadcast=True)
        lcc.log_debug(str(broadcast_result))

        lcc.set_step("Get new asset info")
        param = [new_asset_id]
        response_id = self.send_request(self.get_request("get_assets", [param]),
                                        self.__database_api_identifier)
        response = self.get_response(response_id, log_response=True)
