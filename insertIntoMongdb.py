import json
from pymongo import MongoClient

# Hàm đọc dữ liệu từ file JSON
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Hàm chèn dữ liệu vào MongoDB
def insert_data(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['smartcity']
    
    # Tạo collection 'place' nếu chưa tồn tại
    if 'place' not in db.list_collection_names():
        db.create_collection('place')
        print("Collection 'place' đã được tạo.")
    else:
        print("Collection 'place' đã tồn tại.")
        
    collection = db['place']
    
    # Chuyển đổi dữ liệu và chèn vào MongoDB
    documents = []
    
    # Duyệt qua từng danh sách con bên trong data
    for sublist in data:
        # Kiểm tra nếu sublist là danh sách
        if isinstance(sublist, list):
            for item in sublist:
                # Xử lý và chuyển đổi dữ liệu
                doc = {
                    "type": item["type"],
                    "name": item["name"],
                    "star": float(item["star"].replace(',', '.')) if item["star"] else None,  # Chuyển đổi số sao từ string sang float
                    "longitude": float(item["longitude"]),
                    "latitude": float(item["latitude"]),
                    "img": item["img"],
                    "status": True,  # Gán trạng thái mặc định là True
                    "timeOpen": None,  # Thêm thời gian mở cửa nếu có
                    "timeClose": None,  # Thêm thời gian đóng cửa nếu có
                }
                documents.append(doc)

    # Chèn dữ liệu vào collection
    if documents:
        collection.insert_many(documents)
        print("Dữ liệu đã được import thành công!")

# Chạy chương trình chính
if __name__ == "__main__":
    # Đọc dữ liệu từ tệp JSON
    file_path = 'places1.json'  # Đường dẫn đến file JSON
    data = read_data(file_path)
    
    # Chèn dữ liệu vào MongoDB
    insert_data(data)
