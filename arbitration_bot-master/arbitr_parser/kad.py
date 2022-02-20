import time
import arbitr_parser.case_numbers as case_numbers
import os
from pathlib import Path
from datetime import datetime

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth

class DriverScrapping:
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        #chrome_options.add_argument("--js-flags=--noexpose_wasm")
        path_to_driver = Path("C:/Users/Admin/Desktop/arbitration_bot/arbitr_parser/chromedriver.exe").resolve()
        s = Service(str(path_to_driver))
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def checkexistsbypath(self, path):
        try:
            self.driver.find_element(By.XPATH, path)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True

    def actionchains(self, element):
        action = ActionChains(self.driver)
        return action.move_to_element(element).click(element).perform()

    def switchtowindow(self, i):
        window_after = self.driver.window_handles[i]
        self.driver.switch_to.window(window_after)


    def signin(self):
        self.driver.get('https://ras.arbitr.ru')
        time.sleep(1)
        # decision_bank = self.driver.find_element(By.XPATH, '//*[@id="b-header"]/tbody/tr/td[2]/div/table/tbody/tr/td[3]/a')
        # self.actionchains(decision_bank)
        check_work = self.checkexistsbypath('//*[@id="js"]/div[13]/div[2]/div/div/div/div')
        if check_work:
            closecheckwork = self.driver.find_element(By.XPATH, '//*[@id="js"]/div[13]/div[2]/div/div/div/div/a[1]')
            self.actionchains(closecheckwork)
        field_court = self.driver.find_element(By.XPATH, '//*[@id="caseCourt"]/span/label/input')
        field_court.send_keys('АС Оренбургской области')
        search_button = self.driver.find_element(By.XPATH, '//*[@id="b-form-submit"]/div/button')
        self.actionchains(search_button)
        self.driver.find_element(By.XPATH,'//*[@id="sug-dates"]/label[1]').send_keys("20122021")
        self.actionchains(search_button)
        self.driver.find_element(By.XPATH, '//*[@id="sug-dates"]/label[2]').send_keys("20122021")
        self.actionchains(search_button)

    def search(self, type_of_case):
        time.sleep(2)
        field_type = self.driver.find_element(By.XPATH, '//*[@id="caseType"]/span/label/input')
        field_type.clear()
        field_type.send_keys(type_of_case)
        search_button = self.driver.find_element(By.XPATH, '//*[@id="b-form-submit"]/div/button')
        self.actionchains(search_button)
        time.sleep(2)

    def solve_problem(self, count2):
        self.driver.close()
        self.switchtowindow(0)
        self.driver.window_handles.pop()
        if count2==0 :
            last_page = self.driver.find_element(By.XPATH, '//*[@id="pages"]/li[' + str(count2 + 3) + ']/a')
        else:
            last_page = self.driver.find_element(By.XPATH, '//*[@id="pages"]/li[' + str(count2 + 1) + ']/a')
        self.actionchains(last_page)
        time.sleep(5)
        now_page = self.driver.find_element(By.XPATH, '//*[@id="pages"]/li[' + str(count2 + 2) + ']/a')
        self.actionchains(now_page)
        time.sleep(5)

    def pdf_name(self, num):
        s1 = '//*[@id="chrono_list_content"]/div[2]/div/div[' + str(num + 1) + ']/div[2]/h2/a/span[2]'
        # // *[ @ id = "chrono_list_content"] / div[2] / div / div[8] / div[2] / h2 / a / span[2]
        s2 = '//*[@id="chrono_list_content"]/div[2]/div/div[' + str(num + 1) + ']/div[2]/h2/a/span'

        if self.checkexistsbypath(s1) == False:
            s1 = s2
        pdf_file = self.driver.find_element(By.XPATH, s1)
        name_of_pdf_file = pdf_file.text
        return [name_of_pdf_file, pdf_file]



    def one_page_scrap(self, casename):
        output = []
        print(casename.text)
        time.sleep(2)
        right_name_of_pdf_file = ["Принять к производству", "Принять к рассмотрению", "О принятии к рассмотрен",
                                  "О принятии к производс", "Рассмотреть дело по об", "Привлечь к участию в д"]
        self.actionchains(casename)
        time.sleep(5)
        self.switchtowindow(-1)

        find_el = self.driver.find_elements(By.CLASS_NAME, 'l-col')
        if not self.checkexistsbypath('//*[@id="b-case-header"]/ul[2]/li[1]'):
            return False
        if len(find_el) == 1:
            s = '//*[@id="chrono_list_content"]/div[1]/div/div[2]'
            plus_bottom = self.driver.find_element(By.XPATH, s)
            self.actionchains(plus_bottom)
            time.sleep(1)
            find_casetype = self.driver.find_elements(By.CLASS_NAME, 'case-type')
            amount_of_opred = 0
            num = 0
            end = False
            for i in range(len(find_casetype)):
                print(find_casetype[i].text)
                if find_casetype[i].text == "Определение":
                    name_of_opred = self.pdf_name(i)[0]
                    print(name_of_opred)
                    if name_of_opred[0:22]!="Оставить без движения " or name_of_opred[0:22]!="Продлить срок оставлен":
                        amount_of_opred += 1
                        num = i
                if find_casetype[i].text == "Решение" or find_casetype[i].text == "Решение (резолютивная часть)":
                    end=True
                    break
            if amount_of_opred == 1 and (len(find_casetype) == 2 or len(find_casetype) == 3 or len(find_casetype) == 4) and end==False:
                name_of_pdf_file, pdf_file=self.pdf_name(num)
                print(name_of_pdf_file)
                time.sleep(5)
                price_path = '//*[@id="chrono_list_content"]/div[2]/div/div[' + str(
                    len(find_casetype)) + ']/div[2]/span'
                price = self.driver.find_element(By.XPATH, price_path)
                price_output = price.text
                price_output_with_point = ''.join([ch if ch != ',' else '.' for ch in price_output])
                price_output_with_point=price_output_with_point[::-1]
                price_output_with_point=price_output_with_point.split(' ')[0]
                price_output_with_point=price_output_with_point[::-1]
                print(price_output_with_point)
                for i in range(len(right_name_of_pdf_file)):
                    if name_of_pdf_file[0:22] == right_name_of_pdf_file[i] and \
                            float(price_output_with_point) >= float(1000000):
                        output.append(self.driver.current_url)
                        self.actionchains(pdf_file)
                        self.switchtowindow(-1)
                        time.sleep(5)
                        output.append(self.driver.current_url)
                        self.driver.close()
                        self.switchtowindow(1)
                        self.driver.window_handles.pop()
        time.sleep(3)
        self.driver.close()
        self.switchtowindow(0)
        self.driver.window_handles.pop()
        # print(output)
        return output

    def main_page_scraping(self, current_datetime):
        nowdatetime = []
        casename = []
        date = self.driver.find_elements(By.CLASS_NAME, 'date')
        date = [date[i].text for i in range(len(date) - 1)]
        if date[0] != current_datetime:
            return casename
        nowdatetime += [date[i] for i in range(len(date)) if date[0] == date[i]]
        for link in range(len(nowdatetime)):
            casename.append(
                self.driver.find_element(By.XPATH, '//*[@id="b-cases"]/li[' + str(link + 1) + ']/div[2]/div[1]/a'))
        return casename


    def page_click(self, count2):
        pagelink = self.driver.find_element(By.XPATH, '//*[@id="pages"]/li[' + str(count2 + 2) + ']/a')
        self.actionchains(pagelink)

    def saving_case_number(self, casename):
        case_numbers.numbers.add(casename.text)
        date = datetime.now()
        day = date.day
        time = date.time()
        time = str(time)[:5]
        hour = str(time)[:2]
        minute = str(time)[3:5]
        # print(hour, minute)
        if day % 3 == 0 and int(hour) == 3 and int(minute) > 0 and int(minute) <= 30:
            case_numbers.numbers.clear()
        # print(case_numbers.numbers)

    def check_casenumber(self, casename):
        casenumber = case_numbers.numbers
        for el in casenumber:
            if el == casename:
                return True
        return False

    def all_types(self):
        document_link = []
        try:
            self.signin()
            type_of_case = [ 'о несостоятельности (банкротстве) организаций и граждан',
                            'экономические споры по гражданским правоотношениям']
            date = datetime.now()
            # current_datetime = str(date.day-15) + '.' + str(date.month) + '.' + str(date.year)
            current_datetime = '20' + '.' + '12' + '.' + '2021'
            # print(current_datetime)

            time.sleep(2)
            k = 0
            for i in range(len(type_of_case)):
                count = 0
                count2 = 0
                self.search(type_of_case[i])
                time.sleep(3)
                # zaver = self.driver.find_element(By.XPATH, '//*[@id="b-container"]/div/div[2]/dl/div/div[1]/button[2]')
                # self.actionchains(zaver)
                # time.sleep(2)
                # zaver1 = self.driver.find_element(By.CSS_SELECTOR,
                #                                   '#js > div.ui-multiselect-menu.ui-widget.ui-widget-content.ui-corner-all.ui-multiselect-single > ul > li:nth-child(3) > label > span')
                # self.actionchains(zaver1)
                # time.sleep(2)

                while True:
                    if count % 11 == 0 and count != 0:
                        if count > 20:
                            count2 = count2 - 12
                        else:
                            count2 = count - 8
                    case = self.main_page_scraping(current_datetime)
                    # print(case)
                    for j in range(len(case)):
                        if not self.check_casenumber(case[j].text):
                            link = self.one_page_scrap(case[j])
                            if link == False:
                                self.solve_problem(count2)
                                k = 1
                                break
                            else:
                                k = 0
                                self.saving_case_number(case[j])
                                if len(link) > 0:
                                    document_link.append(link)
                    if len(case) == 25 and k == 0:
                        count += 1
                        count2 += 1
                        self.page_click(count2)
                        time.sleep(5)
                    elif len(case) != 25:
                        break
            return document_link
        except:
            return document_link
