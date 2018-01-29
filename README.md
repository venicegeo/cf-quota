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
You need the following environment variables set:

- `PCF_API_ENDPOINT`: 'api.yourpcfendpoing.io'
- `PHASE_ONE_PCF_SPACE`: 'space-one''
- `PHASE_TWO_PCF_SPACE`: 'space-two'
- `PROD_PCF_SPACE`: 'space-three'

You can set each of those with `$ export VARIABLE_NAME="somevalue"`.

Then in this directory:

    $ python
        from cfutils import CFQuery
        api_url = "api.system.someorg.com"
        pzspaces = ["space-one", "space-two", "space-three"]
        res = CFQuery(api_url).get_space_quotas(pzspaces)


Which will return:

```
Getting quotas for space space-one...
Getting quotas for space space-two...
Getting quotas for space space-three...
No quota set for space: space-one
No quota set for space: space-two
No quota set for space: space-three
```

