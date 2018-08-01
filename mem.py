#-*- coding: UTF-8 -*-
#aa监测内存信息
# 1、adb shell top
#     vss(虚拟内存)、rss（实际使用物理内存）
# 2、adb shell top -d(指定刷新频率) 3（刷新频率具体数值）| grep com.wudaokou.*  >(重定向) meminfo.csv

#控制类
import csv
import os
import time
import threading

import re


class Controller(object):

    def __init__(self):
        #self.counter = count
        #保存数据到列表 时间、虚拟内存、物理内存、名
        self.allData = [("timestamp", "VSS", "RSS", "CPU","User","System","name")]
        #self.second = ''
        self.totalTime = ''
        self.system = ''
        self.user=''
        self.CPU =''
        self.vss = ''
        self.rss = ''
        self.name =''


    #运行命令获取数据
    def getMemInfo(self, device):
        # 保存数据
        meminfo = open("meminfo.csv", 'w')
        #cmd = 'adb -s %s:5555 shell top -m 2 -n 1 | grep org.suirui.huijian.tv' % device
        cmd = 'adb -s %s:5555 shell top -m 2 -n 1' % device

        #读取几秒钟取一次数据
        #second = input("请设置频率（s）: ")
        #设置持续时间
        # self.totalTime = input("持续时间（s）: ")
        # locTime = self.getCurrentTime()
        #  while (self.totalTime + locTime) >
        # #每10秒钟获取一次com.wudaokou.*的内存信息
        # #result = os.popen("adb shell top -d " + second + " | findstr com.wudaokou.*")
        while True:
            result = os.popen(cmd)
            print(result)
            for line in result.readlines():
                m = re.search(r'User\s*(\d+)%,\s*System\s*(\d+)%,\s*IOW\s*(\d+)%,\s*IRQ\s*(\d+)%', line)
                if m:
                    print(line)
                    ret = {"User": int(m.group(1)), "System": int(m.group(2)), "IOW": int(m.group(3)), "IRQ": int(m.group(4))}
                    self.user = int(m.group(1))
                    self.system = int(m.group(2))
                    #print(ret)
                else:
                    if 'org.suirui.huijian.tv' in line:
                        #print 'Exist'
                        print(line)
                        data_list = line.split()
                        self.CPU = data_list[2]
                        self.vss = data_list[5]
                        self.rss = data_list[6]
                        self.name = data_list[9]
                        print(self.rss)
                    else:
                        #print 'Not exist'
                        continue


            currentTime = self.getCurrentTime()
            self.allData.append((currentTime, self.vss, self.rss,self.CPU,self.user,self.system,self.name))
            writer = csv.writer(meminfo)
            writer.writerows(self.allData)
            self.allData.pop()
            self.allData = []

            time.sleep(1)

        meminfo.close()
    #print(self.allData)


    #获取当前时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

def GetMem():
    controller = Controller()
    controller.getMemInfo('10.10.6.112')
    global timer
    timer = threading.Timer(2.0, GetMem)
    timer.start()



if __name__ == '__main__':
    #timer = threading.Timer(2.0, GetMem)
    #timer.start()
    controller = Controller()
    controller.getMemInfo('10.10.6.112')
