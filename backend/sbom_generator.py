import subprocess
import os


def generate_sbom(project_path):
    output_file = "sbom.json"

    syft_path = os.path.join(os.getcwd(), "syft.exe")
    project_full_path = os.path.abspath(project_path)

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