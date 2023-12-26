import base64

original_string = "RimmelAsghar"

encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
encoded_string = encoded_bytes.decode('utf-8')

print("Original String:", original_string)
print("Base64 Encoded String:", encoded_string)
