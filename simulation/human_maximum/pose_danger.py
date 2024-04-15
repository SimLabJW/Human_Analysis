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

        # self.pose_determine()
        # 입력 값에 대한 정보 수정    
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            # 동작 기준 정보 불러오기
            self.landmarks_frame = msg.retrieve()[0]

           
            self._cur_state = "Generate"

      
    def output(self): 

        if self._cur_state == "Generate":
            pass
            # self.anglist = self.check_angle()
            
        #     for sf in self.anglist:
        #         if not  sf[1]: 
        #             self.faillist.append([sf[1],sf[2]])

        #     if len(self.faillist) > 0:
        #         self._cur_state = "GET_F"

        # if self._cur_state == "GET_F":
        #     print(self.faillist)
        
            #요기서 데이터 전달하는 코드 작성하면 될듯
            # 문제가 나는 부분에 해당하는 이름만 지금 전달하는중임, 값은 추가 코드 작성필요.

            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"
        elif self._cur_state == "GET_F":
            self._cur_state = "Wait"
            
    
    # def pose_determine(self):

    #     self.elbow_setangle = [30,180]
    #     self.shoulder_setangle = [30,150]
    #     self.neck_setangle = [85,90]
    #     self.hip_setangle = [120,180]
    #     self.knee_setangle = [30,180]

  
    # def check_angle(self):
    #     anglist_all = []

    #     l_elbow = self.elbow_setangle[0]< self.elbow_angle[0][0] <self.elbow_setangle[1]
    #     l_shoulder = self.shoulder_setangle[0]< self.shoulder_angle[0][0] <self.shoulder_setangle[1]
    #     l_neck = self.neck_setangle[0]< self.neck_angle[0][0] <self.neck_setangle[1]
    #     l_hip = self.hip_setangle[0]< self.hip_angle[0][0] <self.hip_setangle[1]
    #     l_knee = self.knee_setangle[0]< self.knee_angle[0][0] <self.knee_setangle[1]

    #     r_elbow = self.elbow_setangle[0]< self.elbow_angle[1][1][0] <self.elbow_setangle[1]
    #     r_shoulder = self.shoulder_setangle[0]< self.shoulder_angle[1][1][0] <self.shoulder_setangle[1]
    #     r_neck = self.neck_setangle[0]< self.neck_angle[1][1][0] <self.neck_setangle[1]
    #     r_hip = self.hip_setangle[0]< self.hip_angle[1][1][0] <self.hip_setangle[1]
    #     r_knee = self.knee_setangle[0]< self.knee_angle[1][1][0] <self.knee_setangle[1]
    #     anglist_all.append(["l_elbow",l_elbow,self.elbow_angle[0][0][1]], \
    #                        ["l_shoulder",l_shoulder,self.shoulder_angle[0][0][1]], \
    #                         ["l_neck",l_neck,self.neck_angle[0][0][1]],\
    #                             ["l_hip",l_hip,self.hip_angle[0][0][1]], \
    #                                 ["l_knee",l_knee,self.knee_angle[0][0][1]],\
    #                                     ["r_elbow",r_elbow,self.elbow_angle[1][1][1]], \
    #                                         ["r_shoulder",r_shoulder,self.shoulder_angle[1][1][1]], \
    #                                             ["r_neck",r_neck,self.neck_angle[1][1][1]], \
    #                                                 ["r_hip",r_hip,self.hip_angle[1][1][1]], \
    #                                                     ["r_knee",r_knee,self.knee_angle[1][1][1]])
    #     return anglist_all

        