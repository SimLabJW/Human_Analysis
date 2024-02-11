import matplotlib.pyplot as plt
import numpy as np

def plot_pose(file_data):
    for entry in file_data["files"]:
        plt.figure()
        plt.title(f"Pose {entry[0]}")
        
        # Extracting data
        elbow = np.array(entry[1][1])
        shoulder = np.array(entry[2][1])
        knee = np.array(entry[3][1])

        # Plotting lines
        plt.plot([elbow[0], shoulder[0]], [elbow[1], shoulder[1]], label='Arm')
        plt.plot([shoulder[0], knee[0]], [shoulder[1], knee[1]], label='Leg')

        # Plotting joints
        plt.scatter(elbow[0], elbow[1], color='red', marker='o', label='Elbow')
        plt.scatter(shoulder[0], shoulder[1], color='blue', marker='o', label='Shoulder')
        plt.scatter(knee[0], knee[1], color='green', marker='o', label='Knee')

        plt.legend()
        plt.show()

# 데이터 샘플 사용
data = {
    "arm_leg_.png": {
        "files": [
            [1, ["elbow", [176.20373732456994, 177.11076305799543]],
             ["shoulder", [9.936236418993877, 13.50451136031985]],
             ["knee", [177.8235356530215, 177.92432727487738]]],
            [2, ["elbow", [170.8856355307854, 185.5529710330368]],
             ["shoulder", [92.83044715607141, 92.79092055099628]],
             ["knee", [175.10477374514338, 180.82315858332905]]],
            [3, ["elbow", [176.20373732456994, 177.11076305799543]],
             ["shoulder", [9.936236418993877, 13.50451136031985]],
             ["knee", [177.8235356530215, 177.92432727487738]]]
        ],
        "count": 3
    }
}

# plot_pose 함수 호출
plot_pose(data["arm_leg_.png"])
