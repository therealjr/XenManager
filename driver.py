import sys
import subprocess
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QLabel, QColorDialog, QLineEdit
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer

class XenManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xen Guest Manager")
        self.setGeometry(100, 100, 900, 600)
        
        self.dom_table = QTableWidget()
        self.dom_table.setColumnCount(7)
        self.dom_table.setHorizontalHeaderLabels(["Domain", "Status", "Template", "NetVM", "CPU", "RAM", "Color Label"])
        self.dom_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_domains)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.dom_table)
        self.layout.addWidget(self.refresh_button)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        self.refresh_domains()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_domains)
        self.timer.start(5000)  # Auto-refresh every 5 seconds
    
    def run_command(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            return output
        except subprocess.CalledProcessError:
            return ""
    
    def parse_xl_list(self):
        output = self.run_command("xl list -l")
        if output:
            return json.loads(output)
        return []
    
    def refresh_domains(self):
        domains = self.parse_xl_list()
        self.dom_table.setRowCount(len(domains))
        
        for row, dom in enumerate(domains):
            dom_name = dom.get("name", "Unknown")
            dom_status = dom.get("state", "Unknown")
            template = dom.get("template", "N/A")
            netvm = dom.get("netvm", "N/A")
            cpu = dom.get("vcpu", "N/A")
            ram = dom.get("memory", "N/A")
            
            self.dom_table.setItem(row, 0, QTableWidgetItem(dom_name))
            self.dom_table.setItem(row, 1, QTableWidgetItem(dom_status))
            self.dom_table.setItem(row, 2, QTableWidgetItem(template))
            self.dom_table.setItem(row, 3, QTableWidgetItem(netvm))
            self.dom_table.setItem(row, 4, QTableWidgetItem(str(cpu)))
            self.dom_table.setItem(row, 5, QTableWidgetItem(str(ram)))
            
            color_button = QPushButton("Set Color")
            color_button.clicked.connect(lambda _, r=row: self.pick_color(r))
            self.dom_table.setCellWidget(row, 6, color_button)
    
    def pick_color(self, row):
        color = QColorDialog.getColor()
        if color.isValid():
            self.dom_table.item(row, 0).setBackground(color)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XenManager()
    window.show()
    sys.exit(app.exec())
