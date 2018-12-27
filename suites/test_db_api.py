import lemoncheesecake.api as lcc
from lemoncheesecake.matching import is_, check_that, check_that_in, is_str, is_integer

from common.utils import BaseTest

SUITE = {
    "description": "Test 'Database API'"
}


@lcc.suite("Test database methods")
class TestDatabaseMethod(BaseTest):
    __get_block = "get_block"
    __get_block_header = "get_block_header"
    __get_block_header_exp = "get_block_header_exp"
    __get_block_exp = "block_exp"
    __get_transaction = "get_transaction"
    __get_transaction_exp = "transaction_exp"
    __get_chain_properties = "get_chain_properties"
    __get_chain_properties_exp = "get_chain_properties_exp"
    __get_global_properties = "get_global_properties"
    __get_global_properties_exp = "get_global_properties_exp"
    __get_config = "get_config"
    __get_config_exp = "get_config_exp"
    __get_chain_id = "get_chain_id"
    __get_chain_id_exp = "get_chain_id_exp"
    __get_dynamic_global_properties = "get_dynamic_global_properties"
    __get_dynamic_global_properties_exp = "get_dynamic_global_properties_exp"
    __get_key_references = "get_key_references"
    __get_key_references_exp = "get_key_references_exp"
    __get_account_by_name = "get_account_by_name"
    __get_account_by_name_exp = "get_account_by_name_exp"
    __get_accounts = "get_accounts"
    __get_accounts_exp = "get_accounts_exp"
    __get_full_accounts = "get_full_accounts"
    __get_full_accounts_ids_exp = "get_full_accounts_ids_exp"
    __get_full_accounts_names_exp = "get_full_accounts_names_exp"
    __get_account_references = "get_account_references"
    __get_account_references_exp = "get_account_references_exp"
    __lookup_account_names = "lookup_account_names"
    __lookup_account_names_exp = "lookup_account_names_exp"
    __lookup_accounts = "lookup_accounts"
    __lookup_accounts_exp = "lookup_accounts_exp"
    __get_account_count = "get_account_count"
    __get_account_balances = "get_account_balances"
    __get_account_balances_exp_empty = "get_account_balances_exp_empty"
    __get_account_balances_exp = "get_account_balances_exp"

    def __init__(self):
        super().__init__()
        self.__resp = None

    def setup_test(self, test):
        # Get database api identifier
        self.get_identifier(self._database_api)

    @lcc.test("Get objects")
    @lcc.hidden()
    def test_get_objects(self, array_ids):
        pass

    @lcc.test("Set subscribe callback")
    @lcc.hidden()
    def test_set_subscribe_callback(self, callback, notify_remove_create):
        pass

    @lcc.test("Set pending transaction callback")
    @lcc.hidden()
    def test_set_pending_transaction_callback(self, callback):
        pass

    @lcc.test("Set block applied callback")
    @lcc.hidden()
    def test_set_block_applied_callback(self, callback):
        pass

    @lcc.test("Cancel all subscriptions")
    @lcc.hidden()
    def test_cancel_all_subscriptions(self):
        pass

    @lcc.test("Get block")
    def test_get_block(self):
        # Get block
        lcc.set_step("Retrieve a full, signed block")
        param = ["1054038"]
        self.send_request(self.get_request(self.__get_block, param), self._identifier)
        self.__resp = self.get_response()

        # Check all block info
        lcc.set_step("Check block info")
        check_that(
            "'block info'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_block_exp)),
        )

    @lcc.test("Get block header")
    def test_get_block_header(self):
        # Get block header
        lcc.set_step("Retrieve header of signed block.")
        param = ["1054038"]
        self.send_request(self.get_request(self.__get_block_header, param), self._identifier)
        self.__resp = self.get_response()

        # Check all block header info
        lcc.set_step("Check block header info")
        check_that(
            "'block header info'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_block_header_exp)),
        )

    @lcc.test("Get transaction")
    def test_get_transaction(self):
        # Get transaction
        lcc.set_step("Retrieve transaction")
        params = ["1054038", "0"]
        self.send_request(self.get_request(self.__get_transaction, params), self._identifier)
        self.__resp = self.get_response()

        # Check all transaction info
        lcc.set_step("Check transaction info")
        check_that(
            "'transaction info'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_transaction_exp)),
        )

    @lcc.test("Get recent transaction by id")
    @lcc.hidden()
    def test_get_recent_transaction_by_id(self, id):
        pass

    @lcc.test("Get chain properties")
    def test_get_chain_properties(self):
        # Get chain properties
        lcc.set_step("Get chain properties")
        self.send_request(self.get_request(self.__get_chain_properties), self._identifier)
        self.__resp = self.get_response()

        # Check chain properties info
        lcc.set_step("Check chain properties info")
        check_that(
            "'chain properties'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_chain_properties_exp)),
        )

    @lcc.test("Get global properties")
    def test_get_global_properties(self):
        # Get global properties
        lcc.set_step("Get global properties")
        self.send_request(self.get_request(self.__get_global_properties), self._identifier)
        self.__resp = self.get_response()

        # Check global properties info
        lcc.set_step("Check global properties info")
        check_that(
            "'global properties'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_global_properties_exp)),
        )

    @lcc.test("Get config")
    def test_get_config(self):
        # Get config
        lcc.set_step("Get config")
        self.send_request(self.get_request(self.__get_config), self._identifier)
        self.__resp = self.get_response()

        # Check config info
        lcc.set_step("Check config info")
        check_that(
            "'config'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_config_exp)),
        )

    @lcc.test("Get chain id")
    def test_get_chain_id(self):
        # Get chain id
        lcc.set_step("Get chain id")
        self.send_request(self.get_request(self.__get_chain_id), self._identifier)
        self.__resp = self.get_response()

        # Check chain id info
        lcc.set_step("Check chain id info")
        check_that(
            "'chain id'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_chain_id_exp)),
        )

    @lcc.test("Get dynamic global properties")
    def test_get_dynamic_global_properties(self):
        # Get dynamic global properties
        lcc.set_step("Get dynamic global properties")
        self.send_request(self.get_request(self.__get_dynamic_global_properties), self._identifier)
        self.__resp = self.get_response()

        # Check dynamic global properties info
        lcc.set_step("Check dynamic global properties info")
        check_that_in(
            self.__resp["result"],
            "id", is_str(is_("2.1.0")),
        )

    @lcc.test("Get key references")
    def test_get_key_references(self):
        # Get key references
        lcc.set_step("Get key references")
        param = ["ECHO6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"]
        self.send_request(self.get_request(self.__get_key_references, [param]), self._identifier)
        self.__resp = self.get_response()

        # Check key references
        lcc.set_step("Check key references")
        check_that(
            "'key references'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_key_references_exp)),
        )

    @lcc.test("Get accounts")
    def test_get_accounts(self):
        # Get accounts
        lcc.set_step("Get accounts")
        params = ["1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14"]
        self.send_request(self.get_request(self.__get_accounts, [params]), self._identifier)
        self.__resp = self.get_response()

        # Check key references
        lcc.set_step("Check accounts")
        check_that(
            "'accounts'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_accounts_exp)),
        )

    @lcc.test("Get full accounts by ids")
    def test_get_full_accounts_ids(self):
        # Get full accounts by ids
        lcc.set_step("Get full accounts by ids")
        params = [["1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.14"], False]
        self.send_request(self.get_request(self.__get_full_accounts, params), self._identifier)
        self.__resp = self.get_response()

        # Check full accounts by ids
        lcc.set_step("Check full accounts by ids")
        check_that(
            "'full accounts by ids'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_full_accounts_ids_exp)),
        )

    @lcc.test("Get full accounts by names")
    def test_get_full_accounts_names(self):
        # Get full accounts by names
        lcc.set_step("Get full accounts by names")
        params = [["init0", "init1", "init2", "init3", "init4", "init5", "nathan", "test124"], False]
        self.send_request(self.get_request(self.__get_full_accounts, params), self._identifier)
        self.__resp = self.get_response()

        # Check full accounts
        lcc.set_step("Check full accounts by names")
        check_that(
            "'full accounts by names'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_full_accounts_names_exp)),
        )

    @lcc.test("Get account by name")
    def test_get_account_by_name(self):
        # Get account by name
        lcc.set_step("Get account by name")
        param = ["init2"]
        self.send_request(self.get_request(self.__get_account_by_name, param), self._identifier)
        self.__resp = self.get_response()

        # Check account by name
        lcc.set_step("Check account by name")
        check_that(
            "'init2'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_account_by_name_exp)),
        )

    @lcc.test("Get account references")
    def test_get_account_references(self):
        # Get account references
        lcc.set_step("Get account references")
        param = ["1.2.28"]  # todo нет необходимого аккаунта для проверки
        self.send_request(self.get_request(self.__get_account_references, param), self._identifier)
        self.__resp = self.get_response()

        # Check account references
        lcc.set_step("Check account references")
        check_that(
            "'1.2.28'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_account_references_exp)),
        )

    @lcc.test("Lookup account names")
    def test_lookup_account_names(self):
        # Lookup account names
        lcc.set_step("Lookup account names")
        params = ["init0", "init1", "init2", "init3", "init4", "init5", "nathan", "test124"]
        self.send_request(self.get_request(self.__lookup_account_names, [params]), self._identifier)
        self.__resp = self.get_response()

        # Check lookup account names
        lcc.set_step("Check lookup account names")
        check_that(
            "'lookup account names'",
            self.__resp["result"],
            is_(self.get_expected(self.__lookup_account_names_exp)),
        )

    @lcc.test("Lookup accounts")
    def test_lookup_accounts(self):
        # Lookup accounts
        lcc.set_step("Lookup accounts")
        params = ["in", 7]  # todo непонятно как работает limit
        self.send_request(self.get_request(self.__lookup_accounts, params), self._identifier)
        self.__resp = self.get_response()

        # Check lookup account names
        lcc.set_step("Check lookup accounts")
        check_that(
            "'lookup accounts'",
            self.__resp["result"],
            is_(self.get_expected(self.__lookup_accounts_exp)),
        )

    @lcc.test("Get account count")
    def test_get_account_count(self):
        # Lookup accounts
        lcc.set_step("Get account count")
        self.send_request(self.get_request(self.__get_account_count), self._identifier)
        self.__resp = self.get_response()

        # Check lookup account names
        lcc.set_step("Check get account count")
        check_that(
            "'account count'",
            self.__resp["result"],
            is_integer(is_(15))
        )

    @lcc.test("Get account balances, empty param: assets")
    def test_get_account_balances_empty_assets(self):
        # Lookup accounts
        lcc.set_step("Get account balances")
        param = ["1.2.8", []]
        self.send_request(self.get_request(self.__get_account_balances, param), self._identifier)
        self.__resp = self.get_response()

        # Check lookup account names
        lcc.set_step("Check get account balances")
        check_that(
            "'account balances'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_account_balances_exp_empty)),
        )

    @lcc.test("Get account balances")
    def test_get_account_balances(self):
        # Lookup accounts
        lcc.set_step("Get account balances")
        param = ["1.2.8", ["1.3.0", "1.3.1", "1.3.2"]]
        self.send_request(self.get_request(self.__get_account_balances, param), self._identifier)
        self.__resp = self.get_response()

        # Check lookup account names
        lcc.set_step("Check get account balances")
        check_that(
            "'account balances'",
            self.__resp["result"],
            is_(self.get_expected(self.__get_account_balances_exp)),
        )
