"""Print the size of the data returned by a Morphware query (data reported)."""
import json
import sys

import requests

from telliot_core.queries.morphware import Morphware


def main():
    """
    Print the size of the data returned by a Morphware query
    using Morphare-provided data source endpoint:

    curl --request POST http://167.172.239.133:5000/products -H "Content-Type: application/json" \
    -d '{"provider":"amazon","service":"compute","region":"us-east-1"}'

    Example:
    $ python scripts/morphware_data_sizes.py
    """
    # Retrieve data from source provided by Morphware
    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }
    json_data = {
        "provider": "amazon",
        "service": "compute",
        "region": "us-east-1",
    }
    rsp = requests.post("http://167.172.239.133:5000/products", headers=headers, json=json_data)
    d = json.loads(rsp.text)
    unfiltered_data = d["products"]
    print("Num products:", len(unfiltered_data))

    # Remove unneeded product data
    data = []
    for i in range(len(unfiltered_data)):
        data.append(
            json.dumps(
                {
                    "instanceType": unfiltered_data[i]["type"],
                    "numCPUs": str(unfiltered_data[i]["cpusPerVm"]),
                    "RAM": str(unfiltered_data[i]["memPerVm"]),
                    "onDemandPricePerHour": str(unfiltered_data[i]["onDemandPrice"]),
                }
            )
        )
    print("Expample filtered data:")
    print(json.dumps(data[:2], indent=4))

    # Get size of encoded string[]
    q = Morphware(version=1)
    submit_value = q.value_type.encode(data)
    print(f"Size of data being reported: {sys.getsizeof(submit_value)} bytes")
    # print(submit_value.hex())


if __name__ == "__main__":
    main()
