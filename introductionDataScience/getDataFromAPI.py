import requests
import pandas as pd 

def getLength(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            numberComment = data['data']['total']
            return numberComment
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data ',e)
        return 0

def getData(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            comments_data = data['data']['items']
            comments_list = []
            for comment in comments_data:
                comment_info = {
                    'full_name': comment['full_name'],
                    'content': comment['content'],
                    'creation_time': comment['creation_time'],
                    'time': comment['time']
                }
                comments_list.append(comment_info)
            return comments_list
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

if __name__=="__main__":
    url = 'https://usi-saas.vnexpress.net/index/get?offset=0&limit=5&frommobile=0&sort_by=like&is_onload=1&objectid=4751249&objecttype=1&siteid=1000000&categoryid=1004933&sign=92262bef48c0cacdc078bbb788ad3f4e&tab_active=most_like&reactions=&cookie_aid=1100702882&usertype=4'
    length = getLength(url)
    offset = 0
    limit  = 25
    all_comments = []
    if (length!=0):
        comments = getData(url)
        all_comments.extend(comments)
    
    while offset < length:
        url1 = f"https://usi-saas.vnexpress.net/index/get?offset={offset}&limit={limit}&frommobile=0&sort_by=like&is_onload=1&objectid=4751249&objecttype=1&siteid=1000000&categoryid=1004933&sign=92262bef48c0cacdc078bbb788ad3f4e&tab_active=most_like&reactions=&cookie_aid=1100702882&usertype=4"
        comments = getData(url1)
        all_comments.extend(comments)
        offset += limit

    # Xuất dữ liệu ra file Excel bằng pandas
    df = pd.DataFrame(all_comments)
    excel_file = 'comments.xlsx'
    df.to_excel(excel_file, index=False)

    # ! Bữa sau update lên cái reply nữa chừ ri là được rồi 


    
