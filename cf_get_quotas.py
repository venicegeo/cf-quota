#!/usr/bin/env/python

# -*- coding: utf-8 -*-

from cfutils import Cfutils as cf

# Get environment variables from Jenkins for API url and spaces
base_url = os.getenv("PCF_API_ENDPOINT")
phase_one_space = os.getenv("PHASE_ONE_PCF_SPACE")
phase_two_space = os.getenv("PHASE_TWO_PCF_SPACE")
prod_space = os.getenv("PROD_PCF_SPACE")
pz_spaces = [phase_one_space, phase_two_space, prod_space]


if __name__ == '__main__':
    cf(base_url).get_space_quotas(pz_spaces)

