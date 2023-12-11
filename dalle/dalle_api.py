import requests
import os
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import dotenv
 
def download_image(url, folder_path):
    response = requests.get(url)
    file_path = os.path.join(folder_path, os.path.basename(url))
    with open(file_path, "wb") as file:
        file.write(response.content)
    return file_path
 
def dalle_function():
    # 获取输入的提示词
    prompt = entry.get()
    model_name = "dall-e-3"
    image_size = "1024x1024"
    
    try:
        print("正在生成图片，请耐心等待……")
        response = requests.post(
            os.getenv('BASE_URL'),
            headers={"Authorization": os.getenv('API_KEY')},
            json={"model": model_name, "size": image_size, "prompt": prompt, "n": 1},
        )
        response.raise_for_status()
        data = response.json()["data"]
        
        download_folder = r"figs"
        os.makedirs(download_folder, exist_ok=True)
        current_time = datetime.now(timezone.utc) + timedelta(hours=8)  # GMT+8
        current_time_str = current_time.strftime("%Y%m%d-%H%M%S")
        
        for i, image in enumerate(data):
            image_url = image["url"]
            file_name = current_time_str + f"-{str(i+1).zfill(3)}.png"
            file_path = download_image(image_url, download_folder)
            new_file_path = os.path.join(download_folder, file_name)
            os.rename(file_path, new_file_path)
            print("图片已下载至：", new_file_path)
        # 显示图片
        img = Image.open(new_file_path)
        img = img.resize((300, 300))  # 调整图片大小
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        panel.image = img  # 保持对图片的引用
            
    
    except requests.exceptions.HTTPError as err:
        print("请求错误：", err.response.text)
    
    except Exception as e:
        print("发生错误：", str(e))
 
if __name__ == "__main__":
    # load .ENV variables
    dotenv.load_dotenv()
    
    # 创建窗口
    window = tk.Tk()
    window.geometry("500x300")
    window.title("Dall-E 3 Demo")
    
    entry = tk.Entry(window, text="请输入提示词")
    entry.pack()
    button = tk.Button(window, text="生成图片", command=dalle_function)
    button.pack()
    panel = tk.Label(window)
    panel.pack()

    # 运行窗口
    window.mainloop()
    