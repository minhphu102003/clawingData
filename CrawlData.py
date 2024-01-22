import requests
from bs4 import BeautifulSoup
import pandas as pd

information = {
    'Link img': [],
    'Họ và tên': [],
    'Giới tính': [],
    'Năm sinh': [],
    'Địa chỉ': [],
    'Số điện thoại': [],
    'Email': [],
    'Website cá nhân': [],
    'Chức Danh': [],
    'Ngành đào tạo': [],
    'Chuyên ngành đào tạo': [],
    'Chuyên môn giảng dạy': [],
    'Lĩnh vực nghiên cứu': [],
    'Trình độ ngoại ngữ': [],
    'ID': [],
}

listTitle = ['Link img', 'Họ và tên', 'Giới tính', 'Năm sinh', 'Địa chỉ', 'Số điện thoại', 'Email', 'Website cá nhân', 'Chức Danh',
             'Ngành đào tạo', 'Chuyên ngành đào tạo', 'Chuyên môn giảng dạy', 'Lĩnh vực nghiên cứu', 'Trình độ ngoại ngữ', 'ID']

managerUnit = {
    'Đơn vị': [],
    'Địa chỉ cơ quan': [],
    'Điện thoại cơ quan': [],
    'Email cơ quan': [],
    'Id': []
}

listManagerUnit = ['Đơn vị', 'Địa chỉ cơ quan',
                   'Điện thoại cơ quan', 'Email cơ quan']

wokingProcess = {
    'Thời gian': [],
    'Chức danh công tác': [],
    'Cơ quan công tác': [],
    'Chức vụ': [],
    'Id': []
}

listWorkingProcess = ['Thời gian',
                      'Chức danh công tác', 'Cơ quan công tác', 'Chức vụ']

trainningProcess = {
    'Bậc đào tạo': [],
    'Cơ sở đào tạo': [],
    'Ngành đào tạo': [],
    'Năm tốt nghiệp': [],
    'Id': []
}

listTrainingProcess = ['Bậc đào tạo', 'Cơ sở đào tạo',
                       'Ngành đào tạo', 'Năm tốt nghiệp']


def remove_extra_spaces(input_string_or_list):
    if isinstance(input_string_or_list, str):
        cleaned_string = ' '.join(input_string_or_list.split())
        result = []
        is_space = False
        for char in cleaned_string:
            if char.isspace():
                if not is_space:
                    result.append(' ')
                    is_space = True
            else:
                result.append(char)
                is_space = False
        return ''.join(result)
    elif isinstance(input_string_or_list, list):
        return [remove_extra_spaces(value) for value in input_string_or_list]
    else:
        return input_string_or_list


def scrape_data(url, id):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        unique = 0
        imgElement = soup.find('div', class_='thumb')
        if imgElement:
            imgElementchild = imgElement.find('img')
            if imgElementchild:
                sourceImg = imgElementchild['src']
                information[listTitle[unique]].append(sourceImg)
                unique += 1
        media_body_elements = soup.find_all('div', class_='media-body')
        if media_body_elements:
            for index, media_body in enumerate(media_body_elements[:1]):
                string1 = media_body.text
                lines = string1.split('\n')
                count = 1
                for line in lines:
                    line = line.strip()
                    if count % 2 == 0 and count not in [2, 10]:
                        information[listTitle[unique]].append(line)
                        unique += 1
                    count += 1
            for index, media_body in enumerate(media_body_elements[1:2]):
                string2 = media_body.text
                if ':' in string2:
                    values = string2.split(':', 1)
                    cleaned_values = [remove_extra_spaces(
                        value) for value in values]
                    cleaned_string = ' '.join(cleaned_values)
                    cleaned_string = cleaned_string[8:]
                    if cleaned_string[0] == ',':
                        cleaned_string = cleaned_string[2:]
                    elif cleaned_string[0] == '.':
                        cleaned_string = ' '
                    information[listTitle[unique]].append(cleaned_string)
                    unique += 1
            for index, media_body in enumerate(media_body_elements[2:3]):
                string3 = media_body.text
                lines = string3.split('\n')
                count = 0
                for line in lines:
                    if count == 0:
                        count += 1
                        continue
                    else:
                        index = line.find(': ')
                        if index != -1:
                            phoneNumber = line[index+2:]
                            information[listTitle[unique]].append(phoneNumber)
                            unique += 1
                    count += 1
                if unique == 7:
                    information[listTitle[unique]].append('')
                    unique += 1
            listh5s = media_body_elements[3].find_all(
                'h5', class_='mt-0 mb-0 font-weight-600')
            count = 0
            for listh5 in listh5s:
                content = listh5.find_next('p')
                result = content.text.strip()
                result = remove_extra_spaces(result)
                information[listTitle[unique]].append(result)
                unique += 1
                count += 1
            while unique < 14:
                information[listTitle[unique]].append('')
                unique += 1
            information[listTitle[14]].append(id)
            countk = 0
            for index, media_body in enumerate(media_body_elements[4:]):
                tableUnits = media_body.find_all(
                    'table', class_='table table-hover')
                for tableUnit in tableUnits:
                    rows = tableUnit.find_all('tr')
                    for row in rows:
                        cells = row.find_all('td')
                        index = 0
                        for cell in cells:
                            stringValue = remove_extra_spaces(cell.text)
                            if countk == 0:
                                managerUnit[listManagerUnit[index]].append(
                                    stringValue)
                            elif countk == 1:
                                wokingProcess[listWorkingProcess[index % 4]].append(
                                    stringValue)
                            else:
                                trainningProcess[listTrainingProcess[index % 4]].append(
                                    stringValue)
                            index += 1
                            if countk == 0 and index == 4:
                                managerUnit['Id'].append(id)
                            elif countk == 1 and index == 4:
                                wokingProcess['Id'].append(id)
                            elif countk == 2 and index == 4:
                                trainningProcess['Id'].append(id)
                    countk = countk + 1
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


if __name__ == "__main__":
    for i in range(2, 4000):
        target_url = "https://csdlkhoahoc.hueuni.edu.vn/index.php/scientist/detail/id/"
        target_url = target_url+str(i)
        scrape_data(target_url, i)
        print(i)
    df = pd.DataFrame(information)
    df1 = pd.DataFrame(managerUnit)
    df2 = pd.DataFrame(wokingProcess)
    df3 = pd.DataFrame(trainningProcess)
    with pd.ExcelWriter('clawData.xlsx') as writer:
        df.to_excel(writer, sheet_name='Information', index=False)
        df1.to_excel(writer, sheet_name='Manager', index=False)
        df2.to_excel(writer, sheet_name='Working', index=False)
        df3.to_excel(writer, sheet_name='Training', index=False)
