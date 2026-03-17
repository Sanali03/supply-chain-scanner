from sbom_generator import generate_sbom
from sbom_parser import parse_sbom
from db_service import save_project_and_dependencies


def main():
    project_path = "../venv"
    project_name = "Test Project"

    sbom_file = generate_sbom(project_path)

    if sbom_file:
        dependencies = parse_sbom(sbom_file)
        save_project_and_dependencies(project_name, project_path, dependencies)


if __name__ == "__main__":
    main()