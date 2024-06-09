import pandas as pd

# Khởi tạo một list rỗng để chứa giá trị nhập từ người dùng
my_array = []

# Cho người dùng nhập giá trị vào mảng
while True:
    user_input = input("Nhập giá trị (nhập 'exit' để kết thúc): ")

    if user_input.lower() == 'exit':
        break

    my_array.append(user_input)

# Dùng vòng lặp để thực hiện chuyển đổi giá trị
for i in range(len(my_array)):
    if '.' in my_array[i]:
        my_array[i] = my_array[i].replace('.', ',')

# Tạo DataFrame từ mảng
df = pd.DataFrame({"Column_Name": my_array})

# Ghi giá trị trong DataFrame vào file Excel
df.to_excel("output.xlsx", index=False)
