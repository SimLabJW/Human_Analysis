def calculate_individual_avgs(data):
    individual_avgs = [[sum(item) / len(item) for item in sublist] for sublist in data]
    return individual_avgs

# 주어진 데이터
list1 = [[196.26094276589902, 161.09588014458723], [100.11451895970575, 15.79033470800142], [181.1045284571304, 183.3543642897043]]
list2 = [[176.20373732456994, 177.11076305799543], [9.936236418993877, 13.50451136031985], [177.8235356530215, 177.92432727487738]]
# 추가 리스트를 필요한 만큼 추가할 수 있습니다.

# 각 리스트의 개별 항목에 대한 평균값 계산 및 출력
individual_avgs = calculate_individual_avgs([list1, list2])

def result_acces(individual_avgs, threshold):
    for i in range(len(individual_avgs)):

        lower_limit = individual_avgs[1][i] - threshold
        upper_limit = individual_avgs[1][i] + threshold
        
        if lower_limit < 0:
            # 처리를 위해 음수를 +360하여 범위를 맞춰줍니다.
            lower_limit = 0

        if not (lower_limit <= individual_avgs[0][i] <= upper_limit):
            print(f"{lower_limit} {individual_avgs[0][i]} {upper_limit}")
            return False

    return True

result = result_acces(individual_avgs,15)
print(result)