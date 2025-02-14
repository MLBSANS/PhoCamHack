#!/bin/bash

# Cập nhật và cài đặt Python
sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-venv python3-pip

# Xóa môi trường ảo cũ nếu nó bị lỗi hoặc mất file quan trọng
if [ -d "myenv" ]; then
    if [ ! -f "myenv/bin/activate" ]; then
        echo "Môi trường ảo bị lỗi, đang xóa và tạo lại..."
        rm -rf myenv
    fi
fi

# Tạo lại môi trường ảo nếu nó không tồn tại
if [ ! -d "myenv" ]; then
    python3 -m venv myenv
    echo "Môi trường ảo đã được tạo!"
fi

# Kích hoạt môi trường ảo
source myenv/bin/activate

# Kiểm tra lại xem đã vào môi trường ảo chưa
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "Môi trường ảo đã được kích hoạt!"
else
    echo "Lỗi: Không thể kích hoạt môi trường ảo!"
    exit 1
fi

# Chạy install.py nếu có
if [ -f "install.py" ]; then
    python3 install.py
else
    echo "Không tìm thấy install.py!"
fi