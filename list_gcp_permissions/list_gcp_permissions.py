import argparse
import subprocess
import yaml


def get_roles():
    roles = []
    try:
        output = subprocess.check_output("gcloud iam roles list", shell=True)
    except:
        return []
    for document in yaml.safe_load_all(output):
        roles.append(document["name"])
    return roles


def get_permissions(role):
    if role:
        output = subprocess.check_output("gcloud iam roles describe {}".format(role), shell=True)
        try:
            return yaml.safe_load(output).get("includedPermissions", [])
        except:
            return []
    return []


def setup_cli():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--output", type=str, help="output filename")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    roles = get_roles()
    permissions_map = {}
    for role in roles:
        permissions_map["role"] = get_permissions(role)
    args = setup_cli()
    if args.output:
        with open(args.output, "w") as f:
            yaml.dump(permissions_map, f, default_flow_style=False)
    else:
        print(yaml.dump(permissions_map))
