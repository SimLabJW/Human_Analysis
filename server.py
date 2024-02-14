from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
from core.instance.config import *
import json
from flask import Flask
from flask import request, Response, jsonify

app = Flask(__name__)
shared_data = ''
class Server_POST_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("trans",1)

        self.insert_input_port("start")
        self.insert_output_port("trans_data")
        app.run(host=SimulationWebServerConfig.HOST, port=SimulationWebServerConfig.PORT)

    def ext_trans(self, port, msg):
        
        if port == "start":
            # 동작 기준 정보 불러오기
            
            self._cur_state = "Generate"

      
    def output(self): 

        if self._cur_state == "Generate":
            # 조건 자동삽입
            # if shared_data:
            msg = SysMessage(self.get_name(), "trans_data")
            msg.insert([shared_data])
            # print(f"server-----------------{shared_data}------------")
            # self._cur_state = "Generate"
            return msg
            
            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

            
    
    @app.route('/simulate', methods=['POST'])
    def simulate_handler():
        global shared_data
        '''
        Input Data Type == json / return data must me json
        '''
        if request.method == 'POST':
            try:
                input_data = request.data
                if request.data:
                    input_data = json.loads(input_data)
                    shared_data = input_data['data']
                    return jsonify('')
                else:
                    return jsonify('')
            except Exception as e:
                return jsonify('')