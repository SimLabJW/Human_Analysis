from pyevsim import BehaviorModelExecutor, SysMessage, Infinite
# from return_result import Return_result_Model

# from image_angle import Image_Pose_Angle_Model
# from image_folder import Reading_Folder_Model

class Manager():
    def __init__(self) -> None:
        
        # Result_m = Return_result_Model(0, Infinite, "Result_m", "CARE")
        self.reading = ""


    def start(self) -> None:
        while True:
            print(self.reading)

    def save_data(self,data):
        self.reading = data
        # print(f"data_manager.py {self.reading}")

        # return self.reading
    
    def return_data(self):
        return self.reading
    
