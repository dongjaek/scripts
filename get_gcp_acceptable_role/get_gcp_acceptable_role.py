import argparse
import yaml


def setup_cli():
  parser = argparse.ArgumentParser(description="Process some integers.")
  parser.add_argument("--output", type=str, help="output filename")
  parser.add_argument("--input", type=str, help="input filename")
  parser.add_argument("--roles", type=str, help="roles filename")
  args = parser.parse_args()
  return args


def read_input(input_file):
  if input_file:
    with open(input_file, "r") as f:
      return yaml.safe_load(f)


def write_output(output_file, candidates):
  if output_file:
    with open(output_file, "w") as f:
      yaml.dump(candidates, f, default_flow_style=False)
  else:
    print(yaml.dump(candidates))


if __name__ == "__main__":
  args = setup_cli()

  roles = read_input(args.roles)
  query_dict = read_input(args.input)
  candidates = {"roles": []}
  query = set(query_dict["permissions"])

  for role in roles["roles"]:
    role_permissions_set = set(role["role"]["permissions"])
    if query.issubset(role_permissions_set):
      candidates["roles"].append(role["role"]["name"])

  write_output(args.output, candidates)
