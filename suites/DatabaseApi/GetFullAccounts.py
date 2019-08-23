# -*- coding: utf-8 -*-
import lemoncheesecake.api as lcc
from lemoncheesecake.matching import check_that_in, check_that, has_length, is_integer, is_str, is_dict, is_list, \
    require_that, equal_to, is_bool

from common.base_test import BaseTest

SUITE = {
    "description": "Method 'get_full_accounts'"
}


@lcc.prop("suite_run_option_1", "main")
@lcc.prop("suite_run_option_2", "positive")
@lcc.prop("suite_run_option_3", "negative")
@lcc.tags("database_api", "get_full_accounts")
@lcc.suite("Check work of method 'get_full_accounts'", rank=1)
class GetFullAccounts(BaseTest):

    def __init__(self):
        super().__init__()
        self.__database_api_identifier = None

    def check_fields_account_ids_format(self, response, field):
        if not self.validator.is_account_id(response[field]):
            lcc.log_error("Wrong format of '{}', got: {}".format(field, response[field]))
        else:
            lcc.log_info("'{}' has correct format: account_object_type".format(field))

    def setup_suite(self):
        super().setup_suite()
        lcc.set_step("Setup for {}".format(self.__class__.__name__))
        self.__database_api_identifier = self.get_identifier("database")
        lcc.log_info("Database API identifier is '{}'".format(self.__database_api_identifier))

    @lcc.prop("type", "method")
    @lcc.test("Simple work of method 'get_full_accounts'")
    def method_main_check(self):
        lcc.set_step("Get full info about default accounts")
        params = ["1.2.0", "1.2.1"]
        response_id = self.send_request(self.get_request("get_full_accounts", [params, False]),
                                        self.__database_api_identifier)
        results = self.get_response(response_id)["result"]
        lcc.log_info("Call method 'get_full_accounts' with params: {}".format(params))

        lcc.set_step("Check length of received accounts")
        require_that(
            "'list of received accounts'",
            results, has_length(len(params))
        )

        for i, result in enumerate(results):
            lcc.set_step("Checking account #{} - '{}'".format(i, params[i]))
            check_that("account_id", result[0], equal_to(params[i]))
            full_account_info = result[1]
            if check_that("full_account_info", full_account_info, has_length(8)):
                account_info = full_account_info.get("account")
                if check_that("account_info", account_info, has_length(15)):
                    check_that_in(
                        account_info,
                        "id", is_str(params[i]),
                        "network_fee_percentage", is_integer(),
                        "active", is_dict(),
                        "options", is_dict(),
                        "whitelisting_accounts", is_list(),
                        "blacklisting_accounts", is_list(),
                        "whitelisted_accounts", is_list(),
                        "blacklisted_accounts", is_list(),
                        "active_special_authority", is_list(),
                        "top_n_control_flags", is_integer(),
                        "extensions", is_list(),
                        quiet=True
                    )
                    if not self.validator.is_account_id(account_info["registrar"]):
                        lcc.log_error("Wrong format of 'registrar', got: {}".format(account_info["registrar"]))
                    else:
                        lcc.log_info("'registrar' has correct format: account_object_type")
                    if not self.validator.is_account_name(account_info["name"]):
                        lcc.log_error("Wrong format of 'name', got: {}".format(account_info["name"]))
                    else:
                        lcc.log_info("'name' has correct format: account_name")
                    if not self.validator.is_echorand_key(account_info["echorand_key"]):
                        lcc.log_error(
                            "Wrong format of 'echorand_key', got: {}".format(account_info["echorand_key"]))
                    else:
                        lcc.log_info("'echorand_key' has correct format: echo_rand_key")
                    if not self.validator.is_account_statistics_id(account_info["statistics"]):
                        lcc.log_error("Wrong format of 'statistics', got: {}".format(account_info["statistics"]))
                    else:
                        lcc.log_info("'statistics' has correct format: account_statistics_object_type")

                    lcc.set_step("Check 'active' field")
                    if check_that("active", account_info["active"], has_length(3)):
                        check_that_in(
                            account_info["active"],
                            "weight_threshold", is_integer(),
                            "account_auths", is_list(),
                            "key_auths", is_list(),
                            quiet=True
                        )

                    lcc.set_step("Check 'options' field")
                    if check_that("active", account_info["options"], has_length(5)):
                        account_ids_format = ["voting_account", "delegating_account"]
                        for account_id_format in account_ids_format:
                            self.check_fields_account_ids_format(account_info["options"], account_id_format)
                        check_that_in(
                            account_info["options"],
                            "num_committee", is_integer(),
                            "votes", is_list(),
                            "extensions", is_list(),
                            quiet=True
                        )

                lcc.set_step("Check 'statistics' field")
                account_statistics = full_account_info.get("statistics")
                if check_that("account_statistics", account_statistics, has_length(11)):
                    if not self.validator.is_account_statistics_id(account_statistics["id"]):
                        lcc.log_error("Wrong format of 'id', got: {}".format(account_statistics["id"]))
                    else:
                        lcc.log_info("'id' has correct format: account_statistics_object_type")
                    if not self.validator.is_account_transaction_history_id(account_statistics["most_recent_op"]):
                        lcc.log_error("Wrong format of 'most_recent_op', got: {}".format(
                            account_statistics["most_recent_op"]))
                    else:
                        lcc.log_info("'most_recent_op' has correct format: account_transaction_history_object_type")
                    check_that_in(
                        account_statistics,
                        "owner", is_str(params[i]),
                        "total_ops", is_integer(),
                        "removed_ops", is_integer(),
                        "total_blocks", is_integer(),
                        "total_core_in_orders", is_integer(),
                        "pending_fees", is_integer(),
                        "generated_eth_address", is_bool(),
                        "committeeman_rating", is_integer(),
                        "extensions", is_list(),
                        quiet=True
                    )

                lcc.set_step("Check 'registrar_name' field")
                if not self.validator.is_account_name(full_account_info["registrar_name"]):
                    lcc.log_error(
                        "Wrong format of 'registrar_name', got: {}".format(full_account_info["registrar_name"]))
                else:
                    lcc.log_info("'registrar_name' has correct format: account_name")
                lcc.set_step("Check 'votes' field")
                check_that_in(
                    full_account_info, "votes", is_list(), quiet=True
                )
                lcc.set_step("Check 'balances' field")
                check_that_in(
                    full_account_info, "balances", is_list(), quiet=True
                )
                balances = full_account_info["balances"]
                if balances:
                    for j, balance in enumerate(balances):
                        lcc.set_step("Check 'balance #{}' field".format(j))
                        if check_that("account_balances", balance, has_length(5)):
                            if not self.validator.is_account_balance_id(balance["id"]):
                                lcc.log_error(
                                    "Wrong format of 'id', got: {}".format(balance["id"]))
                            else:
                                lcc.log_info("'id' has correct format: account_balance_object_type")
                            self.check_fields_account_ids_format(balance, "owner")
                            if not self.validator.is_asset_id(balance["asset_type"]):
                                lcc.log_error(
                                    "Wrong format of 'asset_type', got: {}".format(balance["asset_type"]))
                            else:
                                lcc.log_info("'asset_type' has correct format: asset_object_type")
                            check_that_in(
                                balance,
                                "balance", is_integer(),
                                "extensions", is_list(),
                                quiet=True
                            )
                lcc.set_step("Check 'vesting_balances' field")
                check_that_in(
                    full_account_info, "vesting_balances", is_list(), quiet=True
                )
                lcc.set_step("Check 'proposals' field")
                check_that_in(
                    full_account_info, "proposals", is_list(), quiet=True
                )
                lcc.set_step("Check 'assets' field")
                check_that_in(
                    full_account_info, "assets", is_list(), quiet=True
                )
                lcc.set_step("Check 'withdraws' field")