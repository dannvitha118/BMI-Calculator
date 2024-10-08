# -*- coding: utf-8 -*-
"""BMI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bRhUNFGjGQ4rCf5yyCAORDPlkUHdLvij
"""

import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Set up SQLite database
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records
             (username TEXT, weight REAL, height REAL, bmi REAL, date TEXT)''')
conn.commit()

# Function to calculate BMI
def calculate_bmi(weight, height):
    bmi = round(weight / (height * height), 2)
    return bmi

# Function to save data
def save_bmi_data(username, weight, height, bmi):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO bmi_records (username, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
              (username, weight, height * 100, bmi, date))
    conn.commit()

# Function to view BMI history
def view_history(username):
    c.execute("SELECT date, weight, height, bmi FROM bmi_records WHERE username = ?", (username,))
    records = c.fetchall()
    if records:
        for date, weight, height, bmi in records:
            print(f"{date}: Weight: {weight} kg, Height: {height} cm, BMI: {bmi}")
    else:
        print("No history found for this user.")

# Function to show BMI trend
def show_bmi_trend(username):
    c.execute("SELECT date, bmi FROM bmi_records WHERE username = ?", (username,))
    records = c.fetchall()

    if records:
        dates = [r[0] for r in records]
        bmis = [r[1] for r in records]

        plt.plot(dates, bmis, marker='o')
        plt.title(f'BMI Trend for {username}')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No trend data available for this user.")

# User interaction in Google Colab
username = input("Enter your username: ")
weight = float(input("Enter your weight (kg): "))
height = float(input("Enter your height (cm): ")) / 100  # convert to meters

bmi = calculate_bmi(weight, height)
print(f"Your BMI is: {bmi}")

# Save data and show options
save_bmi_data(username, weight, height, bmi)
view_choice = input("Do you want to view your BMI history (y/n)? ")
if view_choice.lower() == 'y':
    view_history(username)

trend_choice = input("Do you want to see your BMI trend (y/n)? ")
if trend_choice.lower() == 'y':
    show_bmi_trend(username)

# Close the connection
conn.close()

1