import pyotp

key = 'QPG5GKKVYOC57EPW6PNF435ACQ6WXRYB'
totp = pyotp.TOTP(key)
print(totp.now())
