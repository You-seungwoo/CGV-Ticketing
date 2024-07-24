## ==============================
## 2024-07-24, YOO SEUNG WOO

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import time


options = webdriver.ChromeOptions()
options.add_argument('--log-level=1')
driver = webdriver.Chrome()
login_url = 'https://m.cgv.co.kr/WebAPP/Member/Login.aspx?RedirectURL=http%3a%2f%2fm.cgv.co.kr%2fWebApp%2fMyCgvV5%2fmyMain.aspx'
movie_list_url = 'https://m.cgv.co.kr/WebAPP/MovieV4/movieList.aspx?iPage=1&Seq=88228&mtype=now&morder=TicketRate&mnowflag=0'
url = ''

print('='*40 + '\n\n영화 티켓 자동 발권 프로그램 \nMade by Yoo Seung Woo\n\n' + '='*40)
id = input('\nCGV 아이디를 입력하세요. : ') 
password = getpass.getpass('\nCGV 비밀번호를 입력해주세요. : ') 
count = 0 # 반복 횟수
cooltime = 1

def close_warning():
    try:
        result = driver.switch_to.alert
        for i in range(5):
            result.accept()    
    except:
        try:
            if WebDriverWait(driver, 2).until(EC.alert_is_present()):
                print('test')
                try:
                    result = driver.switch_to.alert
                    for i in range(5):
                        result.accept()    
                except:
                    pass
        except:
            pass


## ============== 로그인 ==================

driver.get(login_url)
driver.refresh()
driver.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_Login_tbUserID"]').send_keys(id)
driver.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_Login_tbPassword"]').send_keys(password)
driver.execute_script('javascript:clickLogin();') # 로그인 함수 호출

## ============== 영화 선택 ==================

driver.get(movie_list_url)  # 영화 목록 사이트로 이동
movie_list = WebDriverWait(driver, 6).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.main_movie_list.clsAjaxList')))  
movie_table = []

print('\n','='*40,'\n')
for i in range(20):
    movie = driver.find_element(By.XPATH, f'//*[@id="ContainerView"]/div[1]/div[{i+1}]')
    movie_name = movie.find_element(By.CLASS_NAME, 'tit').text
    movie_link = movie.find_element(By.CLASS_NAME, 'btn_reserve').get_attribute('onclick')
    movie_table.append((movie_name, movie_link))
   
    print(f'{i+1}번: {movie.find_element(By.CLASS_NAME, "tit").text} ({movie.find_element(By.CLASS_NAME, "rel_date").text})')
print('\n','='*40,'\n')

driver.execute_script(movie_table[int(input('예매하고 싶은 영화의 번호를 입력하세요. : ')) - 1][1]) 
# Movie_Table에서 input 받은 숫자 튜플의 1번째 값 인덱싱(링크)



## ============= 영화 지역 선택 =================

try:
    region_button_Table = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.CLASS_NAME, 'popArea_list'))).find_elements(By.TAG_NAME, 'li')
except:
    driver.refresh()
    region_button_Table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'popArea_list'))).find_elements(By.TAG_NAME, 'li')

region_table = []
k = 0
print('\n','='*40,'\n')
for i in region_button_Table:
    if i.get_attribute('style') == 'display: block;':
        
        region_button = i.find_element(By.TAG_NAME, 'a')
        region_text = region_button.get_attribute('title') 

        if region_text != '추천 CGV':
            k += 1
            region_table.append((region_text, region_button))
            print(f'{k}번: {region_text}')

print('\n','='*40,'\n')

region_table[int(input('영화를 시청할 지역을 선택해주세요. : ')) - 1][1].click()

## ============= 영화관 선택 =================

Cinema_table = []
k = 0
print('\n','='*40,'\n')
for i in WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME, 'popCinema_list'))).find_elements(By.TAG_NAME, 'li'):
    if i.get_attribute('style') != 'display:none' and i.get_attribute('style') != 'display: none;':
        k += 1
        Cinema_button = i.find_element(By.TAG_NAME, 'a')
        Cinema_text = i.get_attribute('data-name')
        Cinema_table.append((Cinema_text, Cinema_button))
        print(f'{k}번: {Cinema_text}')

print('\n','='*40,'\n')
Cinema_table[int(input('예매 할 영화관을 선택해주세요. : ')) - 1][1].click()

time.sleep(0.5)
driver.execute_script('javascript:fnSchTheaterResult();') # 영화관 선택 호출
url = driver.current_url # 선택 된 영화 사이트를 url 변수로 선언

## ============== 날짜 선택 =====================

Day_table = []
k = 0
print('\n','='*40,'\n')
for i in WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME, 'screeningSchedule_time_list'))).find_elements(By.TAG_NAME, 'li'):
    if i.get_attribute('class')[-6:] != 'dimmed':
        k += 1
        Day_link = i.find_element(By.TAG_NAME, 'a').get_attribute('onclick')
        Day_text = i.get_attribute('data-sel-cd')[:-13]
        Day_table.append((Day_text, Day_link))
        print(f'{k}번: {Day_text}')

print('\n','='*40,'\n')
day_number = int(input('예매 할 날짜를 선택해주세요. : ')) - 1 # 표시를 +1 해서 (1번 ... 3번) 표기했으므로
driver.execute_script(Day_table[day_number][1])
print('\n','='*40,'\n')


## ============= 날짜 선택 =================

def ask_time():
    Want_Time = input('선호하는 영화 시작 시간대를 입력해주세요. (ex : 12:00~15:00 ): ')


