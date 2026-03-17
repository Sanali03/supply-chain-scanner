import json


def parse_sbom(sbom_file):
    with open(sbom_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dependencies = []
    artifacts = data.get("artifacts", [])

    for item in artifacts:
        name = item.get("name")
        version = item.get("version")

        if name and version:
            dependencies.append({
                "name": name,
                "version": version,
                "ecosystem": "PyPI"
            })

    print(f"Found {len(dependencies)} dependencies")

    return dependencies