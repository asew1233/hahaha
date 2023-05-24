# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:27:52 2023

@author: ksm
"""

import random
import requests
from bs4 import BeautifulSoup
import re

# 단일 번호 출현 빈도를 가져오는 함수
def get_single_number_freq():
    url = "https://www.dhlottery.co.kr/gameResult.do?method=statByNumber"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.select('.tbl_data.tbl_data_col tbody tr')
    single_number_freq = {}
    for row in data:
        tds = row.select('td')
        num = int(tds[0].text)
        freq = int(tds[1].text.replace('%', '').strip())
        single_number_freq[num] = freq
    return single_number_freq

# 연속 번호 출현 빈도를 가져오는 함수
def get_consecutive_number_freq():
    url = "https://www.dhlottery.co.kr/gameResult.do?method=statConsNumber"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    data = soup.select('.tbl_data.tbl_data_col tbody tr')
    consecutive_number_freq = {}
    for row in data:
        tds = row.select('td')
        nums_text = tds[2].text.strip()
        nums = tuple(map(int, re.findall(r'\d+', nums_text)))
        freq_text = tds[3].text.strip().split()[0]  # '쌍'을 제외하고 숫자 부분만 추출
        freq = int(freq_text) if freq_text.isdigit() else 0
        consecutive_number_freq[nums] = freq
    return consecutive_number_freq

# 단일 번호 출현 빈도를 가져옴
single_number_freq = get_single_number_freq()

# 연속 번호 출현 빈도를 가져옴
consecutive_number_freq = get_consecutive_number_freq()

# 단일 번호와 연속 번호의 확률을 계산
total_single_number_freq = sum(single_number_freq.values())
single_number_prob = {k: v / total_single_number_freq for k, v in single_number_freq.items()}

total_consecutive_number_freq = sum(consecutive_number_freq.values())
consecutive_number_prob = {k: v / total_consecutive_number_freq for k, v in consecutive_number_freq.items()}

# 출현 빈도의 비율을 계산
single_number_ratio = total_single_number_freq / (total_single_number_freq + total_consecutive_number_freq)
consecutive_number_ratio = total_consecutive_number_freq / (total_single_number_freq + total_consecutive_number_freq)

# 로또 번호를 생성
num_samples = 10  # 생성할 로또 번호 세트의 개수
lotto_numbers = set()
while len(lotto_numbers) < num_samples:
    numbers = []
    while len(numbers) < 6:
        choice = random.random()
        if choice < single_number_ratio:  # single_number_ratio의 확률로 단일 번호 선택
            number = random.choices(list(single_number_prob.keys()), list(single_number_prob.values()))[0]
            if number not in numbers:  # 중복된 번호 제거
                numbers.append(number)
        else:  # consecutive_number_ratio의 확률로 연속 번호 선택
            consecutive = random.choices(list(consecutive_number_prob.keys()), list(consecutive_number_prob.values()))[0]
            if all(num not in numbers for num in consecutive):  # 중복된 번호 제거
                numbers.extend(consecutive)
    if len(numbers) >= 6:  # 6개 이상의 번호를 선택한 경우만 추가
        lotto_numbers.add(tuple(sorted(numbers[:6])))

# 생성된 로또 번호 출력
for i, numbers in enumerate(lotto_numbers, start=1):
    print(f"Lotto Numbers {i}: {numbers}")
