import boto3
from moto import mock_aws
from aws_idc_list_user_permissions.list_utils import list_accounts


@mock_aws
def test_create_org():
    client = boto3.client("organizations")

    client.create_organization(FeatureSet="ALL")

    for num_account in range(1, 10):
        client.create_account(
            Email=f"{num_account}@example.com", AccountName=f"Account-{num_account}"
        )

    accounts = list_accounts(client)

    assert len(accounts.keys()) == 10
