import discord_webhook
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import schedule
import sqlite3
from os import path
import os.path
import re
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from dotenv import load_dotenv  # for python-dotenv method
load_dotenv()

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_argument("--use-fake-ui-for-media-stream")
opt.add_argument("use-fake-ui-for-media-stream")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

# driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
driver = None
URL = "https://cuchd.blackboard.com"

# create .env file and store your email and password there
email = os.environ.get('EMAIL')
passwd = os.environ.get('PASSWORD')


def createDB():
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    # Create table
    c.execute(
        '''CREATE TABLE IF NOT EXISTS timetable(class text, start_time text, end_time text, day text)''')
    conn.commit()
    conn.close()
    print("Created timetable Database")


def validate_input(regex, inp):
    if not re.match(regex, inp):
        return False
    return True


def validate_day(inp):
    days = ["monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"]

    if inp.lower() in days:
        return True
    else:
        return False


def add_timetable():
    if(not(path.exists("timetable.db"))):
        createDB()
    op = int(input("1. Add class\n2. Done adding\nEnter option : "))
    while(op == 1):
        name = input("Enter class name : ")
        start_time = input(
            "Enter class start time in 24 hour format: (HH:MM) ")
        while not(validate_input("\d\d:\d\d", start_time)):
            print("Invalid input, try again")
            start_time = input(
                "Enter class start time in 24 hour format: (HH:MM) ")

        end_time = input("Enter class end time in 24 hour format: (HH:MM) ")
        while not(validate_input("\d\d:\d\d", end_time)):
            print("Invalid input, try again")
            end_time = input(
                "Enter class end time in 24 hour format: (HH:MM) ")

        day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
        while not(validate_day(day.strip())):
            print("Invalid input, try again")
            end_time = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")

        conn = sqlite3.connect('timetable.db')
        c = conn.cursor()

        # Insert a row of data
        c.execute(
        '''CREATE TABLE IF NOT EXISTS timetable(class text, start_time text, end_time text, day text)''')
        c.execute("INSERT INTO timetable VALUES ('%s','%s','%s','%s')" %
                  (name, start_time, end_time, day))

        conn.commit()
        conn.close()

        print("Class added to database\n")

        op = int(input("1. Add class\n2. Done adding\nEnter option : "))


