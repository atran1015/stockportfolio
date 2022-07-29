#!/usr/bin/env python3
from operator import pos
import pprint
from turtle import position
from dotenv import dotenv_values


import yfinance as yf
import pandas as pd
import sqlite3
import requests
import os
import math
import time

from typing import Text
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.expansionpanel import MDExpansionPanel,MDExpansionPanelTwoLine
from kivymd.uix.list import TwoLineListItem,OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDIconButton
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton

data_list = []

# pop up function
class PopupWindow(Widget):
    def btn(self):
        popUp()

# pop up window GUI
class P(FloatLayout):
    pass

# content of pop up
def popUp():
    show = P()
    window = Popup(title = "Error", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()


class LoginPage(MDScreen):
        def show_alert_dialog(self):
                if not self.dialog:
                        self.dialog = MDDialog()
                self.dialog.open()
        def validate(self):
                connection = sqlite3.connect("login.db")
                cursor = connection.cursor()
                username_input = self.manager.get_screen('loginpage').ids.user.text
                
                # check if username exists in table
                if cursor.execute("SELECT * FROM login WHERE username = ?", (username_input,)).fetchall():
                        # print("True")
                        self.parent.current = 'homepage'
                else:
                        # print("False")
                        popUp()         

Dummy = """
        OneLineListItem:
            id: item1
            text: "Awesome"
"""

class HomePage(MDScreen):
    def fetchData(self, stock):
        #Get list of stocks
        config = dotenv_values(".env")
        header = {
                'authority': 'finance.yahoo.com',
                'method': 'GET',
                'scheme': 'https',
                'accept': 'application/json',
                'X-API-KEY': str(config["APIKEY"]),
        }
        print(header['X-API-KEY'])
        urls = [
                'https://yfapi.net/v7/finance/options/' + stock + '?date=' + str(math.floor(time.time())), #contains open, close, ask, bid, volume, eps
                'https://yfapi.net/v6/finance/recommendationsbysymbol/' + stock, #contains the anaylst recomendations
                'https://yfapi.net/v6/finance/quote?region=US&lang=en&symbols=' + stock #contains the trailing ratio
        ]
        data = {}
        for url in urls: # combine all data into one chunk
                response = requests.get(url, headers=header).json()
                data.update(response)
        self.response = data
        if self.response:
                layout = GridLayout(rows=1,cols=2)
                self.manager.get_screen('homepage').availablelist.clear_widgets() #clear widgets

                leftLayout = GridLayout(rows=6,cols=2)
                leftLayout.add_widget(TwoLineListItem(text="Open",secondary_text=str(self.response['optionChain']['result'][0]['quote']['regularMarketOpen'])))  
                leftLayout.add_widget(TwoLineListItem(text="Close",secondary_text=str(self.response['optionChain']['result'][0]['quote']['regularMarketPreviousClose']))) 
                leftLayout.add_widget(TwoLineListItem(text="Bid",secondary_text=str(self.response['optionChain']['result'][0]['quote']['bid']))) 
                leftLayout.add_widget(TwoLineListItem(text="Ask",secondary_text=str(self.response['optionChain']['result'][0]['quote']['ask']))) 
                leftLayout.add_widget(TwoLineListItem(text="Volume",secondary_text=str(self.response['optionChain']['result'][0]['quote']['regularMarketVolume']))) 
                leftLayout.add_widget(TwoLineListItem(text="PE Ratio",secondary_text=str(self.response['optionChain']['result'][0]['quote']['trailingPE']))) 
                leftLayout.add_widget(TwoLineListItem(text="EPS",secondary_text=str(self.response['optionChain']['result'][0]['quote']['epsCurrentYear']))) 
                leftLayout.add_widget(TwoLineListItem(text="Analyst Recommendation",secondary_text="I like this stock"))

                layout.add_widget(leftLayout)   

        # if self.manager.get_screen('homepage').ids.search.on_press:
                
        #         button_box = MDBoxLayout(
        #             pos_hint={"center_x": 0.4,"center_y": 0.9},
        #             adaptive_size=True,
        #             #on_press= lambda widget:self.addToWatchList(),
        #             #on_press= self.addToWatchList(),
        #         )
        #         print("clicked")
        
        # self.ids['watch'] = button_box

        # for button_text in ["Add to watchlist"]:
        #     button_box.add_widget(
        #         MDRaisedButton(
        #             text=button_text, on_release=self.on_button_press
        #         )
        #     )
        # button = MDRaisedButton(
        #         text="Add to watchlist", on_release=self.on_button_press
        # )
        # self.ids['watch'] = button
        # button_box.add_widget(button)
        # leftLayout.add_widget(button_box)
        # layout.add_widget(leftLayout)
        self.manager.get_screen('homepage').availablelist.add_widget(layout)

    def on_button_press(self, instance_button: MDRaisedButton):
        '''Called when a control button is clicked.'''
        try:
            {
                "Add to watchlist": self.addToWatchList
            }[instance_button.text]()
        except KeyError:
            pass

    def addToWatchList(self):
        # TODO: so far can only print out individual table instead of appending row to table
        # tried using global var data_list to build a list and then append list and refresh table
        # problem: can't pass data to on_enter
        ticker_symbol = self.manager.get_screen('homepage').ids.stock.text
        
        layout = GridLayout(rows=1,cols=2)
        rightLayout = GridLayout(rows=1)
        #print(dataofrow)
        dataofrow = [(ticker_symbol), (10), (15)]
        if self.manager.get_screen('homepage').ids.watch.on_press:
                # need to clear widgets
                # self.manager.get_screen('homepage').availablelist.clear_widgets()
                data_list.append(dataofrow)
        print(data_list, "data_list from addToWatchList")
        
        
        #data_list.append(dataofrow)
        #print(data_list)
        data_table = MDDataTable(
        
                column_data=[
                        ("Stock Name",dp(30)),
                        ("Open",dp(30)),
                        ("Close",dp(30))
                ],
                
                row_data=data_list
                
        )
        rightLayout.add_widget(data_table)
        #print(data_table.row_data)
        layout.add_widget(rightLayout)
        count = 0
        current_symbol = self.manager.get_screen('homepage').ids.stock.text
        current_data = [(current_symbol), (10), (15)]
        
        for i in data_list:
            if i == current_data:
                # counting occurence of same data
                count +=1 
                if count > 1:
                    #print("data is the same")
                    
                    content = Button(text='You have already added this ticker into your watchlist.  \nPlease restart the program.')
                    popup = Popup(title='Error', content=content,size_hint=(None, None), size=(400, 400), auto_dismiss=False)
                    content.bind(on_press=popup.dismiss)
                    popup.open()
        
            # else:
            #     print("data not the same")
        
 
        #self.userBalance()
        return self.manager.get_screen('homepage').availablelist.add_widget(layout)
        
    
    def buyStock(self):
        print("Buying Stock")

    def sellStock(self):
        print("Selling Stock")

    def userBalance(self):
        userMoney = self.manager.get_screen('homepage').ids.money.text
        print(int(userMoney))

#####################################################################################################               
 
def PrintHistoricalAndRec(ticker):
        hist = ticker.history(period="1d")
        analyst_recdf = pd.DataFrame(ticker.recommendations)
        df = pd.DataFrame(hist)
        df2 = df[["Open","Volume","Close","Low"]]
        df3 = pd.concat([df2, analyst_recdf])
        print(df3)
        df3.to_csv("concat_data.csv")
        return df3

def PrintPERatios(ticker):
        print("two PE ratios are trailingPE and forwardPE: ", ticker["trailingPE"], ticker["forwardPE"])
        return ticker["trailingPE"], ticker["forwardPE"]

def PrintAsk(ticker):
        print("Ask: ", ticker["ask"])
        return ticker["ask"]

def PrintBid(ticker):
        print("Bid: ", ticker["bid"])
        return ticker["bid"]

def PrintEPS(ticker):
        print("EPS: ", ticker["revenuePerShare"])
        return ticker["revenuePerShare"]


############################## SCREEN MANAGER ##########################
class PageManager(ScreenManager):
    pass

#########################################################################

################# MAIN APP CLASS #################################
class stockPortfolio(MDApp):
   
    def __init__(self,**kwargs):
        super(stockPortfolio,self).__init__(**kwargs)
        self.root= Builder.load_file('pagescreen.kv')

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette= "Blue"
        self.theme_cls.accent_palette= "Orange"
       
        return self.root
    

######################################################
#run the application
##using command line call
if __name__ == '__main__':
        
        stockPortfolio().run()
        inp = input('Input a stock ticker: ')
        stock = yf.Ticker(inp)
        hist = stock.history(period="1d")
        df = pd.DataFrame(hist)
        df2 = df[["Open","Volume","Close","Low"]]
        df2.to_csv("history.csv")
        rec = stock.recommendations
        rec.to_csv("recommendations.csv")

        

        PrintHistoricalAndRec(stock)
        PrintPERatios(stock.info)
        PrintAsk(stock.info)
        PrintBid(stock.info)
        PrintEPS(stock.info)

#without command line in IDE
stockPortfolio().run()
###################################################