## ============= 인원 선택 =================

## 24-07-23 인원 선택할때 만약 좌석이 하나밖에 남지 않았다면 -> 오류 발생할것 
## 그러므로 영화 시간 선택이 true 되더라도 잔여좌석이 people_count 보다 작다면 pass 하게끔 수정하기

## 24-07-24 인원 선택할 때 1명 이상일 경우 장애인석이 같이 선택될 수도 있는 문제 발생 -> 오류 발생함 
## 어떻게 고치지?????


people_count = 1
def people_number():
    global people_count
    people_count = int(input('예매하고 싶은 인원을 입력하세요. : '))
    if people_count > 9999:
        print('\n 예매 인원은 최대 3명입니다.')
        people_count = 1
        people_number()

people_number()
print('\n','='*40,'\n')

## ============= 메인 함수 =================

#2024-07-23 장애인 석 예매 안되도록 수정할 것 -수정함
#2024-07-24 여분 좌석 < people_count 일때 오류 발생함 -> 나중에 해결
def main():
    try:
        driver.get(url)
    except:
        raise Exception("[Error] 비밀번호 또는 아이디가 일치하지 않습니다. 다시 시도해주세요.")

    while True:
        global count
        time.sleep(cooltime)
        wait = WebDriverWait(driver, 2)
        try:
            Time_button = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, f'btn_miniMap')))
            
            found = True
        except:

            ## ============= 여분 표 탐색 =================

            count += 1
            try: 
                driver.execute_script(Day_table[day_number][1]) # 유저가 설정 한 날짜의 버튼을 누르면 자동으로 불러오기 되는 것 이용ㅇ
            except:
                time.sleep(2)
                
            print(f'\r[info] 여분 표 탐색 중.. {count}번째 새로고침', end='')
            found = False
            continue
            
            ## ============= 여분 표 확보시 (found True) ================= 

        if found:
            for button in Time_button:
                if int(WebDriverWait(button,3).until(EC.presence_of_element_located((By.TAG_NAME, 'span'))).text) < people_count:
                    count += 1
                    try: 
                        driver.execute_script(Day_table[day_number][1]) # 유저가 설정 한 날짜의 버튼을 누르면 자동으로 불러오기 되는 것 이용ㅇ
                    except:
                        time.sleep(2)
                
                    print(f'\r[info] 여분 표 탐색 중.. {count}번째 새로고침', end='')
                    found = False
                    continue

                if button.is_enabled() == True: 
                    print(f'\n[info] 여분 티켓을 찾았습니다!')
                    try_time = time.time() # 실행시간 
                    try:
                        button.click() 
                    except: 
                        close_warning() # 혹시 경고 뜨면 막아야 하니까
                        try:
                            button.click()
                        except:
                            print('[info] 예매에 실패했습니다. 다시 탐색합니다.')
                            result = driver.switch_to.alert
                            for i in range(5):
                                result.accept() 
                            main()
                            break
                    
                    ## ============= 의자 유형 선택 =================
                    
                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="General"]/a[{people_count}]'))).click()
                    except:
                        print('[info] 버튼 클릭 실패, 다시 시도합니다.')
                        close_warning()
                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="General"]/a[{people_count}]'))).click()
                        except:
                            print('[info] 예매에 실패했습니다. 다시 탐색합니다.')
                            main()
                            break
                        
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="totSelCnt"]'))).click()

                    try: 
                        wait = WebDriverWait(driver, 1)  
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn_close'))).click() # 12세 이용가 뭐시기
                    except:
                        pass
                        
                    seat_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pointer"))) 

                    done = False
                    k = 0
                    clicked_seat = []
                    for i in seat_buttons:
                            if done == True: # 결제 창구로 넘어가면 attribute를 불러 오지 못하는 현상 발생으로 인한 추가
                                break

                            if i.get_attribute('rating_nm') != '일반석': 
                                continue
                            
                            k += 1 
                            msg = f'{i.get_attribute("locynm")}열 {i.get_attribute("locxnm")}석'


                            try:
                                clicked_seat.append(msg)
                                driver.execute_script(f'jQuery(\'#seat_table td[seatname="{i.get_attribute("seatname")}"]\').click();')
                                if len(clicked_seat) < people_count: ## 클릭 된 좌석이 예매할 수보다 적으면 고의로 오류를 날려서 한번 더 반복하게 함
                                    raise Exception

                                time.sleep(0.5)
                                driver.execute_script('javascript:chkSnackOrderPop();') # 예매하기
                                print('\n[info] 좌석 선택 창구에 진입했습니다.')
                                try:
                                    result = driver.switch_to.alert
                                    for i in range(5):
                                        result.accept() 

                                    print('[info] 예매에 실패했습니다. 다시 탐색합니다.')
                                    main()
                                    break
                                
                                except:
                                    done = True
                                    print(f'\n[ 좌석 선택 완료 ] \n- 소요시간 : {round(time.time() - try_time,2)}초 \n- 선택좌석 : ', end='') 
                                    print(clicked_seat)
                                    time.sleep(2)
                                    driver.execute_script('javascript:fn_skip();')
                                    break

                            except:
                                print(f'\r[info] 좌석 선택 시도 중 : {k} 회', end='')
                                pass
                    
                    time.sleep(4)

                    a = 0
                    for a in range(600):
                        a += 1
                        print(f'\r약 10분 내로 결제를 완료해야 합니다. ({600-a}초)', end='')
                        time.sleep(1)

                    time.sleep(99999)

main()
