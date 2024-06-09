from faker import Faker
import mysql.connector

# ! Hàm để check kết nối


def check_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="payroll"
        )

        mycursor = mydb.cursor()

        # Thực hiện một truy vấn SQL đơn giản
        mycursor.execute("SELECT VERSION()")

        # Lấy kết quả từ truy vấn
        db_version = mycursor.fetchone()

        # In ra phiên bản MySQL
        print("Kết nối MySQL thành công. Phiên bản MySQL:", db_version)

        # Đóng kết nối
        mydb.close()

    except mysql.connector.Error as err:
        print("Lỗi kết nối MySQL:", err)


def createDataEmployee(fake, idEmployee, lastName, firstName):
    employee = {
        "Employee_Number": fake.unique.random_int(min=10**10, max=(10**11)-1),
        "idEmployee": idEmployee,
        "Last_Name": lastName,  # Lấy từ bên SQL server qua nốt
        "First_Name": firstName,  # Lấy từ bên SQL server qua nốt
        "SSN": fake.random_int(min=10**10, max=(10**11)-1),
        "Pay_Rate": fake.pystr(max_chars=40),  # Tạo chuỗi ngẫu nhiên có độ dài tối đa là 40 ký tự
        "PayRates_id": fake.unique.random_number(digits=11),  # Trường này khả năng cao là khóa ngoại được tham chiếu từ bảng pay_rates nhưng trong code lại không có
        "Vacation_Days": fake.random_number(digits=11),
        "Paid_To_Date": fake.randint(0, 99),
        "Paid_Last_Year": fake.randint(0, 99)
    }
    return employee

def createDataPayRates(fake):
    payRates ={
        "idPay_Rates": fake.unique.random_int(min=10**10, max=(10**11 - 1)),
        "Pay_Rate_Name":fake.pystr(max_chars=40),
        "Value": fake.random_int(min = 10**10,max=(10**11-1)),
        "Tax_Percentage": fake.randint(0,99),
        "Pay_Type": fake.random_int(min = 10**10,max =(10**11-1)),
        "Pay_Amount": fake.random_int(min = 10**10,max =(10**11-1)),
        "PT_Level_C" : fake.random_int(min = 10**10,max =(10**11-1)),
    }
    return payRates


def createDataUsers(fake):
    users={
        "User_Name": fake.user_name(),
        "Password": fake.password(),
        "Email": fake.email(),
        "Active": fake.random_element(elements=(0, 1))
    }
    return users



if __name__ == '__main__':
    
