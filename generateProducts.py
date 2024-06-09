from faker import Faker

import pymongo



# Kết nối đến MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Thay "mydatabase" bằng tên cơ sở dữ liệu MongoDB

db = client["apicompany"]

collection = db["products"]  # Thay "products" bằng tên collection tương ứng



# Khởi tạo đối tượng Faker

fake = Faker()



# Hàm tạo dữ liệu giả mạo cho mỗi sản phẩm





def create_fake_product():

    return {

        "name": fake.sentence(nb_words=3)[:-1],

        "category": fake.word(),

        # làm tròn 2 số thập phân

        "price": round(fake.random.uniform(1, 10**5), 2),

        # Giả lập userId

        "userId": fake.unique.random_int(min=100, max=(10**11-1)),

        "imgURL": fake.image_url(),

    }





# Số lượng sản phẩm cần tạo

num_products = 50



# Tạo và lưu dữ liệu giả mạo vào MongoDB

for _ in range(num_products):

    product_data = create_fake_product()

    collection.insert_one(product_data)



print("insert successfully! ")

client.close()