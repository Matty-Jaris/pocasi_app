import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Vytvoření hlavního okna
root = tk.Tk()
root.title = ("Počasí")
root.geometry("500x400")
root.config(bg="#2C3E50")  # Tmavé pozadí

background_label = tk.Label(root, bg="#2C3E50")
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Funkce, která se spustí po stisknutí tlačítka
def get_weather ():
    city = city_entry.get()
    API_KEY = "22cf61ec3c1f44665e6140df5891c249"
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    
    # Požadavek na API
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        temperature = data ['main'] ['temp']
        feels_like = data ['main']['feels_like']
        description = data ['weather'][0]['main']
        humidity = data ['main']['humidity']
        wind_speed = data ['wind']['speed']
        weather_main = data ['weather'][0]['main']

        # Získání ikony počasí
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        # Stáhnutí a zobrazení ikony
        icon_response = requests.get(icon_url)
        icon_data = Image.open(BytesIO(icon_response.content))  
        icon_image = ImageTk.PhotoImage(icon_data) 

        icon_label.config(image=icon_image)
        icon_label.image = icon_image  # Uloží, aby obraz nezmizel

        # Zobrazení výsledků
        result = (f"🌍Počasí v {city}: \n"
                  f"🌡Teplota: {temperature}°C\n"
                  f"☁Popis: {description}\n"
                  f"🌡Pocitová teplota: {feels_like}°C\n"
                  f"💧Vlhkost: {humidity}%\n"
                  f"💨Rychlost větru: {wind_speed}m/s")

        result_label.config(text=result, fg="white", bg="#404040")
        set_background(weather_main)
    else:
        result_label.config(text="Chyba, zkontrolujte název města.", fg="red", bg="#404040")
        background_label.config (image="")
        background_label.config(bg="#2C3E50")
        root.config (bg="#2C3E50")
        icon_label.config(image="")
        icon_label.image = None

# Funkce pro přidání pozadí podle počsí
def set_background (weather_condition):
    weather_images = {"Clear" : "Program_na_počasí.py/images/clear.png",
                      "Clouds" : "Program_na_počasí.py/images/cloudy.jpg",
                      "Snow" : "Program_na_počasí.py/images/snow.jpg",
                      "Rain": "Program_na_počasí.py/images/rain.jpg",
                      "Drizzle" : "Program_na_počasí.py/images/drizzle.png",
                      "Thunderstorm" : "Program_na_počasí.py/images/storm.png",
                      "Mist" : "Program_na_počasí.py/images/storm.png"
                      }
    
    img_path = weather_images.get (weather_condition, None)
    
    if img_path:
        bg_image = Image.open(img_path)
        bg_image = bg_image.resize((500, 400))
        bg_photo = ImageTk.PhotoImage(bg_image)
        background_label.config(image=bg_photo)
        background_label.image = bg_photo
    else:
        background_label.config(image=None, bg="#2C3E50")
        root.config(bg="#2C3E50")
        

# Titulek
title_label = tk.Label(root, text="Aplikace na počasí", font=("Helvetica", 16, "bold"), fg = "white", bg="#2C3E50")
title_label.pack (pady=5)
# Vytvoření widgetu pro textový popis
city_label = tk.Label(root, text="Zadej město: ", font=("Helvetica", 12), fg = "white", bg="#2C3E50")
city_label.pack()

# Vytvoření widgetu pro textové pole
city_entry = tk.Entry(root, font=("Helvetica", 12), width=20, bg="#BDC3C7")
city_entry.pack(pady=5)

# Tlačítko
get_button = tk.Button(root, text="Zobrazit počasí", font=("Helvetika", 12, "bold"), bg="#2980B9", fg="white", command=get_weather)
get_button.pack(pady=10)

# Vytvoření widgetu pro zobrazení výsledků
result_label = tk.Label(root, text="Počasí se zobrazí zde", font=("Helvetica", 12),fg="white" ,bg="#404040", width=40, height=6)
result_label.pack(pady=10)

# Ikona počasí
icon_label = tk.Label(root, bg="#2C3E50")
icon_label.pack(pady=10)

    
# Spuštení aplikace
root.mainloop() 