from faker import Faker
import pymongo
from pymongo import MongoClient
import random
import pyodbc


def ConectToMongo(firstName, lastName):
    # Kết nối đến MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.apicompany  # Thay thế 'apicompany' bằng tên của cơ sở dữ liệu MongoDB của bạn
    # Thay thế 'employee' bằng tên của collection bạn muốn insert dữ liệu
    collection = db.employees
    fake = Faker()
    employee = {
        # Khóa chính bảng employee ràng buộc của mysql bên spring
        'employeeId': fake.unique.random_int(min=100, max=(10**11 - 1)),
        'firstName': firstName,
        'lastName': lastName,
        'vacationDays': random.randint(0, 30),
        'paidToDate': random.randint(1, 99),
        'paidLastYear': random.randint(1, 99),
        'payRate': round(random.uniform(1, 99.99), 2),
        # Khóa chính bảng payr_rate ràng buộc của mysql bên spring
        'payRateId': fake.unique.random_int(min=100, max=(10**11-1))
    }
    collection.insert_one(employee)

# ! Mặc định nếu không truyền tham số thì sẽ là 400


def RenderDataMongo(numberOfLoop=400):
    # Kết nối đến MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.apicompany
    collection = db.employees
    fake = Faker()
    for _ in range(numberOfLoop):
        employee = {
            # Khóa chính bảng employee ràng buộc của mysql bên spring
            'employeeId': fake.unique.random_int(min=100, max=(10**11 - 1)),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'vacationDays': random.randint(0, 30),
            'paidToDate': random.randint(1, 99),
            'paidLastYear': random.randint(1, 99),
            'payRate': round(random.uniform(1, 99.99), 2),
            'payRateId': fake.unique.random_int(min=100, max=(10**11-1))
        }
        collection.insert_one(employee)
    print("Insert Thành công")


def ConnectoSqlServer(serverName, databaseName, username, password):
    conn_str = (
        r'DRIVER={SQL Server};'
        f'SERVER={serverName};'
        f'DATABASE={databaseName};'
        f'UID={username};'
        f'PWD={password}'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # ! Chỉ lấy 200 dòng đầu tiên để lấy firstname và lastname
    cursor.execute("SELECT Top 300 * FROM personal")
    data_from_sql = []
    for row in cursor.fetchall():
        data_from_sql.append(row)
    conn.close()
    #! Đổ cột 1 và cột 2 tương ứng là firstname và lastname để generate vào mongodb
    for row in data_from_sql:
        ConectToMongo(row[1], row[2])


if __name__ == '__main__':
    # Truyền vào thông tin database tương ứng với hr
    # ConnectoSqlServer('TOBI', 'HR', 'sa', '1234')
    # truyền vào số lượng các colection độc lập không đồng bộ với  sql server databse hr
    RenderDataMongo(300)
