from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Cấu hình Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy không giao diện để nhanh hơn
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Đường dẫn đến chromedriver (chỉnh lại nếu cần)
service = Service("/Users/nguyentiendang0106/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Truy cập trang web
    url = "https://sjc.com.vn/"
    driver.get(url)

    # Đợi cho tới khi bảng giá xuất hiện
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sjc-table-show-price"))
    )

    # Cuộn xuống để đảm bảo dữ liệu hiển thị đầy đủ
    for _ in range(20):  # Cuộn 20 lần, mỗi lần 200 pixels
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(1)

    # Lấy HTML sau khi trang tải xong
    page_source = driver.page_source

finally:
    driver.quit()  # Đóng trình duyệt sau khi lấy dữ liệu

# Dùng BeautifulSoup để phân tích lại HTML
soup = BeautifulSoup(page_source, 'html.parser')

# Tìm bảng bằng class
table_element = soup.find("table", class_="sjc-table-show-price")

# Kiểm tra nếu bảng không tồn tại
if table_element is None:
    print("⚠️ Không tìm thấy bảng dữ liệu!")
    driver.quit()
    exit()

# Lấy tất cả hàng trong tbody
rows = table_element.find("tbody").find_all("tr")

# Kiểm tra nếu không có hàng nào trong bảng
if not rows:
    print("⚠️ Không tìm thấy hàng dữ liệu trong bảng!")
    driver.quit()
    exit()

data = []
for row in rows:
    cols = row.find_all("td")
    cols_text = [col.get_text(strip=True) for col in cols]

    # Bỏ qua hàng có ít hơn 3 cột
    if len(cols_text) < 3:
        continue

    data.append(cols_text[:3])

# Tạo DataFrame với đúng 3 cột
df = pd.DataFrame(data, columns=["Loại vàng", "Mua vào", "Bán ra"])

# Lưu vào file Excel
df.to_excel("gia_vang.xlsx", index=False)
print(f"✅ Đã lấy {len(df)} dòng dữ liệu và lưu vào 'gia_vang.xlsx'.")
