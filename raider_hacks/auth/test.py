import base64

x = base64.b64encode(bytes("swag","utf-8"))

print(x)

try:
    y = base64.b64decode(bytes(x))
#    y = base64.b64decode("flarg")

except ValueError:
    print("Fail")
else:
    print("Success")

print(y)
