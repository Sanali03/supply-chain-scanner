from backend.sbom_generator import generate_sbom
from backend.sbom_parser import parse_sbom
from backend.db_service import save_project_and_dependencies


def run_scan(project_name, project_path, progress_callback=None):
    """
    Main scan pipeline with real-time progress support
    """

    print("Starting scan...")

    # =========================
    # STEP 1: Generate SBOM
    # =========================
    sbom_file = generate_sbom(project_path)

    if not sbom_file:
        print("Failed to generate SBOM")
        return None

    # Optional small progress bump
    if progress_callback:
        progress_callback(5)

    # =========================
    # STEP 2: Parse SBOM
    # =========================
    dependencies = parse_sbom(sbom_file)

    print(f"Found {len(dependencies)} dependencies")

    # Optional progress bump before heavy work
    if progress_callback:
        progress_callback(10)

    # =========================
    # STEP 3: Save + Scan Vulnerabilities
    # =========================
    save_project_and_dependencies(
        project_name,
        project_path,
        dependencies,
        progress_callback=progress_callback  # ✅ CRITICAL LINE
    )

    # =========================
    # FINAL COMPLETE
    # =========================
    if progress_callback:
        progress_callback(100)

    print("✅ Scan completed")

    return True