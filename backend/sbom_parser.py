import json

def detect_ecosystem(item):
    """
    Detect ecosystem based on Syft metadata
    """

    purl = item.get("purl", "")

    if "npm" in purl:
        return "npm"
    elif "pypi" in purl:
        return "PyPI"
    elif "maven" in purl:
        return "Maven"
    else:
        return "UNKNOWN"

def parse_sbom(sbom_file):
    with open(sbom_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dependencies = []
    artifacts = data.get("artifacts", [])

    for item in artifacts:
        name = item.get("name")
        version = item.get("version")

        if name and version:
            ecosystem = detect_ecosystem(item)

            dependencies.append({
                "name": name,
                "version": version,
                "ecosystem": ecosystem
            })

    print(f"Found {len(dependencies)} dependencies")

    return dependencies