# ! Giới thiệu một chút về chương trình mà ta chuẩn bị phải thực hiện
#  ! Ta sẽ sử dụng thư viện faker để render ra dữ liệu sau đó insert vào database để test xem web có thực sự chạy được không
from faker import Faker
import pyodbc
import random

def generate_personal_data(fake, benefit_plan):
    personal_data = {
        "Employee_ID": fake.unique.random_int(min=10**5, max=(10**8)-1),
        "First_Name": fake.first_name(),
        "Last_Name": fake.last_name(),
        "Middle_Initial": fake.random_letter(),
        "Address1": fake.street_address(),
        "Address2": fake.secondary_address(),
        "City": fake.city(),
        "State": fake.state(),
        "Zip":  fake.random_int(min=10**5, max=(10**8)-1),
        "Email": fake.email(),
        "Phone_Number": fake.phone_number(),
        "Social_Security_Number": fake.ssn(),
        "Drivers_License": fake.license_plate(),
        "Marital_Status": fake.random_element(elements=('Single', 'Married', 'Divorced', 'Widowed')),
        "Gender": fake.boolean(),
        "Shareholder_Status": fake.boolean(),
        "Benefit_Plans": benefit_plan,
        "Ethnicity": fake.random_element(elements=('Asian', 'Black', 'White', 'Hispanic', 'Other'))
    }
    return personal_data


def generate_job_history_data(fake, employee_ID):
    departments = ['Engineering', 'Accounting', 'Sales',
                   'Human Resources', 'Product Development', 'Marketing']
    job_history_data = {
        # numeric(18,0) not null
        # "ID":  fake.unique.random_int(min=10**17, max=(10**18)-1),
        # numeric(18,0) not null  #! Đây là khóa ngoại
        # fake.unique.random_int(min=10**17, max=(10**18)-1),
        "Employee_ID": employee_ID,
        "Department": random.choice(departments),
        "Division": fake.text(max_nb_chars=40),
        "Start_Date": fake.date_time(),
        "End_Date": fake.date_time(),
        "Job_Title": fake.text(max_nb_chars=40),
        # numeric(18,0)
        "Supervisor": fake.random_int(min=10**16, max=(10**17)-1),
        "Job_Category": fake.text(max_nb_chars=40),
        "Location": fake.text(max_nb_chars=40),
        # numeric(18,0)
        "Departmen_Code":  fake.random_int(min=10**16, max=(10**17)-1),
        # numeric(18,0)
        "Salary_Type":  fake.random_int(min=10**16, max=(10**17)-1),
        "Pay_Period": fake.text(max_nb_chars=40),
        # numeric(18,0)
        # ! Vì làm full tuần thì 168 ngày thôi còn nếu có quy định 1 ngày tối đa bao nhiều giờ và tăng ca tối đa bao nhiêu giờ thì có thể tính được số max nhỏ hơn (ở đây lấy 24*7 luôn cho lẹ)
        "Hours_per_Week": fake.random_int(min=1, max=168),
        "Hazardous_Training": fake.boolean()  # bit
    }
    return job_history_data


def generate_employment_data(fake, employee_ID):
    # ! trạng thái ở đây chỉ có full time và part time để dữ liệu đồng bộ với yêu cầu trong case-study
    employment_status = random.choice(['part-time', 'full-time'])
    employment_data = {
        "Employee_ID":  employee_ID,  # ! Vừa khóa chính vừa khóa ngoại là một phần tử yếu
        "Employment_Status": employment_status,
        "Hire_Date": fake.date_time(),
        "Workers_Comp_Code": fake.word(),
        "Termination_Date": fake.date_time(),
        "Rehire_Date": fake.date_time(),
        "Last_Review_Date": fake.date_time()
    }
    return employment_data


def generate_emergency_contacts_data(fake, employee_ID):
    emergency_contacts_data = {
        # numeric(18,0) not null
        "Employee_ID": employee_ID,  # ! Vừa khóa chính vừa là khóa ngoại  phần tử yếu
        #! tham chiếu đến khóa ngoại nhưng đây cũng là khóa chính trong bản nên cần một giải thuật kĩ càng hơn
        "Emergency_Contact_Name": fake.name(),
        "Phone_Number": fake.phone_number(),
        "Relationship": fake.word()
    }
    return emergency_contacts_data


