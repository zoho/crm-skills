#!/usr/bin/env python3
"""Extract a single operation + its requestBody/2xx schemas from a Zoho CRM OAS YAML file."""
import argparse
import sys

try:
    import yaml
except ImportError:
    print("pyyaml not installed. Run: pip3 install pyyaml")
    sys.exit(1)

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "options", "head", "trace"}


def collect_refs(node, refs=None):
    """Collect $ref names pointing to #/components/schemas/ without recursing into found schemas."""
    if refs is None:
        refs = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str) and v.startswith("#/components/schemas/"):
                refs.add(v.split("/")[-1])
            else:
                collect_refs(v, refs)
    elif isinstance(node, list):
        for item in node:
            collect_refs(item, refs)
    return refs


def extract(api_dir, resource, operation_id):
    yaml_path = f"{api_dir}/{resource}/{resource}.yaml"
    try:
        with open(yaml_path) as f:
            spec = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"File not found: {yaml_path}")
        print(f"Check --api-dir ({api_dir!r}) and --resource ({resource!r}).")
        sys.exit(1)

    # --- SERVERS ---
    servers = spec.get("servers", [])
    print("=== SERVERS ===")
    if servers:
        print(yaml.dump(servers[0], default_flow_style=False).rstrip())
    print()

    # --- OPERATION ---
    paths = spec.get("paths", {})
    found_path = found_method = found_op = None

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, op in path_item.items():
            if method.lower() not in HTTP_METHODS:
                continue
            if isinstance(op, dict) and op.get("operationId") == operation_id:
                found_path, found_method, found_op = path, method.lower(), op
                break
        if found_op:
            break

    if not found_op:
        available = sorted(
            op.get("operationId", "")
            for path_item in paths.values()
            if isinstance(path_item, dict)
            for method, op in path_item.items()
            if method.lower() in HTTP_METHODS and isinstance(op, dict) and "operationId" in op
        )
        print(f"operationId '{operation_id}' not found in {yaml_path}")
        print(f"Available operationIds: {', '.join(available)}")
        sys.exit(1)

    print("=== OPERATION ===")
    print(yaml.dump({found_path: {found_method: found_op}}, default_flow_style=False).rstrip())
    print()

    # --- SCHEMAS: requestBody + 2xx responses only; error schemas excluded ---
    components = spec.get("components", {}).get("schemas", {})
    scope_nodes = []

    if "requestBody" in found_op:
        scope_nodes.append(found_op["requestBody"])

    for code, response in found_op.get("responses", {}).items():
        if str(code).startswith("2"):
            scope_nodes.append(response)

    refs = set()
    for node in scope_nodes:
        collect_refs(node, refs)

    print("=== SCHEMAS ===")
    for name in sorted(refs):
        if name in components:
            print(yaml.dump({name: components[name]}, default_flow_style=False).rstrip())
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Extract an OAS operation and its requestBody/2xx schemas."
    )
    parser.add_argument("--api-dir", required=True, help="Path to .zoho-crm/references/api/")
    parser.add_argument("--resource", required=True, help="Resource folder name (e.g. record)")
    parser.add_argument("--operation", required=True, help="operationId to extract")
    args = parser.parse_args()
    extract(args.api_dir, args.resource, args.operation)


if __name__ == "__main__":
    main()
