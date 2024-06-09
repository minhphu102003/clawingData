import requests
from bs4 import BeautifulSoup
import mysql.connector
import sys
import pandas as pd

def connectionMysql(host,user,password,databaseName):
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=databaseName
    )
    cursor = db_connection.cursor()
    return db_connection, cursor

# Hàm chuyển đổi giá trị 
# VD ta cào được dữ liệu trên web như sau like': '3.7k', 'sell': '2.5k' và ta sẽ sử dụng hàm này để chuyển về dạng int 
def convert_str_to_int(s):
    if s[-1] == 'k':
        return int(float(s[:-1]) * 1000)  # Chuyển đổi '3.7k' thành 3700
    else:
        return int(s)

def commitAction(db_connection):
    db_connection.commit()

def closeAction(db_connection):
    db_connection.close()

def clawingDataProduct(stringUrl):
    url = stringUrl
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    #Với code này ta có thể lưu ảnh ,Tên thuốc, NGoài ra còn có thể lưu giá bán ,số tim và đã bán 
    if response.status_code == 200:
        # Tạo một mảng lưu danh sách các sản phẩm
        products = []

        # Lấy file html về để láy dữ liệu
        soup = BeautifulSoup(response.text, 'html.parser')
        productList = soup.find_all(class_='product-list')[0]
        relative_classes = productList.find_all(class_='relative')

        # In ra kết quả để kiểm tra
        for item in relative_classes:
            # Tạo một dictionary product để lưu dữ liệu 
            product = {}
            #! Lấy link của product
            linkProduct = item.find_all(class_='product-card')[0]['href']
            product['linkProduct'] = str(linkProduct)
            # Lấy link ảnh
            cardImg = item.find_all(class_='product-card-image')[0]
            linkImgItem = cardImg.find('img')['src']
            product['linkImg'] = str(linkImgItem)
            # Lấy tên thuốc
            productItem = item.find_all(class_='font-medium')[0]
            product_name = productItem.find('h3').text.strip().replace('\xa0',' ')  # Lấy nội dung của thẻ h3 và loại bỏ các khoảng trắng ở hai đầu
            product['medicineName'] = str(product_name)

            detailProduct = productItem.find_all(class_='whitespace-nowrap')
            if(detailProduct):
                spans = detailProduct[0].find_all('span')
                priceItem = spans[0].text.strip()
                priceItem = priceItem.split('\xa0')[0].replace('.','')
                likeItem = spans[2].text.strip()
                sellItem = spans[4].text.strip()
                
                # Chuyển sell từ 'sell': 'Đã bán 25k' sang  sell': '2.5k' dể đồng bộ với like rồi sử dụng 1 hàm chuyển 
                sellItem  =sellItem.split(' ')[2]

                sellItem = convert_str_to_int(sellItem)
                likeItem = convert_str_to_int(likeItem)
                # ! Lấy giá bán số lượng like cũng như số lượng đã bán 
                product['price'] = int(priceItem)
                product['like'] = int(likeItem)
                product['sell'] = int(sellItem)
                products.append(product)         
        return products
    else:
        return None




if __name__ == "__main__":
    # host = "localhost"
    # user = "root"
    # password = "1234"
    # databaseName = "pharmacy"
    # db_connection, cursor = connectionMysql(host, user, password, databaseName)
    all_products = []
    sys.stdout.reconfigure(encoding='utf-8')
    for i in range(1,136):
        stringUrl = f"https://www.pharmacity.vn/duoc-pham?index={i}&refresh=false&total=2873"
        clawingDataProduct(stringUrl)
        products_on_page = clawingDataProduct(stringUrl)
        
        # Nếu có dữ liệu từ trang hiện tại, thêm vào danh sách chính
        if products_on_page:
            all_products.extend(products_on_page)
    print(all_products)
    
    # !lưu dữ liệu vào excel sau đó for pandas để lấy link và get thêm thông tin chi tiết về product 
    
    df1 = pd.DataFrame(all_products)
    df1.to_csv('product.csv', index=False)
    
