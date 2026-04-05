from backend.sbom_generator import generate_sbom
from backend.sbom_parser import parse_sbom
from backend.db_service import save_project_and_dependencies

def run_scan(project_name, project_path):
    sbom_file = generate_sbom(project_path)

    if not sbom_file:
        return None

    dependencies = parse_sbom(sbom_file)

    save_project_and_dependencies(
        project_name,
        project_path,
        dependencies
    )

    return True