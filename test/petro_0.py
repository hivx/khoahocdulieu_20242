import os
import time
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
    
    # Thư mục chứa file
    os.makedirs("test/data", exist_ok=True)

    # Ghi vào file
    with open("test/data/petro.txt", "w", encoding="utf-8") as file:
        file.write(fina_text)

    print("Dữ liệu đã được ghi vào petro.txt")

except Exception as e:
    print(f"Lỗi: {e}")
finally:
    time.sleep(5)
    driver.quit()
