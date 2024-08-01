import pyotp as tp
import credentials as cr

#create a method and return totp
def get_totp():
    totp = tp.TOTP(cr.totp_key).now()
    return totp
