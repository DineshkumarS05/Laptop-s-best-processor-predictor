from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import re
link='https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&page=1'

laptopprocessor=[]
laptoprating=[]
laptopprice=[]
laptopactualPrice=[]
laptopRAM=[]
laptopROM=[]
laptopcompany=[]
nclass=[]
pages=[]
for j in range(1,5):
    driver=webdriver.Chrome("/Users/dineshkumar/Downloads/chromedriver")
    
    driver.get(link)
    content=driver.page_source
    cont=bs(content)
    for i in cont.find_all('div',attrs={'class':'_1-2Iqu row'}):
        specifications=i.find('div',attrs={'class':'_3ULzGw'})
        company=i.find('div',attrs={'class':'_3wU53n'})
        rating=i.find('div',attrs={'class':'hGSR34'})
        price=i.find('div',attrs={'class':'_1vC4OE _2rQ-NK'})
        actualPrice=i.find('div',attrs={'class':'_3auQ3N _2GcJzG'})
        
        specificationss=specifications.find_all('li',attrs={'class':'tVe95H'})
        try:
            for i in specificationss:
                RAM1=re.findall(r'RAM',''.join(i))
                try:
                    RAM1[0]
                    RA=''.join(i)
                    RA=RA.split()
                    RAM=int(RA[0])
                    break
                except IndexError:
                    pass                
        except:
            RAM=None
        try:
            for i in specificationss:
                ROM1=re.findall(r'HDD|SSD',''.join(i))
                try:
                    ROM1[0]
                    RO=''.join(i)
                    RO=re.findall(r'\d+',RO)
                    RO=''.join(RO)
                    RO=int(RO)
                    ROM=RO
                    break
                except IndexError:
                    pass  
        except:
            ROM=None
        try:
            for i in specificationss:
                processor1=re.findall(r'Processor',''.join(i))
                try:
                    processor1[0]
                    processor=''.join(i)
                    break
                except IndexError:
                    pass
        except:
            processor=None
        try:    
            rating=rating.text
            rating=re.findall(r'\d.\d|\d+',rating)
            rating=float(rating[0])
        except:
            rating=None
        try:
            price=price.text
            price=re.findall(r'\d+',price)
            price=''.join(price)
            price=float(price)
        except:
            price=None
        try:
            actualPrice=actualPrice.text
            actualPrice=re.findall(r'\d+',actualPrice)
            actualPrice=''.join(actualPrice)
            actualPrice=float(actualPrice)
        except:
            actualPrice=None
        try:
            company=company.text.split()
            companyy=company[0]
        except:
            companyy=None
        laptopRAM.append(RAM)
        laptopROM.append(ROM)
        laptoprating.append(rating)
        laptopprocessor.append(processor)
        laptopprice.append(price)
        laptopactualPrice.append(actualPrice)
        laptopcompany.append(companyy)
    for i in cont.find_all('div',attrs={'class':'_2zg3yZ'}):
        possible_links = i.find_all('a')
        for links in possible_links:
            if links.has_attr('href'):
                pages.append(links.attrs['href'])
                link="https://www.flipkart.com"+pages[j+1]


x=pd.DataFrame({'Company':laptopcompany,'RAM':laptopRAM,'ROM':laptopROM,'Processor':laptopprocessor,'Price':laptopprice,'Actual Price':laptopactualPrice,'Ratings':laptoprating})
x=x[['Company','RAM','ROM','Actual Price', 'Price', 'Ratings']]
import numpy as np
x=np.array(x)
y=np.array(laptopprocessor)
#for i in range(len(y)):
#    if(y[i]==None):
#        y[i]=3
from sklearn.preprocessing import LabelEncoder
lbl=LabelEncoder()
x[:,0]=lbl.fit_transform(x[:,0])
y=lbl.fit_transform(y)

from sklearn.impute import SimpleImputer
imp=SimpleImputer()
x=imp.fit_transform(x)

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2)
ytrain=ytrain.astype('int')
print('Brain started getting train from past experiences')

from sklearn.ensemble import RandomForestRegressor
lr=RandomForestRegressor(n_estimators=1000)
lr.fit(xtrain,ytrain)
ypred=lr.predict(xtest)

xaxis=np.linspace(1,len(ytest),len(ytest))
import matplotlib.pyplot as plt
plt.xlabel('Time/series')
plt.ylabel('Processor')
plt.plot(xaxis,ypred,color='blue',label='Predicted')
plt.plot(xaxis,ytest,color='red',label='Actual')
plt.legend()
plt.show()

print("Congratulations brain is trained for future predictions. Press any key for entering GUI mode")
timepass=input()
print("Please write the company name of laptop in integer format as given in the list.")
comp=np.array(laptopcompany)
comp=np.unique(comp)
numb=np.unique(x[:,0])
for ii in range(len(comp)):
    print(numb[ii],' : ',comp[ii])
from tkinter import *
window=Tk()
window.title('Processor finder of Laptop')
window.geometry('350x350')
lbl0=Label(window,text='Please write only integer/floating value')
lbl0.grid(row=0,column=0)   
lbl=Label(window,text='Company')
lbl.grid(row=1,column=0)   
lbl1=Label(window,text='RAM')
lbl1.grid(row=2,column=0)
lbl2=Label(window,text='ROM')
lbl2.grid(row=3,column=0)
lbl3=Label(window,text='Actual Price')
lbl3.grid(row=4,column=0)
lbl4=Label(window,text='Price')
lbl4.grid(row=5,column=0)
lbl5=Label(window,text='Ratings')
lbl5.grid(row=6,column=0)

ent=Entry(window,width=10)
ent.grid(row=1,column=1)
ent1=Entry(window,width=10)
ent1.grid(row=2,column=1)   
ent2=Entry(window,width=10)
ent2.grid(row=3,column=1)   
ent3=Entry(window,width=10)
ent3.grid(row=4,column=1)   
ent4=Entry(window,width=10)
ent4.grid(row=5,column=1)   
ent5=Entry(window,width=10)
ent5.grid(row=6,column=1)   

proce=np.unique(laptopprocessor)
num=np.unique(y)

def clicked():
    count=0
    value1=ent.get()
    value2=ent1.get()
    value3=ent2.get()
    value4=ent3.get()
    value5=ent4.get()
    value6=ent5.get()
    try:
        value1=int(value1)
        value2=int(value2)
        value3=int(value3)
        value4=int(value4)
        value5=int(value5)
        value6=float(value6)
    except ValueError:
        lbl3=Label(window,text="Values are not in requested format")
        lbl3.grid(row=5,column=0)
        count=1
    if(count==0):
        win=Tk()
        window.destroy()
        win.geometry('350x350')
        lbl2=Label(win,text='The processor in demand is:')
        lbl2.grid(row=0,column=0)
        res=lr.predict([[value1,value2,value3,value4,value5,value6]])
        res=int(res)
        finalres=proce[res]
        lbl2=Label(win,text=finalres)
        lbl2.grid(row=1,column=0)
btn=Button(window,text='Submit',command=clicked)
btn.grid(row=9,column=1)
window.mainloop()
