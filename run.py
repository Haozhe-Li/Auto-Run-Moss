import os
import subprocess
import webbrowser
import re

# 定义文件扩展名和对应的Moss语言参数
file_types = {
    '.py': 'python',
    '.c': 'c',
    '.java': 'java',
    '.cpp': 'cc',
}

# 获取当前目录下的所有文件
files = [f for f in os.listdir('.') if os.path.isfile(f)]

# 过滤出支持的文件类型
supported_files = {}
for f in files:
    ext = os.path.splitext(f)[1]
    if ext in file_types:
        lang = file_types[ext]
        supported_files.setdefault(lang, []).append(f)

# 执行Moss提交并打开结果
for lang, lang_files in supported_files.items():
    if len(lang_files) >= 2:
        # 构建Perl脚本命令
        command = f"perl moss.pl -l {lang} {' '.join(lang_files)}"
        print(f"Running Moss for {lang} files...")
        print(f"Command: {command}")

        # 运行Perl脚本
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 处理输出
        if result.stdout:
            print(result.stdout)
            # 使用正则表达式查找URL
            urls = re.findall(r'http[s]?://moss\.stanford\.edu/results/\d+/\d+', result.stdout)
            if urls:
                print("Opening the results in the web browser...")
                webbrowser.open(urls[0])
            else:
                print("No URL found in Moss output.")
        # 如果有错误，打印错误信息
        if result.stderr:
            print("Error:", result.stderr)
        break
else:
    print("Error: There must be at least two files of the same supported type in the directory.")
