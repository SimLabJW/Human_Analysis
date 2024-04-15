from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
# from config import *

class Pose_Danger_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")

        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("GET_F",1)

        self.insert_input_port("start")

        self.pose_determine()
        # 입력 값에 대한 정보 수정    
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            self.anglist = []
            self.faillist = []
            # 동작 기준 정보 불러오기
            self.landmarks_frame = msg.retrieve()[0]

            self.elbow_angle = self.landmarks_frame[0]
            self.shoulder_angle = self.landmarks_frame[1]
            self.neck_angle = self.landmarks_frame[2]
            self.hip_angle = self.landmarks_frame[3]
            self.knee_angle = self.landmarks_frame[4]
  
            self._cur_state = "Generate"

      
    def output(self): 

        if self._cur_state == "Generate":
            l_elbow = self.elbow_setangle[0][0]< self.elbow_angle[0] <self.elbow_setangle[1][0]
            l_shoulder = self.shoulder_setangle[0][0]< self.shoulder_angle[0] <self.shoulder_setangle[1][0]
            l_neck = self.neck_setangle[0][0]< self.neck_angle[0] <self.neck_setangle[1][0]
            l_hip = self.hip_setangle[0][0]< self.hip_angle[0] <self.hip_setangle[1][0]
            l_knee = self.knee_setangle[0][0]< self.knee_angle[0] <self.knee_setangle[1][0]
    
            r_elbow = self.elbow_setangle[0][1]< self.elbow_angle[1] <self.elbow_setangle[1][1]
            r_shoulder = self.shoulder_setangle[0][1]< self.shoulder_angle[1] <self.shoulder_setangle[1][1]
            r_neck = self.neck_setangle[0][1]< self.neck_angle[1] <self.neck_setangle[1][1]
            r_hip = self.hip_setangle[0][1]< self.hip_angle[1] <self.hip_setangle[1][1]
            r_knee = self.knee_setangle[0][1]< self.knee_angle[1] <self.knee_setangle[1][1]
            self.anglist.append(["l_elbow",l_elbow], ["l_shoulder",l_shoulder], ["l_neck",l_neck],["l_hip",l_hip], ["l_knee",l_knee],\
                                ["r_elbow",r_elbow], ["r_shoulder",r_shoulder], ["r_neck",r_neck], ["r_hip",r_hip], ["r_knee",r_knee])
            
            for sf in self.anglist:
                if not  sf[1]: 
                    self.faillist.append(sf)

            if len(self.faillist) > 0:
                self._cur_state = "GET_F"

        if self._cur_state == "GET_F":
            pass
            #요기서 데이터 전달하는 코드 작성하면 될듯
            # 문제가 나는 부분에 해당하는 이름만 지금 전달하는중임, 값은 추가 코드 작성필요.

            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"
        elif self._cur_state == "GET_F":
            self._cur_state = "Wait"
            
    
    def pose_determine(self):

        self.elbow_setangle = [ #min, max
            {1 :  [[176.20373732456994,177.11076305799543],[9.936236418993877,13.50451136031985]]}
        ]
        self.shoulder_setangle = [ #min, max
            {1 :  [[176.20373732456994,177.11076305799543],[9.936236418993877,13.50451136031985]]}
        ]
        self.neck_setangle = [ #min, max
            {1 :  [[176.20373732456994,177.11076305799543],[9.936236418993877,13.50451136031985]]}
        ]
        self.hip_setangle = [ #min, max
            {1 :  [[176.20373732456994,177.11076305799543],[9.936236418993877,13.50451136031985]]}
        ]
        self.knee_setangle = [ #min, max
            {1 :  [[176.20373732456994,177.11076305799543],[9.936236418993877,13.50451136031985]]}
        ]
        
        # self.default_angle.append(armleg_angle)

  
    # def contrast_angle(self, input_data, default_data,threshold):

    #     individual_avgs = [[sum(item) / len(item) for item in sublist] for sublist in [input_data, default_data]]
    #     for i in range(len(individual_avgs)):

    #         lower_limit = individual_avgs[1][i] - threshold
    #         upper_limit = individual_avgs[1][i] + threshold
            
    #         if lower_limit < 0:
    #             lower_limit = 0

    #         if not (lower_limit <= individual_avgs[0][i] <= upper_limit):
    #             return False

    #     return True

        