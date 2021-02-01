# -*- coding: utf-8 -*-
import numpy as np
import cv2
import time
import math

cam = cv2.VideoCapture('outpy.avi')
potato_low = np.array([160, 165, 80])                                                                     # Параметры необходимые для определения облака точек каждого цвета:
potato_high = np.array([180, 210, 185])																      # Красного

water_low = np.array([106,65,62])                                                                         # Синего
water_high = np.array([130,255,255])

seed_low = np.array([15, 65, 90])                                                                         # И желтого
seed_high = np.array([41, 220, 240])

pastures_low = np.array([65,86,42])                                                                       # И зеленого
pastures_high = np.array([95,255,99])
     
soil_low = np.array([0,90,55])                                                                            # И коричневого
soil_high = np.array([15,165,150]) 


pix_x = 320
pix_y = 240
yaw_x = 160
yaw_y = 120
out = cv2.VideoWriter('out.mp4', -1, 20.0, (320,240))

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('X','V','I','D'), 20, (638,480))

def point(mas, text):
    global mark,b
    for i in range (len(mas)):
        for j in (i+1,len(mas)):
            if j+1 != len(mas):
                break
            if math.sqrt(abs(mas[i][0] - mas[j][0])**2 + abs(mas[i][1] - mas[j][1])**2) <= b:
                mas[i][0] = (mas[i][0] + mas[j][0])/2
                mas[i][1] = (mas[i][1] + mas[j][1])/2
                del mas[j]
            if j+1 != len(mas):
                break
        if mas[i][0] <= 2 and mas[i][1] <= 2:
            mark['C'].append([text,mas[i][0],mas[i][1]])
        elif mas[i][0] > 2 and mas[i][1] < 2:
            mark['D'].append([text,mas[i][0],mas[i][1]])
        elif mas[i][0] > 2 and mas[i][1] > 2:
            mark['B'].append([text,mas[i][0],mas[i][1]])
        elif mas[i][0] < 2 and mas[i][1] > 2:
            mark['A'].append([text,mas[i][0],mas[i][1]])
        if i+1 != len(mas):
            break
   
def distance_x(x):
    z = 120
    if x >= 160:
        return ((x - 160)*0.00524437269 * z)
    else:
        return -((160 - x)*0.00524437269 * z)
        
def distance_y(y):
    z = 120
    if y >= 120:
        return -((y - 120)*0.00481125224 * z)
    else:
        return ((120 - y)*0.00481125224 * z)
        
