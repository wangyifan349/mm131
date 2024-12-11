import os
import hashlib
import shutil

# 配置
source_dirs = ['C:\\']  # 要扫描的目录
destination_dir = 'D:\\Images'  # 目标目录
excluded_folder_names = ['LSR', 'Temp', 'Backup']  # 排除的文件夹名称列表
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # 支持的图片格式

# 计算文件的哈希值
def calculate_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 检查目录是否被排除
def is_excluded(dir_path):
    # 检查路径中是否包含任何排除的文件夹名称
    return any(folder in dir_path.split(os.sep) for folder in excluded_folder_names)

# 移动文件并处理重命名
def move_file(file_path, destination, hash_dict):
    file_hash = calculate_hash(file_path)

    # 检查是否存在重复文件
    if file_hash in hash_dict:
        print(f"重复文件: {file_path} 已存在于 {hash_dict[file_hash]}")
        return  # 跳过重复文件

    base_name = os.path.basename(file_path)
    new_file_name = base_name
    new_file_path = os.path.join(destination, new_file_name)

    # 处理重命名
    counter = 1
    while os.path.exists(new_file_path):
        name, ext = os.path.splitext(base_name)
        new_file_name = f"{name}_{counter}{ext}"
        new_file_path = os.path.join(destination, new_file_name)
        counter += 1

    # 移动文件
    shutil.move(file_path, new_file_path)
    hash_dict[file_hash] = new_file_path
    print(f"移动文件: {file_path} 到 {new_file_path}")

# 主函数
def main():
    hash_dict = {}
    
    for source_dir in source_dirs:
        for root, dirs, files in os.walk(source_dir):
            # 检查当前目录是否被排除
            if is_excluded(root):
                # 如果当前目录被排除，跳过该目录及其子目录
                dirs[:] = []  # 清空 dirs 列表，避免进入被排除的目录
                continue
            
            # 处理文件
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    file_path = os.path.join(root, file)
                    move_file(file_path, destination_dir, hash_dict)

if __name__ == "__main__":
    main()
