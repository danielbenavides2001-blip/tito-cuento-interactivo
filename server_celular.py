import os
import sys
import socket
import webbrowser
import http.server
import socketserver
import qrcode
from PIL import Image

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ip = get_local_ip()
    port = 8000
    url = f"http://{ip}:{port}/index.html"
    
    # 1. Generate QR code
    qr = qrcode.QRCode(box_size=10, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#1B4A38", back_color="#FFFFFF")
    qr_path = os.path.join(base_dir, "qr_celular.png")
    qr_img.save(qr_path)
    
    # 2. Generate friendly guide HTML
    guide_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Ver Tito en Celular</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;800;900&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Nunito', sans-serif;
      background: #FAF7F0;
      color: #26372B;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      padding: 20px;
    }}
    .card {{
      background: #FFFFFF;
      border-radius: 24px;
      padding: 36px 40px;
      box-shadow: 0 16px 45px rgba(27, 74, 56, 0.1);
      max-width: 520px;
      text-align: center;
      border: 1px solid rgba(215, 200, 170, 0.5);
    }}
    .badge {{
      background: #E8F3EE;
      color: #1B4A38;
      font-weight: 800;
      padding: 6px 14px;
      border-radius: 20px;
      display: inline-block;
      margin-bottom: 14px;
      font-size: 0.85rem;
    }}
    h1 {{
      font-size: 1.6rem;
      font-weight: 900;
      color: #1B4A38;
      margin: 0 0 10px 0;
    }}
    p.desc {{
      color: #556B5D;
      font-size: 1rem;
      margin-bottom: 24px;
      line-height: 1.4;
    }}
    .qr-frame {{
      background: #FAF7F0;
      border: 2px dashed #B4731E;
      border-radius: 18px;
      padding: 16px;
      display: inline-block;
      margin-bottom: 20px;
    }}
    .qr-frame img {{
      display: block;
      width: 260px;
      height: 260px;
      border-radius: 8px;
    }}
    .url-box {{
      background: #F4EFE6;
      border-radius: 12px;
      padding: 12px;
      font-family: monospace;
      font-size: 1.15rem;
      font-weight: bold;
      color: #B4731E;
      margin-bottom: 24px;
      word-break: break-all;
    }}
    .steps {{
      text-align: left;
      background: #F9Fbf9;
      border-radius: 16px;
      padding: 18px 22px;
      border: 1px solid #E0ECE5;
      font-size: 0.95rem;
      color: #334D3E;
    }}
    .steps ol {{
      margin: 0;
      padding-left: 20px;
    }}
    .steps li {{
      margin-bottom: 8px;
    }}
    .steps li:last-child {{
      margin-bottom: 0;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">📱 Conexión Wi-Fi Instantánea</div>
    <h1>Abre el Cuento en tu Celular</h1>
    <p class="desc">Apunta la cámara de tu teléfono al código QR para empezar a leer con música y efectos interactivos.</p>
    
    <div class="qr-frame">
      <img src="qr_celular.png" alt="Código QR para abrir en celular">
    </div>

    <div class="url-box">
      {url}
    </div>

    <div class="steps">
      <ol>
        <li>Asegúrate de que tu celular esté conectado al <b>mismo Wi-Fi</b> que este computador.</li>
        <li>Abre la <b>cámara de tu celular</b> (o escáner QR).</li>
        <li>Apunta al código QR y toca el enlace que aparece en pantalla.</li>
        <li>¡Gira tu celular de forma <b>horizontal</b> para la mejor experiencia de lectura!</li>
      </ol>
    </div>
  </div>
</body>
</html>
"""
    guide_path = os.path.join(base_dir, "abrir_en_celular.html")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide_html)
    
    # 3. Open guide in browser
    webbrowser.open(f"file:///{guide_path.replace(os.sep, '/')}")
    
    print("\n" + "="*60)
    print("🐻 SERVIDOR ACTIVO PARA CELULAR (Tito Interactivo)")
    print("="*60)
    print(f"Direccion en celular:  {url}")
    print(f"Guia con Codigo QR:   {guide_path}")
    print("="*60)
    print("Mantén esta ventanita abierta mientras usas el celular.")
    print("Para salir o apagar el servidor, presiona: Ctrl + C")
    print("="*60 + "\n")
    
    os.chdir(base_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido. ¡Hasta pronto!")

if __name__ == "__main__":
    main()
