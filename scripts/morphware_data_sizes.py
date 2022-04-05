"""Print the size of the data returned by a Morphware query (data reported)."""
import json
import sys

import requests

from telliot_core.queries.morphware import Morphware


def main():
    """
    Print the size of the data returned by a Morphware query
    using Morphare-provided data source endpoint:

    curl --request POST http://167.172.239.133:5000/products-2 -H "Content-Type: application/json" \
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
    rsp = requests.post("http://167.172.239.133:5000/products-2", headers=headers, json=json_data)
    unfiltered_data = json.loads(rsp.text)
    print("Num products:", len(unfiltered_data))

    # Remove unneeded product data
    data = []
    for i in range(len(unfiltered_data)):
        data.append(
            json.dumps(
                {
                    "instanceType": unfiltered_data[i]["Instance Type"],
                    "cudaCores": unfiltered_data[i]["CUDA Cores"],
                    "numCPUs": unfiltered_data[i]["Number of CPUs"],
                    "RAM": unfiltered_data[i]["RAM"],
                    "onDemandPricePerHour": unfiltered_data[i]["On-demand Price per Hour"],
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
