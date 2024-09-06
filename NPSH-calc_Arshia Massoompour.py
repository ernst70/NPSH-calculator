# -*- coding: utf-8 -*-
"""Erwin/Ernest/dani.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r-RnyLeH3Jp-hLLk4n8POUmGQqZW7Zhh
"""

!pip install pytelegrambotapi

import telebot
import math

infotext = open("cavitation (1).txt","r")
infotext.read()

bot = telebot.TeleBot('5833821399:AAFa6-mDjAs5rUVdZXAaP5iH74x6Ab_bkfo')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi there!\nThis bot is designed for recognition of CAVITATION.\n\nFor recognition cavitation please enter vriables of the pump use /NPSH_calc in format below:\n/NPSH_calc pipe_material matter NPSHr Tempreture height pressure kinematic_viscousity deby diameter lenght\n\nExample:\n/NPSH_calc glass water 23 20 5.5 101000 0.000001 0.2 0.2 1\n\nTempreture is in cetigrade\nAll pressures are in pascals\nAvailable pipe materials: glass, steel, cast iron, galvanized iron\nAvailable matters for calculation: water, ethanol, methanol\n!ALL UNITS ARE IN SI\n\nUse command /format to review the required format or to see an example\n\nuse /info for extended information about cavitation')

@bot.message_handler(commands=['info'])
def info(message):
  with open('info.txt', 'r') as f:
    bot.send_message(message.chat.id, f.read())


@bot.message_handler(commands=['format'])
def calc(message):
  bot.send_message(message.chat.id, 'For recognition cavitation please enter vriables of the pump use /NPSH_calc in format below:\n/NPSH_calc pipe_material matter NPSHr Tempreture height pressure kinematic_viscousity deby diameter lenght\n\nExample:\n/NPSH_calc glass water 23 20 5.5 101000 0.000001 0.2 0.2 1')

def StartCALC(message):
  variables = message.text.split()
  if len(variables) > 0:
    return True
  else:
    return False

@bot.message_handler(commands=['NPSH_calc'])
def NPSH_calc(message):
  variables = message.text.split()
  if len(variables) != 11:
    return bot.send_message(message.chat.id, 'not enough arguments\nUse command /format to review the required format or to see an example')
  try:
    pipe=variables[1]
    matter = variables[2]
    NPSHr = float(variables[3]) # hadeaghal head lazem kedar shenasname pump ast
    T = float(variables[4]) # dama e cantigerad
    z = float(variables[5]) # sath mabda pump 
    p = float(variables[6]) # feshar ghabl pump
    v = float(variables[7]) # kinematik viscousity
    Q = float(variables[8]) # deby
    D = float(variables[9]) # diametr
    L = float(variables[10]) #lenght
  except (ValueError, TypeError):
    return bot.send_message(message.chat.id, 'enter valid inputs\nUse command /format to review the required format or to see an example')
    
  mydict = {"water": [16.3872,3885.70,30.170] ,"methanol":[16.5785,3638.27,239.5],"ethanol":[16.8958,3795.17,230.918]}
    
  mydict2 = {"water":9806 , "methanol":7766.352,"ethanol":7736.934} #####GAMA
    
  mydict3 = {"glass":3*(10**(-7)) ,"cast iron":2.6*(10**(-4)) ,"steel":4.6*(10**(-5)) , "galvanized iron":1.5*(10**(-4)) }
    
  A=((math.pi)*(D**2)/4) #area
    
  u=Q/A #velocity
  u = round(u,4)
  textu = str(u)
  Re=(u*D)/v
  Re = round(Re,7)
  textRe = str(Re)
  if Re<2000:
        firsttext = "The flow is laminar"
  elif 2000<Re<4000 :
        firsttext = 'The flow is transitional'
  elif Re>4000:
        firsttext = 'The flow is turbulent'
  elif Re>10**5:
        firtsttext = 'The flow is fully turbulent'
    
    
  if matter=="water":
        gama = mydict2.get("water")
  elif matter=="methanol":
        gama = mydict2.get("methanol")
  elif matter=="ethanoal":
        gama = mydict2.get("ethanol")
    
    
  if matter=="water":
        x = mydict.get("water")
        A = x[0]
        B = x[1]
        C = x[2]
  elif matter=="methanol":
        x = mydict.get("methanol")
        A = x[0]
        B = x[1]
        C = x[2]
  elif matter=="ethanoal":
        x = mydict.get("ethanol")
        A = x[0]
        B = x[1]
        C = x[2]
  
  if pipe=="glass":
        e = mydict3.get("glass")
      
  elif pipe=="cast iron":
        e = mydict3.get("cast iron")
      
  elif pipe=="steel":
        e = mydict3.get("steel")
        
  elif pipe=="galvanized iron":
       e = mydict3.get("galvanized iron")
    
  w =math.exp(A-(B/(T+C)))
  textw = str(w)
    
    ##  HAALAND EQUATOIN
    
  f = (-2*math.log(6.9/Re+(e/D)**(1.11),10))**(-2)
  f = round(f,5)
  textf = str(f)
  
    
  h =(f*L*(u**2))/(D*2*9.806)
  h = round(h, 4)
  texth = str(h)
  NPSHa=(p/gama)-(w/gama)+(z)-h
  NPSHa = round(NPSHa,4)
  textNPSHa = str(NPSHa)

  if NPSHa>= NPSHr :
      secondtext = 'no cavitation'
  else:
      secondtext = 'cavitation'
  bot.send_message(message.chat.id, firsttext+'\n\n'+secondtext + '\n\nvelocity: ' + textu + ' m/s' + '\n\nReynolds number: ' + textRe + '\n\nP*: ' + textw + ' kPa'+ '\n\nfriction factor: ' + textf +'\n\nhead loss: ' + texth+' m' +'\n\nNPSHa: ' + textNPSHa+' m')
  

bot.polling()