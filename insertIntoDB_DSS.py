import pyodbc
from faker import Faker
import random

# Kết nối đến SQL Server
connection_string = "Driver={SQL Server};Server=TOBI;Database=QLI_KHOHANG;UID=sa;PWD=1234;"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Khởi tạo Faker
fake = Faker()

# Hàm để giới hạn độ dài của chuỗi
def truncate_string(value, length):
    if len(value) > length:
        return value[:length]
    return value

# Hàm để chèn dữ liệu ảo vào bảng KHACHHANG
def insert_fake_data_into_khachhang(num_records):
    for _ in range(num_records):
        makh = _ + 1
        ho_lot_kh = truncate_string(fake.last_name(), 50)
        ten_kh = truncate_string(fake.first_name(), 50)
        diachi_kh = truncate_string(fake.address().replace("\n", ", "), 50)
        tel_kh = truncate_string(fake.phone_number(), 50)
        matk_kh = random.randint(1000, 9999)

        cursor.execute("""
            INSERT INTO KHACHHANG (MAKH, HOLOTKH, TENKH, DIACHIKH, TELKH, MATKKH)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (makh, ho_lot_kh, ten_kh, diachi_kh, tel_kh, matk_kh))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng KHO
def insert_fake_data_into_kho(num_records):
    for _ in range(num_records):
        makho = _ + 1
        tenkho = truncate_string(fake.word(), 50)
        diachikho = truncate_string(fake.address().replace("\n", ", "), 50)
        telkho = truncate_string(fake.phone_number(), 50)

        cursor.execute("""
            INSERT INTO KHO (MAKHO, TENKHO, DIACHIKHO, TELKHO)
            VALUES (?, ?, ?, ?)
        """, (makho, tenkho, diachikho, telkho))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng LOAIHANG
def insert_fake_data_into_loaihang(num_records):
    for _ in range(num_records):
        maloaih = _ + 1
        tenloaih = truncate_string(fake.word(), 50)
        makho = random.randint(1, num_records)

        cursor.execute("""
            INSERT INTO LOAIHANG (MALOAIH, TENLOAIHANG, MAKHO)
            VALUES (?, ?, ?)
        """, (maloaih, tenloaih, makho))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng HANGHOA
def insert_fake_data_into_hanghoa(num_records):
    for _ in range(num_records):
        mahh = _ + 1
        tenhh = truncate_string(fake.word(), 100)
        donvitinh = truncate_string(fake.word(), 100)
        minton = random.randint(1, 100)
        luongton = random.randint(1, 500)
        maloaih = random.randint(1, num_records)

        cursor.execute("""
            INSERT INTO HANGHOA (MAHH, TENHH, DONVITINH, MINTON, LUONGTON, MALOAIHANG)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (mahh, tenhh, donvitinh, minton, luongton, maloaih))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng NHACUNGCAP
def insert_fake_data_into_nhacungcap(num_records):
    for _ in range(num_records):
        mancc = _ + 1
        tenncc = truncate_string(fake.company(), 100)
        diachinc = truncate_string(fake.address().replace("\n", ", "), 100)
        telncc = truncate_string(fake.phone_number(), 50)
        matk_ncc = random.randint(1000, 9999)

        cursor.execute("""
            INSERT INTO NHACUNGCAP (MANCC, TENNCC, DIACHINCC, TELNCC, MATKNCC)
            VALUES (?, ?, ?, ?, ?)
        """, (mancc, tenncc, diachinc, telncc, matk_ncc))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng PHIEU_XUAT
def insert_fake_data_into_phieu_xuat(num_records):
    for _ in range(num_records):
        maphieuxuat = _ + 1
        ngayx = fake.date_time_this_year()
        makh = random.randint(1, num_records)

        cursor.execute("""
            INSERT INTO PHIEU_XUAT (MAPHIEUXUAT, NGAYX, MAKH)
            VALUES (?, ?, ?)
        """, (maphieuxuat, ngayx, makh))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng PHIEU_NHAP
def insert_fake_data_into_phieu_nhap(num_records):
    for _ in range(num_records):
        maphieun = _ + 1
        ngayn = fake.date_time_this_year()
        mancc = random.randint(1, num_records)

        cursor.execute("""
            INSERT INTO PHIEU_NHAP (MAPHIEUN, NGAYN, MANCC)
            VALUES (?, ?, ?)
        """, (maphieun, ngayn, mancc))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng DONGPHIEUX
def insert_fake_data_into_dongphieux(num_records):
    for _ in range(num_records):
        maphieux = random.randint(1, num_records)
        mahh = random.randint(1, num_records)
        soluongx = random.randint(1, 100)
        dongiax = random.randint(1000, 5000)

        cursor.execute("""
            INSERT INTO DONGPHIEUX (MAPHIEUX, MAHH, SOLUONGX, DONGIAX)
            VALUES (?, ?, ?, ?)
        """, (maphieux, mahh, soluongx, dongiax))
    
    conn.commit()

# Hàm để chèn dữ liệu ảo vào bảng DONGPHIEUN
def insert_fake_data_into_dongphieun(num_records):
    for _ in range(num_records):
        maphieun = random.randint(1, num_records)
        mahh = random.randint(1, num_records)
        soluongn = random.randint(1, 100)
        dongian = random.randint(1000, 5000)

        cursor.execute("""
            INSERT INTO DONGPHIEUN (MAPHIEUN, MAHH, SOLUONGN, DONGIAXN)
            VALUES (?, ?, ?, ?)
        """, (maphieun, mahh, soluongn, dongian))
    
    conn.commit()

# Gọi các hàm để chèn 100 dòng dữ liệu ảo vào mỗi bảng
num_records = 100
insert_fake_data_into_khachhang(num_records)
insert_fake_data_into_kho(num_records)
insert_fake_data_into_loaihang(num_records)
insert_fake_data_into_hanghoa(num_records)
insert_fake_data_into_nhacungcap(num_records)
insert_fake_data_into_phieu_xuat(num_records)
insert_fake_data_into_phieu_nhap(num_records)
insert_fake_data_into_dongphieux(num_records)
insert_fake_data_into_dongphieun(num_records)

# Đóng kết nối
cursor.close()
conn.close()
print("Đã chèn 100 dòng dữ liệu ảo vào tất cả các bảng.")
