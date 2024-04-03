from pyevsim import BehaviorModelExecutor, Infinite, SysMessage

class TEST3_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")

        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
      
       

    def ext_trans(self, port, msg):
        
        if port == "start":
            self._cur_state = "Generate"

      
    def output(self): 

        if self._cur_state == "Generate":
            print("test3")
            self._cur_state = "Wait"
        else: 
            print("test3_wait")
            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"

            
    
 