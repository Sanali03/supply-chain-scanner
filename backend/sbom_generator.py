import subprocess
import os


def generate_sbom(project_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    syft_path = os.path.join(BASE_DIR, "syft.exe")

    output_file = os.path.join(BASE_DIR, "sbom.json")
    project_full_path = os.path.abspath(project_path)

    # Check if syft exists
    if not os.path.exists(syft_path):
        print("syft.exe not found in backend folder!")
        return None

    command = [
        syft_path,
        project_full_path,
        "-o",
        "json"
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("Syft Error:")
            print(result.stderr)
            return None

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print("SBOM generated successfully!")
        return output_file

    except Exception as e:
        print("Unexpected error:", e)
        return None