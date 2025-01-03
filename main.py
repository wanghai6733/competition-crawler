from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import csv


# 账号密码
username = "*********"
password = "*********"

# 初始化浏览器
options = Options()
options.add_argument('--headless')  # 启用 headless 模式
options.add_argument('--disable-gpu')  # 禁用 GPU 加速（避免某些图形问题）
options.add_argument('--no-sandbox')  # 提高性能，防止某些操作系统错误

driver = webdriver.Edge(options=options)
driver.implicitly_wait(8)

# 打开目标网站
driver.get("https://student.dhu.edu.cn/xg_dhu/identity/index.action;jsessionid=B4BEAAAD6877BC16E1EDA0C3551E39A4.tomcatcs")

# 输入账号密码登录网站
element = driver.find_element(By.ID, 'username')
element.send_keys(username)
element = driver.find_element(By.ID, 'password')
element.send_keys(password)
element = driver.find_element(By.XPATH,"//button")
# print(element)
element.click()

# 打开代办
driver.get("https://student.dhu.edu.cn/xg_dhu/identity/index.action?groupid=9f411d0f2ac24439851dc8a7cdd12b7f&url=http://student.dhu.edu.cn:80/xg_dhu//s/biz/gxXnjxj/dx/tab/input?wid=ea7cf423bfb4462bb6119b6376f1e9fe")


data = []

driver.switch_to.frame('iframe1124123')
driver.maximize_window()
# 日期选择
select = Select(driver.find_element(By.XPATH,"//*[@id='nd']"))
dates = ["2024-2025学年","2023-2024学年","2022-2023学年"]
for date in dates:
    select.select_by_visible_text(date)
    element = driver.find_element(By.XPATH,"//button[@id='doSearch']")
    element.click()
    time.sleep(3)
    element = driver.find_element(By.XPATH,"//a[@data-current-page-no='1']")
    element.click()
    time.sleep(3)

    # 按页读取
    while True:
        time.sleep(2)
        elements = driver.find_elements(By.XPATH,"//tbody/tr")
        print(len(elements))
        for ele in elements:
            row = []
            # print(ele.get_attribute('outerHTML'))
            
            

            # 跳转查询
            x = ele.find_element(By.XPATH,"./td[3]/a")
            x.click()
            time.sleep(1)

            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH,"//iframe[@class='J_iframe'][3]"))

            x = driver.find_element(By.XPATH,"//*[@id='jxmc']")
            row.append(x.get_attribute("value"))
            
            x = driver.find_element(By.XPATH,"//*[@id='fdyyj']")
            row.append(x.text)
            x = driver.find_element(By.XPATH,"//*[@id='yxyj']")
            row.append(x.text)
            x = driver.find_element(By.XPATH,"//*[@id='xxyj']")
            row.append(x.text)

            driver.switch_to.default_content()
            x = driver.find_element(By.XPATH,"//a[@title='210110419']/i")
            x.click()
            time.sleep(2)

            driver.switch_to.frame('iframe1124123')

            # 表格查询
            x = ele.find_element(By.XPATH,"./td[2]")
            row.append(x.text)
            x = ele.find_element(By.XPATH,"./td[last()-4]")
            row.append(x.text)
            x = ele.find_element(By.XPATH,"./td[last()-3]")
            row.append(x.text)
            x = ele.find_element(By.XPATH,"./td[last()-2]")
            row.append(x.text) 
            x = ele.find_element(By.XPATH,"./td[last()-1]")
            row.append(x.text) 
            x = ele.find_element(By.XPATH,"./td[last()]")
            row.append(x.text) 
            data.append(row)
            print(row)

        
        next = driver.find_elements(By.XPATH,"//li[@class='next']/a/i[@class='fa fa-angle-right']")
        if(len(next) == 0):
            break
        next = next[0]
        next.click()
            


print(data)
with open("data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # 写入数据
    writer.writerows(data)

print("数据已成功保存为data.csv")
input("回车退出")
driver.quit()