def view_timetable():
    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS timetable(class text, start_time text, end_time text, day text)''')
    for row in c.execute('SELECT * FROM timetable'):
        print(row)
    conn.close()


def login():
    global driver
    # login required user_id
    cookiebtn = driver.find_element_by_xpath('//*[@id="agree_button"]')
    cookiebtn.click()
    time.sleep(1)
    print("logging in")
    emailField = driver.find_element_by_xpath('//*[@id="user_id"]')
    emailField.click()
    emailField.send_keys(email)
    passwordField = driver.find_element_by_xpath('//*[@id="password"]')
    passwordField.click()
    passwordField.send_keys(passwd)
    driver.find_element_by_xpath(
        '//*[@id="entry-login"]').click()  # Sign in button
    time.sleep(5)
    return driver


def joinclass(class_name, start_time, end_time):
    #for localtest
    start_browser()

    #using db  
    # global driver
   
    try_time = int(start_time.split(":")[1]) + 15
    try_time = start_time.split(":")[0] + ":" + str(try_time)

    classSearch = driver.find_element_by_xpath(
        '//*[@id="main-content-inner"]/div/div[1]/div[1]/div/div/div[1]/div/header/bb-search-box/div/input')
    classSearch.click()
    classSearch.send_keys(class_name)
    time.sleep(3)
    classbtn = driver.find_element_by_partial_link_text(class_name)
    classbtn.click()
    time.sleep(5)
    try:
        sessionlist = driver.find_element_by_id('sessions-list')
        items = sessionlist.find_elements_by_tag_name("li")
        print ('Total no. of session under this course: ' + str(len(items)))
        time.sleep(2)
        try:
            driver.execute_script("""
            var session= document.getElementById('sessions-list');
            var lists = session.getElementsByTagName('li');
            for (let index = 0; index < lists.length; index++) {
                if(lists[index].innerText.trim() === "Course Room"){
                    lists[index].getElementsByTagName('a')[0].click();
                }
            }
            """)
            # time.sleep(10)
            driver.switch_to_window(driver.window_handles[1])
            
            n=1
            while n<2:
                try:
                    #  options
                    # time.sleep(5)
                    # driver.find_element_by_css_selector('#techcheck-modal > div.modal-content-wrap.techcheck-audio-wrapper > div > button').click()
                    # driver.find_element_by_css_selector('#announcement-modal-page-wrap > button').click()
                    driver.execute_script("""
                        localStorage.setItem("techcheck.status", "completed");
                        localStorage.setItem("techcheck.initial-techcheck", "completed");
                        localStorage.setItem("ftue.announcement.introduction", true);
                        localStorage.setItem("apollo.hidesrnotification", true);
                        localStorage.setItem("new.tutorials-menu-button.private-chat", true);
                    """)
                    time.sleep(2)
                    driver.execute_script("""
                        document.querySelector('#techcheck-modal > div.modal-content-wrap.techcheck-audio-wrapper > div > button').click();
                    """)
                    driver.execute_script("""
                        document.querySelector('#announcement-modal-page-wrap > button').click();
                    """)
                    driver.execute_script("""
                        document.querySelector("#techcheck-modal > div.modal-content-wrap.techcheck-video-wrapper > div > button").click();
                    """)
                    print(driver.find_element_by_xpath('//*[@id="side-panel-open"]').is_displayed())
                    print("ok")
                    n=2
                except:
                    driver.execute_script("""
                        localStorage.setItem("techcheck.status", "completed");
                        localStorage.setItem("techcheck.initial-techcheck", "completed");
                        localStorage.setItem("ftue.announcement.introduction", true);
                        localStorage.setItem("apollo.hidesrnotification", true);
                        localStorage.setItem("new.tutorials-menu-button.private-chat", true);
                    """)
                    print("not ok")
                    time.sleep(2)

        except:
            time.sleep(1)

    except:
        # join button not found
        # refresh every minute until found
        k = 1
        while(k <= 2):
            print("Join button not found, trying again")
            time.sleep(10)
            driver.refresh()
            joinclass(class_name, start_time, end_time)
            # schedule.every(1).minutes.do(joinclass,class_name,start_time,end_time)
            k += 1
        print("Seems like there is no class today.")
        discord_webhook.send_msg(
            class_name=class_name, status="noclass", start_time=start_time, end_time=end_time)

    discord_webhook.send_msg(
        class_name=class_name, status="joined", start_time=start_time, end_time=end_time)

    # now schedule leaving class
    tmp = "%H:%M"

    class_running_time = datetime.strptime(
        end_time, tmp) - datetime.strptime(start_time, tmp)

    time.sleep(class_running_time.seconds)
    driver.close()
    print("Class left")
    discord_webhook.send_msg(
        class_name=class_name, status="left", start_time=start_time, end_time=end_time)


def start_browser():

    global driver
    driver = webdriver.Chrome(options=opt, service_log_path='NUL')

    driver.get(URL)

    WebDriverWait(driver, 10000).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'body')))

    if("cuchd.blackboard.com" in driver.current_url):
        login()


def sched():

    conn = sqlite3.connect('timetable.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM timetable'):
        # schedule all classes
        name = row[0]
        start_time = row[1]
        end_time = row[2]
        day = row[3]

        

        if day.lower() == "monday":
            schedule.every().monday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
        if day.lower() == "tuesday":
            print('day hai: ', day)
            schedule.every().tuesday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
        if day.lower() == "wednesday":
            schedule.every().wednesday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
        if day.lower() == "thursday":
            schedule.every().thursday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
        if day.lower() == "friday":
            schedule.every().friday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
        if day.lower() == "saturday":
            schedule.every().saturday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
        if day.lower() == "sunday":
            schedule.every().sunday.at(start_time).do(
                joinclass, name, start_time, end_time)
            print("Scheduled class '%s' on %s at %s" % (name, day, start_time))

    # Start browser
    start_browser()
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        all_jobs = schedule.get_jobs()
        # print(all_jobs)
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
       op = int(
        input(("1. Modify Timetable\n2. View Timetable\n3. Start Bot\nEnter option : ")))

       if(op == 1):
        add_timetable()
       if(op == 2):
        view_timetable()
       if(op == 3):
        # sched()
        joinclass("PROJECT-I", "23:52", "20:50")