while True:
    ret, img = cam.read()                                                                                 # Считывание изображения
    #imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.undistort( img,np.array([[332.47884746146343,0,320.0],[0,333.1761847948052,240],[0,0,1]]), np.array([2.15356885e-01,  -1.17472846e-01,  -3.06197672e-04,   -1.09444025e-04,  -4.53657258e-03,   5.73090623e-01,-1.27574577e-01,  -2.86125589e-02,   0.00000000e+00,0.00000000e+00,   0.00000000e+00,   0.00000000e+00,0.00000000e+00,   0.00000000e+00]),np.array([[332.47884746146343,0,324.38022493658536],[0,333.1761847948052,219.6445547142857],[0,0,1]]))
    mtx = np.array([[166.23942373073172,0,162.19011246829268],[0,166.5880923974026,109.82227735714285],[0,0,1]])
    distCoeffs = np.array([2.15356885e-01,-1.17472846e-01,-3.06197672e-04,-1.09444025e-04,-4.53657258e-03,5.73090623e-01,-1.27574577e-01,-2.86125589e-02])
    img = cv2.undistort(img, mtx, distCoeffs)
    Grey = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #out.write(img)
    
    st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
    st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11), (5, 5))
    #mask_1 = cv2.inRange(Grey, red_low, red_high) 
    mask1_1 = cv2.inRange(Grey, potato_low, potato_high)                                                          # Создание облак точек для каждого цвета
    mask2 = cv2.inRange(Grey, water_low, water_high)
    mask3 = cv2.inRange(Grey, seed_low, seed_high)
    mask4 = cv2.inRange(Grey, pastures_low, pastures_high)
    mask5 = cv2.inRange(Grey, soil_low, soil_high)
        
    res1 = cv2.bitwise_and(img, img, mask= mask1_1)                                                         # Метод для отображения облака точек в цвете
    cv2.imshow('Potato',res1)                                                                                # Вывод в отдельное окно
    
    res2 = cv2.bitwise_and(img, img, mask= mask2)                                                         # И так с каждым цветом
    cv2.imshow('Water',res2)
            
    res3 = cv2.bitwise_and(img, img, mask= mask3)
    cv2.imshow('Seed',res3)
        
    res4 = cv2.bitwise_and(img, img, mask= mask4)                                                         # Метод для отображения облака точек в цвете
    cv2.imshow('Pastures',res4)                                                                                # Вывод в отдельное окно

    res5 = cv2.bitwise_and(img, img, mask= mask5)                                                         # И так с каждым цветом
    cv2.imshow('Soil',res5)
        
    cv2.line(img,(160,0),(160,240), (0,0,255), 2)
    cv2.line(img,(0,120),(320,120), (0,0,255), 2)
    
    cv2.line(img,(0,0),(10,0),(0,0,255), 2)
    
    thresh = cv2.morphologyEx(mask1_1, cv2.MORPH_CLOSE, st1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    potato = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                                  # Поиск контуров в облаке точек (Красном)
    try:
        for c in potato[0]:                                                                                      # Перебор каждого контура
            try:    
                #print(len(c))
                y,x = 0,0
                moments = cv2.moments(c, 1)                                                                   # Метод создающий матрицу объекта
                sum_y = moments['m01']
                sum_x = moments['m10']
                sum_pixel = moments['m00']
                if sum_pixel > 2500:                                                                           # Отсеивание помех(нужно подстроить под ваше разрешение камеры)
                    x = int(sum_x / sum_pixel)                                                                # Определение центра объекта
                    y = int(sum_y / sum_pixel)
                    cv2.drawContours(img, [c], 0, (0, 0, 0), 2)
                    
                    cv2.putText(img,'@'+ str(sum_pixel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

                    #cv2.putText(img, str(round(distance_y(y),2))+'   '+ str(y), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            except:pass
    except:pass
    
    thresh = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, st1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    water = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )                                  # Поиск контуров в облаке точек (Красном)
    mas2,m = [],0
    try:
        for c in water[0]:
            try:
        
                moments = cv2.moments(c, 1)
                sum_y = moments['m01']
                sum_x = moments['m10']
                sum_pixel = moments['m00']
                approx = cv2.approxPolyDP(c, 0.05* cv2.arcLength(c, True), True)
                if sum_pixel > 2500:
                    m += sum_pixel                                                                            # Только добавлен подсчет площади (+= так как я нахожу площадь каждой фигуры по отдельности и потом суммирую их)
                    x = int(sum_x / sum_pixel)
                    y = int(sum_y / sum_pixel)
                    cv2.drawContours(img, [c], 0, (0, 0, 0), 2)
                    #cv2.putText(img, str(round(distance_y(y),2))+'   '+ str(y), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #if True:
                    #
                    #    cv2.putText(img, '* Water'+str(len(c)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #else:
                    #    cv2.putText(img, 'Posadca Water'+str(len(c)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
                    #cv2.putText(img,'@'+ str(sum_pixel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

                    cv2.putText(img, str(len(approx)), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img,'*'+ str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #print(abs(c[0,0,0] - c[len(c)//2,0,0]),'x1')
                    #print(math.sqrt(2)*abs(c[0,0,0] - c[(len(c)*3)//4,0,0]),'x2')
                    #print(c[[[0]]] - c[[[len(c)//2]]]- c[[[0]]] + c[[[(len(c)*3)//4]]])
                    #mas2.append([x,y])                                                                        # Добавление каждой фигуры для подсчета колличества (С сохранением координат объектов)
            except:pass
    except:pass
    
    thresh = cv2.morphologyEx(mask3, cv2.MORPH_CLOSE, st1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    seed = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                                  # Поиск контуров в облаке точек (Красном)
    
    try:
        for c in seed[0]:
            try:
                
                #print(len(c))
                approx = cv2.approxPolyDP(c, 0.01* cv2.arcLength(c, True), True)
                moments = cv2.moments(c, 1)
                sum_y = moments['m01']
                sum_x = moments['m10']
                sum_pixel = moments['m00']
                if sum_pixel > 2500:
                    x = int(sum_x / sum_pixel)
                    y = int(sum_y / sum_pixel)
                    cv2.drawContours(img, [c], 0, (0, 0, 0), 2)    
                    #cv2.putText(img, str(round(distance_y(y),2))+'   '+ str(y), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #if len(approx) < 10:
                    #    cv2.putText(img, 'Seed'+str(len(approx)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))                       
                    #else:
                 #   cv2.putText(img,'@'+ str(sum_pixel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    cv2.putText(img, str(len(approx)), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

                    #    cv2.putText(img, 'Posadca'+str(len(approx)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            except:pass
    except:pass
    
    thresh = cv2.morphologyEx(mask4, cv2.MORPH_CLOSE, st1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    pastures = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                               # Поиск контуров в облаке точек (Красном)
    try:
        for c in pastures[0]:
            try:
                approx = cv2.approxPolyDP(c, 0.01* cv2.arcLength(c, True), True)
                moments = cv2.moments(c, 1)
                sum_y = moments['m01']
                sum_x = moments['m10']
                sum_pixel = moments['m00']
                if sum_pixel > 2500:
                    x = int(sum_x / sum_pixel)
                    y = int(sum_y / sum_pixel)
                    cv2.drawContours(img, [c], 0, (0, 0, 0), 2)
                    #cv2.putText(img, str(round(distance_y(y),2))+'   '+ str(y), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

                    #cv2.drawContours(img, [c], 0, (0, 0, 0), 2)
                    #cv2.putText(img,'@'+ str(sum_pixel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    cv2.putText(img, str(len(approx)), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #if len(approx) < 10:
                    #    cv2.putText(img, 'Pastures'+str(len(approx)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))                       
                    #else:
                    #    cv2.putText(img, 'Posadca'+str(len(approx)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    
            except:pass
    except:pass
    
    thresh = cv2.morphologyEx(mask5, cv2.MORPH_CLOSE, st1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    soil = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)                                  # Поиск контуров в облаке точек (Красном)
    try:
        for c in soil[0]:
            try:
                moments = cv2.moments(c, 1)
                sum_y = moments['m01']
                sum_x = moments['m10']
                sum_pixel = moments['m00']
                if sum_pixel > 2500:
                    x = int(sum_x / sum_pixel)
                    y = int(sum_y / sum_pixel)
                    cv2.drawContours(img, [c], 0, (0, 0, 0), 2)
                    #cv2.putText(img, str(round(distance_y(y),2))+'   '+ str(y), (x, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #cv2.putText(img, str(round(distance_x(x),2))+'   '+ str(x), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    cv2.putText(img,'@'+ str(sum_pixel), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

                    #if len(c) < 10:
                    #    cv2.putText(img, '* Soil'+str(len(c)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    #else:
                    #    cv2.putText(img, 'Posadca Soil', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            except:pass
    except:pass
    
    
    cv2.imshow("camera", img)                                                                             # Вывод финального изображения на дисплей
    if cv2.waitKey(10) == 27:                                                                             # Вывод из программы на кнопку ESC
        break                                                                       
        
cap.release()
#out.release()
cv2.destroyAllWindows() 