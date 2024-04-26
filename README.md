# AWS IDC List User Permissions

List all users and their corresponding permissions within AWS SSO.

Will iterate through all users, and determine their permissions (either directly attached, or via a Group)

## Install & Use

    $ pip install aws-idc-list-user-permissions
    $ aws-idc-list-user-permissions

Ensure that the you run this in the account where AWS Identity Center (previously AWS SSO) is setup, and the in the correct region. Use the corresponding environment variables:

## Output

The script outputs two files, a short 5 column CSV, and a long jsonl file. 

The jsonl file contains all details about the user, account, permission set, and group (if applicable), in a denormalized jsonl file. This file contains one json document per line, which makes reading and discovery easy.

The csv file contains only the 5 columns:
    * User Name (this is the user's display name in AWS IDC)
    * Account Name (the name of the account in AWS Organizations)
    * Permission Set Name (the name of the permission set)
    * InheritfromGroup (a column to indicate if the user inherited the permissions from a group or not)
    * GroupName (if the user inherited this permission set from a group, this is the name of that group)

## Other Notes

I made this over a weekend -- still very much beta.
