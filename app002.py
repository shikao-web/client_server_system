import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import csv

DOCUMENT_ROOT_DIR = "./www"
CSV_FILE_PATH = "./data.csv"

class StaticFileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # URL → ファイルパス変換
        path = self.path.strip("/")
        if path == "":
            path = "index.html"

        file_path = os.path.join(DOCUMENT_ROOT_DIR, path)

        # セキュリティ対策（ディレクトリトラバーサル防止）
        file_path = os.path.abspath(file_path)
        if not file_path.startswith(os.path.abspath(DOCUMENT_ROOT_DIR)):
            self.send_error(403)
            return

        # ファイル存在チェック
        if not os.path.exists(file_path):
            self.send_error(404)
            return

        # MIMEタイプ判定（簡易）
        if file_path.endswith(".html"):
            content_type = "text/html"
        elif file_path.endswith(".css"):
            content_type = "text/css"
        elif file_path.endswith(".js"):
            content_type = "application/javascript"
        else:
            content_type = "application/octet-stream"

        # レスポンス送信
        with open(file_path, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content)
    
    # --- 以下を追記 ---
    def do_POST(self):
        if self.path == "/api":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            # JSONとして受信
            data = json.loads(body)
            print("受信JSON:", data)

            # 受信したデータをCSVに書き込み
            # CSV書き込み

            with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())

                # ファイルが存在しない or 空ならヘッダーを書く
                if (not os.path.isfile(CSV_FILE_PATH)) or os.path.getsize(CSV_FILE_PATH) == 0:
                    writer.writeheader()
                writer.writerow(data)

                print(data, "をCSVに書き込みました。\n")
        else: 
            self.send_response(405)
        
    # --- 以上を追記 ---

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), StaticFileHandler)
    print("Serving at http://localhost:8000")
    server.serve_forever()