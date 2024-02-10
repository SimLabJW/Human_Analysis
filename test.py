import os
import re

# 폴더 경로 지정
folder_path = "./Pose_zip/"

# 폴더 내 모든 파일 리스트 가져오기
files = os.listdir(folder_path)

# 파일 이름에서 숫자 부분을 추출하는 함수
def extract_number(file_name):
    match = re.search(r'\d+', file_name)
    return int(match.group()) if match else None

# 파일들을 그룹화할 딕셔너리 생성
grouped_files = {}

# 파일들을 그룹화
for file_name in files:
    base_name = re.sub(r'\d+', '', file_name)  # 파일 이름에서 숫자 부분 제거
    key = base_name.lower()  # 대소문자 구분 없이 그룹화하기 위해 소문자로 변환
    number = extract_number(file_name)  # 파일 이름에서 숫자 추출

    if key not in grouped_files:
        grouped_files[key] = []

    grouped_files[key].append((file_name, number))

# 그룹화된 파일들을 출력
for key, group in grouped_files.items():
    print(f"그룹: {key}")
    for file_name, number in sorted(group, key=lambda x: x[1]):
        print(f"  {file_name}")
