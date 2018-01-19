# CF Quotas

This utility is meant to be run from a Jenkins job. It queries the
cloudfoundry API for any quotas set on an arbitrary space.

It uses environment variables already present for populate the values
for the spaces to query, as well as the cloudfoundry API url.

