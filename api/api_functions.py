import requests
import json


BASE_URL = "https://ws.efsllc.com/axis2/services/CardManagementWS/"


# shu datalarni olish kk, kontraktda yozilgan bosa kk
CLIENT_ID = ""
CONTRACT_ID = ""
MASTER_CONTRACT_ID = ""

# bularni bilsez kk
username = ''
password = ''



# Login to the EFS API to get a client ID
def login():
    response = requests.post(f'{BASE_URL}/login', data={'username': username, 'password': password})
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()['clientId']

def logout(client_id):
    response = requests.post(f'{BASE_URL}/logout', data={'clientId': client_id})
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()




# Issue a money code
def issue_money_code(client_id, contract_id, master_contract_id, amount, fee_type, issued_to, notes, currency):
    data = {
        'clientId': client_id,
        'contractId': contract_id,
        'masterContractId': master_contract_id,
        'amount': amount,
        'feeType': fee_type,
        'issuedTo': issued_to,
        'notes': notes,
        'currency': currency,
    }
    response = requests.post(f'{BASE_URL}/issueMoneyCode', data=json.dumps(data))
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()


# Use the functions
# client_id = login()
# money_code = issue_money_code(client_id, contract_id=CONTRACT_ID, master_contract_id=-1, amount=5.00, fee_type=0, issued_to='Test driver', notes='Test', currency='USD')
# print(money_code)
# logout(CLIENT_ID)