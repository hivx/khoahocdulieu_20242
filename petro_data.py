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

# Đọc danh sách URL từ file
input_file = "crawl_T1/data/petro_link.txt"

# Thư mục chứa dữ liệu tổng
os.makedirs("petro", exist_ok=True)

def download_image(img_url, save_folder, file_name):
    """Hàm tải ảnh về thư mục chỉ định"""
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
    with open(input_file, "r", encoding="utf-8") as file:
        urls = file.readlines()  # Đọc từng dòng (mỗi dòng là một URL)

    for idx, url in enumerate(urls, start=2):  # n bắt đầu từ 2
        url = url.strip()
        if not url:
            continue

        print(f"Đang crawl: {url}")

        try:
            # Mở trang web
            driver.get(url)

            # Chờ phần tử xuất hiện
            header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "blogDetail__header"))
            )
            entry_detail = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "entry-detail"))
            )

            # Tạo thư mục riêng cho từng trang
            folder_name = f"petro/petro-{idx}"
            os.makedirs(folder_name, exist_ok=True)

            # Lưu nội dung text
            text_filename = os.path.join(folder_name, "content.txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(header.text + "\n" + entry_detail.text)

            print(f"Lưu xong: {text_filename}")

            # Lấy danh sách ảnh trong bài viết
            img_elements = entry_detail.find_elements(By.TAG_NAME, "img")
            for i, img in enumerate(img_elements):
                img_url = img.get_attribute("src")
                if img_url:
                    img_name = f"image-{i}.jpg"
                    download_image(img_url, folder_name, img_name)

        except Exception as e:
            print(f"Lỗi khi crawl {url}: {e}")

        time.sleep(5)  # Nghỉ giữa các request để tránh bị chặn

    print("\nCrawl hoàn tất!")

except Exception as e:
    print(f"Lỗi tổng quát: {e}")

finally:
    time.sleep(10)
    driver.quit()
