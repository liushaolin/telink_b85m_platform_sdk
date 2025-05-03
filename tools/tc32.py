import os
import platform
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

# 配置信息
TOOL_URLS = {
    "Windows": "http://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32-win.rar",
    "Linux": "https://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32_gcc_v2.0.tar.bz2",
    "Darwin": "http://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32-mac.zip"
}

TOOLS = {
    "unrar": Path(__file__).parent / "unrar.exe",
    "wget": Path(__file__).parent / "wget.exe"
}

TOOLS_PATH = {
    "Windows":  Path(__file__).parent / "TC32/tc32_win.rar",
    "Linux": Path(__file__).parent / "TC32/tc32_gcc_v2.0.tar.bz2",
    "Darwin": Path(__file__).parent / "TC32/tc32-mac.zip"
}

def check_tools():
    """检查必需工具是否存在"""
    missing = []
    for name, path in TOOLS.items():
        if not path.exists():
            missing.append(str(path))
    
    if missing:
        raise FileNotFoundError(
            f"必需工具缺失，请将以下文件放入脚本同级目录:\n" + "\n".join(missing)
        )

def get_os_name():
    system = platform.system()
    return "Mac" if system == "Darwin" else system

def download_with_wget(url):
    """使用wget下载文件"""
    cmd = [
        str(TOOLS["wget"]),
        "--no-check-certificate",
        "--show-progress",
        "-O", Path(url).name,
        url
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"下载失败: {e.stderr}")
        sys.exit(1)

def extract_rar(file_path):
    """使用unrar.exe解压"""
    cmd = [
        str(TOOLS["unrar"]),
        "x", "-o+", "-inul",  # -o+ 覆盖已存在文件
        str(file_path)
    ]
    subprocess.run(cmd, check=True)

def main():
    check_tools()
    os_name = get_os_name()
    print(f"当前系统: {os_name}")
    
    file_path = TOOLS_PATH.get(os_name)
    if not file_path:
        print(f"不支持的系统: {os_name}")
        return
    
    file_name = Path(file_path).name

    print(f"file_path: {file_path}, file_name: {file_name}")
    # 下载文件
    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        sys.exit(1)
   
    # 解压文件
    print(f"开始解压: {file_name}")
    try:
        if os_name == "Windows":
            extract_rar(file_path)
        elif os_name == "Linux":
            with tarfile.open(file_path, 'r:bz2') as tar:
                tar.extractall()
        elif os_name == "Mac":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall()
        print("解压完成")
    except Exception as e:
        print(f"解压失败: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()