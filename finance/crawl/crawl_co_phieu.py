from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Cấu hình trình duyệt
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

# Khởi tạo trình duyệt
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Mở trang web
url = "https://liveboard.cafef.vn/"
driver.get(url)
time.sleep(5)

# Chờ bảng dữ liệu xuất hiện
try:
    table = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "tblLiveboard"))
    )
    print("✅ Tìm thấy bảng dữ liệu!")

    # Chờ ít nhất 1 ô dữ liệu xuất hiện
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#tblLiveboard tbody tr td"))
    )

    # Cuộn trang để tải hết dữ liệu
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Chờ dữ liệu tải xong

except:
    print("❌ Không tìm thấy bảng dữ liệu hoặc không có dữ liệu!")
    driver.quit()
    exit()

# Lấy dữ liệu từ bảng
rows = table.find_elements(By.TAG_NAME, "tr")
print(f"🔍 Số dòng dữ liệu tìm thấy: {len(rows)}")  # Debug số dòng

data = []
for row in rows[1:]:  # Bỏ qua tiêu đề
    cols = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text.strip() for col in cols]
    if row_data:  # Chỉ thêm nếu hàng có dữ liệu
        data.append(row_data)

# Kiểm tra số cột thực tế
if data:
    num_columns = len(data[0])
    print(f"🔍 Số cột thực tế: {num_columns}")

    column_names = [
    "Mã", "T.C", "Trần", "Sàn",  # Mã cổ phiếu & Giá tham chiếu
    "Giá 3", "KL 3", "Giá 2", "KL 2", "Giá 1", "KL 1",  # Bên mua
    "+/-", "Giá", "KL", "Tổng KL",  # Khớp lệnh
    "Giá 1", "KL 1", "Giá 2", "KL 2", "Giá 3", "KL 3",  # Bên bán
    "Cao", "Thấp",  # Cao & Thấp
    "KL Mua", "KL Bán"  # ĐTNN (Đầu tư nước ngoài)
   ]

    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(data, columns=column_names)

    # Lưu vào Excel
    df.to_excel("co_phieu_data.xlsx", index=False, engine="openpyxl")

    print("✅ Crawl thành công! Dữ liệu đã lưu vào co_phieu_data.xlsx 🚀")
else:
    print("⚠️ Không có dữ liệu để lưu!")

# Đóng trình duyệt
driver.quit()
