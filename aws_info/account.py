#!/usr/bin/env python
from __future__ import print_function

def get_account_aliases(iam_conn):
    igaa = iam_conn.get_account_alias()
    return igaa.list_account_aliases_response.list_account_aliases_result.account_aliases

def get_account_id(iam_conn):
    return iam_conn.get_user()['get_user_response']['get_user_result']['user']['arn'].split(':')[4]
