from telliot.queries import LegacyQuery

q = LegacyQuery(legacy_tip_id=1)
print(q.descriptor)
print(f"addTip data: 0x{q.tip_data.hex()}")
print(f"addTip ID: 0x{q.tip_id.hex()}")

value = 10000.1234567
print(f"submitValue (float): {value}")

encoded_bytes = q.value_type.encode(value)
print(f"submitValue (bytes): 0x{encoded_bytes.hex()}")

decoded_value = q.value_type.decode(encoded_bytes)
print(f"Decoded value (float): {decoded_value}")
