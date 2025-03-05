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

# Thư mục chứa file
os.makedirs("crawl_T1/data", exist_ok=True)

# File lưu kết quả
output_file = "crawl_T1/data/petro_link.txt"

# Xóa file cũ (nếu có) để tránh trùng lặp
if os.path.exists(output_file):
    os.remove(output_file)

try:
    for n in range(2, 52):  # Duyệt từ trang 2 đến 51
        url = f"https://www.petrolimex.com.vn/ndi/thong-cao-bao-chi{n}.html"
        print(f"Đang crawl: {url}")

        # Mở trang web
        driver.get(url)

        # Chờ tất cả các thẻ h3 có class "post-default__title" xuất hiện
        h3_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "post-default__title"))
        )

        # Ghi vào file
        with open(output_file, "a", encoding="utf-8") as file:
            for h3 in h3_elements:
                try:
                    # Tìm thẻ <a> bên trong và lấy thuộc tính href
                    a_element = h3.find_element(By.TAG_NAME, "a")
                    link = a_element.get_attribute("href")

                    # Ghi link vào file
                    file.write(link + "\n")

                except Exception as e:
                    print(f"Lỗi khi lấy link từ thẻ h3: {e}")
                    
        # In ra màn hình
        print("Lấy link thanh cong tai trang ", n)

        time.sleep(2)  # Nghỉ một chút để tránh bị chặn

    print("\nCrawl hoàn tất! Link đã lưu vào petro_link.txt")

except Exception as e:
    print(f"Lỗi tổng quát: {e}")
finally:
    driver.quit()
