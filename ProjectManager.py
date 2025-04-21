import sys
import subprocess
import threading
import re
import time
import socket
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
import os


class OutputSignals(QObject):
    frontend_output_signal = pyqtSignal(str)
    backend_output_signal = pyqtSignal(str)


ANSI_COLORS = {
    "30": "black",
    "31": "red",
    "32": "green",
    "33": "yellow",
    "34": "blue",
    "35": "magenta",
    "36": "cyan",
    "37": "white",
    "90": "brightblack",
    "91": "brightred",
    "92": "brightgreen",
    "93": "brightyellow",
    "94": "brightblue",
    "95": "brightmagenta",
    "96": "brightcyan",
    "97": "brightwhite",
    "40": "bg-black",
    "41": "bg-red",
    "42": "bg-green",
    "43": "bg-yellow",
    "44": "bg-blue",
    "45": "bg-magenta",
    "46": "bg-cyan",
    "47": "bg-white",
    "100": "bg-brightblack",
    "101": "bg-brightred",
    "102": "bg-brightgreen",
    "103": "bg-brightyellow",
    "104": "bg-brightblue",
    "105": "bg-brightmagenta",
    "106": "bg-brightcyan",
    "107": "bg-brightwhite",
}


def ansi_to_html(text):
    ansi_pattern = re.compile(r"\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]")
    result = ""
    style = ""
    pos = 0
    for match in ansi_pattern.finditer(text):
        start, end = match.span()
        result += f'<span style="{style}">{text[pos:start]}</span>'
        pos = end
        codes = match.group(1).split(";") if match.group(1) else []
        for code in codes:
            if code == "0":
                style = ""
            elif code == "1":
                style += "font-weight:bold;"
            elif code in ANSI_COLORS:
                if code.startswith("4") or code.startswith("10"):
                    style += f"background-color:{ANSI_COLORS[code].replace('bg-', '')};"
                else:
                    style += f"color:{ANSI_COLORS[code]};"
    result += f'<span style="{style}">{text[pos:]}</span>'
    return result


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


class ProjectManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.frontend_process = None
        self.backend_process = None
        self.frontend_thread = None
        self.backend_thread = None
        self.signals = OutputSignals()
        self.signals.frontend_output_signal.connect(self.append_frontend_output)
        self.signals.backend_output_signal.connect(self.append_backend_output)

    def initUI(self):
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        start_button = QPushButton("Start")
        start_button.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """
        )
        start_button.clicked.connect(self.start_projects)

        stop_button = QPushButton("Stop")
        stop_button.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """
        )
        stop_button.clicked.connect(self.stop_projects)

        restart_button = QPushButton("Restart")
        restart_button.setStyleSheet(
            """
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
        """
        )
        restart_button.clicked.connect(self.restart_projects)

        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(restart_button)

        # 输出布局
        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)
        self.frontend_output = QTextEdit()
        self.frontend_output.setReadOnly(True)
        self.frontend_output.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
            }
        """
        )

        self.backend_output = QTextEdit()
        self.backend_output.setReadOnly(True)
        self.backend_output.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
            }
        """
        )

        # 设置前端和后端输出的宽度比例为2:3
        output_layout.addWidget(self.frontend_output, 2)
        output_layout.addWidget(self.backend_output, 3)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Project Manager")
        self.setGeometry(300, 300, 1000, 600)
        self.show()

    def start_projects(self):
        if self.frontend_process is None:
            self.frontend_thread = threading.Thread(target=self.start_frontend)
            self.frontend_thread.start()
        if self.backend_process is None:
            self.backend_thread = threading.Thread(target=self.start_backend)
            self.backend_thread.start()

    def start_frontend(self):
        try:
            current_dir = os.getcwd()
            frontend_dir = os.path.join(current_dir, "Frontend")
            npm_path = os.path.join(os.environ.get("APPDATA"), "npm", "npm.cmd")
            port = 5173

            command = [npm_path, "run", "dev", "--", f"--port={port}"]
            self.frontend_process = subprocess.Popen(
                command,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
            )
            while True:
                output = self.frontend_process.stdout.readline()
                if output == "" and self.frontend_process.poll() is not None:
                    break
                if output:
                    output = ansi_to_html(output)
                    self.signals.frontend_output_signal.emit(output.strip())
        except Exception as e:
            self.signals.frontend_output_signal.emit(f"Error starting frontend: {e}")

    def start_backend(self):
        try:
            current_dir = os.getcwd()
            backend_dir = os.path.join(current_dir, "Backend")
            python_path = sys.executable
            self.backend_process = subprocess.Popen(
                [python_path, "app.py"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
            )
            while True:
                output = self.backend_process.stdout.readline()
                if output == "" and self.backend_process.poll() is not None:
                    break
                if output:
                    output = ansi_to_html(output)
                    self.signals.backend_output_signal.emit(output.strip())
        except Exception as e:
            self.signals.backend_output_signal.emit(f"Error starting backend: {e}")

    def stop_projects(self):
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                # 等待一段时间让进程有机会正常终止
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # 如果超时，强制杀死进程
                self.frontend_process.kill()
            self.frontend_process = None

        if self.backend_process:
            try:
                self.backend_process.terminate()
                # 等待一段时间让进程有机会正常终止
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # 如果超时，强制杀死进程
                self.backend_process.kill()
            self.backend_process = None

    def restart_projects(self):
        self.stop_projects()
        # 清空输出框
        self.frontend_output.clear()
        self.backend_output.clear()
        # 延迟 1 秒
        time.sleep(1)
        self.start_projects()

    def append_frontend_output(self, text):
        # 过滤掉端口被占用的提示信息
        if "is in use, trying another one..." not in text:
            self.frontend_output.append(text)

    def append_backend_output(self, text):
        try:
            pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[([^\]]+)\] "(\w+) (\S+) HTTP/[\d.]+ (\d+) -$'
            match = re.match(pattern, text)
            if match:
                _, datetime_str, method, path, status_code = match.groups()
                date_time = f"[{datetime_str.split(' ')[0].split('/')[0]}/{datetime_str.split(' ')[0].split('/')[1]} {datetime_str.split(' ')[1].split(':')[0]}:{datetime_str.split(' ')[1].split(':')[1]}:{datetime_str.split(' ')[1].split(':')[2]}]"
                method_color = {
                    "GET": "blue",
                    "POST": "green",
                    "PUT": "orange",
                    "DELETE": "red",
                }.get(method, "black")
                formatted_method = f'<span style="color:{method_color}; font-weight: bold;">{method}</span>'
                formatted_status_code = (
                    f'<span style="text-decoration: underline;">{status_code}</span>'
                )
                formatted_text = (
                    f"{date_time} {formatted_method} {path} {formatted_status_code}"
                )
                self.backend_output.append(formatted_text)
            else:
                self.backend_output.append(text)
        except Exception as e:
            print(f"Error parsing backend output: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = ProjectManager()
    sys.exit(app.exec())
