import time
from tkinter.font import BOLD

import pywhatkit
import pyautogui
from tkinter import *
# import os
# import configparser
from configfile_utils import get_setting, update_setting


def MarginCalck(event):
    global cConfigValue

    nInPrice = float(InPrice.get())
    nTakePrice = float(TakePrice.get())
    nStopPrice = float(StopPrice.get())
    nRiskValue = int(RiskValue.get())

    if nStopPrice > nInPrice:
        nPercent = round((nStopPrice * 100 / nInPrice) - 100, 2)
        nRatio = round((nInPrice - nTakePrice) / (nStopPrice - nInPrice), 1)
    else:
        nPercent = round(100 - (nStopPrice * 100 / nInPrice), 2)
        nRatio = round((nTakePrice - nInPrice) / (nInPrice - nStopPrice), 1)
        LabelOrderVolume["fg"] = 'green'

    nValue = int((nRiskValue * 100) / nPercent)
    nPos = nValue / nInPrice
    if nPos >= 1:
        nPos = round(nPos, 0)
    else:
        nPos = round(nPos, 4)

    nLeverage = int(100 / nPercent)

    print(f"Вход={nInPrice} Тейк={nTakePrice} Стоп={nStopPrice} Риск={nRiskValue}")
    print(f"Процент движения={nPercent}")
    print(f"Объём= {nPos}  ${nValue}")
    v["text"] = f"${nValue}  {nPercent}%  {nRatio}"
    LabelOrderVolume["text"] = f"{nPos}  {nLeverage}x"
    root.update()

    if str(nRiskValue) != cConfigValue or str(nInPrice)!= cInPrice or str(nTakePrice)!= cTakePrice or str(nStopPrice) != cStopPrice:
        print("Config update")
        update_setting(cConfigFile, "Settings", "$", str(nRiskValue))
        update_setting(cConfigFile, "Settings", "InPrice", str(nInPrice))
        update_setting(cConfigFile, "Settings", "TakePrice", str(nTakePrice))
        update_setting(cConfigFile, "Settings", "StopPrice", str(nStopPrice))

if __name__ == '__main__':
    cConfigFile = "config"
    root = Tk()
    root.title('MarginCalck by -=Crocko=-')
    root.resizable(width=False, height=False)

    cConfigValue=get_setting(cConfigFile, "Settings", "InPrice")
    print(f"Risk= {cConfigValue}")
    cInPrice=get_setting(cConfigFile, "Settings", "InPrice")
    InPrice = StringVar(root, value = cInPrice )
    cTakePrice=get_setting(cConfigFile, "Settings", "TakePrice")
    TakePrice = StringVar(root, value=cTakePrice)
    cStopPrice=get_setting(cConfigFile, "Settings", "StopPrice")
    StopPrice = StringVar(root, value=cStopPrice)
    RiskValue = StringVar(root, value='10')
    nValue = 0

    cConfigValue = get_setting(cConfigFile, "Settings", "$")
    print(f"Risk= {cConfigValue}")

    RiskValue = StringVar(root, value=cConfigValue)

    Label(text="Вход").pack(padx=150)
    Entry(textvariable=InPrice).pack()
    Label(text="Тейк").pack()
    Entry(textvariable=TakePrice).pack()
    Label(text="Стоп").pack()
    Entry(textvariable=StopPrice).pack()
    Label(text="Риск").pack()
    Entry(textvariable=RiskValue).pack()
    LabelOrderVolume = Label(text="", font=("Times", 16, "bold"), fg='#F00')
    LabelOrderVolume.pack()
    v = Label(text="", font=("Times", 10, "bold"), fg='black')
    v.pack()
    b = Button(text="MarginCalck")
    b.bind('<Button-1>', MarginCalck)
    b.pack(side=BOTTOM, pady=20)
    root.mainloop()
