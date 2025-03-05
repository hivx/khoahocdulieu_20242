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
# chrome_options.add_argument("--headless")  # Chạy không giao diện để nhanh hơn
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Đường dẫn đến chromedriver (chỉnh lại nếu cần)
service = Service("/Users/nguyentiendang0106/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Truy cập trang web
    url = "https://www.x-rates.com/table/?from=USD&amount=1"
    driver.get(url)
    time.sleep(5)

    # Đợi cho tới khi bảng giá xuất hiện
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.tablesorter.ratesTable"))
    )

    # Cuộn xuống để đảm bảo dữ liệu hiển thị đầy đủ
    for _ in range(10):  # Cuộn 10 lần, mỗi lần 200 pixels
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(1)

    # Lấy HTML sau khi trang tải xong
    page_source = driver.page_source

finally:
    driver.quit()  # Đóng trình duyệt sau khi lấy dữ liệu

# Dùng BeautifulSoup để phân tích lại HTML
soup = BeautifulSoup(page_source, 'html.parser')

# Tìm bảng bằng class
table_element = soup.find("table", class_="tablesorter ratesTable")

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
df = pd.DataFrame(data, columns=["US Dollar", "1.00 USD", "inv. 1.00 USD"])

# Lưu vào file Excel
df.to_excel("ty_gia_ngoai_te.xlsx", index=False)
print(f"✅ Đã lấy {len(df)} dòng dữ liệu và lưu vào 'ty_gia_ngoai_te.xlsx'.")
