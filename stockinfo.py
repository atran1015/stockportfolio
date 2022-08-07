#!/usr/bin/env python3
from operator import pos
import pprint
from turtle import position
from dotenv import dotenv_values
import bt
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
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
from kivy.properties import ObjectProperty, StringProperty
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
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.theming import ThemeManager
from kivy.uix.image import Image
import matplotlib.pyplot as plt

# for watchlist
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

# for strategy popup/dialog
class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        
        for check in check_list:
            if check != instance_check:
                check.active = False

        app = MDApp.get_running_app() # Access the running app instance.
        home_screen = app.root.get_screen('homepage') # Access required screen.
        home_screen.selected_item = self.text


# bt library
class SelectWhere(bt.Algo):

    """
    Selects securities based on an indicator DataFrame.

    Selects securities where the value is True on the current date (target.now).

    Args:
        * signal (DataFrame): DataFrame containing the signal (boolean DataFrame)

    Sets:
        * selected

    """
    def __init__(self, signal):
        self.signal = signal

    def __call__(self, target):
        # get signal on target.now
        if target.now in self.signal.index:
            sig = self.signal.loc[target.now]

            # get indices where true as list
            selected = list(sig.index[sig])

            # save in temp - this will be used by the weighing algo
            target.temp['selected'] = selected

        # return True because we want to keep on moving down the stack
        return True

        # first we create the Strategy
        
class WeighTarget(bt.Algo):
    """
    Sets target weights based on a target weight DataFrame.

    Args:
        * target_weights (DataFrame): DataFrame containing the target weights

    Sets:
        * weights

    """

    def __init__(self, target_weights):
        self.tw = target_weights

    def __call__(self, target):
        # get target weights on date target.now
        if target.now in self.tw.index:
            w = self.tw.loc[target.now]

            # save in temp - this will be used by the weighing algo
            # also dropping any na's just in case they pop up
            target.temp['weights'] = w.dropna()

        # return True because we want to keep on moving down the stack
        return True
            
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

class responseData_Adapter():
        def __init__(self,**adapted_method):
             self.__dict__.update(adapted_method)

