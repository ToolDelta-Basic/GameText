import os, sys, re, json, shutil

lang_file_path = "./zh_CN.lang"
lang_file_mode = "r"
w_lang_file_path = "./zh_CN_Cp.lang"
w_lang_file_path_mode = "w"

with open(lang_file_path, lang_file_mode) as lang_data_io:
    lines = lang_data_io.readlines()
    # data = lang_data_io.read()

def check_digit(string):
    for char in string:
        if char.isdigit():
            return True
    return False

def process_line(line):
    processed_line = line.replace('"', "'")
    processed_line = f'"{processed_line}'.replace('=', '":').replace("\n", "")
    return processed_line + '",\n'

def process_file(file_path, name):
    new_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            processed_line = process_line(line)
            new_lines.append(processed_line)
    if check_digit(name):data = f'Error: dict'
    else:data = f'{name}: dict = {{\n    {"    ".join(new_lines)}\n}}'
    with open(file_path, 'w') as file:
        file.write(data)

def process_files_in_directory(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, root.split("src/")[1])

tmp_1 = [line for line in lines if not line.startswith(' ')] # 删除前面带有两个空格的行
tmp_2 = [line for line in lines if not line.startswith('##')] # 删除前面带有##的行
tmp_3 = [line.replace('#', '') for line in tmp_2] # 删除
tmp_4 = [line for line in tmp_3 if not line.startswith('\n')]  # 删除开头是空行的行
tmp_5 = [re.sub(r':.*', ':', line).replace('1:', '') for line in tmp_4]
tmp_6 = [re.sub(r'\s+$', '', line)+"\n" for line in tmp_5]
if os.path.exists('src'):shutil.rmtree('src')
_ = [(
        (folder_name := os.path.join("src", line[:line.find('.')])),
        (file_name := line[:line.find('.')] + ".py"),
        os.makedirs(folder_name, exist_ok=True) if not os.path.exists(folder_name) else None,
        open(os.path.join(folder_name, file_name), 'a').write(line)
    ) for line in tmp_6 if '.' in line]
process_files_in_directory('src')



# with open(w_lang_file_path, w_lang_file_path_mode) as w_lang_data_io:
#     w_lang_data_io.writelines(tmp_6)

# import re
# data = "已为 %3$s 添加 %1$d 到 [%2$s] （现在为 %4$d）"
# data = re.sub(r'\$[^"\'\]\)）}\s]*', '', data)
# mylist = [10, "somevalue", 20, "currentvalue"]

# for i, value in enumerate(mylist, start=1):
#     data = data.replace("%{}".format(i), "{" + str(i-1) + "}")

# result = data.format(*mylist)
# print(result)
