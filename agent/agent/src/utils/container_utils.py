import docker
from loguru import logger

class ContainerManager:
    """
    A class for managing Docker containers.
    This is used to run code inside a container.
    """

    def __init__(self, client, container_name: str, code_path: str, in_con_env: bool):
        """
        Initializes the ContainerManager with necessary details.

        Args:
            client (docker.client.DockerClient): The Docker client object
            container_name (str): The name of the container
            code_path (str): Path to the code to be executed
            in_con_env (bool): Flag to determine if it's in a containerized environment
        """
        self.client = client
        self.container_name = container_name
        self.code_path = code_path
        self.in_con_env = in_con_env

    def _get_container(self):
        """
        Returns the container object based on the container name.
        """
        return self.client.containers.get(self.container_name)

    def run_code_in_con(self, code: str, task_name: str):
        """
        Runs code inside the container and returns the result.

        Args:
            code (str): The code to run in the container.
            task_name (str): The name of the task for logging.

        Returns:
            str: The result of running the code in the container.
        """
        logger.info(f"Running {task_name} in container {self.container_name}")

        container = self._get_container()

        try:
            result = container.exec_run(f"python {self.code_path}/{task_name}.py", stdin=True, stdout=True, stderr=True)
            logger.info(f"Result from running {task_name}: {result.output.decode('utf-8')}")
            return result
        except Exception as e:
            logger.error(f"Error running {task_name}: {e}")
            raise RuntimeError(f"Failed to run {task_name} inside container")

# Export the class to make it available for import
__all__ = ["ContainerManager"]
