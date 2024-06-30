#!/usr/bin/python3
# encoding:utf-8

import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义下载图片的目录
directory = "美女图片"
if not os.path.exists(directory):
    try:
        os.mkdir(directory)  # 创建目录
    except OSError as e:
        print(f"错误: 无法创建目录 {directory} - {e.strerror}")
        exit(1)  # 无法创建目录时退出程序
os.chdir(directory)  # 切换到指定目录

# 设置HTTP请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Referer": "https://m.mm131.net/xinggan/"
}

# 定义基础URL和图片范围
base_url = "https://img1.hnllsy.com/pic/"
image_ranges = range(3200, 4000)  # 图片集范围
max_images_per_set = 50  # 每个集最多图片数
min_image_size = 1024  # 最小图片大小，单位为字节

filename_counter = 0  # 文件名计数器
max_workers = 10  # 最大线程数

# 定义下载图片的函数
def download_image(image_url, filename):
    try:
        response = requests.get(image_url, headers=headers, timeout=10)  # 发送HTTP请求
        if response.status_code == 200:  # 请求成功
            with open(filename, "wb") as f:
                f.write(response.content)  # 保存图片内容到文件
            
            # 检查文件大小
            if os.path.getsize(filename) <= min_image_size:
                os.remove(filename)  # 删除无效图片
                print(f"删除无效图片: {filename}")
                return False
            else:
                print(f"下载成功: {image_url}")
                return True
        else:
            print(f"下载失败: {image_url} - 状态码: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"下载错误 {image_url}: {e}")
        return False
    except Exception as e:
        print(f"意外错误: {e}")
        return False

# 使用线程池并行下载图片
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for image_set in image_ranges:
        for image_number in range(1, max_images_per_set + 1):
            image_url = f"{base_url}{image_set}/{image_number}.jpg"  # 构建图片URL
            filename_counter += 1
            filename = f"{filename_counter}.jpg"  # 生成文件名
            futures.append(executor.submit(download_image, image_url, filename))  # 提交下载任务到线程池
    
    # 等待所有任务完成
    for future in as_completed(futures):
        future.result()  # 获取任务结果，触发异常处理

