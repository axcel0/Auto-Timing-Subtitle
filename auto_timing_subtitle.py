import sys
import platform
import torch
import torch.nn as nn
import os
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QComboBox, QErrorMessage
from process import auto_sub_jp

class WhisperModel(nn.Module):
    def __init__(self, model_name, device):
        super(WhisperModel, self).__init__()
        self.model = torch.hub.load('snakers4/silero-models', model_name, source='local', path='pretrained')
        self.model.to(device)
        self.model.eval()

    def forward(self, input_values):
        with torch.no_grad():
            output = self.model(input_values)
        return output
    

os.environ['KMP_DUPLICATE_LIB_OK']='True'
def print_hardware_info():
    # Print CPU info
    cpu_info = f"CPU: {platform.processor()}"

    # Check for CUDA (GPU)
    if torch.cuda.is_available():
        gpu_info = f"GPU: {torch.cuda.get_device_name(0)}"
    else:
        gpu_info = "No GPU available."

    return cpu_info, gpu_info

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Auto timing subtitle')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        cpu_info, gpu_info = print_hardware_info()
        self.hardware_info_label = QLabel(f"Hardware Info:\n{cpu_info}\n{gpu_info}")
        self.layout.addWidget(self.hardware_info_label)

        self.beam_size_label = QLabel("The higher the Beam Size value, the more paths are explored during recognition, which can help improve recognition accuracy within a certain range,\nbut the relative VRAM usage will also be higher. At the same time, the Beam Size may decrease after exceeding 5-10.\nDefaut Beam size is 5")
        self.layout.addWidget(self.beam_size_label)

        self.beam_size = QLineEdit()
        self.beam_size.setText('5')
        self.layout.addWidget(self.beam_size)

        self.button_explore = QPushButton("Browse Files")
        self.button_explore.clicked.connect(self.browseFiles)
        self.layout.addWidget(self.button_explore)

        self.setLayout(self.layout)

    def createComboBox(self, items):
        combo_box = QComboBox()
        combo_box.addItems(items)
        self.layout.addWidget(combo_box)
        return combo_box

    def browseFiles(self):
        filename = QFileDialog.getOpenFileName(self, "Select a File", "/", "MP4 Files (*.mp4);;All Types (*.*);;")[0]

        if filename:
            self.path_ = QLabel(f"Selected files:\n{filename}", width=100, height=5)
            self.layout.addWidget(self.path_)

            self.type_menu = self.createComboBox(["audio","video"])
            self.split_menu = self.createComboBox(["No","Yes"])
            self.method_menu = self.createComboBox(["Modest","Aggressive"])
            self.model_menu = self.createComboBox(["large-v2", "large-v3"])

            self.button_process = QPushButton("Click to Process")
            self.button_process.clicked.connect(self.callback)
            self.layout.addWidget(self.button_process)
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No file selected.')
            error_dialog.exec()

    def callback(self):
        type_ = self.type_menu.currentText()
        model = self.model_menu.currentText()
        split = self.split_menu.currentText()
        method = self.method_menu.currentText()
        beam = self.beam_size.text()
        file_name = self.path_.text()

        try:
            time_consum = auto_sub_jp(type_, model, split, method, beam, file_name)
            self.done = QLabel(f"Done with {round(time_consum)}s!")
            self.layout.addWidget(self.done)
        except Exception as e:
            self.process = QLabel(f"Error: {e}")
            self.layout.addWidget(self.process)
            print(f"Error: {e}", file=sys.stderr)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()