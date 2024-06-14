import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Khởi tạo trình duyệt Chrome với các tùy chọn
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

# Mở trang web cần đăng nhập
driver.get("https://vnexpress.net/dua-tre-khong-duoc-an-dui-ga-4751249.html")
# ! Tương tự trang web cũng ngăn chặn bot từ selenium và không thể login vào được 

# Đợi cho người dùng đăng nhập thủ công và chờ một thời gian để chắc chắn đăng nhập hoàn tất
input("Đã đăng nhập xong? Nhấn Enter để tiếp tục...")

# Lấy và lưu cookies vào file
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# Đóng trình duyệt
driver.quit()
