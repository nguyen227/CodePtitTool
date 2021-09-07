import pyperclip
from time import sleep

from selenium import webdriver
from selenium.webdriver.edge import options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


options = Options()
# Suppress DevTools listening
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)  # Keep browser open
options.add_argument("--disable-notifications")  # to disable notification
options.add_argument("start-maximized")  # to start with maximized window

UserID = 'B19DCCN481'
UserPW = 'Nguyen2702$ptit'

# UserID = input('Tài khoản:  ')
# UserPW = input('Mật khẩu:   ')

driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)
driver.get('https://code.ptit.edu.vn/')

sleep(1)
loginUser = driver.find_element(By.NAME, 'username')
loginPw = driver.find_element(By.NAME, 'password')

loginUser.send_keys(UserID)
loginPw.send_keys(UserPW, Keys.ENTER)

sleep(1)

courseList = Select(driver.find_element(By.ID, "course"))
print('\nDANH SÁCH KHÓA HỌC')
for i in range(len(courseList.options)):
    print('{0}. {courseName}'.format(
        i, courseName=courseList.options[i].get_attribute('text')))

selectedCourse = int(input('\nChọn khóa học: '))

driver.get('https://code.ptit.edu.vn/student/question' + '?course=' +
           courseList.options[selectedCourse].get_attribute('value'))
print('Loading ...', end=' ')
quesList = driver.find_elements(By.TAG_NAME, 'tr')
quesHead = [i.text for i in quesList[0].find_elements(By.TAG_NAME, 'th')]

listData = []
for i in range(1, len(quesList)):
    quesData = quesList[i].find_elements(By.TAG_NAME, 'td')
    data = {}
    data['class'] = quesList[i].get_attribute('class')
    for i in range(len(quesData)):
        data[quesHead[i]] = quesData[i].text
    listData.append(data)
print('Done!\n')

notDone = []

while 1:
    print('MENU'.center(30, ' '))
    print('1. Lọc bài chưa làm và sai')
    mode = input('Chọn chế độ: ')
    if mode == '1':
        if len(notDone) == 0:
            for i in listData:
                if i['class'] == '' or i['class'] == 'bg--50th':
                    notDone.append(i)
        print('Bạn chưa làm xong:', len(notDone), 'bài')
        for i in range(len(notDone)):
            print(str(i).ljust(3, ' '), '-', notDone[i]['Tiêu đề'].ljust(50, ' '), 'Lv',
                  notDone[i]['Độ khó'], 'Done', notDone[i]['Làm đúng'])

        quesSelected = int(input('Xem bài: '))
        driver.get('https://code.ptit.edu.vn/student/question/' +
                   notDone[quesSelected]['Mã'])
        sleep(2)
        print('\nĐỀ BÀI')
        thread = driver.find_element(By.CLASS_NAME, 'submit__des')
        # print(thread.text)
        threadDes = thread.find_elements(
            By.XPATH, './/span[@style="font-family:Arial,Helvetica,sans-serif"]')
        for i in threadDes:
            if str(i.text) == 'Ví dụ':
                print('\nVí Dụ')
                break
            print(i.text)
        inOutBox = thread.find_elements(By.TAG_NAME, 'tr')
        # find appearence style
        inputList = []
        if len(inOutBox[0].find_elements(By.TAG_NAME, 'td')) == 1:
            for i in range(len(inOutBox)):
                inOutText = inOutBox[i].find_element(By.TAG_NAME, 'td')
                if i % 4 == 1:
                    inputList.append(inOutText.text)
                if i % 4 == 0:
                    print('Input')
                elif i % 4 == 2:
                    print('Output')
                else:
                    print(inOutText.text)
        else:
            for i in range(1, len(inOutBox)):
                inOutText = inOutBox[i].find_elements(By.TAG_NAME, 'td')
                inputList.append(inOutText[0].text)
                print('Input')
                print(inOutText[0].text)
                print('Output')
                print(inOutText[1].text)
        while 1:
            print('\nMODE'.center(30, ' '))
            print('1. Copy input')
            print('2. Submit')
            print('0. Back')
            mode1 = int(input('\nChoose: '))
            if mode1 == 1:
                ordinal = 0
                if len(inputList) > 1:
                    ordinal = int(input('Ví dụ thứ mấy?: ')-1)
                pyperclip.copy(inputList[ordinal])
                print("Input đã được copy vào clipboard!")
            elif mode1 == 2:
                submitButton = driver.find_element(
                    By.XPATH, '//div[@class="submit__pad__nav__input col-6"]')
                submitButton.click()
            else:
                break
    elif mode == 'q':
        break
