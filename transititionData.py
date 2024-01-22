import pandas as pd
import pyodbc
import re

server = 'LAPTOP-97PV2JG5\INSTANCESQL'
database = 'NhaKhoaHoc'
username = 'sa'
password = '123'
driver = '{ODBC Driver 17 for SQL Server}'

# Kết nối đến SQL Server
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()


def insert_thongTin(id, hoVaTen, gioiTinh, namSinh, diaChi, dienThoai, email, websiteCaNhan, chucDanh,
                    nganhDaoTao, chuyenNganhDaoTao, chuyenMonGiangDay, linhVucNghienCuu, trinhDoNgoaiNgu, linkImg):
    try:
        cursor.execute("EXEC insert_thongTin ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
                       id, hoVaTen, gioiTinh, namSinh, diaChi, dienThoai, email, websiteCaNhan, chucDanh,
                       nganhDaoTao, chuyenNganhDaoTao, chuyenMonGiangDay, linhVucNghienCuu, trinhDoNgoaiNgu, linkImg)
    except Exception as e:
        print("Lỗi:", e)


def insert_quanLy(donVi, diaChiCoQuan, dienThoaiCoQuan, emailCoQuan, idThongTin):
    try:
        # Gọi thủ tục lưu trữ
        cursor.execute("EXEC insert_quanLy ?,?,?,?,?", donVi,
                       diaChiCoQuan, dienThoaiCoQuan, emailCoQuan, idThongTin)
        # Commit thay đổi vào database
    except Exception as e:
        print("Lỗi:", e)


def insert_congTac(batDau, ketThuc, chucDanhCongTac, coQuanCongTac, chucVu, idThongTin, index):
    try:
        cursor.execute("EXEC insert_congTac ?,?,?,?,?,?", batDau,
                       ketThuc, chucDanhCongTac, coQuanCongTac, chucVu, idThongTin)
    except Exception as e:
        print("Lỗi:", e)
        print(f"{batDau}:{ketThuc}")
        print(index)


def insert_daoTao(bacDaoTao, coSoDaoTao, nganhDaoTao, namTotNghiep, idThongTin):
    try:
        cursor.execute("EXEC insert_daoTao ?,?,?,?,?", bacDaoTao,
                       coSoDaoTao, nganhDaoTao, namTotNghiep, idThongTin)
    except Exception as e:
        print("Lỗi : ", e)
# ! Viết một function để chuẩn hóa dữ liệu string


def refineString(input_string):
    match_start = re.search(r'Từ : (\d{2}/\d{2}/\d{4}) *', input_string)
    match_end = re.search(r'Đến : (\d{2}/\d{2}/\d{4})', input_string)

    start_date = match_start.group(1) if match_start else ''
    end_date = match_end.group(1) if match_end else ''
    return start_date, end_date


if __name__ == "__main__":
    excel_file_path = 'clawData.xlsx'
    # Đọc tất cả các sheets và lưu chúng vào một danh sách
    all_sheets = pd.read_excel(
        excel_file_path, sheet_name=None)
    sheet_names = list(all_sheets.keys())
    print("Danh sách các sheets:", sheet_names)
    for sheet_name, df in all_sheets.items():
        if sheet_name == 'Information':
            print("information")
            for index, row in df.iterrows():
                # Lấy giá trị từ các cột tương ứng với tham số của hàm
                id = str(row['ID'])
                hoVaTen = str(row['Họ và tên'])
                gioiTinh = str(row['Giới tính'])
                namSinh = row['Năm sinh']
                diaChi = str(row['Địa chỉ'])
                dienThoai = str(row['Số điện thoại'])
                email = str(row['Email'])
                websiteCaNhan = str(row['Website cá nhân'])
                chucDanh = str(row['Chức Danh'])
                nganhDaoTao = str(row['Ngành đào tạo'])
                chuyenNganhDaoTao = str(row['Chuyên ngành đào tạo'])
                chuyenMonGiangDay = str(row['Chuyên môn giảng dạy'])
                linhVucNghienCuu = str(row['Lĩnh vực nghiên cứu'])
                trinhDoNgoaiNgu = str(row['Trình độ ngoại ngữ'])
                linkImg = str(row['Link img'])
                # Gọi hàm insert_thongTin với các giá trị từ dòng hiện tại
                insert_thongTin(id, hoVaTen, gioiTinh, namSinh, diaChi, dienThoai, email, websiteCaNhan, chucDanh,
                                nganhDaoTao, chuyenNganhDaoTao, chuyenMonGiangDay, linhVucNghienCuu, trinhDoNgoaiNgu, linkImg)
                connection.commit()
        if sheet_name == 'Manager':
            print("Manager")
            for index, row in df.iterrows():
                donVi = str(row['Đơn vị'])
                diaChiCoQuan = str(row['Địa chỉ cơ quan'])
                dienThoaiCoQuan = str(row['Điện thoại cơ quan'])
                emailCoQuan = str(row['Email cơ quan'])
                idThongTin = str(row['Id'])
                # Gọi hàm insert_quanLy với các giá trị từ dòng hiện tại
                insert_quanLy(donVi, diaChiCoQuan,
                              dienThoaiCoQuan, emailCoQuan, idThongTin)
                connection.commit()
        if sheet_name == 'Working':
            print("working")
            for index, row in df.iterrows():
                startDate, endDate = refineString(row['Thời gian'])
                if startDate == '':
                    startDate = str(startDate)
                else:
                    startDate = pd.to_datetime(
                        startDate, format='%d/%m/%Y').strftime('%Y-%m-%d')
                if endDate == '':
                    endDate = str(endDate)
                else:
                    endDate = pd.to_datetime(
                        endDate, format='%d/%m/%Y').strftime('%Y-%m-%d')
                chucDanhCongTac = str(row['Chức danh công tác'])
                coQuanCongTac = str(row['Cơ quan công tác'])
                chucVu = str(row['Chức vụ'])
                idThongTin = str(row['Id'])
                insert_congTac(startDate, endDate, chucDanhCongTac,
                               coQuanCongTac, chucVu, idThongTin, index)
                connection.commit()
        if sheet_name == 'Training':
            print("Training")
            for index, row in df.iterrows():
                bacDaotao = str(row['Bậc đào tạo'])
                coSoDaoTao = str(row['Cơ sở đào tạo'])
                nganhDaoTao = str(row['Ngành đào tạo'])
                namTotNghiep = str(row['Năm tốt nghiệp'])
                idThongTin = str(row['Id'])
                insert_daoTao(bacDaotao, coSoDaoTao, nganhDaoTao,
                              namTotNghiep, idThongTin)
                connection.commit()
    if connection:
        connection.close()
