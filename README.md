# Automated Tests for Echo 
The project is intended for testing Echo. Includes testing:
* [**Echo Node API**](https://docs.echo.org/api-reference/echo-node-api)
* [**Echo Operations**](https://docs.echo.org/api-reference/echo-operations)
* Testing according to specified scenarios

## Installation
### Manual installation:
#### Windows
    $ git clone https://gitlab.pixelplex.by/631_echo/pytests.git
    $ cd pytests
    $ virtualenv venv
    $ .\venv\Scripts\activate
    $ pip install -r requirements.txt

#### Linux
    $ git clone https://gitlab.pixelplex.by/631_echo/pytests.git
    $ cd pytests
    $ virtualenv venv
    $ source .\venv\bin\activate
    $ pip install -r requirements.txt
    
#### Mac OS
*please see Linux installation*

## Usage
### Note:
##### Before running the tests, you should specify a environment variables: 
- *BASE_URL* - URL on which tests will be connected to the Echo node
- *ETHEREUM_URL* - URL on which tests will be connected to the Ethereum node
- *NATHAN_PK* - private key of "nathan" account
- *INIT0_PK* - private key of "init0" initial account

##### Optional:
- *ROPSTEN* - flag to run tests in the ropsten network (bool type)
- *DEBUG* - run tests with debug mode that log all in\out communication messages with Echo node (bool type)

##### For this you need, example:
* Linux OS: export BASE_URL=_[needed_url]()_
* Windows OS: set BASE_URL=_[needed_url]()_

### Run docker to use Echo and Ethereum nodes locally:
    $ cd pytests
    $ docker-compose pull
    $ docker-compose up build --no-cache
    $ docker-compose up migrate
    $ docker-compose up pytests

### To run tests you can use following commands in console:
    
Filter                           | lcc commands
---------------------------------|----------------------
Run all tests                    | `$ lcc run`
Run tests with special tag       | `$ lcc run -a tag_name`
Run tests with special property  | `$ lcc run -m property_kind:property_name`
Run tests with special link      | `$ lcc run -l link_name`
Run only passed tests            | `$ lcc run --passed`
Run only failed tests            | `$ lcc run --failed`
Run only skipped tests           | `$ lcc run --skipped`
Run only non-passed tests        | `$ lcc run --non-passed`
Run only disabled tests          | `$ lcc run --disabled`
Run only enabled tests           | `$ lcc run --enabled`
Run tests from special report    | `$ lcc run --from-report path_to_report`

_note:_ can combine run options, for example - `$ lcc run --failed --from-report reports/report-2`

## Echo Node API:

### Login API

- [x] [login](https://docs.echo.org/api-reference/echo-node-api/login-api#login-user-password)

### Asset API

- [x] [get_asset_holders](https://docs.echo.org/api-reference/echo-node-api/asset-api#get_asset_holders-string-asset_id-int-start-int-limit)
- [x] [get_asset_holders_count](https://docs.echo.org/api-reference/echo-node-api/asset-api#get_asset_holders_count-string-asset_id)
- [x] [get_all_asset_holders](https://docs.echo.org/api-reference/echo-node-api/asset-api#get_all_asset_holders)

### Database API

#### Objects 
- [ ] [get_objects](https://docs.echo.org/api-reference/echo-node-api/database-api#get_objects-ids)
#### Subscriptions
- [x] [set_subscribe_callback](https://docs.echo.org/api-reference/echo-node-api/database-api#set_subscribe_callback-callback-clear_filter)
- [x] [set_pending_transaction_callback](https://docs.echo.org/api-reference/echo-node-api/database-api#set_pending_transaction_callback-callback)
- [x] [set_block_applied_callback ](https://docs.echo.org/api-reference/echo-node-api/database-api#set_block_applied_callback-callback)
- [ ] [cancel_all_subscriptions](https://docs.echo.org/api-reference/echo-node-api/database-api#cancel_all_subscriptions)
#### Blocks and transactions
- [x] [get_block_header](https://docs.echo.org/api-reference/echo-node-api/database-api#get_block_header-block_num)
- [ ] [get_block_header_batch](https://docs.echo.org/api-reference/echo-node-api/database-api#get_block_header_batch-block_nums)
- [x] [get_block](https://docs.echo.org/api-reference/echo-node-api/database-api#get_block-block_num)
- [ ] [get_block_tx_number](https://docs.echo.org/api-reference/echo-node-api/database-api#get_block_tx_number-id)
- [ ] [get_block_virtual_ops](https://docs.echo.org/api-reference/echo-node-api/database-api#get_block_virtual_ops-block_num)
- [x] [get_transaction](https://docs.echo.org/api-reference/echo-node-api/database-api#get_transaction-block_num-trx_in_block)
- [x] [get_recent_transaction_by_id](https://docs.echo.org/api-reference/echo-node-api/database-api#get_recent_transaction_by_id-id)
#### Globals
- [x] [get_chain_properties](https://docs.echo.org/api-reference/echo-node-api/database-api#get_chain_properties)
- [x] [get_global_properties](https://docs.echo.org/api-reference/echo-node-api/database-api#get_global_properties)
- [x] [get_config](https://docs.echo.org/api-reference/echo-node-api/database-api#get_config)
- [x] [get_chain_id](https://docs.echo.org/api-reference/echo-node-api/database-api#get_chain_id)
- [x] [get_dynamic_global_properties](https://docs.echo.org/api-reference/echo-node-api/database-api#get_dynamic_global_properties)
#### Keys
- [x] [get_key_references](https://docs.echo.org/api-reference/echo-node-api/database-api#get_key_references-keys)
- [ ] [is_public_key_registered](https://docs.echo.org/api-reference/echo-node-api/database-api#is_public_key_registered-public_key)
#### Accounts
- [x] [get_accounts](https://docs.echo.org/api-reference/echo-node-api/database-api#get_accounts-account_ids)
- [x] [get_full_accounts](https://docs.echo.org/api-reference/echo-node-api/database-api#get_full_accounts-names_or_ids-subscribe)
- [x] [get_account_by_name](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_by_name-name)
- [x] [get_account_references](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_references-account_id)
- [x] [lookup_account_names](https://docs.echo.org/api-reference/echo-node-api/database-api#lookup_account_names-account_names)
- [x] [lookup_accounts](https://docs.echo.org/api-reference/echo-node-api/database-api#lookup_accounts-lower_bound_name-limit)
- [x] [get_account_count](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_count)
- [x] [get_account_addresses](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_addresses-account_id-from-limit)
- [x] [get_account_by_address](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_by_address-address)
#### Contracts
- [x] [get_contract](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contract-contract_id)
- [x] [get_contracts](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contracts-contract_ids)
- [x] [get_contract_logs](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contract_logs-contract_id-from-to)
- [x] [subscribe_contracts](https://docs.echo.org/api-reference/echo-node-api/database-api#subscribe_contracts-contracts_ids)
- [x] [subscribe_contract_logs](https://docs.echo.org/api-reference/echo-node-api/database-api#subscribe_contract_logs-callback-contract_id-from-to)
- [x] [get_contract_result](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contract_result-id)
- [x] [call_contract_no_changing_state](https://docs.echo.org/api-reference/echo-node-api/database-api#call_contract_no_changing_state-contract_id-registrar_account-asset_type-code)
#### Balances
- [x] [get_account_balances](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_balances-id-assets)
- [x] [get_contract_balances](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contract_balances-contract_id)
- [x] [get_named_account_balances](https://docs.echo.org/api-reference/echo-node-api/database-api#get_named_account_balances-name-assets)
- [x] [get_balance_objects](https://docs.echo.org/api-reference/echo-node-api/database-api#get_balance_objects-keys)
- [x] [get_vested_balances](https://docs.echo.org/api-reference/echo-node-api/database-api#get_vested_balances-objs)
- [x] [get_vesting_balances](https://docs.echo.org/api-reference/echo-node-api/database-api#get_vesting_balances-account_id)
#### Assets
- [x] [get_assets](https://docs.echo.org/api-reference/echo-node-api/database-api#get_assets-asset_ids)
- [x] [list_assets](https://docs.echo.org/api-reference/echo-node-api/database-api#list_assets-lower_bound_symbol-limit)
- [x] [lookup_asset_symbols](https://docs.echo.org/api-reference/echo-node-api/database-api#lookup_asset_symbols-symbols_or_ids)
#### Verifiers
- [ ] [get_current_verifiers](https://docs.echo.org/api-reference/echo-node-api/database-api#get_current_verifiers-stage_num)
#### Committee members
- [x] [get_committee_members](https://docs.echo.org/api-reference/echo-node-api/database-api#get_committee_members-committee_member_ids)
- [x] [get_committee_member_by_account](https://docs.echo.org/api-reference/echo-node-api/database-api#get_committee_member_by_account-account)
- [x] [lookup_committee_member_accounts](https://docs.echo.org/api-reference/echo-node-api/database-api#lookup_committee_member_accounts-lower_bound_name-limit)
- [x] [get_committee_count](https://docs.echo.org/api-reference/echo-node-api/database-api#get_committee_count)
#### Votes
- [x] [lookup_vote_ids](https://docs.echo.org/api-reference/echo-node-api/database-api#lookup_vote_ids-votes)
#### Authority / validation
- [x] [get_transaction_hex](https://docs.echo.org/api-reference/echo-node-api/database-api#get_transaction_hex-trx)
- [ ] [get_required_signatures](https://docs.echo.org/api-reference/echo-node-api/database-api#get_required_signatures-ctrx-available_keys)
- [x] [get_potential_signatures](https://docs.echo.org/api-reference/echo-node-api/database-api#get_potential_signatures-ctrx)
- [x] [verify_authority](https://docs.echo.org/api-reference/echo-node-api/database-api#verify_authority-trx)
- [ ] [verify_account_authority](https://docs.echo.org/api-reference/echo-node-api/database-api#verify_account_authority-name_or_id-signers)
- [x] [validate_transaction](https://docs.echo.org/api-reference/echo-node-api/database-api#validate_transaction-trx)
- [x] [get_required_fees](https://docs.echo.org/api-reference/echo-node-api/database-api#get_required_fees-ops-id)
#### Proposed transactions
- [ ] [get_proposed_transactions](https://docs.echo.org/api-reference/echo-node-api/database-api#get_proposed_transactions-id)
#### Sidechain
- [x] [get_eth_address](https://docs.echo.org/api-reference/echo-node-api/database-api#get_eth_address-account)
- [x] [get_account_deposits](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_deposits-account)
- [x] [get_account_withdrawals](https://docs.echo.org/api-reference/echo-node-api/database-api#get_account_withdrawals-account)
#### Sidechain ERC20
- [x] [get_erc20_token](https://docs.echo.org/api-reference/echo-node-api/database-api#get_erc-20-_token-eth_addr)
- [x] check_erc20_token
- [x] [get_erc20_account_deposits](https://docs.echo.org/api-reference/echo-node-api/database-api#get_erc-20-_account_deposits-account)
- [x] [get_erc20_account_withdrawals](https://docs.echo.org/api-reference/echo-node-api/database-api#get_erc-20-_account_withdrawals-account)
#### Contract Feepool
- [x] [get_contract_pool_balance](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contract_pool_balance-id)
- [x] [get_contract_pool_whitelist](https://docs.echo.org/api-reference/echo-node-api/database-api#get_contract_pool_whitelist-id)

### History API

- [x] [get_account_history](https://docs.echo.org/api-reference/echo-node-api/history-api#get_account_history-account-stop-limit-100-start)
- [x] [get_relative_account_history](https://docs.echo.org/api-reference/echo-node-api/history-api#get_relative_account_history-account-stop-0-limit-100-start-0)
- [x] [get_account_history_operations](https://docs.echo.org/api-reference/echo-node-api/history-api#get_account_history_operations-account-operation_id-start-stop-limit-100)
- [x] [get_contract_history](https://docs.echo.org/api-reference/echo-node-api/history-api#get_contract_history-contract-stop-limit-start)

### Network broadcast API

- [ ] [broadcast_transaction](https://docs.echo.org/api-reference/echo-node-api/network-broadcast-api#broadcast_transaction-signed_transaction)
- [ ] [broadcast_transaction_with_callback](https://docs.echo.org/api-reference/echo-node-api/network-broadcast-api#broadcast_transaction_with_callback-callback-trx)
- [ ] [broadcast_transaction_synchronous ](https://docs.echo.org/api-reference/echo-node-api/network-broadcast-api#broadcast_transaction_synchronous-trx)

### Registration API

- [x] [register_account](https://docs.echo.org/api-reference/echo-node-api/registration-api#register_account-name-active_key-echorand_key)

## Echo Operations:

### Account Management

- [ ] [account_create_operation](https://docs.echo.org/api-reference/echo-operations/account-management#account_create_operation)
- [ ] [account_update_operation](https://docs.echo.org/api-reference/echo-operations/account-management#account_update_operation)
- [ ] [account_whitelist_operation](https://docs.echo.org/api-reference/echo-operations/account-management#account_whitelist_operation)
- [ ] [account_transfer_operation](https://docs.echo.org/api-reference/echo-operations/account-management#account_transfer_operation)
    
### Asset Management

- [ ] [asset_create_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_create_operation)
- [ ] [asset_update_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_update_operation)
- [ ] [asset_update_bitasset_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_update_bitasset_operation)
- [ ] [asset_update_feed_producers_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_update_feed_producers_operation)
- [ ] [asset_issue_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_issue_operation)
- [ ] [asset_reserve_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_reserve_operation)
- [ ] [asset_fund_fee_pool_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_fund_fee_pool_operation)
- [ ] [asset_publish_feed_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_publish_feed_operation)
- [ ] [asset_claim_fees_operation](https://docs.echo.org/api-reference/echo-operations/asset-management#asset_claim_fees_operation)
    
### Balance Object

- [ ] [balance_claim_operation](https://docs.echo.org/api-reference/echo-operations/balance-object#balance_claim_operation)

### Committee Members

- [ ] [committee_member_create_operation](https://docs.echo.org/api-reference/echo-operations/committee-members#committee_member_create_operation)
- [ ] [committee_member_update_operation](https://docs.echo.org/api-reference/echo-operations/committee-members#committee_member_update_operation)
- [ ] [committee_member_update_global_parameters_operation](https://docs.echo.org/api-reference/echo-operations/committee-members#committee_member_update_global_parameters_operation)
    
### Contract

- [ ] [contract_create_operation](https://docs.echo.org/api-reference/echo-operations/contract#contract_create_operation)
- [ ] [contract_call_operation](https://docs.echo.org/api-reference/echo-operations/contract#contract_call_operation)
- [ ] [contract_transfer_operation [VIRTUAL]](https://docs.echo.org/api-reference/echo-operations/contract#contract_transfer_operation)
- [ ] [contract_update_operation](https://docs.echo.org/api-reference/echo-operations/contract#contract_update_operation)
- [ ] [contract_fund_pool_operation](https://docs.echo.org/api-reference/echo-operations/contract#contract_fund_pool_operation)
- [ ] [contract_whitelist_operation](https://docs.echo.org/api-reference/echo-operations/contract#contract_whitelist_operation)

### Proposal

- [ ] [proposal_create_operation](https://docs.echo.org/api-reference/echo-operations/proposal#proposal_create_operation)
- [ ] [proposal_update_operation](https://docs.echo.org/api-reference/echo-operations/proposal#proposal_update_operation)
- [ ] [proposal_delete_operation](https://docs.echo.org/api-reference/echo-operations/proposal#proposal_delete_operation)

### Asset Transfer

- [ ] [transfer_operation](https://docs.echo.org/api-reference/echo-operations/asset-transfer#transfer_operation)
- [ ] [transfer_to_address_operation](https://docs.echo.org/api-reference/echo-operations/asset-transfer#transfer_to_address_operation)
- [ ] [override_transfer_operation](https://docs.echo.org/api-reference/echo-operations/asset-transfer#override_transfer_operation)

### Vesting Balances

- [ ] [vesting_balance_create_operation](https://docs.echo.org/api-reference/echo-operations/vesting-balances#vesting_balance_create_operation)
- [ ] [vesting_balance_withdraw_operation](https://docs.echo.org/api-reference/echo-operations/vesting-balances#vesting_balance_withdraw_operation)
    
### Sidechain

- [ ] [sidechain_eth_create_address_operation](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_create_address_operation)
- [ ] [sidechain_eth_approve_address_operation](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_approve_address_operation)
- [ ] [sidechain_eth_deposit](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_deposit)
- [ ] [sidechain_eth_withdraw](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_withdraw)
- [ ] [sidechain_eth_approve_withdraw](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_approve_withdraw)
- [ ] [sidechain_eth_issue [VIRTUAL]](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_issue)
- [ ] [sidechain_eth_burn [VIRTUAL]](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_eth_burn)
- [ ] [sidechain_erc20_register_token](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_erc20_register_token)
- [ ] [sidechain_erc20_deposit_token](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_erc20_deposit_token)
- [ ] [sidechain_erc20_withdraw_token](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_erc20_withdraw_token)
- [ ] [sidechain_erc20_approve_token_withdraw](https://docs.echo.org/api-reference/echo-operations/sidechain#sidechain_erc20_approve_token_withdraw)
