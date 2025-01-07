import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

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
    
    # Từ điển ánh xạ cho các loại địa điểm
    type_mapping = {
        1: "Restaurant",
        2: "Hotel",
        3: "Tourist destination",
        4: "Museum"
    }
    
    # Chuyển đổi dữ liệu và chèn vào MongoDB
    documents = []
    
    # Duyệt qua từng danh sách con bên trong data
    for sublist in data:
        if isinstance(sublist, list):
            for item in sublist:
                # Xử lý và chuyển đổi dữ liệu
                doc = {
                    "type": type_mapping.get(int(item["type"]), "Unknown"),  # Ánh xạ type
                    "name": item["name"],
                    "star": float(item["star"].replace(',', '.')) if item["star"] else None,
                    "location": {
                        "type": "Point",
                        "coordinates": [float(item["longitude"]), float(item["latitude"])]
                    },
                    "img": item.get("img"),
                    "status": item.get("status", True),  # Gán trạng thái mặc định là True
                    "timeOpen": item.get("timeOpen"),
                    "timeClose": item.get("timeClose"),
                }
                documents.append(doc)

    # Chèn dữ liệu vào collection
    for doc in documents:
        try:
            collection.insert_one(doc)
        except DuplicateKeyError:
            print(f"Bỏ qua đối tượng với img {doc['img']} do trùng lặp.")
        except Exception as e:
            print(f"Lỗi khi chèn dữ liệu: {e}")

    print("Dữ liệu đã được import thành công!")

# Chạy chương trình chính
if __name__ == "__main__":
    file_path = 'places1.json'  # Đường dẫn đến file JSON
    data = read_data(file_path)
    insert_data(data)
