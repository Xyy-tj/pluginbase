import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore
from Ui_dalle import Ui_MainWindow  # 假设你的UI文件名为dalle.ui
from qt_material import apply_stylesheet
import requests
import os
from datetime import datetime, timedelta, timezone
import dotenv

class MyWindow(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        apply_stylesheet(self.app, theme='dark_teal.xml')
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        
    def init_ui(self):
        # 初始化方法，这里可以写按钮绑定等的一些初始函数
        print('init ui')
        self.ui.pushButton.clicked.connect(self.push_button_clicked)
        self.ui.progressBar.setValue(0)
        self.setWindowIcon(QIcon('dalle/favicon.ico'))
        self.show()
        # load .ENV variables
        dotenv.load_dotenv()
        
    def push_button_clicked(self):
        # 按钮点击事件
        print('button clicked')
        self.ui.progressBar.setValue(0)
        print(self.ui.comboBox_imgsize.currentText())
        model_name = self.ui.comboBox_model.currentText()
        image_size = self.ui.comboBox_imgsize.currentText()
        self.ui.sub_system_info.append("正在创建请求，请耐心等待……")
        prompts = self.ui.textEdit.toPlainText()
        if len(prompts) == 0:
            self.ui.sub_system_info.append("提示词不能为空！")
            return
        try:
            self.ui.sub_system_info.append("当前prompts：{}, 正在生成图片，请耐心等待……".format(prompts))
            QApplication.processEvents()
            response = requests.post(
                os.getenv('BASE_URL'),
                headers={"Authorization": os.getenv('API_KEY')},
                json={"model": model_name, "size": image_size, "prompt": prompts, "n": 1},
            )
            self.ui.progressBar.setValue(30)
            self.ui.sub_system_info.append("正在下载图像，请耐心等待……")
            QApplication.processEvents()
            response.raise_for_status()
            data = response.json()["data"]
            
            download_folder = r"figs"
            os.makedirs(download_folder, exist_ok=True)
            current_time = datetime.now(timezone.utc) + timedelta(hours=8)  # GMT+8
            current_time_str = current_time.strftime("%Y%m%d-%H%M%S")
            
            for i, image in enumerate(data):
                image_url = image["url"]
                file_name = current_time_str + f"-{str(i+1).zfill(3)}.png"
                file_path = self.download_image(image_url, download_folder)
                new_file_path = os.path.join(download_folder, file_name)
                os.rename(file_path, new_file_path)
                self.ui.sub_system_info.append("图片已下载至：{}".format(new_file_path))
                pixmap = QPixmap(new_file_path)
                self.ui.label.setPixmap(pixmap.scaled(self.ui.label.size()))
            self.ui.progressBar.setValue(100)
            QApplication.processEvents()
        except requests.exceptions.HTTPError as err:
            self.ui.sub_system_info.append("请求错误：{}".format(err.response.text))
            print(("请求错误：{}".format(err.response.text)))
        
        except Exception as e:
            self.ui.sub_system_info.append("发生错误：{}".format(str(e)))
            print("发生错误：{}".format(str(e)))
            
    def download_image(self, url, folder_path):
        response = requests.get(url)
        file_path = os.path.join(folder_path, os.path.basename(url))
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    
    def bt_fileselect(self, param=''):
        # 选择文件
        self.ui.sub_system_info.clear()
        if param == 'figs_dir':
            default_dir = os.path.join(os.getcwd(), 'figs')
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", default_dir, "所有文件 (*)")
            # 如果用户选择了文件，则更新
            if file_path:
                print(file_path)
                self.ui.lineEdit.setText(file_path)
                self.ui.sub_system_info.append("数据路径更新成功！")
                return file_path
            else:
                print("未选择文件")
                return
        elif param == 'xx':
            
            return

# 程序入口
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    e = MyWindow()
    sys.exit(e.app.exec())