import time
from datetime import datetime
import keyboard  # Thư viện để nhận diện phím bấm

while True:
    # Kiểm tra xem người dùng có nhấn phím Esc hay không
    if keyboard.is_pressed('esc'):  # Kiểm tra phím Esc
        print("Đã thoát khỏi chương trình.")
        break

    # Nhận đầu vào từ người dùng
    expiry_str = input("Nhập thời gian hết hạn (hoặc nhấn Esc để thoát): ")

    try:
        # Chuyển đổi chuỗi thời gian thành đối tượng datetime
        expiry_datetime = datetime.fromisoformat(expiry_str[:-1])  # Loại bỏ 'Z' ở cuối

        # Chuyển đổi đối tượng datetime thành timestamp (giây từ Epoch)
        expiry_timestamp = int(time.mktime(expiry_datetime.timetuple()))

        print(f"Thời gian hết hạn dưới dạng timestamp: {expiry_timestamp}")
    
    except ValueError:
        print("Định dạng thời gian không hợp lệ. Vui lòng nhập lại.")
