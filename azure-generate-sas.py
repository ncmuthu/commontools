from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def generate_sas_url(storage_account_name, storage_account_key, container_name, blob_name, expiry_hours):
    # Construct the connection string
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};"

    # Create the BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get the BlobClient for the specified blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Set the expiry time for the SAS token
    expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)

    # Generate the SAS token for the blob
    sas_token = generate_blob_sas(
        account_name=storage_account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=storage_account_key,
        permission=BlobSasPermissions(read=True),  # Specify the permissions for the SAS token
        expiry=expiry_time
    )

    # Construct the SAS URL
    sas_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

    return sas_url

if __name__ == "__main__":
    storage_account_name = ""
    storage_account_key = ""
    container_name = ""
    blob_name = ""
    expiry_hours = 1  # SAS token expiry time in hours

    sas_url = generate_sas_url(storage_account_name, storage_account_key, container_name, blob_name, expiry_hours)
    print("Generated SAS URL:", sas_url)
