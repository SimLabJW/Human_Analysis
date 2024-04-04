from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
from config import *
import json
import random
import string
import socket

class Return_result_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("data-ing",1)
        self.insert_state("pose_in",1)

        self.insert_input_port("next")
        self.insert_input_port("stop")
        self.insert_input_port("start")

        self.insert_output_port("pose_select")

        self.client_socket = self.connect_to_server()

        self.result_dic = {}
        
    def ext_trans(self, port, msg):
        if port == "start":
            print("It checks that the data is not empty and while data is being added for the action.")
            self._cur_state = "Generate"

        if port == "next":
            self.result = msg.retrieve()
            self.send_data(self.result_dic)
        
        if port == "stop":
            # 동작 기준 정보 불러오기
            self.result = msg.retrieve()
            # 보낼 정보 모음집
            for key in Key_LIST:
                if key == 'Way':
                    # 랜덤으로 4, 5, 6 중에서 하나의 숫자 선택
                    way_values = random.sample([4, 5, 6], 2)
                    self.result_dic[key] = way_values
                elif key == 'Health':
                    self.result_dic[key] = 100
                elif key == 'S/F':
                    self.result_dic[key] = self.result
                elif key == 'Pose_Data':
                    self.result_dic[key] = [
                        [1, 2],
                        [3, 4],
                        [5, 6]
                    ]
                else:
                    # 랜덤 문자열 생성
                    random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
                    self.result_dic[key] = random_string

            self.send_data(self.result_dic)
            self._cur_state = "Wait"
            
        if self._cur_state == "angle_trans":
            msg = SysMessage(self.get_name(), "pose_select")
            msg.insert()
            
            return msg
        
    def output(self): 

        if self._cur_state == "Generate":
            self.rec_data = self.receive_data()
            if self.rec_data == "arm_leg":
                self._cur_state = "pose_in"
            else:
                print("run----arm_leg")
            
        if self._cur_state == "pose_in":
            msg = SysMessage(self.get_name(), "pose_select")
            # 포즈 선택 후 같은 소켓으로 이미지 데이터 받을 수 있도록
            # msg.insert([self.rec_data]) 
            return msg
           

        if self._cur_state == "data-ing":
            msg = SysMessage(self.get_name(), "messeging")
            return msg
        
        if self._cur_state == "Wait":
            self._cur_state = "Wait"


            
    def int_trans(self):
        if self._cur_state == "data-ing":
            self._cur_state = "Wait"
        if self._cur_state == "Wait":
            self._cur_state = "Wait"
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

    
 
    def connect_to_server(self):
        # 서버 주소와 포트
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 12345

        # 소켓 생성
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # 서버에 연결
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            # print("서버에 연결되었습니다.")
            return self.client_socket

        except Exception as e:
            # print("서버 연결 중 오류 발생:", e)
            return None
        

    def send_data(self,data):
    
        if self.client_socket:
            try:
                # 리스트를 JSON 형식의 문자열로 변환
                json_data = json.dumps(data)
                # 첫 번째 데이터 전송
                self.client_socket.send(json_data.encode())

            except Exception as e:
                pass
                # print("데이터 전송 중 오류 발생:", e) 



    def receive_data(self):
        if self.client_socket:
            try:
                # 데이터 수신
                response = self.client_socket.recv(1024).decode()
                # print("서버 응답:", response)
                return response

            except Exception as e:
                # print("데이터 수신 중 오류 발생:", e)
                return None
        else:
            # print("소켓이 연결되지 않았습니다.")
            return None