import argparse
import subprocess
import yaml


def get_user_roles(project, user):
  cmd_segments = [
    "gcloud projects get-iam-policy",
    project,
    '--flatten="bindings[].members"',
    '--format="yaml(bindings.role)"',
    '--filter=bindings.members:{}'.format(user)
  ]
  cmd = " ".join(cmd_segments)
  roles = []
  try:
    output = subprocess.check_output(cmd, shell=True)
    documents = yaml.safe_load_all(output)
    for document in documents:
      roles.append(document['bindings']['role'])
  except:
    print("Error obtaining roles for user: {} in project: {}".format(user, project))
  return roles


def get_role_permissions(role):
  try:
    output = subprocess.check_output("gcloud iam roles describe {}".format(role), shell=True)
    return yaml.safe_load(output).get("includedPermissions", [])
  except:
    print("Error obtaining permissions for role: {}".format(role))
    return []
  return []


def setup_cli():
  parser = argparse.ArgumentParser(description="Get permissions a user has")
  parser.add_argument("--output", type=str, help="output filename")
  parser.add_argument("--project", type=str, help="project-id")
  parser.add_argument("--user", type=str, help="user to query")
  args = parser.parse_args()
  return args

if __name__ == "__main__":
  args = setup_cli()
  roles = get_user_roles(args.project, args.user)
  permissions_map = {}
  permissions_map['user'] = args.user
  permissions_map['roles'] = []
  for role in roles:
    permissions = get_role_permissions(role)
    permissions_map['roles'].append({"role": role, "permissions": permissions})

  if args.output:
    with open(args.output, "w") as f:
      yaml.dump(permissions_map, f, default_flow_style=False)
  else:
    yaml.dump(permissions_map)
