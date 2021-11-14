from re import U
import pyperclip
from time import sleep
import tkinter
from tkinter import filedialog
from os import name, system
from selenium import webdriver
from selenium.webdriver.edge import options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tqdm import tqdm
from colorama import Fore, Back, Style, init

# Auto reset style
init(autoreset=True)

# show file dialog without GUI elements
root = tkinter.Tk()
root.withdraw()

options = Options()
# Suppress DevTools listening
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_experimental_option("detach", True)  # Keep browser open
# options.add_argument("--disable-notifications")  # to disable notification
# options.add_argument("start-maximized")  # to start with maximized window
# run without UI
options.add_argument("headless")
# options.add_argument("disable-gpu")
# increase performance
options.add_argument('--no-proxy-server')

driver = webdriver.Edge('./edgedriver_win64/msedgedriver.exe', options=options)
driver.get('https://code.ptit.edu.vn/')

submitStatus = {'bg--50th': 'WA', '': 'DS', 'bg--10th': 'AC'}
listData = []
notDone = []
quesIdx = 0
inputList = []
courseList = []


def printMenu():
    print(Fore.YELLOW + 'MENU'.center(40, '_'))
    print('|' + ' '*38 + '|')
    print('|', '1. Hiển thị tất cả các bài'.ljust(36, ' '), '|')
    print('|', '2. Lọc bài chưa làm và làm sai'.ljust(36, ' '), '|')
    print('|', '3. Chọn lại khóa học'.ljust(36, ' '), '|')
    print('|', Fore.RED + 'q. Thoát chương trình'.ljust(36, ' '), '|')
    print('|' + '_'*38 + '|')


def printMenu1():
    print('MODE'.center(30, '_'))
    print('1. Sao chép Input')
    print('2. Nộp bài')
    print('0. Trở lại')


def clearScreen():

    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def loginToWeb():
    print(Fore.YELLOW + 'LOGIN'.center(40, ' '))
    UserID = input('Tài khoản:  ')
    UserPW = input('Mật khẩu:   ')
    loginUser = driver.find_element(By.NAME, 'username')
    loginPw = driver.find_element(By.NAME, 'password')
    loginUser.send_keys(Keys.CONTROL + 'a')
    loginUser.send_keys(UserID)
    loginPw.send_keys(UserPW, Keys.ENTER)
    clearScreen()


def getCourseList():
    courseListElement = Select(driver.find_element(By.ID, "course"))
    for i in range(len(courseListElement.options)):
        courseList.append([courseListElement.options[i].get_attribute(
            'text'), courseListElement.options[i].get_attribute('value')])


def selectCourse():
    print(Fore.YELLOW + 'DANH SÁCH KHÓA HỌC'.center(40, '_'))
    for i in range(1, len(courseList)):
        print(i, courseList[i][0])
    selectedCourse = int(input('\nChọn khóa học: '))
    # Get into course
    driver.get('https://code.ptit.edu.vn/student/question' + '?course=' +
               courseList[selectedCourse][1])
    clearScreen()


def getData():
    global listData
    listData = []
    print('Loading Data...')
    quesList = driver.find_element(By.TAG_NAME, 'tr')
    quesHead = [i.text for i in quesList.find_elements(By.TAG_NAME, 'th')]
    for i in range(1, 10):
        driver.get('https://code.ptit.edu.vn/student/question?page=' + str(i))
        quesList = driver.find_elements(By.TAG_NAME, 'tr')
        if len(quesList) == 1:
            break
        # Get data
        for j in tqdm(range(1, len(quesList)), desc='Loading Page %d...' % i, ncols=75):
            quesData = quesList[j].find_elements(By.TAG_NAME, 'td')
            data = {k: v.text for k, v in zip(quesHead, quesData)}
            data['Status'] = submitStatus[quesList[j].get_attribute('class')]
            listData.append(data)
    print('Successful!')
    sleep(2)
    clearScreen()


def printListData():
    for i in range(len(listData)-1, -1, -1):
        text = ' '.join([str(i+1).ljust(3, ' '), listData[i]['Status'], '-', listData[i]['Tiêu đề'].ljust(50, ' '), 'Lv',
                        listData[i]['Độ khó'], '    Done', listData[i]['Làm đúng']])
        if listData[i]['Status'] == 'AC':
            print(Fore.GREEN + text)
        elif listData[i]['Status'] == 'WA':
            print(Fore.RED + text)
        else:
            print(text)


def getInput(td):
    global inputList
    inputList = []
    print()
    inOutBox = td.find_elements(By.TAG_NAME, 'tr')
    # find appearence style
    if len(inOutBox[0].find_elements(By.TAG_NAME, 'td')) == 1:
        for i in range(len(inOutBox)):
            inOutText = inOutBox[i].find_element(By.TAG_NAME, 'td')
            if i % 4 == 1:
                inputList.append(inOutText.text)
            if i % 4 == 0:
                print(Fore.BLUE + 'Input')
            elif i % 4 == 2:
                print(Fore.BLUE + 'Output')
            else:
                print(inOutText.text)
    else:
        for i in range(1, len(inOutBox)):
            inOutText = inOutBox[i].find_elements(By.TAG_NAME, 'td')
            inputList.append(inOutText[0].text)
            print(Fore.BLUE + 'Input')
            print(inOutText[0].text)
            print(Fore.BLUE + 'Output')
            print(inOutText[1].text)


