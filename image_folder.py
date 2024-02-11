from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import os
import re
import json
from config import *

class Reading_Folder_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_input_port("start")

        self.grouped_files = {}
        self.count = 0
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            self._cur_state = "Generate"
      
    def output(self): 
        #code
        if self._cur_state == "Generate":
            file_list = os.listdir(IMAGE_FILES)
            for file_name in file_list:
                base_name = re.sub(r'\d+', '', file_name)  # 파일 이름에서 숫자 부분 제거
                key = base_name.lower()  # 대소문자 구분 없이 그룹화하기 위해 소문자로 변환
                number = self.extract_number(file_name)  # 파일 이름에서 숫자 추출

                if key not in self.grouped_files:
                    self.grouped_files[key] = {'files': [], 'count': 0}

                self.grouped_files[key]['files'].append((file_name, number))
                self.grouped_files[key]['count'] += 1

            print(self.grouped_files)
            # JSON 파일로 저장
            json_file_path = IMAGE_JSON
            with open(json_file_path, 'w') as json_file:
                json.dump(self.grouped_files, json_file, indent=2)
                
            self._cur_state = "Wait"  
            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"


    def extract_number(self,file_name):
        match = re.search(r'\d+', file_name)
        return int(match.group()) if match else None