class HomePage(MDScreen):
    availablelist=ObjectProperty(None)
    dialog = None
    theme_cls = ThemeManager()
    selected_item = StringProperty() 
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
        urls = [
                'https://yfapi.net/v7/finance/options/' + stock + '?date=' + str(math.floor(time.time())), #contains open, close, ask, bid, volume, eps
                'https://yfapi.net/v6/finance/recommendationsbysymbol/' + stock, #contains the anaylst recomendations
                'https://yfapi.net/v6/finance/quote?region=US&lang=en&symbols=' + stock, #contains the trailing ratio
                'https://yfapi.net/ws/insights/v1/finance/insights?symbol=' + stock
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
                if 'epsCurrentYear' in self.response['optionChain']['result'][0]['quote']:
                    leftLayout.add_widget(TwoLineListItem(text="EPS",secondary_text=str(self.response['optionChain']['result'][0]['quote']['epsCurrentYear']))) 
                else:
                    leftLayout.add_widget(TwoLineListItem(text="EPS",secondary_text='N/A'))
                leftLayout.add_widget(TwoLineListItem(text="Analyst Recommendation",secondary_text=str(self.response['finance']['result']['instrumentInfo']['recommendation']['rating'])))

                # for watchlist
                global open_var
                global close_var
                open_var = str(self.response['optionChain']['result'][0]['quote']['regularMarketOpen'])
                close_var = str(self.response['optionChain']['result'][0]['quote']['regularMarketPreviousClose'])


        # if self.manager.get_screen('homepage').ids.search.on_press:
        #         # create button box layout
        #         button_box = MDBoxLayout(
        #             pos_hint={"center_x": 0.4,"center_y": 0.9},
        #             adaptive_size=True,
        #         )
        #         print("clicked")
        
        # # create button
        # button = MDRaisedButton(
        #         text="Add to watchlist", on_release=self.on_button_press
        # )
        # self.ids['watch'] = button
        # button_box.add_widget(button)
        # leftLayout.add_widget(button_box)
        layout.add_widget(leftLayout)
        self.manager.get_screen('homepage').availablelist.add_widget(layout)

    # def on_button_press(self, instance_button: MDRaisedButton):
    #     '''Called when a control button is clicked.'''
    #     try:
    #         {
    #             "Add to watchlist": self.addToWatchList
    #         }[instance_button.text]()
    #     except KeyError:
    #         pass

    def addToWatchList(self):
        ticker_symbol = self.manager.get_screen('homepage').ids.stock.text
        layout = GridLayout(rows=1,cols=2)
        rightLayout = GridLayout(rows=1)
        #print(dataofrow)
        dataofrow = [(ticker_symbol), (open_var), (close_var)]
        if self.manager.get_screen('homepage').ids.watch.on_press:
                # append to list to be displayed on click
                data_list.append(dataofrow)
        #print(data_list, "data_list from addToWatchList")
        
        # create table
        data_table = MDDataTable(
        
                column_data=[
                        ("Stock Name",dp(30)),
                        ("Open",dp(30)),
                        ("Close",dp(30))
                ],
                
                row_data=data_list
                
        )
        rightLayout.add_widget(data_table)
        layout.add_widget(rightLayout)
        count = 0
        current_symbol = self.manager.get_screen('homepage').ids.stock.text
        current_data = [(current_symbol), (open_var), (close_var)]
        

        # this is for err message if user tries to append same symbol
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
        
        return self.manager.get_screen('homepage').availablelist.add_widget(layout)
        
    def buyStock(self):
        userMoney = self.manager.get_screen('homepage').ids.money.text
        ticker_symbol = self.manager.get_screen('homepage').ids.stock.text
        self.getStockData(ticker_symbol)['optionChain']['result'][0]['quote']['regularMarketOpen']
        balance = float(userMoney) - float(self.getStockData(ticker_symbol)['optionChain']['result'][0]['quote']['regularMarketOpen'])
        self.manager.get_screen('homepage').ids.money.text = str("{:0.2f}".format(balance))
        print("Buying Stock")

    def sellStock(self):
        userMoney = self.manager.get_screen('homepage').ids.money.text
        ticker_symbol = self.manager.get_screen('homepage').ids.stock.text
        self.getStockData(ticker_symbol)['optionChain']['result'][0]['quote']['regularMarketOpen']
        balance = float(userMoney) + float(self.getStockData(ticker_symbol)['optionChain']['result'][0]['quote']['regularMarketOpen'])
        self.manager.get_screen('homepage').ids.money.text = str("{:0.2f}".format(balance))
        print("Selling Stock")

    # creating a dialog window    
    def chooseStrat(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Choose a strategy to use for backtest",
                type="confirmation",
                items=[
                    ItemConfirm(text="SMA"), #, on_press=lambda x: print("SMA")),
                    ItemConfirm(text="SMA Crossover"), #, on_press=lambda x: print("Mean Reversion")),
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog,
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.ok_dialog,
                    ),
                ],
            )
        self.ids['strat'] = self.dialog
        self.dialog.open()

    # functional CANCEL button
    def close_dialog(self, obj):
        self.dialog.dismiss()

    # functional OK button
    def ok_dialog(self, obj, *args, **kwargs):
        self.dialog.dismiss()
        self.ids.strat.text = self.selected_item
        currStock = self.manager.get_screen('homepage').ids.stock.text
        if self.ids.strat.text == 'SMA':
                # get user input
                # call bt library
                backtestdata = bt.get(currStock, start='2012-01-01', end='2022-01-01')
                sma = backtestdata.rolling(100).mean() # over 100 days
                plot = bt.merge(backtestdata, sma).plot(figsize=(15, 5))
                # export plot image
                fig = plot.get_figure()
                fig.savefig("output.png")
                # call library
                s = bt.Strategy('above100sma', [SelectWhere(backtestdata > sma),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
                t = bt.Backtest(s, backtestdata)
                res = bt.run(t) # res['above100sma'].stats to get variables
                layout = GridLayout(rows=2,cols=1)
                layout.add_widget(MDTextField(text="Strategy: SMA, Backtest results:"))
                self.manager.get_screen('homepage').availablelist.clear_widgets() #clear widgets
                leftLayout = GridLayout(rows=7,cols=2)
                leftLayout.add_widget(TwoLineListItem(text="% profitability",secondary_text=str(res['above100sma'].stats['ytd'])))
                leftLayout.add_widget(TwoLineListItem(text="Win/Loss ratio",secondary_text=str(res['above100sma'].stats['win_year_perc'])))
                leftLayout.add_widget(TwoLineListItem(text="Annualized return",secondary_text=str(res['above100sma'].stats['total_return'])))
                leftLayout.add_widget(TwoLineListItem(text="Max drawdown",secondary_text=str(res['above100sma'].stats['max_drawdown'])))
                leftLayout.add_widget(TwoLineListItem(text="Volatility",secondary_text=str(res['above100sma'].stats['yearly_vol'])))
                leftLayout.add_widget(TwoLineListItem(text="Sharpe Ratio",secondary_text=str(res['above100sma'].stats['yearly_sharpe'])))
                # render image
                wimg = Image(source='output.png')
                leftLayout.add_widget(wimg)
                
                layout.add_widget(leftLayout)
                
                self.manager.get_screen('homepage').availablelist.add_widget(layout)
                print("i selected sma for backtest") # debug
        elif self.ids.strat.text == 'SMA Crossover':
                ## download some data & calc SMAs
                data = bt.get('spy', start='2010-01-01')
                sma50 = data.rolling(50).mean()
                sma200 = data.rolling(200).mean()

                ## now we need to calculate our target weight DataFrame
                # first we will copy the sma200 DataFrame since our weights will have the same strucutre
                tw = sma200.copy()
                # set appropriate target weights
                tw[sma50 > sma200] = 1.0
                tw[sma50 <= sma200] = -1.0
                # here we will set the weight to 0 - this is because the sma200 needs 200 data points before
                # calculating its first point. Therefore, it will start with a bunch of nulls (NaNs).
                tw[sma200.isnull()] = 0.0
                tmp = bt.merge(tw, data, sma50, sma200)
                tmp.columns = ['tw', 'price', 'sma50', 'sma200']
                ax = tmp.plot(figsize=(15,5), secondary_y=['tw'])

                ma_cross = bt.Strategy('ma_cross', [WeighTarget(tw),
                                                    bt.algos.Rebalance()])
                t = bt.Backtest(ma_cross, data)
                res = bt.run(t)

                print(res.stats)

                layout = GridLayout(rows=2,cols=1)
                layout.add_widget(MDTextField(text="Strategy: SMA Crossover, Backtest results:"))
                self.manager.get_screen('homepage').availablelist.clear_widgets() #clear widgets
                leftLayout = GridLayout(rows=6,cols=2)
                leftLayout.add_widget(TwoLineListItem(text="% profitability",secondary_text=str(res.stats.values[10][0])))
                leftLayout.add_widget(TwoLineListItem(text="Win/Loss ratio",secondary_text=str(res.stats.values[-2][0])))
                leftLayout.add_widget(TwoLineListItem(text="Annualized return",secondary_text=str(res.stats.values[3][0]))) 
                leftLayout.add_widget(TwoLineListItem(text="Max drawdown",secondary_text=str(res.stats.values[5][0])))
                leftLayout.add_widget(TwoLineListItem(text="Volatility",secondary_text=str(res.stats.values[-11][0])))
                leftLayout.add_widget(TwoLineListItem(text="Sharpe Ratio",secondary_text=str(res.stats.values[-14][0])))
                layout.add_widget(leftLayout)
                self.manager.get_screen('homepage').availablelist.add_widget(layout)
                print("i selected SMA Crossover for backtest") # debug

    def userBalance(self):
        userMoney = self.manager.get_screen('homepage').ids.money.text
        print(int(userMoney))

    def getStockData(self, stock):
        config = dotenv_values(".env")
        header = {
                'authority': 'finance.yahoo.com',
                'method': 'GET',
                'scheme': 'https',
                'accept': 'application/json',
                'X-API-KEY': str(config["APIKEY"]),
        }
        urls = [
                'https://yfapi.net/v7/finance/options/' + stock + '?date=' + str(math.floor(time.time())), #contains open, close, ask, bid, volume, eps
                'https://yfapi.net/v6/finance/recommendationsbysymbol/' + stock, #contains the anaylst recomendations
                'https://yfapi.net/v6/finance/quote?region=US&lang=en&symbols=' + stock #contains the trailing ratio
        ]
        data = {}
        for url in urls: # combine all data into one chunk
                data_adapter = responseData_Adapter(responseData=requests.get(url, headers=header).json())
                response = data_adapter.responseData()
                #response = requests.get(url, headers=header).json()
                data.update(response)
        return data

#####################################################################################################               
 
# def PrintHistoricalAndRec(ticker):
#         hist = ticker.history(period="1d")
#         analyst_recdf = pd.DataFrame(ticker.recommendations)
#         df = pd.DataFrame(hist)
#         df2 = df[["Open","Volume","Close","Low"]]
#         df3 = pd.concat([df2, analyst_recdf])
#         print(df3)
#         df3.to_csv("concat_data.csv")
#         return df3

# def PrintPERatios(ticker):
#         print("two PE ratios are trailingPE and forwardPE: ", ticker["trailingPE"], ticker["forwardPE"])
#         return ticker["trailingPE"], ticker["forwardPE"]

# def PrintAsk(ticker):
#         print("Ask: ", ticker["ask"])
#         return ticker["ask"]

# def PrintBid(ticker):
#         print("Bid: ", ticker["bid"])
#         return ticker["bid"]

# def PrintEPS(ticker):
#         print("EPS: ", ticker["revenuePerShare"])
#         return ticker["revenuePerShare"]


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
# if __name__ == '__main__':
        
        # stockPortfolio().run()
        # inp = input('Input a stock ticker: ')
        # stock = yf.Ticker(inp)
        # hist = stock.history(period="1d")
        # df = pd.DataFrame(hist)
        # df2 = df[["Open","Volume","Close","Low"]]
        # df2.to_csv("history.csv")
        # rec = stock.recommendations
        # rec.to_csv("recommendations.csv")

        

        # PrintHistoricalAndRec(stock)
        # PrintPERatios(stock.info)
        # PrintAsk(stock.info)
        # PrintBid(stock.info)
        # PrintEPS(stock.info)

#without command line in IDE
stockPortfolio().run()
###################################################
