import os
import time
import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Cấu hình Chrome WebDriver
options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

# URL của trang web
url = "https://www.petrolimex.com.vn/ndi/thong-cao-bao-chi/petrolimex-dieu-chinh-gia-xang-dau-tu-15-gio-00-phut-ngay-27-02-2025.html"

# Thư mục chứa file
os.makedirs("test", exist_ok=True)
os.makedirs("test/images", exist_ok=True)  # Thư mục lưu ảnh

def download_image(img_url, save_folder, file_name):
    """Hàm tải ảnh về máy"""
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Đã tải ảnh: {file_path}")
        else:
            print(f"Không thể tải ảnh: {img_url}")
    except Exception as e:
        print(f"Lỗi khi tải ảnh {img_url}: {e}")

try:
    # Mở trang web
    driver.get(url)

    # Chờ phần tử xuất hiện 
    header = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "blogDetail__header"))
    )

    entry_detail = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "entry-detail"))
    )

    # Lấy nội dung text
    fina_text = header.text + "\n" + entry_detail.text

    # Ghi vào file
    with open("test/petro.txt", "w", encoding="utf-8") as file:
        file.write(fina_text)

    print("Dữ liệu đã được ghi vào petro.txt")

    # Lấy danh sách ảnh trong bài viết
    img_elements = entry_detail.find_elements(By.TAG_NAME, "img")
    for i, img in enumerate(img_elements):
        img_url = img.get_attribute("src")
        if img_url:
            img_name = f"petro_{i}.jpg"
            download_image(img_url, "test/images", img_name)

except Exception as e:
    print(f"Lỗi: {e}")

finally:
    time.sleep(5)
    driver.quit()
