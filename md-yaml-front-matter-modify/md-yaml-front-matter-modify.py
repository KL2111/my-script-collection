#!/usr/bin/env python3

import os
import re

# 1. 要求用户输入路径
path = input("请输入文件夹路径：")

# 初始化计数器
total_files = 0
updated_files = 0

# 默认的frontmatter
default_keys = {
	"draft": "true",
	"description": "",
	"slug": "",
	"author": "me",
	"categories": "",
	"tags": "",
	"showtoc": "false",
	"showInHomeList": "false",
	"datetimeUpdate": ""
}

print("\n当前的默认frontmatter为：")
for key, value in default_keys.items():
	print(f"{key}: {value}")
	
# 修改默认的frontmatter
modify_default = input("\n是否要修改默认的frontmatter? (y/n): ").lower()
if modify_default == "y":
	new_frontmatter = input("请输入新的frontmatter，格式为 key1: value1, key2: value2,... : ")
	for item in new_frontmatter.split(','):
		key, value = item.split(':')
		default_keys[key.strip()] = value.strip()
		
	delete_key = input("\n是否要删除某个frontmatter键? (y/n): ").lower()
	if delete_key == "y":
		del_key = input("请输入要删除的键：")
		if del_key in default_keys:
			del default_keys[del_key]
			print(f"已删除键 {del_key}")
			
# 批量修改已存在的frontmatter
modify_existing = input("\n是否要批量修改已存在的frontmatter? (y/n): ").lower()
modifications = {}
if modify_existing == "y":
	number_of_changes = int(input("您想修改几个键值对? "))
	for i in range(number_of_changes):
		original = input(f"请输入第{i+1}个要修改的原键值对，格式为 key: value: ")
		new = input(f"请输入第{i+1}个键值对的新值，格式为 key: value: ")
		modifications[original] = new
		
# 删除特定键或键值对
delete_existing = input("\n是否要删除特定的frontmatter键或特定的键值对? (y/n): ").lower()
deletions = []
if delete_existing == "y":
	number_of_deletions = int(input("您想删除几个键或键值对? "))
	for i in range(number_of_deletions):
		item_to_delete = input(f"请输入第{i+1}个要删除的键或键值对：")
		deletions.append(item_to_delete)
		
# 检查并删除YAML中的空行
remove_empty_lines = input("\n是否要检查并删除YAML中的空行? (y/n): ").lower

def process_content(content):
	# Extract YAML front matter
	match = re.search(r'---\s*([\s\S]*?)\s*---', content)
	if not match:
		return content
	
	yaml_content = match.group(1)
	new_yaml_content = []
	
	# Handle deletions
	for line in yaml_content.splitlines():
		for deletion in deletions:
			if ":" in deletion:
				key, value = deletion.split(":")
				key, value = key.strip(), value.strip()
				if f"{key}: {value}" == line.strip():
					break
			else:
				if deletion.strip() == line.split(":")[0].strip():
					break
		else:
			new_yaml_content.append(line)
			
	yaml_content = "\n".join(new_yaml_content)
	
	# Handle modifications
	for original, new in modifications.items():
		yaml_content = yaml_content.replace(original, new)
		
	# Remove empty lines if needed
	if remove_empty_lines == "y":
		yaml_content = "\n".join([line for line in yaml_content.splitlines() if line.strip()])
		
	updated_content = content.replace(match.group(0), f"---\n{yaml_content}\n---")
	return updated_content

# 文件遍历和处理逻辑保持不变
for subdir, _, files in os.walk(path):
	for file in files:
		if file.endswith(".md"):
			total_files += 1
			filepath = os.path.join(subdir, file)
			
			with open(filepath, 'r', encoding="utf-8") as f:
				content = f.read()
				
			new_content = process_content(content)
			
			# 如果内容有所更改，则保存文件
			if new_content != content:
				updated_files += 1
				with open(filepath, 'w', encoding="utf-8") as f:
					f.write(new_content)
					
print(f"遍历了{total_files}个文档，更改了{updated_files}个文档。")
