import subprocess
import os
import sys
import shutil
import tempfile


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def generate_sbom(project_path):

    BASE_DIR = get_base_dir()

    # Correct syft path
    syft_path = os.path.join(BASE_DIR, "backend", "syft.exe")

    if not os.path.exists(syft_path):
        syft_path = os.path.join(BASE_DIR, "syft.exe")

    print("Syft path:", syft_path)

    if not os.path.exists(syft_path):
        print("syft.exe not found!")
        return None

    # Use SAFE temp directory
    temp_dir = tempfile.gettempdir()
    temp_syft = os.path.join(temp_dir, "syft_temp.exe")

    try:
        shutil.copy(syft_path, temp_syft)
    except Exception as e:
        print("Copy failed:", e)
        temp_syft = syft_path  # fallback

    output_file = os.path.join(temp_dir, "sbom.json")
    project_full_path = os.path.abspath(project_path)

    command = [
        temp_syft,
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
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=120   # prevents hanging
        )

        print("Return code:", result.returncode)

        if result.returncode != 0:
            print("Syft Error:")
            print(result.stderr)
            return None

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print("SBOM generated successfully!")
        return output_file

    except subprocess.TimeoutExpired:
        print("Syft timed out!")
        return None

    except Exception as e:
        print("Unexpected error:", e)
        return None

    finally:
        # Clean temp file
        try:
            if os.path.exists(temp_syft):
                os.remove(temp_syft)
        except:
            pass