import os
import shutil
import re

def update_makefile_variables(makefile_path, tel_path, project_name):
    with open(makefile_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换TEL_PATH
    tel_path_pattern = re.compile(r'^(TEL_PATH\s*:=\s*)(.*)$', re.MULTILINE)
    content = tel_path_pattern.sub(r'\1{}'.format(tel_path), content)
    
    # 替换PROJECT_NAME
    proj_name_pattern = re.compile(r'^(PROJECT_NAME\s*:=\s*)(.*)$', re.MULTILINE)
    content = proj_name_pattern.sub(r'\1{}'.format(project_name), content)

    with open(makefile_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    initial_dir = os.getcwd()  # 获取当前工作目录作为初始目录
    tools_dir = os.path.join(initial_dir, 'tools')
    source_makefile = os.path.join(tools_dir, 'Makefile')

    # 检查工具目录下的Makefile是否存在
    if not os.path.isfile(source_makefile):
        raise FileNotFoundError(f"Makefile not found in tools directory: {source_makefile}")

    # 遍历所有目录寻找main.c
    for root, dirs, files in os.walk(initial_dir):
        if 'main.c' in files:
            main_c_dir = root  # main.c所在目录
            
            # 计算相对路径（到初始目录）并标准化为UNIX路径格式
            tel_path = os.path.relpath(initial_dir, main_c_dir).replace('\\', '/')
            
            # 获取项目名称（main.c所在目录的父目录名）
            project_name = os.path.basename(main_c_dir)
            
            # 拷贝Makefile
            dest_makefile = os.path.join(main_c_dir, 'Makefile')
            shutil.copyfile(source_makefile, dest_makefile)
            
            # 更新Makefile变量
            update_makefile_variables(dest_makefile, tel_path, project_name)
            print(f"Processed: {main_c_dir}, tel_path : {tel_path} , project_name : {project_name}")

if __name__ == "__main__":
    main()