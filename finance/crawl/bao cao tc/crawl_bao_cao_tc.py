from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Cấu hình Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Chạy không giao diện để nhanh hơn
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Đường dẫn đến ChromeDriver (Cập nhật đúng vị trí của bạn)
service = Service("/Users/nguyentiendang0106/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL danh sách mã chứng khoán trên Vietstock
url = "https://vietstock.vn/tai-chinh.htm"
driver.get(url)
time.sleep(5)  # Chờ trang tải

# Lấy HTML sau khi trang đã tải
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Tìm tất cả mã chứng khoán trong class chứa tên mã
stocks = soup.find_all("span", class_="name-index")

# Lưu danh sách mã chứng khoán và link
stock_list = []
for stock in stocks:
    link = stock.find("a")["href"] if stock.find("a") else None
    ticker = stock.find("a").text.strip() if stock.find("a") else None
    if ticker and link:
        stock_list.append((ticker, link))

# Đóng trình duyệt sau khi lấy dữ liệu
driver.quit()

# Lưu danh sách mã chứng khoán vào DataFrame
df_stocks = pd.DataFrame(stock_list, columns=["Ticker", "URL"])
df_stocks.to_csv("danh_sach_ma_chung_khoan.csv", index=False)
print(f"✅ Đã lấy {len(df_stocks)} mã chứng khoán!")

# Khởi động lại Selenium
driver = webdriver.Chrome(service=service, options=chrome_options)

# Đọc danh sách mã chứng khoán từ file CSV (đã crawl ở bước trước)
df_stocks = pd.read_csv("danh_sach_ma_chung_khoan.csv")

# Tạo Dictionary để lưu dữ liệu từng bảng
financial_reports = {
    "KQKD": [],  # Kết quả kinh doanh
    "CĐKT": [],  # Cân đối kế toán
    "CSKD": []   # Chỉ số tài chính
}

# Hàm lấy dữ liệu từ bảng
def extract_table_data(table):
    data = []
    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols_text = [col.get_text(strip=True) for col in cols]
            if len(cols_text) > 1:
                data.append(cols_text)
    return data

# Lặp qua từng mã chứng khoán
for index, row in df_stocks.iterrows():
    ticker = row["Ticker"]
    url = row["URL"]

    print(f"🔍 Đang lấy dữ liệu báo cáo tài chính của {ticker}...")

    driver.get(url)
    time.sleep(5)  # Chờ trang tải

    # Lấy HTML trang web
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Lấy 3 bảng báo cáo tài chính
    tables = {
        "KQKD": soup.find("table", id="table-0"),  # Kết quả kinh doanh
        "CĐKT": soup.find("table", id="table-1"),  # Cân đối kế toán
        "CSKD": soup.find("table", id="table-2")   # Chỉ số tài chính
    }

    # Lưu dữ liệu của từng bảng
    for key, table in tables.items():
        data = extract_table_data(table)
        for row in data:
            financial_reports[key].append([ticker] + row)

# Đóng trình duyệt sau khi lấy dữ liệu
driver.quit()

# Chuyển dữ liệu thành DataFrame
df_kqkd = pd.DataFrame(financial_reports["KQKD"])
df_cdkt = pd.DataFrame(financial_reports["CĐKT"])
df_cskd = pd.DataFrame(financial_reports["CSKD"])

# Lưu vào file Excel với 3 sheet
with pd.ExcelWriter("bao_cao_tai_chinh.xlsx") as writer:
    df_kqkd.to_excel(writer, sheet_name="Ket_Qua_Kinh_Doanh", index=False)
    df_cdkt.to_excel(writer, sheet_name="Can_Doi_Ke_Toan", index=False)
    df_cskd.to_excel(writer, sheet_name="Chi_So_Tai_Chinh", index=False)

print("✅ Đã lưu báo cáo tài chính vào 'bao_cao_tai_chinh.xlsx' với 3 sheet.")