from telliot.queries import StringQuery

q = StringQuery(text='What is the meaning of life?')
print(q.descriptor)
print(f"addTip data: 0x{q.tip_data.hex()}")
print(f"addTip ID: 0x{q.tip_id.hex()}")

value = "Please refer to: https://en.wikipedia.org/wiki/Meaning_of_life"
print(f"submitValue (str): {value}")

encoded_bytes = q.value_type.encode(value)
print(f"submitValue (bytes): 0x{encoded_bytes.hex()}")

decoded_value = q.value_type.decode(encoded_bytes)
print(f"Decoded value (float): {decoded_value}")
