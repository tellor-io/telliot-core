
from telliot_core.queries.abi_query import AbiQuery


class APIQuery(AbiQuery):
    """Returns the output of an API.

    Attributes:
        api_url:
            url to call to get the data
        arg_string:
            Names of the values in the returned JSON dict to be returned (comma separated string)

    """

    api_url: str
    arg_string: str

    def __init__(self, api_url, arg_string):
        self.api_url = api_url
        self.arg_string = arg_string

    #: ABI used for encoding/decoding parameters
    abi = [{"name": "api_url", "type": "string"}, {"name": "arg_string", "type": "string"}]