def generate_benefit_plans_data(fake):
    benefit_plans_data = {
        # bảng này có khóa chính tự tăng dần
        # numeric(18,0) IDENTITY(1,1) not null
        # "Benefit_Plan_ID":  fake.unique.random_int(min=10**17, max=(10**18)-1),   #! Trường dữ liệu tự tăng không cần phải insert
        "Plan_Name": fake.word(),
        "Deductable": fake.unique.random_int(min=10**17, max=(10**18)-1),
        "Percentage_CoPay": fake.random_int(min=0, max=100)  # int
    }
    return benefit_plans_data

# ! Ta sẽ viết unit test cho hàm personal_data ở trên và ở đây ta chỉ cần kiểm tra khóa chính của chúng không bị trùng lặp
# ! Ta sẽ thực hiện giải quyết vấn đề này bằng việc thực hiện hàm set để hỗ trợ thực hiện việc làm đó


def check_true(existing_ids, new_id):
    if new_id in existing_ids:
        return False
    existing_ids.add(new_id)
    return True


def testLenghtEmail(fake):
    for i in range(100000):
        email = fake.email()
        if (len(email) <= 50):
            print(i)
        else:
            return False
    # ! Đã test hàm fake.email() với số đủ lớn và giá trị len của nó không vượt quá 50


def testLengthlSsn(fake):
    for i in range(100000):
        email = fake.ssn()
        if (len(email) <= 50):
            print(i)
        else:
            return False
    # ! Đã test hàm fake.Ssn() với số đủ lớn và giá trị len của nó không vượt quá 50


def testLengthlLicensePlate(fake):
    for i in range(100000):
        email = fake.license_plate()
        if (len(email) <= 50):
            print(i)
        else:
            return False
    # ! Đã test hàm fake.license_plate() với số đủ lớn và giá trị len của nó không vượt quá 50


def testLengthWord(fake):
    for i in range(100000):
        email = fake.word()
        if (len(email) <= 50):
            print(i)
        else:
            return False
    #! Đã test và nó render phù hợp với kiểu dữ liệu trong sql


# ! Hàm này customize dùng để test độ chính xác render khóa chính ( chắc chắn phải không bị trùng lặp)
def testUnique(fake):
    existing_employee_ids = set()
    for i in range(5000):
        datarow = generate_personal_data(fake)
        is_unique = check_true(existing_employee_ids, datarow["Employee_ID"])
        if is_unique:
            print(i)
            print(datarow)
        else:
            print("Data is not unique. Employee_ID already exists:", datarow)
            print("Fails")
            break


def insert_data_personal(cursor, datarow_personal):
    sql_insert_personal = """
        INSERT INTO [Personal] (
            Employee_ID, First_Name, Last_Name, Middle_Initial, Address1, Address2,
            City, State, Zip, Email, Phone_Number, Social_Security_Number,
            Drivers_License, Marital_Status, Gender, Shareholder_Status,
            Benefit_Plans, Ethnicity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """
    # Thực hiện insert
    cursor.execute(sql_insert_personal,
                   datarow_personal["Employee_ID"], datarow_personal["First_Name"],
                   datarow_personal["Last_Name"], datarow_personal["Middle_Initial"],
                   datarow_personal["Address1"], datarow_personal["Address2"],
                   datarow_personal["City"], datarow_personal["State"],
                   datarow_personal["Zip"], datarow_personal["Email"],
                   datarow_personal["Phone_Number"], datarow_personal["Social_Security_Number"],
                   datarow_personal["Drivers_License"], datarow_personal["Marital_Status"],
                   datarow_personal["Gender"], datarow_personal["Shareholder_Status"],
                   datarow_personal["Benefit_Plans"], datarow_personal["Ethnicity"])
    # Commit các thay đổi vào cơ sở dữ liệu
    connection.commit()


