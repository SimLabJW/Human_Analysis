# import logging
# from healthcare_manager import PoseManager

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )

# logger = logging.getLogger(__name__)
from simulation_start import Simulation
from config import *
# import json
# # from data_manager import Manager
# # JSON 파일 경로
# json_file_path = RESULT_JSON

# # JSON 파일 읽어오기
# with open(json_file_path, 'r') as json_file:
#     loaded_data = json.load(json_file)

data = [{'X': 0.6467458009719849, 'Y': 0.25897085666656494, 'Z': -0.5078572034835815, 'Visibility': 0.9983187913894653}, {'X': 0.6588302254676819, 'Y': 0.23585867881774902, 'Z': -0.46722373366355896, 'Visibility': 0.9977062940597534}, {'X': 0.6652501821517944, 'Y': 0.2402719259262085, 'Z': -0.4674137830734253, 'Visibility': 0.998376727104187}, {'X': 0.6714675426483154, 'Y': 0.2453046441078186, 'Z': -0.4676159918308258, 'Visibility': 0.9976440072059631}, {'X': 0.6389656662940979, 'Y': 0.22521793842315674, 'Z': -0.49076420068740845, 'Visibility': 0.9962491393089294}, {'X': 0.6306278705596924, 'Y': 0.22268527746200562, 'Z': -0.4908744692802429, 'Visibility': 0.9966228008270264}, {'X': 0.6228376626968384, 'Y': 0.22138136625289917, 'Z': -0.4910813868045807, 'Visibility': 0.9944331049919128}, {'X': 0.6748395562171936, 'Y': 0.270757257938385, 'Z': -0.26921528577804565, 'Visibility': 0.9989432692527771}, {'X': 0.6027106046676636, 'Y': 0.2389514446258545, 'Z': -0.3674536943435669, 'Visibility': 0.9980681538581848}, {'X': 0.6517112851142883, 'Y': 0.3037009835243225, 'Z': -0.43346482515335083, 'Visibility': 0.9992939233779907}, {'X': 0.6285585761070251, 'Y': 0.2912771999835968, 'Z': -0.46170902252197266, 'Visibility': 0.9994402527809143}, {'X': 0.6703706979751587, 'Y': 0.4866078794002533, 'Z': -0.12236442416906357, 'Visibility': 0.9987512826919556}, {'X': 0.5226941108703613, 'Y': 0.405294269323349, 'Z': -0.343467652797699, 'Visibility': 0.9910879731178284}, {'X': 0.7015262842178345, 'Y': 0.7071782350540161, 'Z': -0.2441193014383316, 'Visibility': 0.867783784866333}, {'X': 0.4985540807247162, 'Y': 0.694136381149292, 'Z': -0.47982877492904663, 'Visibility': 0.9846654534339905}, {'X': 0.7394772171974182, 'Y': 0.7103092074394226, 'Z': -0.594105064868927, 'Visibility': 0.9089358448982239}, {'X': 0.6607030034065247, 'Y': 0.6812779903411865, 'Z': -0.5936304926872253, 'Visibility': 0.984772801399231}, {'X': 0.7529221773147583, 'Y': 0.7188510894775391, 'Z': -0.660697340965271, 'Visibility': 0.8550906181335449}, {'X': 0.6999939680099487, 'Y': 0.7061100006103516, 'Z': -0.6355092525482178, 'Visibility': 0.9599202871322632}, {'X': 0.7522038221359253, 'Y': 0.6881519556045532, 'Z': -0.6563453078269958, 'Visibility': 0.8642169237136841}, {'X': 0.7040337324142456, 'Y': 0.6724929809570312, 'Z': -0.616919755935669, 'Visibility': 0.9591541886329651}, {'X': 0.7449784874916077, 'Y': 0.6847888231277466, 'Z': -0.6014875173568726, 'Visibility': 0.8672589063644409}, {'X': 0.6935584545135498, 'Y': 0.6669180393218994, 'Z': -0.5831261873245239, 'Visibility': 0.94538414478302}, {'X': 0.6060405373573303, 'Y': 0.8169872760772705, 'Z': 0.06497474759817123, 'Visibility': 0.9238842129707336}, {'X': 0.5061425566673279, 'Y': 0.8105810284614563, 'Z': -0.06426882743835449, 'Visibility': 0.9045533537864685}, {'X': 0.6833434700965881, 'Y': 1.0489978790283203, 'Z': -0.11201267689466476, 'Visibility': 0.28336337208747864}, {'X': 0.5444870591163635, 'Y': 1.0643906593322754, 'Z': -0.18590570986270905, 'Visibility': 0.34894731640815735}, {'X': 0.635342001914978, 'Y': 1.2684848308563232, 'Z': 0.26421964168548584, 'Visibility': 0.026570502668619156}, {'X': 0.5249971151351929, 'Y': 1.3210363388061523, 'Z': 0.117049440741539, 'Visibility': 0.04151872545480728}, {'X': 0.6176978945732117, 'Y': 1.2992465496063232, 'Z': 0.29265010356903076, 'Visibility': 0.04705636203289032}, {'X': 0.5083653926849365, 'Y': 1.3641247749328613, 'Z': 0.1404116302728653, 'Visibility': 0.03915021941065788}, {'X': 0.6510682702064514, 'Y': 1.392106294631958, 'Z': 0.16461512446403503, 'Visibility': 0.013945765793323517}, {'X': 0.5528554916381836, 'Y': 1.429155707359314, 'Z': -0.02324754372239113, 'Visibility': 0.028660213574767113}]


class Sssssss():
    def __init__(self) -> None:
        self.result = ""
        # Result_m = Return_result_Model(0, Infinite, "Result_m", "CARE")
        Simulation(data)
        

Sssssss()