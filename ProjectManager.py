import sys
import subprocess
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt6.QtCore import Qt


class ProjectManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.frontend_process = None
        self.backend_process = None

    def initUI(self):
        # 按钮布局
        button_layout = QHBoxLayout()
        start_button = QPushButton('Start')
        start_button.setStyleSheet('background-color: green')
        start_button.clicked.connect(self.start_projects)
        stop_button = QPushButton('Stop')
        stop_button.setStyleSheet('background-color: red')
        stop_button.clicked.connect(self.stop_projects)
        restart_button = QPushButton('Restart')
        restart_button.setStyleSheet('background-color: blue')
        restart_button.clicked.connect(self.restart_projects)
        force_pause_button = QPushButton('Force Pause')
        force_pause_button.setStyleSheet('background-color: gray')
        frontend_control_button = QPushButton('Restart/Start/Stop Frontend')
        frontend_control_button.setStyleSheet('background-color: purple')
        backend_control_button = QPushButton('Restart/Start/Stop Backend')
        backend_control_button.setStyleSheet('background-color: purple')

        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(restart_button)
        button_layout.addWidget(force_pause_button)
        button_layout.addWidget(frontend_control_button)
        button_layout.addWidget(backend_control_button)

        # 输出布局
        output_layout = QHBoxLayout()
        self.frontend_output = QTextEdit()
        self.frontend_output.setReadOnly(True)
        self.backend_output = QTextEdit()
        self.backend_output.setReadOnly(True)
        self.request_log_output = QTextEdit()
        self.request_log_output.setReadOnly(True)

        output_layout.addWidget(self.frontend_output)
        output_layout.addWidget(self.backend_output)
        output_layout.addWidget(self.request_log_output)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Project Manager')
        self.setGeometry(300, 300, 800, 600)
        self.show()

    def start_projects(self):
        if self.frontend_process is None:
            threading.Thread(target=self.start_frontend).start()
        if self.backend_process is None:
            threading.Thread(target=self.start_backend).start()

    def start_frontend(self):
        try:
            self.frontend_process = subprocess.Popen(['npm', 'run', 'dev'], cwd='./Frontend',
                                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                output = self.frontend_process.stdout.readline()
                if output == '' and self.frontend_process.poll() is not None:
                    break
                if output:
                    self.frontend_output.append(output.strip())
        except Exception as e:
            self.frontend_output.append(f"Error starting frontend: {e}")

    def start_backend(self):
        try:
            self.backend_process = subprocess.Popen(['python', 'app.py'], cwd='./Backend',
                                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                output = self.backend_process.stdout.readline()
                if output == '' and self.backend_process.poll() is not None:
                    break
                if output:
                    self.backend_output.append(output.strip())
        except Exception as e:
            self.backend_output.append(f"Error starting backend: {e}")

    def stop_projects(self):
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process = None
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process = None

    def restart_projects(self):
        self.stop_projects()
        self.start_projects()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = ProjectManager()
    sys.exit(app.exec())
    