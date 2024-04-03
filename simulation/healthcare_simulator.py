import logging
import subprocess
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    # 가상환경 경로
    venv_path = r"C:\Users\USER\Desktop\Code\Python_c\Human_Analysis\simulation\venv"

    # 가상환경 활성화 스크립트 파일 경로
    activate_script = os.path.join(venv_path, "Scripts", "activate")

    # 가상환경 활성화 명령어
    activate_cmd = f'call "{activate_script}"'

    # 활성화된 가상환경 내에서 스크립트 실행
    for script in ["pose_armleg\Pose1_manager.py", "pose_pushup\Pose2_manager.py", "pose_situp\Pose3_manager.py"]:
        script_path = os.path.abspath(script)
        process = subprocess.Popen(["python", script_path])
        process.wait()

if __name__ == '__main__':
    main()
