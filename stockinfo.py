#!/usr/bin/env python3
from operator import pos
from turtle import position
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


class LoginPage(MDScreen):
    pass

Dummy = """
        OneLineListItem:
            id: item1
            text: "Awesome"
"""

class HomePage(MDScreen):

    availablelist=ObjectProperty(None) 

    def fetchData(self, userInputStockData):
        print(userInputStockData)

    def addToWatchList(self):
        print("Added to watchlist")

    #perform actions when entered
    def on_enter(self, *args):
        layout = GridLayout(rows=1,cols=2)
        self.manager.get_screen('homepage').availablelist.clear_widgets() #clear widgets

        leftLayout = GridLayout(rows=6,cols=2)

       
        leftLayout.add_widget(TwoLineListItem(text="Open",secondary_text="51.2"))  
        leftLayout.add_widget(TwoLineListItem(text="Close",secondary_text="46.2")) 
        leftLayout.add_widget(TwoLineListItem(text="Bid",secondary_text="No")) 
        leftLayout.add_widget(TwoLineListItem(text="Ask",secondary_text="No")) 
        leftLayout.add_widget(TwoLineListItem(text="Volume",secondary_text="100")) 
        leftLayout.add_widget(TwoLineListItem(text="PE Ratio",secondary_text="51.2")) 
        leftLayout.add_widget(TwoLineListItem(text="EPS",secondary_text="51.2")) 
        leftLayout.add_widget(TwoLineListItem(text="Analyst Recommendation",secondary_text="51.2")) 
        
        layout.add_widget(leftLayout)   

        rightLayout = GridLayout(rows=1)
        # rightLayout.add_widget(
        rightLayout.add_widget(MDDataTable(
                column_data=[
                        ("Stock Name",dp(30)),
                        ("Open",dp(30)),
                        ("Close",dp(30))
                ],
                row_data=[
                        ("GOOG",51.2,32.6)
                ]
        ))

        layout.add_widget(rightLayout)

        # layout.add_widget(MDDataTable(
        #         use_pagination=True,
        #         check=True,
        #         elevation=2,
        #         ))     
        self.manager.get_screen('homepage').availablelist.add_widget(layout)
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
