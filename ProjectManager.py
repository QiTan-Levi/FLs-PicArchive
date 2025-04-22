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
    QTextEdit,
    QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
import os
import psutil


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


def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.terminate()
        _, still_alive = psutil.wait_procs(children, timeout=5)
        for p in still_alive:
            p.kill()
        parent.terminate()
        parent.wait(timeout=5)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
        pass


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
        self.quit_confirm = False
        self.command_history = []
        self.history_index = -1
        self.is_closed = False

    def initUI(self):
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

        # 底部输入输出布局
        bottom_layout = QVBoxLayout()
        self.manager_output = QTextEdit()
        self.manager_output.setReadOnly(True)
        self.manager_output.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 5px;
                margin-bottom: 5px;
                min-height: 50px;
            }
        """
        )
        self.manager_input = QLineEdit()
        self.manager_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 5px;
            }
        """
        )
        self.manager_input.returnPressed.connect(self.handle_input)
        self.manager_input.keyPressEvent = self.handle_key_press
        bottom_layout.addWidget(self.manager_output)
        bottom_layout.addWidget(self.manager_input)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        # 修改窗口标题
        self.setWindowTitle("**ByInfo** Fs Picture Archive Project Operation & Deployment Manager")
        self.setGeometry(300, 300, 1000, 600)
        # 去掉顶部窗口操作栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.show()
        self.manager_input.setFocus()

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
            self.frontend_process = subprocess.Popen(
                [npm_path, "run", "dev", "--", f"--port={port}"],
                cwd=frontend_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
            )
            self.read_process_output(self.frontend_process, self.signals.frontend_output_signal)
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
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
            )
            self.read_process_output(self.backend_process, self.signals.backend_output_signal)
        except Exception as e:
            self.signals.backend_output_signal.emit(f"Error starting backend: {e}")

    def read_process_output(self, process, signal):
        def reader():
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    output = ansi_to_html(output)
                    signal.emit(output.strip())
        thread = threading.Thread(target=reader)
        thread.start()

    def stop_projects(self):
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            except Exception:
                pass
            finally:
                self.frontend_process = None

        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            except Exception:
                pass
            finally:
                self.backend_process = None

        # 处理子进程
        if self.frontend_process:
            try:
                parent = psutil.Process(self.frontend_process.pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.terminate()
                _, still_alive = psutil.wait_procs(children, timeout=5)
                for p in still_alive:
                    p.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if self.backend_process:
            try:
                parent = psutil.Process(self.backend_process.pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.terminate()
                _, still_alive = psutil.wait_procs(children, timeout=5)
                for p in still_alive:
                    p.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def restart_projects(self):
        self.stop_projects()
        # 清空输出框
        self.frontend_output.clear()
        self.backend_output.clear()
        # 延迟 1 秒
        time.sleep(1)
        self.start_projects()

    def append_frontend_output(self, text):
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

    def handle_input(self):
        command = self.manager_input.text().strip().lower()
        self.manager_input.clear()
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)

        if command == "start":
            self.start_projects()
            self.manager_output.append("Starting projects...")
        elif command == "restart":
            self.restart_projects()
            self.manager_output.append("Restarting projects...")
        elif command == "stop":
            self.stop_projects()
            self.manager_output.append("Stopping projects...")
        elif command == "help":
            help_text = """
Available commands:
- start: Start the frontend and backend projects.
- restart: Restart the frontend and backend projects.
- stop: Stop the frontend and backend projects.
- help: Show this help message.
            """
            self.manager_output.append(help_text)
        else:
            self.manager_output.append(f"Unknown command: {command}")
            self.quit_confirm = False

    def handle_key_press(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                self.manager_input.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key.Key_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.manager_input.setText(self.command_history[self.history_index])
            elif self.history_index == len(self.command_history) - 1:
                self.history_index += 1
                self.manager_input.clear()
        else:
            QLineEdit.keyPressEvent(self.manager_input, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = ProjectManager()
    sys.exit(app.exec())