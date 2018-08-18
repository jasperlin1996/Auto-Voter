from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import os
import sys
import time
import tkinter as tk
import threading

window = tk.Tk()
window.title('Auto Voter v0.2 by JasperLin')
window.geometry('500x200')
window.minsize(500,300)
window.maxsize(500,300)
url = "http://www.trendingmusicawards.com/2018/06/best-fan-army.html"

driver = None
isDone = 0
statusText = tk.StringVar()
statusColor = tk.StringVar()
def doSomeShit():
    try:
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")

        global driver, isDone, statusText, statusColor
        statusText.set('Status: Auto voting...')
        statusColor.set('green')
        tk.Label(textvariable = statusText, fg = statusColor.get()).place(x = 100, y = 180)
        poll = 0
        isDone = 0
        counter = 0
        driver = webdriver.Chrome(executable_path = os.getcwd()+"\\chromedriver.exe", chrome_options = options)
        driver.set_window_position(-10000,0)
        driver.get(url)
        
        while True:
            driver.find_element_by_xpath('//*[@id="PDI_answer46248899"]').click()
            driver.find_element_by_xpath('//*[@id="pd-vote-button10078773"]').click()
            time.sleep(1)
            try:
                temp = int(driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[3]/span').text.replace(",",""))
            except Exception as e:
                if type(e) == NoSuchElementException:
                    print(e)
                    time.sleep(1)
                    temp = int(driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[3]/span').text.replace(",",""))
            if poll < temp:
                counter+=1
                poll = temp
                updateData(counter, temp)
            driver.refresh()
            if isDone == 1:
                break
        statusText.set('Status: Stop')
        statusColor.set('red')
        tk.Label(textvariable = statusText, fg = statusColor.get()).place(x = 100, y = 180)
        driver.quit()
    except Exception as e:
        driver.quit()
        sys.exit("sorry, goodbye!")

def updateData(uVeVoted, totalVotes):
    global driver
    team_1_name = driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[1]/label/span[1]').text
    team_1_percent = driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[1]/label/span[2]/span[1]').text
    team_1_votes = driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[1]/label/span[2]/span[2]').text
    team_2_name = driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[2]/label/span[1]').text
    team_2_percent = driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[2]/label/span[2]/span[1]').text
    team_2_votes = driver.find_element_by_xpath('//*[@id="PDI_container10078773"]/div/div/div/div/div[2]/div[2]/label/span[2]/span[2]').text
    tk.Label(window, text = team_1_name).place(x = 100, y = 90)
    tk.Label(window, text = team_2_name).place(x = 100, y = 120)
    tk.Label(window, text = team_1_percent).place(x = 200, y = 90)
    tk.Label(window, text = team_2_percent).place(x = 200, y = 120)
    tk.Label(window, text = team_1_votes).place(x = 300, y = 90)
    tk.Label(window, text = team_2_votes).place(x = 300, y = 120)
    tk.Label(window, text = "Your contribution: "+str(uVeVoted)).place(x = 100, y = 150)
    tk.Label(window, text = "Total Votes: "+str(totalVotes)).place(x = 300, y = 150)

def stopThatShit():
    global isDone
    isDone = 1

def thread():
    thread_1 = threading.Thread(target = doSomeShit, name = "T1")
    thread_1.start()

def init():
    tk.Label(window, text = 'Auto Voter v0.2').place(x = 215, y = 30)
    tk.Label(window, text = 'Voting URL: '+url).place(x = 30, y = 50)
    bStart = tk.Button(window, text = 'Start Voting', width = 15, height = 2, command = thread)
    bStart.place(x = 100, y = 220)
    bStop = tk.Button(window, text = 'Stop Voting', width = 15, height = 2, command = stopThatShit)
    bStop.place(x = 300, y = 220)
    
    window.mainloop()

init()
