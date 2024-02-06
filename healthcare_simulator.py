import logging
from healthcare_manager import PoseManager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:

    print("start simulator")
    hm = PoseManager()

if __name__ == '__main__':

    main()
    
