from generate_auth_code import generateAuthCode
import credentials as cr
from fyers_apiv3 import fyersModel

client_id = cr.client_id
secret_key = cr.secret_key
redirect_uri = cr.redirect_uri
response_type = cr.response_type  
state = cr.state
grant_type = cr.grant_type
auth_code = cr.auth


def generateAccessToken():
    auth_code = generateAuthCode()
    
    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )

    # Set the authorization code in the session object
    session.set_token(auth_code)

    # Generate the access token using the authorization code
    response = session.generate_token()

    # Print the response, which should contain the access token and other details
    # print(response)

    access_token=response['access_token']
    print(access_token)
    with open('access.txt','w') as k:
        k.write(access_token)