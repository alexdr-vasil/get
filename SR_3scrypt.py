# Подключение необходимых модулей
import pathlib
import shutil
import os
import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt;

# Подключение GPIO для работы
GPIO.setmode(GPIO.BCM)

# Список номеров выходов GPIO
ber=[10, 9 ,11 ,5,6 ,13 ,19, 26]
reb=[26,19,13,6,5,11,9,10]

# Подключение выходов на вывод OUT и ввод(считывание) IN
for n in ber:
    GPIO.setup(n, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)



# Список измеренных значений от времени
measure = []
# Список моментов времени
T = []



# ФУНКЦИИ:

# 1) Подача напряжения на GPIO из выбранного списка
def num2pins(pins, value):
    n=[0,0,0,0,0,0,0,0]
    n=binc(value)
    for i in range(8):
        GPIO.output(pins[i],n[i])

# 2) Перевод в двоичный список
def binc(num):
    n=7
    p=0
    X=[]
    while n>0:
        p=int(num/2**n)
        if p== 1:
            X.append(1)
            num-=2**n
        else:
            X.append(0)
        n-=1
    X.append(num)
    return X

# 3) Измерение мгновенного напряжения
def adc():
    x = 0
    y = 256
    while(y-x)>1:
        p = int((x+y)/2)
        num2pins(reb, p)
        time.sleep(0.001)
        if GPIO.input(4) == 0:
            y=p
        else:
            x = p
    time.sleep(0.001)
    return x




# Начало отсчёта времени
timeStart = time.time()

try:
    
    GPIO.output (17,1)
    a = adc()
    while( a < 250):
        
        a = adc()
        b = float(time.time()) - float(timeStart)
        T.append(b)
        measure.append((float(a/255*3.24)))
        print( a  , "=" , (float(a)/255)*3.24, "V")  
    GPIO.output (17,0)
    a = adc()
    while( a > 1):
        a = adc()
        b = float(time.time()) - float(timeStart)
        T.append(b)
        measure.append((float(a/255*3.24)))
        print( a  , "=" , (float(a/255*3.24)), "V")  
    
    dT = round(T[len(T)-1]/len(T), 3)
    dV = round(max(measure), 4)
    plt.plot(T, measure)
    plt.title( 'Voltage(Time)')
    plt.xlabel( 'Time' )
    plt.ylabel( 'Voltage' )
    plt.show()
    
    # Сохранение dT и dV в файл
    path = str('/home/gr006/Desktop/Scripts/result ACP') +  '/dTdV.txt'
    open(path,  'w').write( str(dT) + "\n" + str(dV))

    # Сохранение Измерения(Время) в файл
    path = str('/home/gr006/Desktop/Scripts/result ACP') +  '/data.txt'
    open(path,  'w').write( str(measure))
    np.savetxt("/home/gr006/Desktop/Scripts/result ACP/data.txt", measure, fmt= "%.2f", delimiter= "\n")  
    # Модуль numpy, Функция Сохранить файл, Путь до файла, Название файла, Записываемое значение (массив), 
    
finally:
    for x in range (8):
        GPIO.output (reb[x],0)
GPIO.output (17,0)
# Очистка всех выходов на GPIO
GPIO.cleanup()