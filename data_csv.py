import os
import time
import csv
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
csv_file = "petro.csv"
csv_header = ['Title', 'Content', 'Image URLs']  # Thêm cột Title

# Kiểm tra nếu file CSV đã tồn tại, nếu không thì tạo mới và viết tiêu đề
file_exists = os.path.exists(csv_file)
with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as file:  # Sử dụng 'utf-8-sig' để tránh lỗi font trong Excel
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(csv_header)  # Ghi tiêu đề cột vào file CSV

    try:
        with open(input_file, "r", encoding="utf-8") as input_file:
            urls = input_file.readlines()  # Đọc từng dòng (mỗi dòng là một URL)

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

                # Lưu nội dung text vào file CSV
                title = header.text  # Lấy tiêu đề của bài viết
                content = entry_detail.text  # Lấy toàn bộ nội dung bài viết

                # Tạo danh sách ảnh cho bài viết (chỉ lấy link ảnh)
                img_urls = []
                img_elements = entry_detail.find_elements(By.TAG_NAME, "img")
                for i, img in enumerate(img_elements):
                    img_url = img.get_attribute("src")
                    if img_url:
                        img_urls.append(img_url)  # Thêm chỉ URL ảnh vào danh sách

                # Ghi dữ liệu vào file CSV
                writer.writerow([title, content, "; ".join(img_urls)])

                print(f"Lưu xong dữ liệu cho URL: {url}")

            except Exception as e:
                print(f"Lỗi khi crawl {url}: {e}")

            time.sleep(5)  # Nghỉ giữa các request để tránh bị chặn

        print("\nCrawl hoàn tất!")

    except Exception as e:
        print(f"Lỗi tổng quát: {e}")
    
    finally:
        time.sleep(10)
        driver.quit()
