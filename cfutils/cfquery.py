#!/usr/bin/env/python

# -*- coding: utf-8 -*-

import requests
from subprocess import check_output, CalledProcessError


class CFQuery:

    """Provides abstraction, authentication and interaction with the CloudFoundry
       API

       Attributes:
           auth_headers (dict): A cookie and token http header
           url (str): The Cloudfoundry API base url
    """
    def __init__(self, api_url):

        """Use the cf shell command to get the account's temporary auth token
           and store them as an authorization header for later use.

           Args:
               api_url (str): The base host for the CloudFoundry API
        """

        self.api_url = api_url

        try:
            cf_oauth_token = check_output(["cf", "oauth-token"]).strip("\n")
        except CalledProcessError as error:
            raise SystemExit(error.returncode, error.output)
        self.auth_headers = {"Cookie": "", "Authorization": cf_oauth_token}

    def get_all_spaces(self):

        """Query the CloudFoundry API and get information about all spaces

           Returns (dict): A JSON formatted response with spaces and attributes
        """

        all_spaces = requests.get("https://{}/v2/spaces".format(self.api_url), headers=self.auth_headers).json()

        return all_spaces

    def get_space_quotas(self, spaces):

        """Get quotas for each space

           Args:
               spaces (list): A list of spaces to query for

           Returns:
             dict: A dictionary of space quota(s) for each space
        """

        org_spaces = self.get_all_spaces()
        pz_space_guids = {}
        # Collect all of the apps and their guid
        for space_name in spaces:
            for idx in org_spaces["resources"]:
                if space_name == idx["entity"]["name"]:
                    pz_space_guids[space_name] = idx["metadata"]["guid"]
        space_quotas = {}
        for space_name in pz_space_guids:
            print "Getting quotas for space " + space_name + "..."
            try:
                space_quotas[space_name] = requests.get("https://{}/v2/spaces/{}".format(self.api_url, pz_space_guids.get(space_name)), headers=self.auth_headers).json()
            except CalledProcessError as error:
                raise SystemExit(error.returncode, error.output)
        for space in space_quotas:
            if space_quotas[space]["entity"]["space_quota_definition_guid"] is not None:
                raise SystemExit(1, "Quota set for space: " + space)
            else:
                print "No quota set for space: " + space

        return space_quotas

    def get_app_logs(self, space, app):

        """Get the logs for a particular app
             Args:
                 space (string): The space the app is in
                 app (string): The app name

             Returns:
               dict: A dictionary of space quota(s) for each space
        """

        logs = "logs go here"

        return logs
