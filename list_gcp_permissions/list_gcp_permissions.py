import argparse
import multiprocessing
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
        try:
            output = subprocess.check_output("gcloud iam roles describe {}".format(role), shell=True) # noqa
            return {"role": {"name": role, "permissions": yaml.safe_load(output).get("includedPermissions", [])}} # noqa
        except:
            return {"role": {"name": role, "permissions": []}}
    return {"role": {"name": role, "permissions": []}}


def setup_cli():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--output", type=str, help="output filename")
    parser.add_argument("--threads", type=int, help="number of threads to use")
    args = parser.parse_args()
    return args


def write_output(output_file, permissions_map):
    if output_file:
        with open(output_file, "w") as f:
            yaml.dump(permissions_map, f, default_flow_style=False)
    else:
        print(yaml.dump(permissions_map))


if __name__ == "__main__":
    args = setup_cli()
    roles = get_roles()
    permissions_map = {}

    if args.threads:
        thread_pool = multiprocessing.Pool(args.threads)
        permissions_role_mappings = thread_pool.map(get_permissions, roles)
        permissions_map["roles"] = permissions_role_mappings
    else:
        permissions_map["roles"] = []
        for role in roles:
            permissions_map["roles"].append(get_permissions(role))

    write_output(args.output, permissions_map)
