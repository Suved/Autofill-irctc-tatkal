#!/usr/bin/python2.7
import time
import pickle
import os.path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

class data:
 def __init__(self):
   self.n=0
   self.fom=""
   self.to=""
   self.date=""
   self.train=""
   self.clas="SL"
   self.p=[]
   self.bank=""
   self.cardno=""
   self.month=""
   self.year=""
   self.cardname=""
   self.pin=""
 
 def get_data(self):
   self.fom=raw_input('Enter From Station(Station_name JN - code):')
   self.to=raw_input('Enter to Station(Station_name JN - code):')
   self.date=raw_input('Enter journey date(DD-MM-YYYY):')
   self.train=raw_input('Enter train no:')
   self.clas=raw_input('Enter class(2A,3A,SL):')
   self.n=int(input("Enter no of passenger(max-5):"))
   self.p=[[list() for i in range(3)] for i in range(self.n)]
   for i in range(self.n):
        self.p[i][0]=raw_input(("Enter Passenger %d name:" % (i)))
        self.p[i][1]=raw_input("Enter age:")
        self.p[i][2]=raw_input("Enter sex:")
   self.bank=raw_input("Enter no for bank\n1.HDFC\n2.SBI\nEnter choice:")
   self.cardno=raw_input('Enter card no:')
   self.month=raw_input('Enter expiry month(M):')
   self.year=raw_input('Enter expiry year(YYYY):')
   self.cardname=raw_input('Enter card holder name:')
   self.pin=raw_input('Enter your pin:')

def login():
 driver=webdriver.Firefox()
 driver.get('http://irctc.co.in')
 driver.find_element_by_id('usernameId').send_keys('ADD_USERNAME_HERE')
 driver.find_element_by_name('j_password').send_keys('ADD_PASSWORD_HERE')
 time.sleep(10)
 driver.find_element_by_name('submit').click()
 return driver

def plan(driver,d):
 driver.find_element_by_id('jpform:fromStation').send_keys(d.fom)
 driver.find_element_by_id('jpform:toStation').send_keys(d.to)
 driver.find_element_by_id('jpform:journeyDateInputDate').send_keys(d.date)
 driver.find_element_by_id('jpform:jpsubmit').click()
 if d.train=="12113" or d.train=="12114":x=0
 elif d.clas=="SL": x=2
 elif d.clas=="3A": x=1
 elif d.clas=="2A": x=0
 

 driver.find_element_by_css_selector("input[type='radio'][value='CK']").click()
 
 select_train="cllink-"+d.train+"-"+d.clas+"-"+str(x)

 driver.find_element_by_id(select_train).click()
 y=d.train+"-"+d.clas+"-CK-0"
 

 WebDriverWait(driver,(60*6)).until(EC.title_is('Book Ticket - Passengers Information'))
 
 try:

  for i in range(d.n):
   driver.find_element_by_xpath('//*[contains(@id,"addPassengerForm:psdetail:%d:p")]' % (i)).send_keys(d.p[i][0])
   driver.find_element_by_xpath('//*[contains(@id,"addPassengerForm:psdetail:%d:psgnAge")]' % (i)).send_keys(d.p[i][1])  
   driver.find_element_by_xpath('//*[@id="addPassengerForm:psdetail:%d:psgnGender"]/option[text()="%s"]' % (i,d.p[i][2])).click()
  driver.find_element_by_id('addPassengerForm:autoUpgrade').click()
  driver.find_element_by_id('addPassengerForm:onlyConfirmBerths').click()
  WebDriverWait(driver,120).until(EC.title_is('Book Ticket - Journey Summary'))


 except:
       print('Errorrrrrrrr....')
  
 

 if(d.bank=="1"):
  driver.find_element_by_xpath('//*[@id="PREFERRED"][@value="57"]').click()
  driver.find_element_by_id('validate').click()
  hdfc(driver,d)
 else:
  driver.find_element_by_xpath('//*[@id="PREFERRED"][@value="3"]').click()
  driver.find_element_by_id('validate').click()
  sbi(driver,d)

def sbi(driver,d):
 WebDriverWait(driver,120).until(EC.title_is('Payment Interface'))
 driver.find_element_by_id('debitCardNumber').send_keys(d.cardno)
 driver.find_element_by_xpath('//*[@id="debiMonth"]/option[@value="%s"]' % (d.month)).click()
 driver.find_element_by_xpath('//*[@id="debiYear"]/option[@value="%s"]' % (d.year)).click()
 driver.find_element_by_id('debitCardholderName').send_keys(d.cardname)
 driver.find_element_by_id('cardPin').send_keys(d.pin)

def hdfc(driver,d):
 WebDriverWait(driver,120).until(EC.title_is('Portal Payment'))

 driver.find_element_by_id('Ecom_Payment_Card_Number_Debit').send_keys(d.cardno)
 driver.find_element_by_xpath('//*[@id="Ecom_Payment_Card_ExpDate_Month_Debit"]/option[@value="%s"]' % (d.month)).click()
 driver.find_element_by_xpath('//*[@id="Ecom_Payment_Card_ExpDate_Year_Debit"]/option[text()="%s"]' % (d.year)).click()
 driver.find_element_by_id('Ecom_Payment_Card_Name_Debit').send_keys(d.cardname)
 driver.find_element_by_id('normalPinID').send_keys(d.pin)

def main():
 ######################MENU####################
 while 1:
  ch=int(input("#########MENU#########\n1.Plan journey\n2.Use old journey details\n3.Book ticket\n4.Exit\nEnter your choice:"))
  if ch==1:
           d=data()
           d.get_data()
           with open('db.pk','wb') as f:
               pickle.dump(d,f)
  elif ch==2:
           if os.path.isfile('db.pk'):
            with open('db.pk','rb')as f:
               d=pickle.load(f)
            print(d.fom+"\n"+d.to+"\n"+d.date)
           else: print('No Previous record found')
  elif ch==3:
          try:
           w=login()
           plan(w,d)
           d.quit()
          except: print('-------------ERROR-------------')
  else:
        exit()

main()
