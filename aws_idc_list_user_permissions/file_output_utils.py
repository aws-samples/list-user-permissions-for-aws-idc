import json
from pathlib import Path
import csv

from datetime import date, datetime


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    This is especially true as Boto sometimes returns date as Datetime object.
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def output_to_jsonl(user_assignments: list, filename: str) -> None:
    """
    Output data to jsonl. One line per user assignment
    """

    file_path = Path(filename)
    with open(file_path, "w", encoding="utf-8") as output_file:
        for assignment in user_assignments:
            output_file.write(json.dumps(assignment, default=json_serial))
            output_file.write("\n")

    print(f"Long output available at {file_path}")


def output_to_csv(user_assignments: list, filename: str) -> None:
    """
    Output data to csv. One line per user assignment
    """

    file_path = Path(filename)
    with open(file_path, "w", encoding="utf-8") as output_file:
        fieldnames = [
            "UserName",
            "AccountName",
            "PermissionSet",
            "InheritFromGroup",
            "GroupName",
        ]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for assignment in user_assignments:
            if assignment["PrincipalType"] == "USER":
                inherit_from_group = False
            elif assignment["PrincipalType"] == "GROUP":
                inherit_from_group = True
            else:
                raise AttributeError

            if inherit_from_group:
                group_name = assignment["group_details"]["DisplayName"]
            else:
                group_name = "n.a"

            assignment_row = {
                "AccountName": assignment["account_details"]["Name"],
                "UserName": assignment["user_details"]["UserName"],
                "PermissionSet": assignment["permission_set_details"]["Name"],
                "InheritFromGroup": str(inherit_from_group),
                "GroupName": group_name,
            }

            writer.writerow(assignment_row)
        print(f"Short output available at {file_path}")
    return None
