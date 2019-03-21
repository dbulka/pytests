import json

import lemoncheesecake.api as lcc

from common.validation import Validator


class Receiver(object):

    def __init__(self, web_socket):
        super().__init__()
        self.web_socket = web_socket
        self.validator = Validator()

    @staticmethod
    def get_positive_result(response, logging):
        if logging:
            lcc.log_info("Received:\n{}".format(json.dumps(response, indent=4)))
        return response

    @staticmethod
    def get_negative_result(response, logging):
        if logging:
            lcc.log_warn("Error received:\n{}".format(json.dumps(response, indent=4)))
        return response

    def get_response(self, id_response, negative, logging):
        response = json.loads(self.web_socket.recv())
        if response.get("method") == "notice":
            return self.get_response(id_response, negative, logging)
        if response.get("id") != id_response:
            lcc.log_error(
                "Wrong 'id' expected '{}', but received:\n{}".format(id_response, json.dumps(response, indent=4)))
            raise Exception("Wrong 'id'")
        if response.get("jsonrpc") != "2.0":
            lcc.log_error("Wrong data received: {}".format(json.dumps(response, indent=4)))
            raise Exception("Wrong response")
        if negative:
            return self.get_negative_result(response, logging)
        return self.get_positive_result(response, logging)

    def get_notice_obj(self, response, expected_id, log_block_id, logging):
        notice_obj = response.get("params")[1][0][0]
        actual_id = notice_obj["id"]
        if (self.validator.is_dynamic_global_object_id(actual_id)) and (actual_id == expected_id):
            if logging:
                lcc.log_info(
                    "Received notice about the update of an account:\n{}".format(json.dumps(response, indent=4)))
            return notice_obj
        if (self.validator.is_block_id(actual_id)) and (actual_id.startswith(expected_id)):
            if not log_block_id:
                return None
            if logging:
                lcc.log_info(
                    "The object with the results of the implementation of contracts of the block:\n{}".format(
                        json.dumps(response, indent=4)))
            return notice_obj
        lcc.log_error(
            "Not valid object id, got '{}' but expected '{}', response: {}".format(actual_id, expected_id,
                                                                                   json.dumps(response, indent=4)))
        raise Exception("Not valid object id")

    def get_notice(self, id_response, object_id, log_block_id, logging):
        response = json.loads(self.web_socket.recv())
        if response.get("params")[0] != id_response:
            lcc.log_error(
                "Wrong 'subscription_id' expected '{}', but received:\n{}".format(id_response,
                                                                                  json.dumps(response, indent=4)))
            raise Exception("Wrong 'subscription_id'")
        if response.get("method") != "notice":
            lcc.log_error(
                "Wrong response, expected ''method': 'notice'', but received:\n{}".format(
                    json.dumps(response, indent=4)))
            raise Exception("Wrong response")
        if (object_id is not None) and (self.validator.is_object_id(response.get("params")[1][0][0]["id"])):
            return self.get_notice_obj(response, object_id, log_block_id, logging)
        notice_params = response.get("params")[1][0]
        if (isinstance(notice_params, str)) and (self.validator.is_hex(notice_params)):
            if logging:
                lcc.log_info(
                    "Received notice about the hash of a new block:\n{}".format(json.dumps(response, indent=4)))
            return notice_params
        if (notice_params[0].get("address")) and (self.validator.is_hex(notice_params[0].get("log")[0])):
            if logging:
                lcc.log_info(
                    "Received notice about new contract logs:\n{}".format(json.dumps(response, indent=4)))
            return notice_params[0]
        lcc.log_warn(
            "Not validate response, got params:\n{}".format(json.dumps(response.get("params")[1], indent=4)))
        raise Exception("Not validate response")