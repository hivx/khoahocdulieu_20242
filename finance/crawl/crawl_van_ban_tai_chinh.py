from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Cấu hình Selenium (Headless Mode để chạy ẩn)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Đường dẫn ChromeDriver của bạn
chrome_driver_path = "/Users/nguyentiendang0106/Downloads/chromedriver-mac-arm64/chromedriver"  # Cập nhật đường dẫn thực tế

# Khởi chạy trình duyệt
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# URL trang web cần crawl
base_url = "https://cafef.vn/"  # Thay thế bằng URL gốc của trang web
crawl_url = f"{base_url}/tai-chinh-quoc-te.chn"  # Thay thế bằng URL của danh sách bài viết

# Mở trang web
driver.get(crawl_url)
time.sleep(3)  # Đợi trang tải

# Lấy source HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

# Tìm danh sách bài viết
articles = soup.find_all("div", class_="tlitem box-category-item")

# Lưu dữ liệu
news_list = []
for article in articles:
    title_tag = article.find("h3").find("a") if article.find("h3") else None
    if title_tag:
        title = title_tag.text.strip()
        link = base_url + title_tag["href"]  # Ghép URL gốc với đường dẫn
        news_list.append({"title": title, "link": link})

# Xuất dữ liệu ra file Excel
df = pd.DataFrame(news_list)
df.to_excel("news_articles.xlsx", index=False)

print("✅ Crawl thành công! Dữ liệu đã lưu vào news_articles.xlsx")

# Đóng trình duyệt
driver.quit()