def processThread():
    global quesIdx
    printMenu1()
    mode1 = input('\nChoose: ')
    if mode1 == '1':
        ordinal = 0
        if len(inputList) > 1:
            ordinal = int(input('Ví dụ thứ mấy?: '))-1
        pyperclip.copy(inputList[ordinal])
        print("Input đã được copy vào clipboard!\n")
    elif mode1 == '2':
        submitPath = driver.find_element(
            By.ID, 'fileInput')
        filepath = filedialog.askopenfilename()
        submitPath.send_keys(filepath)
        submitBtn = driver.find_element(
            By.CLASS_NAME, 'submit__pad__btn')
        submitBtn.click()
        returnStatusBox = driver.find_elements(
            By.TAG_NAME, 'tr')[1]
        returnStatus = returnStatusBox.find_elements(
            By.TAG_NAME, 'td')
        while 1:
            if str(returnStatus[4].text) != '':
                break
        Res = returnStatus[3].text
        print('Kết quả: {0} với thời gian {1} và {2} bộ nhớ\n'.format(
            Fore.GREEN + Res if Res == 'AC' else Fore.RED + Res, returnStatus[4].text, returnStatus[5].text))
        if str(returnStatus[3].text) == 'AC':
            listData[quesIdx]['Status'] = 'AC'
            choose = input('Làm bài chưa AC tiếp? (y/n): ')
            if(choose):
                clearScreen()
                updateNotDone()
                quesIdx = int(notDone[0]['STT'])-1
                driver.get('https://code.ptit.edu.vn/student/question/' +
                           notDone[0]['Mã'])
                printThread()
                return
        elif listData[quesIdx]['Status'] != 'AC':
            listData[quesIdx]['Status'] = 'WA'
        driver.back()
    elif mode1 == '0':
        clearScreen()
        return
    sleep(2)
    processThread()


def printThread():
    print(Fore.YELLOW + listData[quesIdx]['Tiêu đề'])
    submit__des = driver.find_element(By.CLASS_NAME, 'submit__des')
    threadDes = submit__des.find_elements(By.XPATH, './*')
    for i in threadDes:
        if i.tag_name == 'table':
            break
        print(i.text)
    getInput(submit__des)
    processThread()


def getThread(m):
    global quesIdx
    quesSelected = int(input('\nXem bài (Nhập 0 để quay lại Menu): '))-1
    if quesSelected == -1:
        clearScreen()
        return
    if m == 1:
        driver.get('https://code.ptit.edu.vn/student/question/' +
                   notDone[quesSelected]['Mã'])
        quesIdx = int(notDone[quesSelected]['STT'])-1
    elif m == 2:
        driver.get('https://code.ptit.edu.vn/student/question/' +
                   listData[quesSelected]['Mã'])
        quesIdx = int(listData[quesSelected]['STT'])-1
    clearScreen()
    printThread()


def updateNotDone():
    global notDone
    notDone = []
    if len(notDone) == 0:
        for i in listData:
            if i['Status'] == 'WA' or i['Status'] == 'DS':
                notDone.append(i)


def printNotDone():
    print('Bạn chưa làm xong:', len(notDone), 'bài\n')
    for i in range(len(notDone)-1, -1, -1):
        text = ' '.join([str(i+1).ljust(3, ' '), notDone[i]['Status'], '-', notDone[i]['Tiêu đề'].ljust(50, ' '), 'Lv',
                        notDone[i]['Độ khó'], '    Done', notDone[i]['Làm đúng']])
        if notDone[i]['Status'] == 'WA':
            print(Fore.RED + text)
        else:
            print(text)


def process():
    printMenu()
    mode = input('Chọn chế độ: ')
    clearScreen()
    if mode == '1':
        printListData()
        getThread(2)
    elif mode == '2':
        updateNotDone()
        printNotDone()
        getThread(1)
        clearScreen()
    elif mode == '3':
        selectCourse()
        getData()
    elif mode == 'q':
        driver.quit()
        quit()
    process()


clearScreen()

# Main
while 1:
    try:
        loginToWeb()
        sleep(1)
        getCourseList()
        print(Fore.GREEN + 'Đăng nhập thành công!\n')
        break
    except:
        print(Fore.RED + 'Lỗi: Sai tên đăng nhập hoặc mật khẩu!')
        t = input('Đăng nhập lại? (y/n):')
        if t == 'n':
            driver.quit()
            quit()
        elif t == 'y':
            clearScreen()
            continue
selectCourse()
getData()
process()
driver.quit()
quit()
