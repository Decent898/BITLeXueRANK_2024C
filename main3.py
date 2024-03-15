from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from hashlib import md5
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import config 

class OnlineCompetitionMonitor:
    def __init__(self):
        self.smtp_server_address = config.smtp_server_address
        self.sender_email_address = config.sender_email_address
        self.smtp_password = config.smtp_password
        self.receiver_email_address = config.receiver_email_address
        self.website_login_url = config.website_login_url
        self.user_account = config.user_account
        self.user_password = config.user_password

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')  
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        
    def login(self):
        self.driver.get(self.website_login_url)
        time.sleep(1)

        login_form_path = '/html/body/div[1]/div[2]/div/section/'
        self.driver.find_element(By.XPATH, login_form_path + 'div[2]/div[1]/div/form/div/div[1]/div[1]/input').send_keys(self.user_account)
        self.driver.find_element(By.XPATH, login_form_path + 'div[2]/div[1]/div/form/div/div[1]/div[2]/input[1]').send_keys(self.user_password)

        time.sleep(0.5)

        self.driver.find_element(By.XPATH, login_form_path + "/div[2]/div[1]/div/form/div/div[3]/a").click()

        time.sleep(2)

    def monitor(self):
        print("------SYSTEM START------")

        temporary_data = [['' for i in range(2)] for j in range(16)]
        while True:
            self.driver.refresh()
            first_prize_problem_path = '/html/body/div[1]/div[3]/div/div/section[2]/aside/section[3]/div/div/table/tbody'
            count = 1
            with open('data.txt', 'r') as file:
                lines = file.readlines()
                last_line = lines[-1]
            [formatted_time, previous_user_name, previous_problem_name] = eval(last_line)

            current_user_name = self.driver.find_element(By.XPATH, first_prize_problem_path + '/tr[' + str(count) + ']/td[1]/a').text
            current_problem_name = self.driver.find_element(By.XPATH, first_prize_problem_path + '/tr[' + str(count) + ']/td[2]').text

            while (previous_problem_name != current_problem_name or previous_user_name != current_user_name) and count < 15:
                current_user_name = self.driver.find_element(By.XPATH, first_prize_problem_path + '/tr[' + str(count) + ']/td[1]/a').text
                current_problem_name = self.driver.find_element(By.XPATH, first_prize_problem_path + '/tr[' + str(count) + ']/td[2]').text

                count += 1

                temporary_data[count][0] = current_user_name
                temporary_data[count][1] = current_problem_name

            for i in range(count - 1, 1, -1):
                [current_user_name, current_problem_name] = temporary_data[i]

                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S')

                with open('data.txt', 'a') as file:
                    file.write("\n" + str([formatted_time, current_user_name, current_problem_name]))

                print(current_user_name, current_problem_name, formatted_time)

                if current_user_name == '杨 宏宇' and previous_problem_name != current_problem_name:
                    self.send_notification(current_user_name, current_problem_name, formatted_time)

            time.sleep(10)

    def send_notification(self, current_user_name, current_problem_name, formatted_time):
        latest_ac_problem_path = '/html/body/div[1]/div[3]/div/div/section[2]/aside/section[3]'
        ac_problem_element = self.driver.find_element(By.XPATH, latest_ac_problem_path)
        timestamp = str(int(time.time()))
        ac_problem_element.screenshot(".\\" + timestamp + "A.png")

        latest_ranking_path = '/html/body/div[1]/div[3]/div/div/section[2]/aside/section[4]/div'
        ranking_element = self.driver.find_element(By.XPATH, latest_ranking_path)
        timestamp = str(int(time.time()))
        ranking_element.screenshot(".\\" + timestamp + "B.png")

        subject = '睿信C语言 ' + current_user_name + ' ' + '已经完成了' + ' ' + current_problem_name + '。'
        content = '2024年春季睿信-C语言程序设计（反卷王提示脚本By DecEric）\n' + '提醒！\n在' + formatted_time + "\n" + current_user_name + ' 已经完成了\n' + ' ' + current_problem_name + '\n目前前十名情况参考附件PNG图片'

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender_email_address
        msg['To'] = self.receiver_email_address

        msg.attach(MIMEText(content, 'plain', 'utf-8'))

        with open(timestamp + "B.png", 'rb') as file:
            img = MIMEImage(file.read())
            img.add_header('Content-Disposition', 'attachment', filename=timestamp + "B.png")
            msg.attach(img)

        smtp = smtplib.SMTP(self.smtp_server_address, 25)
        smtp.login(self.sender_email_address, self.smtp_password)
        smtp.sendmail(self.sender_email_address, self.receiver_email_address, msg.as_string())
        smtp.quit()

        print("发送成功")

if __name__ == "__main__":
    monitor = OnlineCompetitionMonitor()
    monitor.login()
    monitor.monitor()