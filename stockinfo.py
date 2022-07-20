#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
import requests
import json
# yf.download returns a DataFrame
# print("This is a downloading the data:")
# data = yf.download("DOW", start="2022-06-15", end="2022-07-14")
# print(data)

from typing import Text
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
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


class LoginPage(MDScreen):
    pass

class HomePage(MDScreen):
        # pass
    availablecourseslist=ObjectProperty(None) 
    #perform actions when entered
    def on_enter(self, *args):
        layout = GridLayout(rows=1,cols=2)
        self.manager.get_screen('homepage').availablecourseslist.clear_widgets() #clear widgets
                
        layout.add_widget(MDDataTable(use_pagination=True,check=True,column_data=[("No.", dp(30)),("Status", dp(30)),],
                row_data=[("1",("alert", [255 / 256, 165 / 256, 0, 1], "No Signal")),("2",("alert-circle", [1, 0, 0, 1], "Offline")),("3",("checkbox-marked-circle",[39 / 256, 174 / 256, 96 / 256, 1],"Online",))],sorted_on="Schedule",sorted_order="ASC",elevation=2,))                                                                                                
        layout.add_widget(MDDataTable(
                use_pagination=True,
                check=True,
                column_data=[
                        ("Yes.", dp(30)),
                        ("Great", dp(30))
                ],
                row_data=[
                        (
                        "1",
                        ("alert", [255 / 256, 165 / 256, 0, 1], "No Signal")
                        ),
                        (
                        "2",
                        ("alert-circle", [1, 0, 0, 1], "Offline")
                        )
                ],
                sorted_on="Schedule",
                sorted_order="ASC",
                elevation=2,
                ))     
        self.manager.get_screen('homepage').availablecourseslist.add_widget(layout)
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

        # TODO: pull quote data from Yahoo Finance API

        PrintHistoricalAndRec(stock)
        PrintPERatios(stock.info)
        PrintAsk(stock.info)
        PrintBid(stock.info)
        PrintEPS(stock.info)

#without command line in IDE
stockPortfolio().run()
###################################################