def insert_data_job_history(cursor, datarow_job_history):
    sql_insert_job_history = """
        INSERT INTO [Job_History] (
            Employee_ID, Department, Division, Start_Date, End_Date,
            Job_Title, Supervisor, Job_Category, Location,
            Departmen_Code, Salary_Type, Pay_Period, Hours_per_Week, Hazardous_Training
        )
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(sql_insert_job_history,
                   datarow_job_history["Employee_ID"],
                   datarow_job_history["Department"], datarow_job_history["Division"],
                   datarow_job_history["Start_Date"], datarow_job_history["End_Date"],
                   datarow_job_history["Job_Title"], datarow_job_history["Supervisor"],
                   datarow_job_history["Job_Category"], datarow_job_history["Location"],
                   datarow_job_history["Departmen_Code"], datarow_job_history["Salary_Type"],
                   datarow_job_history["Pay_Period"], datarow_job_history["Hours_per_Week"],
                   datarow_job_history["Hazardous_Training"])
    # Commit các thay đổi vào cơ sở dữ liệu
    connection.commit()


def insert_data_employment(cursor, datarow_employment):
    sql_insert_employment = """
        INSERT INTO [Employment] (
            Employee_ID, Employment_Status, Hire_Date, Workers_Comp_Code,
            Termination_Date, Rehire_Date, Last_Review_Date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql_insert_employment,
                   datarow_employment["Employee_ID"], datarow_employment["Employment_Status"],
                   datarow_employment["Hire_Date"], datarow_employment["Workers_Comp_Code"],
                   datarow_employment["Termination_Date"], datarow_employment["Rehire_Date"],
                   datarow_employment["Last_Review_Date"])
    connection.commit()


def insert_data_emergency_contacts(cursor, datarow_emergency_contacts):
    sql_insert_emergency_contacts = """
        INSERT INTO [Emergency_Contacts] (
            Employee_ID, Emergency_Contact_Name, Phone_Number, Relationship
        )
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(sql_insert_emergency_contacts,
                   datarow_emergency_contacts["Employee_ID"],
                   datarow_emergency_contacts["Emergency_Contact_Name"],
                   datarow_emergency_contacts["Phone_Number"],
                   datarow_emergency_contacts["Relationship"])

    connection.commit()


def insert_data__benefit_plans(cursor, datarow_benefit_plans):
    sql_insert_benefit_plans = """
        INSERT INTO [Benefit_Plans] (
            Plan_Name, Deductable, Percentage_CoPay
        )
        OUTPUT INSERTED.Benefit_Plan_ID
        VALUES (?, ?, ?)
    """

    cursor.execute(sql_insert_benefit_plans,
                   datarow_benefit_plans["Plan_Name"],
                   datarow_benefit_plans["Deductable"],
                   datarow_benefit_plans["Percentage_CoPay"])
    # Fetch the inserted ID
    inserted_id = cursor.fetchone()[0]
    # ! Trả về khóa chính tự tăng

    connection.commit()

    return inserted_id


if __name__ == '__main__':
    fake = Faker()
    conn_str = r'DRIVER={SQL Server};SERVER=TOBI;DATABASE=HR;UID=sa;PWD=1234'
    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()
    for _ in range(500):
        datarow_benefit_plan = generate_benefit_plans_data(fake)
        id_plan = insert_data__benefit_plans(cursor, datarow_benefit_plan)
        datarow_personal = generate_personal_data(fake, id_plan)
        insert_data_personal(cursor, datarow_personal)
        employee_id = datarow_personal.get('Employee_ID')
        datarow_job_history = generate_job_history_data(fake, employee_id)
        insert_data_job_history(cursor, datarow_job_history)
        datarow_emergency_contacts = generate_emergency_contacts_data(
            fake, employee_id)
        insert_data_emergency_contacts(cursor, datarow_emergency_contacts)
        datarow_employment = generate_employment_data(fake, employee_id)
        insert_data_employment(cursor, datarow_employment)
    cursor.close()
    connection.close()
