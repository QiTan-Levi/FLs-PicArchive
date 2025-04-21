import sys
import subprocess
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt6.QtCore import QProcess
import chardet


class ProjectManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.frontend_process = None
        self.backend_process = None

    def initUI(self):
        # 创建按钮
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
        force_pause_button.clicked.connect(self.force_pause)

        frontend_control_button = QPushButton('Restart/Start/Stop Frontend')
        frontend_control_button.setStyleSheet('background-color: purple')
        frontend_control_button.clicked.connect(self.frontend_control)

        backend_control_button = QPushButton('Restart/Start/Stop Backend')
        backend_control_button.setStyleSheet('background-color: purple')
        backend_control_button.clicked.connect(self.backend_control)

        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(restart_button)
        button_layout.addWidget(force_pause_button)
        button_layout.addWidget(frontend_control_button)
        button_layout.addWidget(backend_control_button)

        # 创建文本框
        self.frontend_output = QTextEdit()
        self.frontend_output.setReadOnly(True)
        self.backend_output = QTextEdit()
        self.backend_output.setReadOnly(True)
        self.request_log = QTextEdit()
        self.request_log.setReadOnly(True)

        # 创建文本框布局
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.frontend_output)
        output_layout.addWidget(self.backend_output)
        output_layout.addWidget(self.request_log)

        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Project Manager')
        self.setGeometry(300, 300, 1200, 600)
        self.show()

    def start_projects(self):
        # 启动前端项目
        self.frontend_process = QProcess()
        self.frontend_process.readyReadStandardOutput.connect(self.read_frontend_output)
        self.frontend_process.start('bash', ['-c', 'cd Frontend && npm run serve'])

        # 启动后端项目
        self.backend_process = QProcess()
        self.backend_process.readyReadStandardOutput.connect(self.read_backend_output)
        self.backend_process.start('bash', ['-c', 'cd Backend && python app.py'])

    def stop_projects(self):
        if self.frontend_process:
            self.frontend_process.terminate()
        if self.backend_process:
            self.backend_process.terminate()

    def restart_projects(self):
        self.stop_projects()
        self.start_projects()

    def force_pause(self):
        if self.frontend_process:
            self.frontend_process.kill()
        if self.backend_process:
            self.backend_process.kill()

    def frontend_control(self):
        if self.frontend_process:
            if self.frontend_process.state() == QProcess.ProcessState.Running:
                self.frontend_process.terminate()
            else:
                self.frontend_process = QProcess()
                self.frontend_process.readyReadStandardOutput.connect(self.read_frontend_output)
                self.frontend_process.start('bash', ['-c', 'cd Frontend && npm run serve'])
        else:
            self.frontend_process = QProcess()
            self.frontend_process.readyReadStandardOutput.connect(self.read_frontend_output)
            self.frontend_process.start('bash', ['-c', 'cd Frontend && npm run serve'])

    def backend_control(self):
        if self.backend_process:
            if self.backend_process.state() == QProcess.ProcessState.Running:
                self.backend_process.terminate()
            else:
                self.backend_process = QProcess()
                self.backend_process.readyReadStandardOutput.connect(self.read_backend_output)
                self.backend_process.start('bash', ['-c', 'cd Backend && python app.py'])
        else:
            self.backend_process = QProcess()
            self.backend_process.readyReadStandardOutput.connect(self.read_backend_output)
            self.backend_process.start('bash', ['-c', 'cd Backend && python app.py'])

    def read_frontend_output(self):
        output = self.frontend_process.readAllStandardOutput().data()
        # 去除一些可能干扰解码的特殊字符
        output = re.sub(b'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\xff]', b'', output)
        detected_encoding = chardet.detect(output)['encoding']
        try:
            decoded_output = output.decode(detected_encoding)
        except UnicodeDecodeError:
            decoded_output = output.decode(detected_encoding, errors='replace')
        self.frontend_output.append(decoded_output)

    def read_backend_output(self):
        output = self.backend_process.readAllStandardOutput().data()
        output = re.sub(b'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\xff]', b'', output)
        detected_encoding = chardet.detect(output)['encoding']
        try:
            decoded_output = output.decode(detected_encoding)
        except UnicodeDecodeError:
            decoded_output = output.decode(detected_encoding, errors='replace')
        self.backend_output.append(decoded_output)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = ProjectManager()
    sys.exit(app.exec())
    