import tkinter as tk
from tkinter import  StringVar,PhotoImage,Frame,messagebox,ttk,Label
import requests,os
import pandas as pd
api_key = "dda1e008bab8ec360a35189a0e7445b7"  # Replace this with your actual API key
cities_data=pd.read_csv('cities.csv')
class Weather:
    def __init__(self,root,label_city,entry_city) -> None:
       self.label_city=label_city
       self.entry_city=entry_city
       self.frames=[]
    def drop_d(word):
        result = cities_data[cities_data['name'].str.contains(word, case=False)]
        return result

    def creat_wed(self,m):
        ms1=Frame(root)
        ms1.pack()
        self.frames.append(ms1)
        lab_c=tk.Label(ms1,font=20,text=f'Country : {m[1]}')
        lab_c.pack(side="left",padx=13,pady=7)
        lab_ci=tk.Label(ms1,font=20,text=f'City : {m[0]}')
        lab_ci.pack(side="left",padx=13,pady=7)
        ms2=Frame(root)
        ms2.pack()
        self.frames.append(ms2)
        wea=tk.Label(ms2,font=20,text=f'Weather : {m[7]}')
        wea.pack(side="left")
        path='logo/'+m[6]+'@2x.png'
        img = PhotoImage(file=path)
        logo=Label(ms2,bg='#fff')
        logo.config(image=img)
        logo.photo=img
        logo.pack(side='bottom',padx=13,pady=7)
        ms3=Frame(root)
        ms3.pack()
        self.frames.append(ms3)
        temp=tk.Label(ms3,font=20,text=f'Temparature : {m[2]}°C')
        temp.pack(side="left",padx=13,pady=7)
        t_feel=tk.Label(ms3,font=20,text=f'Temp. feels_like : {m[3]}')
        t_feel.pack(side="left",padx=13,pady=7)
        ms4=Frame(root)
        ms4.pack()
        self.frames.append(ms4)
        wind=tk.Label(ms4,font=20,text=f'Wind : {m[4]}km/hr')
        wind.pack(side="left",padx=13,pady=7)
        humidity=tk.Label(ms4,font=20,text=f'humidity : {m[5]}%')
        humidity.pack(side="left",padx=13,pady=7)

    
    def destroy_fr(self):
        for frame in self.frames:
            frame.destroy()
        # Clear the list
        self.frames.clear()
    def get_weather(self,city):
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:   
            response = requests.get(url)
            data = response.json()
            return data
        except requests.ConnectionError:
            messagebox.showwarning(message="Connection Error. Please check your internet connection.")
        except requests.RequestException as e:
            messagebox.showwarning(message=f"Error: {e}")
    def search(self):
        self.destroy_fr()
        city = self.entry_city.get()
        self.entry_city['value']=''
        data=self.get_weather(city)
        self.entry_city.delete(0,tk.END)
        # print(data)
        if data['cod']==200:
            
            city = data['name']
            country = data['sys']['country']
            
            temp_celsius = data['main']['temp']
            t_feel=data['main']['feels_like']
           
            icon = data['weather'][0]['icon']
            weather = data['weather'][0]['main']
            wind=data['wind']['speed']
            humad=data['main']['humidity']
            data_d = (city, country, temp_celsius,t_feel,wind,humad, icon, weather)
            self.creat_wed(data_d)
        else:
            messagebox.showwarning(title='NOT FOUND',message=data['message'])
            
def drp_dwn(event):
    # print(event.char)
    typed_text = entry_city.get()
    # print(typed_text)
    result = cities_data[cities_data['name'].str.contains(typed_text,  case=False)]
    drop=result.iloc[0:len(result)]
    drop1=drop.values
    n=len(drop1)
    l=[]
    for i in range(0,n):
        x=''
        for j in range(0,4):
            # print(drop1[i][j])
            x+=str(drop1[i][j])+','
        l.append(x)

    entry_city['value']=l


root = tk.Tk()
root.title("Weather App")
root.geometry("510x400")
root.resizable(0, 0)
titlebar_icon = PhotoImage(file='logo/back.png')
# root.configure(bg='#fff')
root.iconphoto(False, titlebar_icon)
fram=Frame(root)
fram.pack(side="top")

label_city = tk.Label(fram, text="Location :  " ,font=30,)
label_city.pack(side="left")
city_text = StringVar(fram)
# city_text=StringVar()
entry_city = ttk.Combobox(root, width=50, font=('Times', 12, 'bold'), textvariable=city_text)
entry_city.pack(side="top", padx=6, pady=10)
entry_city.bind("<KeyRelease>", drp_dwn)

frm_btn=Frame(root)
frm_btn.pack()

button_get_weather = tk.Button(frm_btn, text="Get Weather",width=25,height=2)
button_get_weather.pack(side="left",padx=9,pady=10)
reset_btn=tk.Button(frm_btn,text="Reset all data",width=25,height=2)
reset_btn.pack(side="left",padx=11,pady=12)
fram1=Frame(root)
fram1.pack(side="bottom")

m=Weather(root,label_city,entry_city)
button_get_weather.config(command=m.search)
reset_btn.config(command=m.destroy_fr)

root.mainloop()


