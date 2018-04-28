#coding=utf-8
background_image_filename = r'D:/test.jpg'
#mouse_image_filename = 'fugu.png'
#指定图像文件名称
 
import pygame
import time
#导入pygame库
from pygame.locals import *
#导入一些常用的函数和常量
from sys import exit
#向sys模块借一个exit函数用来退出程序
 
pygame.init()
#初始化pygame,为使用硬件做准备
 
screen = pygame.display.set_mode((640,480), RESIZABLE, 32)
#创建了一个窗口
pygame.display.set_caption("Hello, World!")
#设置窗口标题
 
background = pygame.image.load(background_image_filename).convert()
#mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()
#加载并转换图像
font=pygame.font.SysFont("宋体",40)
text=font.render(u"你好",True,(0,0,255))
x_f=0
y_f=(screen.get_height()-text.get_height())/2
x, y = 0, 0
move_x, move_y = 0, 0
while True:
#游戏主循环
 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                #接收到退出事件后退出程序
                pygame.quit()
                exit()
            
        if event.type == KEYDOWN:
            #键盘有按下？
            if event.key == K_LEFT:
                #按下的是左方向键的话，把x坐标减一
                move_x = -1
            elif event.key == K_RIGHT:
                #右方向键则加一
                move_x = 1
            elif event.key == K_UP:
                #类似了
                move_y = -1
            elif event.key == K_DOWN:
                move_y = 1
        elif event.type == KEYUP:
            #如果用户放开了键盘，图就不要动了
                move_x = 0
                move_y = 0
 
        #计算出新的坐标
    x+= move_x
    y+= move_y
    x_f-=2
    if x_f<-text.get_width():
        x_f=screen.get_width()-text.get_width()
    screen.blit(background, (x,y))
    screen.blit(text,(x_f,y_f))
    #screen.fill((0,0,0))
    
        #在新的位置上画图
   # screen.blit(background, (0,0))
    #将背景图画上去
 
#    x, y = pygame.mouse.get_pos()
    #获得鼠标位置
#    x-= mouse_cursor.get_width() / 2
#3    y-= mouse_cursor.get_height() / 2
    #计算光标的左上角位置
#    screen.blit(mouse_cursor, (x, y))
    #把光标画上去
 
    pygame.display.update()
    time.sleep(0.1)
