# CF Utilities

CF Utilities provides a Python Wrapper to interact with the Cloudfoundry API.

It can be used with Jenkins using the JenkinsFile, or locally as long as you
have some version of Python 2 installed.

For Jenkins, it uses environment variables already present to populate the values
for the spaces to query, as well as the cloudfoundry API url.

## Functionality

This utility currently provides the following:

- A base query utility that takes an endpoint as an argument. It sends OAUTH
headers automatically for authentication.
- Query all apps in a space(s) which returns a JSON response from the Cloudfoundry
API with information about the applications.
- Query all spaces you're authorized for.
- Query app status in a space(s).
- Query if any space quotas are set for a particular space.

## Jenkins Usage
Once you've configured your job in Jenkins, this utility requires no
set up to work with Piazza. The `JenkinsFile` provides the environment
variables needed to:

1. Log in to PCF using credentials stored in Jenkins
2. Retrieve a PCF oauth token for API authentication
3. Query the spaces set as environment variables
4. Get the GUIDS for those spaces
5. Determine whether quotas are set for those GUIDS
6. If any are found, the utility exits with a 1, indicating failure

## Using Locally

First, import `cfutils`:

        from cfutils import Cfutils as cf

For convenience, set your `api_url` and space names `spaces`:

        api_url = "api.system.someorg.com"
        myspaces = ["space-one", "space-two", "space-three"]

### Arbitrary endpoint API queries

*This example queries the services endpoint*

        endpoint = "services"
        services = cf(api_url).cf_query(endpoint)

        ...
          {
            "total_results": 1,
            "total_pages": 1,
            "prev_url": null,
            "next_url": null,
            "resources": [
              {
                "metadata": {
                  "guid": "1993218f-096d-4216-bf9d-e0f250332dc6",
                  "url": "/v2/services/1993218f-096d-4216-bf9d-e0f250332dc6",
                  "created_at": "2016-06-08T16:41:31Z",
                  "updated_at": "2016-06-08T16:41:26Z"
                },
                "entity": {
                  "label": "label-57",
                  "provider": null,
        ...

### Quotas for a space(s)

        quotas = cf.(api_url).get_space_quotas(myspaces)


Which will return:

```
Getting quotas for space space-one...
Getting quotas for space space-two...
Getting quotas for space space-three...
No quota set for space: space-one
No quota set for space: space-two
No quota set for space: space-three
```

### Information about all spaces

        spaces = cf(api_url).get_all_spaces()

### All apps in a space

        apps = cf(api_url).get_all_apps_in_space(myspaces)

### App status in a particular space(s)

        app_status = cf(api_url).get_app_space_status(myspaces)


