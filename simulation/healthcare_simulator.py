import logging
import subprocess
# from healthcare_manager import PoseManager
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:

    scripts = [".\pose_armleg\Pose1_manager.py", ".\pose_pushup\Pose2_manager.py", ".\pose_situp\Pose3_manager.py"]

    processes = []
    for script in scripts:
        process = subprocess.Popen(["python", script])
        processes.append(process)

    for process in processes:
        process.wait()

if __name__ == '__main__':

    
    main()

