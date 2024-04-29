# AWS IDC List User Permissions

List all users and their corresponding permission set within an AWS Identity Center instance. AWS Identity Center is the new name for AWS SSO.

Will iterate through all users, and determine their permission sets (either directly attached to the user, or via a Group).

## Install & Use

    $ pip install aws-idc-list-user-permissions
    $ aws-idc-list-user-permissions

Ensure that the you run this in the account where AWS Identity Center (previously AWS SSO) is setup, and the in the correct region. You may supply a region and aws profile if you use the non default:

    $ aws-idc-list-user-permissions --profile my-org-profile --region us-east-1

## Output

The script outputs two files, a short 5 column CSV, and a long jsonl file. 

The jsonl file contains all details about the user, account, permission set, and group (if applicable), in a denormalized jsonl file. This file contains one json document per line, to make discovery easy.

The csv file contains only the 5 columns:
* User Name (this is the user's display name in AWS IDC)
* Account Name (the name of the account in AWS Organizations)
* Permission Set Name (the name of the permission set)
* InheritfromGroup (a column to indicate if the user inherited the permissions from a group or not)
* GroupName (if the user inherited this permission set from a group, this is the name of that group)

## Notes

If an account or permission set exists with no users attached to it, this report will not have a item on the list for it. Only permissions sets with account assignments associated with actual users will appear on the list.

Similarly, groups with no users as members will also not appear on the list.