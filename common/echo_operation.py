# -*- coding: utf-8 -*-
import json
from copy import deepcopy

import lemoncheesecake.api as lcc

from common.validation import Validator
from project import WALLETS, ECHO_OPERATIONS


class EchoOperations(object):

    def __init__(self):
        super().__init__()
        self.validator = Validator()

    def get_signer(self, signer):
        """
        :param signer: name, id or wif key
        """
        if self.validator.is_wif(signer):
            return signer
        wallets = json.load(open(WALLETS))
        if self.validator.is_account_name(signer):
            return wallets[signer]["private_key"]
        if self.validator.is_account_id(signer):
            wallets_keys = list(wallets.keys())
            for key in range(len(wallets_keys)):
                if wallets[wallets_keys[key]]["id"] == signer:
                    return wallets[wallets_keys[key]]["private_key"]
        lcc.log_error("Try to get invalid signer, get: '{}'".format(signer))
        raise Exception("Try to get invalid signer")

    @staticmethod
    def get_operation_json(variable_name, example=False):
        # Return needed operation template from json file
        if example:
            return deepcopy(ECHO_OPERATIONS[variable_name])
        return deepcopy(ECHO_OPERATIONS[variable_name][1])

    def get_transfer_operation(self, echo, from_account_id, to_account_id, amount=1, fee_amount=0, fee_asset_id="1.3.0",
                               amount_asset_id="1.3.0", extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.TRANSFER
        transfer_props = self.get_operation_json("transfer_operation")
        transfer_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        transfer_props.update({"from": from_account_id, "to": to_account_id, "extensions": extensions})
        transfer_props["amount"].update({"amount": amount, "asset_id": amount_asset_id})
        if debug_mode:
            lcc.log_debug("Transfer operation: \n{}".format(json.dumps(transfer_props, indent=4)))
        if signer is None:
            return [operation_id, transfer_props, from_account_id]
        return [operation_id, transfer_props, signer]

    def get_account_create_operation(self, echo, name, active_key_auths, echorand_key, fee_amount=0,
                                     fee_asset_id="1.3.0", registrar="1.2.12", active_weight_threshold=1,
                                     active_account_auths=None, options_delegating_account="1.2.12", delegate_share=0,
                                     options_extensions=None, extensions=None, signer=None, debug_mode=False):
        if isinstance(active_key_auths, str):
            active_key_auths = [[active_key_auths, 1]]
        if active_account_auths is None:
            active_account_auths = []
        if options_extensions is None:
            options_extensions = []
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.ACCOUNT_CREATE
        account_create_props = self.get_operation_json("account_create_operation")
        account_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        account_create_props.update(
            {"registrar": registrar, "name": name, "echorand_key": echorand_key, "extensions": extensions})
        account_create_props["active"].update(
            {"weight_threshold": active_weight_threshold, "account_auths": active_account_auths,
             "key_auths": active_key_auths})
        account_create_props["options"].update(
            {"delegating_account": options_delegating_account, "delegate_share": delegate_share,
             "extensions": options_extensions})
        if debug_mode:
            lcc.log_debug("Create account operation: \n{}".format(json.dumps(account_create_props, indent=4)))
        if signer is None:
            return [operation_id, account_create_props, registrar]
        return [operation_id, account_create_props, signer]

    def get_account_update_operation(self, echo, account, weight_threshold=None, account_auths=None, key_auths=None,
                                     echorand_key=None, delegate_share=0, delegating_account=None, fee_amount=0,
                                     fee_asset_id="1.3.0", extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.ACCOUNT_UPDATE
        account_update_props = self.get_operation_json("account_update_operation")
        account_update_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        account_update_props.update({"account": account, "extensions": extensions})
        if weight_threshold is not None:
            account_update_props["active"].update(
                {"weight_threshold": weight_threshold, "account_auths": account_auths, "key_auths": key_auths})
        else:
            del account_update_props["active"]
        if echorand_key is not None:
            account_update_props.update({"echorand_key": echorand_key})
        else:
            del account_update_props["echorand_key"]
        if delegating_account is not None:
            account_update_props["new_options"].update(
                {"delegating_account": delegating_account, "delegate_share": delegate_share})
        else:
            del account_update_props["new_options"]
        if debug_mode:
            lcc.log_debug("Update account operation: \n{}".format(json.dumps(account_update_props, indent=4)))
        if signer is None:
            return [operation_id, account_update_props, account]
        return [operation_id, account_update_props, signer]

    def get_asset_create_operation(self, echo, issuer, symbol, precision=0, fee_amount=0, fee_asset_id="1.3.0",
                                   max_supply="1000000000000000", issuer_permissions=79, flags=0, base_amount=1,
                                   base_asset_id="1.3.0", quote_amount=1, quote_asset_id="1.3.1",
                                   whitelist_authorities=None, blacklist_authorities=None, description="",
                                   extensions=None, signer=None, debug_mode=False):
        if whitelist_authorities is None:
            whitelist_authorities = []
        if blacklist_authorities is None:
            blacklist_authorities = []
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.ASSET_CREATE
        asset_create_props = self.get_operation_json("asset_create_operation")
        asset_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        asset_create_props.update(
            {"issuer": issuer, "symbol": symbol, "precision": precision, "extensions": extensions})
        asset_create_props["common_options"].update(
            {"max_supply": max_supply, "issuer_permissions": issuer_permissions, "flags": flags})
        asset_create_props["common_options"]["core_exchange_rate"]["base"].update(
            {"amount": base_amount, "asset_id": base_asset_id})
        asset_create_props["common_options"]["core_exchange_rate"]["quote"].update(
            {"amount": quote_amount, "asset_id": quote_asset_id})
        asset_create_props["common_options"].update(
            {"whitelist_authorities": whitelist_authorities, "blacklist_authorities": blacklist_authorities,
             "description": description})
        if debug_mode:
            lcc.log_debug("Create asset operation: \n{}".format(json.dumps(asset_create_props, indent=4)))
        if signer is None:
            return [operation_id, asset_create_props, issuer]
        return [operation_id, asset_create_props, signer]

    def get_asset_issue_operation(self, echo, issuer, value_amount, value_asset_id, issue_to_account, fee_amount=0,
                                  fee_asset_id="1.3.0", extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.ASSET_ISSUE
        asset_issue_props = self.get_operation_json("asset_issue_operation")
        asset_issue_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        asset_issue_props.update({"issuer": issuer, "issue_to_account": issue_to_account, "extensions": extensions})
        asset_issue_props["asset_to_issue"].update({"amount": value_amount, "asset_id": value_asset_id})
        if debug_mode:
            lcc.log_debug("Asset issue operation: \n{}".format(json.dumps([operation_id, asset_issue_props], indent=4)))
        if signer is None:
            return [operation_id, asset_issue_props, issuer]
        return [operation_id, asset_issue_props, signer]

    def get_proposal_create_operation(self, echo, fee_paying_account, expiration_time, proposed_ops,
                                      review_period_seconds=None, fee_amount=0, fee_asset_id="1.3.0",
                                      extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.PROPOSAL_CREATE
        proposal_create_props = self.get_operation_json("proposal_create_operation")
        proposal_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        proposal_create_props.update(
            {"fee_paying_account": fee_paying_account, "expiration_time": expiration_time, "proposed_ops": proposed_ops,
             "extensions": extensions})
        if review_period_seconds is None:
            del proposal_create_props["review_period_seconds"]
        else:
            proposal_create_props.update({"review_period_seconds": review_period_seconds})
        if debug_mode:
            lcc.log_debug("Proposal create operation: \n{}".format(json.dumps(proposal_create_props, indent=4)))
        if signer is None:
            return [operation_id, proposal_create_props, fee_paying_account]
        return [operation_id, proposal_create_props, signer]

    def get_committee_member_create_operation(self, echo, committee_member_account, eth_address, btc_public_key,
                                              deposit_amount, fee_amount=0, fee_asset_id="1.3.0", url="",
                                              deposit_asset_id="1.3.0", extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.COMMITTEE_MEMBER_CREATE
        committee_member_create_props = self.get_operation_json("committee_member_create_operation")
        committee_member_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        committee_member_create_props["deposit"].update({"amount": deposit_amount, "asset_id": deposit_asset_id})
        committee_member_create_props.update(
            {"committee_member_account": committee_member_account, "url": url, "eth_address": eth_address,
             "btc_public_key": btc_public_key, "extensions": extensions})
        if debug_mode:
            lcc.log_debug("Committee member create operation: \n{}".format(
                json.dumps([operation_id, committee_member_create_props], indent=4)))
        if signer is None:
            return [operation_id, committee_member_create_props, committee_member_account]
        return [operation_id, committee_member_create_props, signer]

    def get_committee_member_update_operation(self, echo, committee_member, committee_member_account,
                                              new_eth_address=None, new_btc_public_key=None, new_url=None, fee_amount=0,
                                              fee_asset_id="1.3.0", extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.COMMITTEE_MEMBER_UPDATE
        committee_member_update_props = self.get_operation_json("committee_member_update_operation")
        committee_member_update_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        committee_member_update_props.update(
            {"committee_member": committee_member, "committee_member_account": committee_member_account,
             "extensions": extensions})
        if new_eth_address is not None:
            committee_member_update_props.update({"new_eth_address": new_eth_address})
        else:
            del committee_member_update_props["new_eth_address"]
        if new_btc_public_key is not None:
            committee_member_update_props.update({"new_btc_public_key": new_btc_public_key})
        else:
            del committee_member_update_props["new_btc_public_key"]
        if new_url is not None:
            committee_member_update_props.update({"new_url": new_url})
        else:
            del committee_member_update_props["new_url"]
        if debug_mode:
            lcc.log_debug("Committee member update operation: \n{}".format(
                json.dumps([operation_id, committee_member_update_props], indent=4)))
        if signer is None:
            return [operation_id, committee_member_update_props, committee_member_account]
        return [operation_id, committee_member_update_props, signer]

    def get_vesting_balance_create_operation(self, echo, creator, owner, fee_amount=0, fee_asset_id="1.3.0", amount=1,
                                             amount_asset_id="1.3.0", begin_timestamp="1970-01-01T00:00:00",
                                             vesting_cliff_seconds=0, vesting_duration_seconds=0, extensions=None,
                                             signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.VESTING_BALANCE_CREATE
        vesting_balance_create_props = deepcopy(self.get_operation_json("vesting_balance_create_operation"))
        vesting_balance_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        vesting_balance_create_props.update({"creator": creator, "owner": owner, "extensions": extensions})
        vesting_balance_create_props["amount"].update({"amount": amount, "asset_id": amount_asset_id})
        vesting_balance_create_props["policy"][1].update(
            {"begin_timestamp": begin_timestamp, "vesting_cliff_seconds": vesting_cliff_seconds,
             "vesting_duration_seconds": vesting_duration_seconds})
        if debug_mode:
            lcc.log_debug("Vesting balance create operation: \n{}".format(
                json.dumps([operation_id, vesting_balance_create_props], indent=4)))
        if signer is None:
            return [operation_id, vesting_balance_create_props, creator]
        return [operation_id, vesting_balance_create_props, signer]

    def get_vesting_balance_withdraw_operation(self, echo, vesting_balance, owner, fee_amount=0, fee_asset_id="1.3.0",
                                               amount=1, amount_asset_id="1.3.0", extensions=None, signer=None,
                                               debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.VESTING_BALANCE_WITHDRAW
        vesting_balance_withdraw_props = deepcopy(self.get_operation_json("vesting_balance_withdraw_operation"))
        vesting_balance_withdraw_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        vesting_balance_withdraw_props.update(
            {"vesting_balance": vesting_balance, "owner": owner, "extensions": extensions})
        vesting_balance_withdraw_props["amount"].update({"amount": amount, "asset_id": amount_asset_id})
        if debug_mode:
            lcc.log_debug("Vesting balance withdraw operation: \n{}".format(
                json.dumps([operation_id, vesting_balance_withdraw_props], indent=4)))
        if signer is None:
            return [operation_id, vesting_balance_withdraw_props, owner]
        return [operation_id, vesting_balance_withdraw_props, signer]

    def get_balance_claim_operation(self, echo, deposit_to_account, balance_owner_public_key, value_amount,
                                    balance_owner_private_key=None, fee_amount=0, fee_asset_id="1.3.0",
                                    balance_to_claim="1.8.0", value_asset_id="1.3.0", extensions=None, signer=None,
                                    debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.BALANCE_CLAIM
        balance_claim_operation_props = self.get_operation_json("balance_claim_operation")
        balance_claim_operation_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        balance_claim_operation_props.update(
            {"deposit_to_account": deposit_to_account, "balance_to_claim": balance_to_claim,
             "balance_owner_key": balance_owner_public_key, "extensions": extensions})
        balance_claim_operation_props["total_claimed"].update({"amount": value_amount, "asset_id": value_asset_id})
        if debug_mode:
            lcc.log_debug("Balance claim operation: \n{}".format(
                json.dumps([operation_id, balance_claim_operation_props], indent=4)))
        if signer is None:
            return [operation_id, balance_claim_operation_props, balance_owner_private_key]
        return [operation_id, balance_claim_operation_props, signer]

    def get_balance_freeze_operation(self, echo, account, value_amount, fee_amount=0, fee_asset_id="1.3.0", duration=0,
                                     value_asset_id="1.3.0", extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.BALANCE_FREEZE
        balance_freeze_operation_props = self.get_operation_json("balance_freeze_operation")
        balance_freeze_operation_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        balance_freeze_operation_props["amount"].update({"amount": value_amount, "asset_id": value_asset_id})
        balance_freeze_operation_props.update({"account": account, "duration": duration,
                                               "extensions": extensions})
        if debug_mode:
            lcc.log_debug("Balance claim operation: \n{}".format(
                json.dumps([operation_id, balance_freeze_operation_props], indent=4)))
        if signer is None:
            return [operation_id, balance_freeze_operation_props, account]
        return [operation_id, balance_freeze_operation_props, signer]

    def get_contract_create_operation(self, echo, registrar, bytecode, fee_amount=0, fee_asset_id="1.3.0",
                                      value_amount=0, value_asset_id="1.3.0", supported_asset_id=None,
                                      eth_accuracy=False, extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.CONTRACT_CREATE
        contract_create_props = self.get_operation_json("contract_create_operation")
        contract_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        contract_create_props.update(
            {"registrar": registrar, "code": bytecode, "eth_accuracy": eth_accuracy, "extensions": extensions})
        if supported_asset_id is not None:
            contract_create_props.update({"supported_asset_id": supported_asset_id})
        else:
            del contract_create_props["supported_asset_id"]
        contract_create_props["value"].update({"amount": value_amount, "asset_id": value_asset_id})
        if debug_mode:
            lcc.log_debug(
                "Create contract operation: \n{}".format(json.dumps([operation_id, contract_create_props], indent=4)))
        if signer is None:
            return [operation_id, contract_create_props, registrar]
        return [operation_id, contract_create_props, signer]

    def get_contract_call_operation(self, echo, registrar, bytecode, callee, fee_amount=0, fee_asset_id="1.3.0",
                                    value_amount=0, value_asset_id="1.3.0", extensions=None, signer=None,
                                    debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.CONTRACT_CALL
        contract_call_props = self.get_operation_json("contract_call_operation")
        contract_call_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        contract_call_props.update(
            {"registrar": registrar, "code": bytecode, "callee": callee, "extensions": extensions})
        contract_call_props["value"].update({"amount": value_amount, "asset_id": value_asset_id})
        if debug_mode:
            lcc.log_debug("Call contract operation: \n{}".format(json.dumps(contract_call_props, indent=4)))
        if signer is None:
            return [operation_id, contract_call_props, registrar]
        return [operation_id, contract_call_props, signer]

    def get_account_address_create_operation(self, echo, owner, label, fee_amount=1, fee_asset_id="1.3.0",
                                             extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.ACCOUNT_ADDRESS_CREATE
        account_address_create_props = self.get_operation_json("account_address_create_operation")
        account_address_create_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        account_address_create_props.update({"owner": owner, "label": label, "extensions": extensions})
        if debug_mode:
            lcc.log_debug(
                "Account address create operation: \n{}".format(json.dumps(account_address_create_props, indent=4)))
        if signer is None:
            return [operation_id, account_address_create_props, owner]
        return [operation_id, account_address_create_props, signer]

    def get_transfer_to_address_operation(self, echo, from_account_id, to_address, fee_amount=0, fee_asset_id="1.3.0",
                                          amount=1, amount_asset_id="1.3.0", extensions=None, signer=None,
                                          debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.TRANSFER_TO_ADDRESS
        transfer_to_address_props = self.get_operation_json("transfer_to_address_operation")
        transfer_to_address_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        transfer_to_address_props.update({"from": from_account_id, "to": to_address, "extensions": extensions})
        transfer_to_address_props["amount"].update({"amount": amount, "asset_id": amount_asset_id})
        if debug_mode:
            lcc.log_debug("Transfer to address operation: \n{}".format(json.dumps(transfer_to_address_props, indent=4)))
        if signer is None:
            return [operation_id, transfer_to_address_props, from_account_id]
        return [operation_id, transfer_to_address_props, signer]

    def get_sidechain_eth_create_address_operation(self, echo, account, fee_amount=0, fee_asset_id="1.3.0",
                                                   extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.SIDECHAIN_ETH_CREATE_ADDRESS
        generate_eth_address_props = self.get_operation_json("sidechain_eth_create_address_operation")
        generate_eth_address_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        generate_eth_address_props.update({"account": account, "extensions": extensions})
        if debug_mode:
            lcc.log_debug(
                "Generate ethereum address operation: \n{}".format(json.dumps(generate_eth_address_props, indent=4)))
        if signer is None:
            return [operation_id, generate_eth_address_props, account]
        return [operation_id, generate_eth_address_props, signer]

    def get_sidechain_eth_withdraw_operation(self, echo, account, eth_addr, value, fee_amount=0, fee_asset_id="1.3.0",
                                             extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.SIDECHAIN_ETH_WITHDRAW
        withdraw_eth_props = self.get_operation_json("sidechain_eth_withdraw_operation")
        withdraw_eth_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        withdraw_eth_props.update({"account": account, "eth_addr": eth_addr, "value": value, "extensions": extensions})
        if debug_mode:
            lcc.log_debug("Withdraw ethereum operation: \n{}".format(json.dumps(withdraw_eth_props, indent=4)))
        if signer is None:
            return [operation_id, withdraw_eth_props, account]
        return [operation_id, withdraw_eth_props, signer]

    def get_contract_fund_pool_operation(self, echo, sender, contract, fee_amount=0, fee_asset_id="1.3.0",
                                         value_amount=1, value_asset_id="1.3.0", extensions=None, signer=None,
                                         debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.CONTRACT_FUND_POOL
        contract_fund_pool_props = self.get_operation_json("contract_fund_pool_operation")
        contract_fund_pool_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        contract_fund_pool_props.update({"sender": sender, "contract": contract, "extensions": extensions})
        contract_fund_pool_props["value"].update({"amount": value_amount, "asset_id": value_asset_id})
        if debug_mode:
            lcc.log_debug("Contract fund pool operation: \n{}".format(json.dumps(contract_fund_pool_props, indent=4)))
        if signer is None:
            return [operation_id, contract_fund_pool_props, sender]
        return [operation_id, contract_fund_pool_props, signer]

    def get_contract_whitelist_operation(self, echo, sender, contract, fee_amount=0, fee_asset_id="1.3.0",
                                         add_to_whitelist=None, remove_from_whitelist=None, add_to_blacklist=None,
                                         remove_from_blacklist=None, extensions=None, signer=None, debug_mode=False):
        if add_to_whitelist is None:
            add_to_whitelist = []
        if remove_from_whitelist is None:
            remove_from_whitelist = []
        if add_to_blacklist is None:
            add_to_blacklist = []
        if remove_from_blacklist is None:
            remove_from_blacklist = []
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.CONTRACT_WHITELIST
        contract_whitelist_props = self.get_operation_json("contract_whitelist_operation")
        contract_whitelist_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        contract_whitelist_props.update({"sender": sender, "contract": contract, "extensions": extensions})
        contract_whitelist_props.update(
            {"add_to_whitelist": add_to_whitelist, "remove_from_whitelist": remove_from_whitelist,
             "add_to_blacklist": add_to_blacklist, "remove_from_blacklist": remove_from_blacklist})
        if debug_mode:
            lcc.log_debug("Contract whitelist operation: \n{}".format(json.dumps(contract_whitelist_props, indent=4)))
        if signer is None:
            return [operation_id, contract_whitelist_props, sender]
        return [operation_id, contract_whitelist_props, signer]

    def get_sidechain_erc20_register_token_operation(self, echo, account, eth_addr, name, symbol, fee_amount=0,
                                                     fee_asset_id="1.3.0", decimals=0, extensions=None, signer=None,
                                                     debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.SIDECHAIN_ERC20_REGISTER_TOKEN
        register_erc20_token_props = self.get_operation_json("sidechain_erc20_register_token_operation")
        register_erc20_token_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        register_erc20_token_props.update(
            {"account": account, "eth_addr": eth_addr, "name": name, "symbol": symbol, "decimals": decimals,
             "extensions": extensions})
        if debug_mode:
            lcc.log_debug(
                "Register erc20 token operation: \n{}".format(json.dumps(register_erc20_token_props, indent=4)))
        if signer is None:
            return [operation_id, register_erc20_token_props, account]
        return [operation_id, register_erc20_token_props, signer]

    def get_sidechain_erc20_withdraw_token_operation(self, echo, account, to, erc20_token, value, fee_amount=0,
                                                     fee_asset_id="1.3.0", extensions=None, signer=None,
                                                     debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.SIDECHAIN_ERC20_WITHDRAW_TOKEN
        withdraw_erc20_token_props = self.get_operation_json("sidechain_erc20_withdraw_token_operation")
        withdraw_erc20_token_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        withdraw_erc20_token_props.update(
            {"account": account, "to": to, "erc20_token": erc20_token, "value": value, "extensions": extensions})
        if debug_mode:
            lcc.log_debug(
                "Withdraw erc20 token operation: \n{}".format(json.dumps(withdraw_erc20_token_props, indent=4)))
        if signer is None:
            return [operation_id, withdraw_erc20_token_props, account]
        return [operation_id, withdraw_erc20_token_props, signer]

    def get_contract_update_operation(self, echo, sender, contract, new_owner=None, fee_amount=0, fee_asset_id="1.3.0",
                                      extensions=None, signer=None, debug_mode=False):
        if extensions is None:
            extensions = []
        operation_id = echo.config.operation_ids.CONTRACT_UPDATE
        contract_update_props = self.get_operation_json("contract_update_operation")
        contract_update_props["fee"].update({"amount": fee_amount, "asset_id": fee_asset_id})
        contract_update_props.update({"sender": sender, "contract": contract, "extensions": extensions})
        if new_owner is not None:
            contract_update_props.update({"new_owner": new_owner})
        else:
            del contract_update_props["new_owner"]
        if debug_mode:
            lcc.log_debug("Contract update operation: \n{}".format(json.dumps(contract_update_props, indent=4)))
        if signer is None:
            return [operation_id, contract_update_props, sender]
        return [operation_id, contract_update_props, signer]

    def broadcast(self, echo, list_operations, return_operations=False, expiration=None, no_broadcast=False,
                  get_signed_tx=False, log_broadcast=False, debug_mode=False, broadcast_with_callback=False):
        tx = echo.create_transaction()
        if debug_mode:
            lcc.log_debug("List operations:\n{}".format(json.dumps(list_operations, indent=4)))
        if type(list_operations[0]) is int:
            list_operations = [list_operations]
        if len(list_operations) > 1:
            list_operations = [item for sublist in list_operations for item in sublist]
        for operation in list_operations:
            tx.add_operation(name=operation[0], props=operation[1])
        if return_operations:
            return tx.operations
        for operation in list_operations:
            tx.add_signer(self.get_signer(signer=operation[2]))
        if expiration:
            tx.expiration = expiration
        tx.sign()
        if no_broadcast:
            return tx.transaction_object.json()
        if broadcast_with_callback:
            broadcast_result = tx.broadcast("1")
        else:
            broadcast_result = tx.broadcast()
        if log_broadcast:
            lcc.log_info("Broadcast result: \n{}".format(json.dumps(broadcast_result, indent=4)))
        if get_signed_tx:
            return broadcast_result, tx.transaction_object.json(), tx.transaction_object
        return broadcast_result
