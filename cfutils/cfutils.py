#!/usr/bin/env/python

# -*- coding: utf-8 -*-

import requests
from subprocess import check_output, CalledProcessError


class Cfutils(object):

    """Provides abstraction, authentication and interaction with the CloudFoundry
       API

       Attributes:
           auth_headers (dict): A cookie and token http header
           api_url (str): The Cloudfoundry API base url
           query: (str): The http query to send to the API
           endpoint: (str): The endpoint to query
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

    def cf_query(self, endpoint):

        """Constructs a requests query to the specified API endpoint

           Args:
               endpoint (str): The API endpont to request
           Returns:
               api_request (dict): A JSON formatted dictionary of the query response
        """

        self.endpoint = endpoint
        api_request = requests.get("https://{}/v2/{}".format(self.api_url,\
                self.endpoint), headers=self.auth_headers).json()

        return api_request

    def get_all_spaces(self):

        """Query the CloudFoundry API and get information about all spaces

           Returns:
               all_spaces (dict): A JSON formatted response with spaces and attributes
        """

        all_spaces = self.cf_query("spaces")
        return all_spaces

    def get_space_quotas(self, spaces):

        """Get quotas for each space

           Args:
               spaces (list): A list of spaces to query for

           Returns:
               pz_space_guids (dict): A dictionary of space quota(s) for each space
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
                space_quotas[space_name] = self.cf_query("spaces/{}".format(pz_space_guids.get(space_name)))
            except CalledProcessError as error:
                raise SystemExit(error.returncode, error.output)
        for space in space_quotas:
            if space_quotas[space]["entity"]["space_quota_definition_guid"] is not None:
                raise SystemExit(1, "Quota set for space: " + space)
            else:
                print "No quota set for space: " + space
        return pz_space_guids

    def get_all_apps_in_space(self, spaces):

        """Get all the apps in the specified space
             Args:
                 spaces (list): The space or spaces to get apps from

             Returns:
                 apps (dict): A JSON formatted dictionary of all apps in a space
        """
        apps = {}
        self.spaces = spaces
        pz_space_guids = self.get_space_quotas(spaces)
        for key, value in pz_space_guids.iteritems():
            endpoint = "spaces/{}/apps".format(value)
            try:
                apps[key] = self.cf_query(endpoint)
            except CalledProcessError as error:
                raise SystemExit(error.returncode, error.output)
        print apps
        return apps

    def get_app_space_status(self, spaces):

        """Get the apps status in a space
             Args:
                 spaces (list): The space or spaces to query

             Returns:
                 app_status (str): A newline formatted string of app name and
                 status.
        """
        self.apps = self.get_all_apps_in_space(spaces)
        for key in self.apps:
            print "Space: {}\n".format(key)
            for i in self.apps[key]["resources"]:
                print  "{} : {}".format(i["entity"]["name"], i["entity"]["state"])

