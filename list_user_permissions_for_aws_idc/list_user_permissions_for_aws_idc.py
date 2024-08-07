import click
from list_user_permissions_for_aws_idc.list_user_permissions import list_user_permissions


@click.command()
@click.option("--profile", default=None, show_default=False)
@click.option("--region", default=None, show_default=False)
def main(profile, region):
    list_user_permissions(profile, region)
