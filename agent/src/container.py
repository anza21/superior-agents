import os
import tempfile
from typing import Tuple, cast, Dict, Any
from result import Result, Ok, Err
import docker
from docker.models.containers import Container
from src.helper import timeout


class ContainerManager:
    def __init__(self, container: Container, in_con_env: Dict[str, str]):
        self.container = container
        self.in_con_env = in_con_env

    def write_code_in_con(self, code: str, postfix: str) -> Tuple[str, str]:
        # Καθαρισμός backticks από τον κώδικα
        cleaned_code = code.strip()
        if cleaned_code.startswith("```python") and cleaned_code.endswith("```"):
            cleaned_code = cleaned_code[9:-3].strip()
        elif cleaned_code.startswith("```") and cleaned_code.endswith("```"):
            cleaned_code = cleaned_code[3:-3].strip()

        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=f"_{postfix}.py") as temp_code_file:
            temp_code_file.write(cleaned_code)
            temp_code_path = temp_code_file.name

        # Αντιγραφή στο container
        archive_name = temp_code_path + ".tar"
        tar_cmd = f"tar -cf {archive_name} -C {os.path.dirname(temp_code_path)} {os.path.basename(temp_code_path)}"
        os.system(tar_cmd)

        with open(archive_name, "rb") as archive:
            self.container.put_archive("/", archive.read())

        os.remove(archive_name)
        return f"/{os.path.basename(temp_code_path)}", cleaned_code

    def run_code_in_con(self, code: str, postfix: str) -> Result[Tuple[str, str], str]:
        temp_file_path, reflected_code = self.write_code_in_con(code, postfix)
        command_str = f"python -u {temp_file_path} 2>&1"
        cmd = ["/bin/sh", "-c", command_str]

        try:
            with timeout(seconds=600):
                python_exit_code, python_output = cast(
                    Tuple[int, bytes],
                    self.container.exec_run(
                        cmd=cmd,
                        environment=self.in_con_env,
                        demux=False,
                        stream=False
                    ),
                )
                python_output_str = python_output.decode("utf-8", errors="replace")
        except TimeoutError as e:
            return Err(f"ContainerManager.run_code_in_con: Code ran too long, error: \n{e}")
        except docker.errors.ContainerError as e:
            return Err(f"ContainerManager.run_code_in_con: Container error, error: \n{e}")

        # Σταματά όλα τα python processes για ασφάλεια
        self.container.exec_run(cmd="kill -9 $(pidof python)")

        if python_exit_code != 0:
            return Err(f"ContainerManager.run_code_in_con: Code that has been run failed, program output: \n{python_output_str}")

        return Ok((python_output_str, reflected_code))
