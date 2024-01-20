# clawingData
Cào dữ liệu từ web với địa chỉ sau :
https://csdlkhoahoc.hueuni.edu.vn/index.php/scientist/detail/id/{#value}
- với giá trị của {#value} chính là giá trị của id được lưu trong csdl của web này
- ý tưởng là dùng vòng for để chạy 1 lần và lấy dữ liệu có trên web

# Yêu cầu của những thư viện cần để thực hiện có thể chạy được:
-  requests
-  bs4
-  BeautifulSoup
-  pandas
# Chức năng chính của file python 
- cào dữ liệu từ web như thông tin của các giảng viên và lưu lại trên file excel cùng thư mục với file python khi chạy chương trình
- trong chương trình có một method main chứa vòng for dùng để thay đổi giá trị đầu vào của địa chỉ
- function scrape_data(id,url) dùng để gửi requests sau đó lấy mã html được phản hồi để phân tích và lấy những dữ liệu cần thiết
- function remove_extra_spaces(input_string) để xử lý string trước khi chuyển sang file excel, chức năng chính là xóa những khoảng trắng dư ra hoặc '\n' (kí tự xuống dòng) trong string ta lấy được từ mã html.
- khi đã lấy được dữ liệu thì chứa vào trong dictionary có **key**: **value** .Với **key** tương ứng với column trong csdl của web mà ta cần cào dữ liệu và **value** là các mảng tương ứng với các record trong csdl
- Từ dictionary ta chuyển sang các dataframe rồi chuyển vào file excel phân ra thành từng sheet với **1 sheet là một bảng** 
