import json
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings


def retrieveAzureData():
    with open('../Sensing/credentials.json') as f:
        creds = json.load(f)

    block_blob_service = BlockBlobService(account_name=creds['azure']['account_name'],
                                        account_key=creds['azure']['account_key'])

    block_blob_service.get_blob_to_path(creds['azure']['container'], 'Twitter_data.csv', 'Twitter_data.csv')
    block_blob_service.get_blob_to_path(creds['azure']['container'], 'CMC_data.csv', 'CMC_data.csv')
    
    print("Twitter_data.csv and CMC_data.csv successfully retrieved from Azure blob storage")

