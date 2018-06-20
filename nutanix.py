#!/usr/bin/env python
#
# Copyright (c) 2016 Nutanix Inc. All Rights reserved.
#
# This script demonstrates how to authenticate, get clusters based
# on UUID, get list of clusters. This script is ready to copy and
# paste for execution, but assign the variables in the script.

import urllib2
import base64
import json
import socket
import sys
import pprint
import time
import ssl

# socket timeout in seconds
TIMEOUT = 30
socket.setdefaulttimeout(TIMEOUT)
pp = pprint.PrettyPrinter(indent=4)

class TestRestApi():

    def __init__(self, ip_addr, username, password):
        # Initialise the options.
        self.ip_addr = ip_addr
        self.username = username
        self.password = password
        self.rest_params_init()

    # Initialize REST API parameters
    def rest_params_init(self, sub_url="", method="",
                         body=None, content_type="application/json"):
        self.sub_url = sub_url
        self.body = body
        self.method = method
        self.content_type = content_type

    # Create a REST client session.
    def rest_call(self):
        base_url = 'https://%s:9440/api/nutanix/v3/%s' % (
            self.ip_addr, self.sub_url)
        if self.body and self.content_type == "application/json":
            self.body = json.dumps(self.body)
        request = urllib2.Request(base_url, data=self.body)
        base64string = base64.encodestring(
            '%s:%s' %
            (self.username, self.password)).replace(
            '\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        request.add_header(
            'Content-Type',
            '%s; charset=utf-8' %
            self.content_type)
        request.get_method = lambda: self.method

        try:
            if sys.version_info >= (2, 7, 9):
                ssl_context = ssl._create_unverified_context()
                response = urllib2.urlopen(request, context=ssl_context)
            else:
                response = urllib2.urlopen(request)
            result = response.read()
            if result:
                result = json.loads(result)
            return response.code, result
        except urllib2.HTTPError as e:
            err_result = e.read()
            if err_result:
                try:
                    err_result = json.loads(err_result)
                except:
                    print "Error: %s" % e
                    return "408", None
            return "408", err_result
        except Exception as e:
            print "Error: %s" % e
            return "408", None
class ApiLibrary:
    def __init__(self):
        pass

    # Parse a list
    # list to parse
    # key for which parse is to be done
    def parse_list(self, toparse, lookfor):
        for data in toparse:
            if isinstance(data, dict):
                return data.get(lookfor)

    # Parse a complex dictionary.
    # result : dictionary to parse
    # meta_key : the key which has sub key for which parse is being done.
    # look_for: the key for which parse is to be done.
    def parse_result(self, result, meta_key, lookfor):
        uuid = None
        if result:
            for key in result:
                if key == meta_key:
                    if isinstance(result[key], list):
                        uuid = self.parse_list(result[key], lookfor)
                        return uuid
                    else:
                        if type(result[key]) == dict:
                            return result[key].get(lookfor, None)
                        return result[key]
                elif isinstance(result[key], dict):
                    uuid = self.parse_result(result[key], meta_key, lookfor)
                    if uuid:
                        return uuid
        return uuid

    # Check the return status of API executed
    def check_api_status(self, status, result):
        if result:
            return self.parse_result(result, "status", "state")
        else:
            return None

    def print_failure_status(self, result):
        if result:
            status = result.get('status')
            if status:
                print '*' * 80
                state = self.parse_result(result, "status", "state")
                if state == "kError":
                    print "Reason: ", status.get('reason')
                    print "Message: ", status.get("message")
                else:
                    print "Reason: ", result.get('reason')
                    print "Details: ", result.get('details')
                    print "Message: ", result.get("message")

    def __is_result_complete(self, status, result):
        if result and str(result.get('code')) == "404":
            return True
        if result and str(status) == "200":
            api_status = self.parse_result(result, "status", "state")
            if api_status == "kComplete":
                return True
            elif api_status == "kError":
                return None
        return False

    def track_completion_status(
            self, testRestApi, status, result, get_api_status):
        retry_count = 5
        wait_time = 2  # seconds
        uuid = None

        if result and str(status) == "200":
            uuid = self.parse_result(result, "metadata", "uuid")

        if self.__is_result_complete(status, result):
            return uuid
        else:
            api_status = self.parse_result(result, "status", "state")
            if uuid and api_status != "kComplete" and api_status != "kError":
                count = 0
                while count < retry_count:
                    count = count + 1
                    time.sleep(wait_time)
                    (status, result) = get_api_status(testRestApi, uuid)
                    get_status = self.__is_result_complete(status, result)
                    # API status is kComplete
                    if get_status is True:
                        return uuid
                    # API status is Error
                    if get_status is None:
                        break

            self.print_failure_status(result)
            api_status = self.parse_result(result, "status", "state")
            print "API status :", api_status
            return None


    def track_deletion_status(self, testRestApi, uuid, get_api_status):
        count = 0
        api_status = ""
        status = 0
        result = None
        while count < 3:
            count = count + 1
            time.sleep(5)
            (status, result) = get_api_status(testRestApi, uuid)
            if result:
                if str(status) == "200":
                    api_status = self.parse_result(result, "status", "state")
                else:
                    api_status = result.get('status', None)
            if api_status == "failure":
                return True
        if not str(status) == "200":
            self.print_failure_status(result)
            return False
        else:
            if api_status == "kComplete":
                return True
            elif api_status == "failure":
                self.print_failure_status(result)
                return False
            elif api_status == "kError":
                print "Reason:", self.parse_result(result, "status", "reason")
                print "Message:", self.parse_result(result, "status", "message")
                return False
            else:
                print "Timed Out"
                print result
                return False

# Get Cluster info based on uuid.
def get_cluster(testRestApi, cluster_uuid):
    sub_url = 'clusters/%s' % cluster_uuid
    testRestApi.rest_params_init(sub_url=sub_url, method="GET")
    (status, result) = testRestApi.rest_call()
    return status, result

# Get the list of clusters.
def get_clusters(testRestApi):
    body = {
        "kind": "cluster",
        "length": 10,
        "offset": 0,
        "filter": ""
    }
    testRestApi.rest_params_init(
        sub_url="clusters/list",
        method="POST",
        body=body)
    (status, result) = testRestApi.rest_call()
    return status, result

def main(ip_addr, username, password):
    cluster_uuid = None
    testRestApi = TestRestApi(ip_addr, username, password)
    api_library = ApiLibrary()

    # Get Clusters by the provided filters.
    (status, cluster_list) = get_clusters(testRestApi)
    if str(status) == "200":
        clusters = cluster_list.get('entities')
        if clusters:
            print "Cluster Name", "\t\t", "Cluster_UUID"
            for cluster in clusters:
                cluster_uuid = api_library.parse_result(cluster, "metadata", "uuid")
                print api_library.parse_result(cluster, "status", "name"), "\t\t", api_library.parse_result(cluster, "metadata", "uuid")
    else:
        print "Failed to get clusters using filters"
        api_library.print_failure_status(cluster_list)
        print '*' * 80
        return

    # Return the cluster definition by the given uuid.
    (status, result) = get_cluster(testRestApi, cluster_uuid)
    if str(status) == "200":
        pp.pprint(result)
    else:
        print "Failed to get clusters definition"
        api_library.print_failure_status(result)
        print '*' * 80

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "Usage: %s <ip> <username> <password>" % __file__
