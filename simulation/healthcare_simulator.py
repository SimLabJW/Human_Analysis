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

    # 각 스크립트에 대해 가상환경 활성화 및 스크립트 실행
    for script in ["pose_armleg\Pose1_manager.py", "pose_pushup\Pose2_manager.py", "pose_situp\Pose3_manager.py"]:
        # 가상환경 활성화 스크립트 파일 경로
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        # 가상환경 활성화 명령어
        activate_cmd = f'call "{activate_script}" && python "{script}"'
        # subprocess로 명령어 실행
        subprocess.call(activate_cmd, shell=True)

if __name__ == '__main__':
    main()
