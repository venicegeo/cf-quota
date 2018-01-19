#!/usr/bin/env/python

# -*- coding: utf-8 -*-
import requests
import os
from subprocess import check_output

base_url = os.getenv("PCF_API_ENDPOINT", "https://api.system.dev.east.paas.geointservices.io")
phase_one_space = os.getenv("PHASE_ONE_PCF_SPACE", "pz-int")
phase_two_space = os.getenv("PHASE_TWO_PCF_SPACE", "pz-test")
prod_space = os.getenv("PROD_PCF_SPACE", "pz-prod")
pz_spaces = [phase_one_space, phase_two_space, prod_space]
pz_space_guids = {}

def cf_api_auth():


    """Use the cf shell command to get the account's temporary auth token
       and store them as an authorization header for later use
    """
    cf_oauth_token = check_output(["cf", "oauth-token"]).strip("\n")
    headers = {"Cookie": "", "Authorization": cf_oauth_token}
    return (headers)

def get_all_spaces(headers):


    """Use the cf API to get each space guid

    Args:
      headers (dict): A cookie and auth header containing the cf auth token

    Returns:
      dict: A dictionary containg all cf space guids
    """
    all_spaces = requests.get("{}/v2/spaces".format(base_url), headers=headers).json()
    # Collect all of the apps and their guid
    for idx in all_spaces["resources"]:
        for space_name in pz_spaces:
          if space_name == idx["entity"]["name"]:
              pz_space_guids[space_name] = idx["metadata"]["guid"]
    return pz_space_guids

def get_space_quotas(headers, pz_space_guids):
    # type: (object, object) -> object


    """Get quotas for each pz space

    Args:
      headers (dict): Cookie and authorization headers
      pz_space_guids (dict): A dictionary containing all guids for the space(s)

    Returns:
      dict: A dictionary of space quota(s) for each space
    """
    space_quotas = {}
    for space_name in pz_space_guids:
      space_quotas[space_name] = requests.get("{}/v2/spaces/{}".format(base_url, pz_space_guids.get(space_name)), headers=headers).json()
    for space in space_quotas:
        if space_quotas[space]["entity"]["space_quota_definition_guid"] is not None:
            raise SystemExit(1, "Quota set for space: "+space)
        else:
            raise SystemExit(0)
    return (space_quotas)

if __name__ == '__main__':
    headers = cf_api_auth()
    pz_space_guids = get_all_spaces(headers=headers)
    get_space_quotas(headers=headers, pz_space_guids=pz_space_guids)
