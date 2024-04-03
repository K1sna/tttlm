import csv
import json
import re

def preprocess_csv(csv_file):
    data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            prompt = row['Prompts']
            responses = row['Responses']
            # 使用正则表达式将responses字符串拆分为多个部分
            response_parts = re.split(r"'probs': \[.*?\]", responses)
            probs_parts = re.findall(r"'probs': \[(.*?)\]", responses)
            # 遍历每个response部分和其对应的probs部分
            for response, probs in zip(response_parts, probs_parts):
                response = response.strip().strip("',").strip()
                probs = json.loads(f"[{probs}]") if probs else []  # 将probs字符串转换为列表
                # 将prompt、response和probs组合成一个条目，并添加到data列表中
            data.append({"prompt": prompt, "response": response, "probs": probs})
    print(len(data))
    return data

def write_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

csv_file = '/share/changzhou/prompt_construt/Demo3/data/neo/responses.csv'
jsonl_file = '/share/changzhou/prompt_construt/Demo3/data/neo/results.jsonl'
processed_data = preprocess_csv(csv_file)
write_jsonl(processed_data, jsonl_file)
