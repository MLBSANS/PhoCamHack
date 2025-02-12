#!/bin/bash

# Cập nhật hệ thống và cài đặt python3-venv nếu chưa có
sudo apt update && sudo apt install -y python3-venv

# Kiểm tra nếu môi trường ảo đã tồn tại, nếu chưa thì tạo
if [ ! -d "myenv" ]; then
    python3 -m venv myenv
fi
clear || cls
# Hướng dẫn chạy script đúng cách
echo "Vui lòng chạy script bằng lệnh: source script.sh hoặc . script.sh"

# Kích hoạt môi trường ảo (chỉ hoạt động nếu chạy bằng source)
source myenv/bin/activate