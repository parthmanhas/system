from fyers_api import accessToken
import sys

with open('config.txt') as f:
    config = f.readlines()

client_id = config[0].split(' = ')[1].split('\n')[0]
secret_key = config[1].split(' = ')[1].split('\n')[0]
redirect_uri = config[2].split(' = ')[1].split('\n')[0]
response_type = config[3].split(' = ')[1].split('\n')[0]
grant_type = config[4].split(' = ')[1].split('\n')[0]
state = config[5].split(' = ')[1].split('\n')[0]
scope = config[6].split(' = ')[1].split('\n')[0]
nonce = config[7].split(' = ')[1].split('\n')[0]

session = accessToken.SessionModel(client_id=client_id,
                                   secret_key=secret_key, redirect_uri=redirect_uri,
                                   response_type=response_type, grant_type=grant_type,
                                   state=state, nonce=nonce)

response = session.generate_authcode()

if(len(sys.argv) > 1):
    auth_code = sys.argv[1].split('auth_code=')[1].split('&state')[0]
else:
    with open('2_auth_code.txt') as f:
        auth_code = f.readlines()[0]
        auth_code = auth_code.split('auth_code=')[1].split('&state')[0]

try:
    session.set_token(auth_code)
    response = session.generate_token()
    if(response['code'] == -413):
        raise Exception("EXCEPTION: " + response['message'])
    access_token = response["access_token"]
    with open('3_access_token.txt', 'w') as f:
        f.write(access_token)
        print('Access token saved!')
except Exception as e:
    print(e)
