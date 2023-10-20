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

# 1. 修改默认的frontmatter
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

# 2. 询问关于date和title的修改策略
print("\n修改策略如下：")
print("1. 如果date为空，可以从文件名中获取日期，格式为YYYY/MM/DD")
print("2. 如果title为空，文件名将被用作标题")
modify_date = input("\n是否要根据文件名修改date? (y/n): ").lower()
modify_title = input("是否要根据文件名修改title? (y/n): ").lower()

modify_all = False

# 遍历指定路径下的所有.md文件
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith(".md"):
            total_files += 1
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r') as f:
                content = f.read()
                match = re.search(r'---(.*?)---', content, re.DOTALL)
                if match:
                    frontmatter = match.group(1).strip()
                    updated = False
                    fm_dict = {}
                    for line in frontmatter.split("\n"):
                        key, sep, value = line.partition(":")
                        if sep:
                            fm_dict[key.strip()] = value.strip()

                    if modify_date == "y" and not fm_dict.get("date"):
                        date_match = re.search(r"(\d{4})(\d{2})(\d{2})", filename)
                        if date_match:
                            fm_dict["date"] = f"{date_match.group(1)}/{date_match.group(2)}/{date_match.group(3)}"
                            updated = True

                    if modify_title == "y" and not fm_dict.get("title"):
                        fm_dict["title"] = os.path.splitext(filename)[0]
                        updated = True

                    for key, default_value in default_keys.items():
                        if not fm_dict.get(key):
                            fm_dict[key] = default_value
                            updated = True

                    if updated and not modify_all:
                        print(f"\n文件 {filename} 需要更新。")
                        choice = input("选择操作：\n1. 执行当前文件\n2. 执行所有文件\n3. 拒绝执行当前文件\n4. 拒绝执行所有文件\n请输入选项(1/2/3/4): ")
                        if choice == "4":
                            print("操作被用户终止。")
                            exit()
                        elif choice == "3":
                            continue
                        elif choice == "2":
                            modify_all = True
                        updated_frontmatter = "\n".join(f"{key}: {value}" for key, value in fm_dict.items())
                        content = content.replace(frontmatter, updated_frontmatter)
                        with open(filepath, 'w') as f:
                            f.write(content)
                        updated_files += 1
                    elif updated and modify_all:
                        updated_frontmatter = "\n".join(f"{key}: {value}" for key, value in fm_dict.items())
                        content = content.replace(frontmatter, updated_frontmatter)
                        with open(filepath, 'w') as f:
                            f.write(content)
                        updated_files += 1

print(f"\n遍历了 {total_files} 文档。")
print(f"更改了 {updated_files} 文档。")
