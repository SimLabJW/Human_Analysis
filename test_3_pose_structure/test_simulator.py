import logging

import subprocess


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:

    scripts = ["test_manager.py", "test2_manager.py", "test3_manager.py"]

    processes = []
    for script in scripts:
        process = subprocess.Popen(["python", script])
        processes.append(process)

    for process in processes:
        process.wait()

if __name__ == '__main__':

    
    main()