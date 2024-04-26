import boto3
from aws_idc_list_user_permissions.list_utils import (
    list_accounts,
    list_instances,
    list_permission_sets,
    list_groups,
    list_user_assignments,
    list_users,
    describe_permissions_sets,
)
from aws_idc_list_user_permissions.output import output_to_jsonl, output_to_csv


def list_user_permissions():
    """
    The main function to run and retrive all details of user permissions
    """

    # setup sessions and clients
    session = boto3.Session()
    org_client = session.client("organizations")
    sso_client = session.client("sso-admin")
    id_store_client = session.client("identitystore")

    # List accounts in AWS Organization, convert to dict
    account_id_lookup = list_accounts(org_client)

    # List AWS IDC instances
    instances = list_instances(sso_client)
    print(f"Found {len(instances)} IDC Instances.")

    # initialize empty list of all user assignments
    full_assignments = list()

    for instance in instances:
        instance_arn = instance["InstanceArn"]
        identity_store_id = instance["IdentityStoreId"]

        # List all permission sets, convert to dict to lookup
        permission_sets = list_permission_sets(sso_client, instance_arn)
        permission_set_arn_lookup = describe_permissions_sets(
            sso_client, permission_sets, instance_arn
        )

        # list all users, convert to dict for lookup
        userid_lookup = list_users(id_store_client, identity_store_id)

        # list all groups, convert to dict for lookup
        groups = list_groups(id_store_client, identity_store_id)
        group_lookup = {item["GroupId"]: item for item in groups}

        # list user_assignments for each user
        user_assignments = []
        total_users = len(userid_lookup.keys())
        for i, user_id in enumerate(userid_lookup.keys()):
            print(f"Looking up user {i+1} of {total_users}")
            user_assignments.extend(
                list_user_assignments(sso_client, user_id, instance_arn)
            )

        # enrich data
        for assignment in user_assignments:
            assignment["instance_arn"] = instance_arn
            assignment["permission_set_details"] = permission_set_arn_lookup[
                assignment["PermissionSetArn"]
            ]
            assignment["user_details"] = userid_lookup[assignment["OriginalPrincipalId"]]
            assignment["account_details"] = account_id_lookup[assignment["AccountId"]]
            # is assignment is via a GROUP, provide details of GROUP
            if assignment["PrincipalType"] == "GROUP":
                assignment["group_details"] = group_lookup[assignment["PrincipalId"]]

        full_assignments.extend(user_assignments)

    sorted_assignments = sorted(
        full_assignments,
        key=lambda d: (d["user_details"]["DisplayName"], d["account_details"]["Name"]),
    )

    output_to_jsonl(sorted_assignments, "./output-full.jsonl")
    output_to_csv(sorted_assignments, "./output-short.csv")

def main():
    list_user_permissions()

