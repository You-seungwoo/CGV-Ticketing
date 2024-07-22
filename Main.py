from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import time

print('='*20 + '\n영화 티켓 자동 발권 프로그램 -  Made by Yoo Seung Woo\n' + '='*20)

id = input('CGV 아이디를 입력하세요. : ') 
password = getpass.getpass('CGV 비밀번호를 입력해주세요. : ') 


driver = webdriver.Chrome()
count = 0 # 반복 횟수
login_url = 'https://m.cgv.co.kr/WebAPP/Member/Login.aspx?RedirectURL=http%3a%2f%2fm.cgv.co.kr%2fWebApp%2fMyCgvV5%2fmyMain.aspx'

# ============================================================

url = "https://m.cgv.co.kr/" ## CGV 모바일 웹 기반

# ============================================================

driver.get(login_url)
driver.refresh()
driver.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_Login_tbUserID"]').send_keys(id)
driver.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_Login_tbPassword"]').send_keys(password)

try:
    driver.find_element(By.XPATH, '//*[@id="ContainerView"]/div/div/div/div/div[3]/button').click()
except:
    print('[info] 비밀번호 또는 아이디가 일치하지 않습니다. 다시 시도해주세요.')

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


def main():
    try:
        driver.get(url)
    except:
        raise Exception("[error] 비밀번호 또는 아이디가 일치하지 않습니다. 다시 시도해주세요.")
        
    driver.refresh()

    while True:
        time.sleep(0.5)
        wait = WebDriverWait(driver, 1)
        try:
            Time_button = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, f'btn_miniMap')))
            found = True
        except:
            global count 
            count += 1
            try: 
                driver.find_element(By.XPATH, '//*[@id="screeningSchedule_time_list"]/li[1]/a/span[1]').click()
            except:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="screeningSchedule_time_list"]/li[1]/a/span[1]'))).click()
                
            print(f'\r[info] 여분 표 탐색 중.. {count}번째 새로고침', end='')
            found = False
            pass
        
        if found:
            for button in Time_button:
                if button.is_enabled() == True:
                    print(f'\n[info] 여분 티켓을 찾았습니다!')
                    try_time = time.time()
                    try:
                        button.click()
                    except:
                        close_warning()
                        try:
                            button.click()
                        except:
                            print('[info] 예매에 실패했습니다. 다시 탐색합니다.')
                            result = driver.switch_to.alert
                            for i in range(5):
                                result.accept() 
                            main()
                            break

                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="General"]/a[1]'))).click()
                    except:
                        print('[info] 버튼 클릭 실패, 다시 시도합니다.')
                        close_warning()
                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="General"]/a[1]'))).click()
                        except:
                            print('[info] 예매에 실패했습니다. 다시 탐색합니다.')
                            main()
                            break
                        
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="totSelCnt"]'))).click()

                    try: 
                        wait = WebDriverWait(driver, 3.5)  
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn_close'))).click() # 12세 이용가 뭐시기
                    except:
                        pass
            
                    seat_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pointer"))) 
                    time.sleep(1)
                    
                    
                    k = 0
                    for i in seat_buttons:
                            k += 1 
                            msg = f'{i.get_attribute("locynm")}열 {i.get_attribute("locxnm")}석'
                            try:
                                driver.execute_script("arguments[0].click();", i)
                                driver.find_element(By.CLASS_NAME, "selectedOnV2")
                                
                                wait.until(EC.element_to_be_clickable((By.ID, 'btnPaymentOn'))).click() # 예매하기
                                print('\n[info] 좌석 선택 창구에 진입했습니다.')
                                try:
                                    result = driver.switch_to.alert
                                    for i in range(5):
                                        result.accept() 

                                    print('[info] 예매에 실패했습니다. 다시 탐색합니다.')
                                    main()
                                    break
                                
                                except:
                                    print(f'\n[ 좌석 선택 완료 ] \n- 소요시간 : {round(time.time() - try_time,2)}초 \n- 선택좌석 : {msg}') 
                                    break

                            except:
                                print(f'\r[info] 좌석 선택 시도 중 : {k} 회 ({msg})', end='')
                                pass

                    time.sleep(4)

                    a = 0
                    for a in range(600):
                        a += 1
                        print(f'\r약 10분 내로 결제를 완료해야 합니다. ({600-a}초)', end='')
                        time.sleep(1)

                    time.sleep(99999)

main()
