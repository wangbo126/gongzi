#!/usr/bin/env python3
import sys
import csv
import os
import time
from multiprocessing import Process,Queue

queue1 = Queue()
queue2 = Queue()


class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        self.get_args(self.args)

    def get_args(self,line_args):
        #mytmp_list = []
        try:
            index = line_args.index('-c')
            self.config_file = line_args[index+1]
        except ValueError:
            print("args -c error!")
            exit(-1)

        #mytmp_list.append(self.config_file)
        try:
            index = line_args.index('-d')
            self.user_file = line_args[index+1]
        except ValueError:
            print("args -d error!")
            exit(-2)

        #mytmp_list.append(self.user_file)
        try:
            index = line_args.index('-o')
            self.gongzi_file = line_args[index+1]
        except ValueError:
            print("args -o error!")
            exit(-3)

        #mytmp_list.append(self.gongzi_file)
        
        #print(mytmp_list)
        #print(self.config_file,self.user_file,self.gongzi_file)
        #return self.config_file,self.user_file,self.gongzi_file
        #return mytmp_list
        return None
        

class Config(object):
    config_dict = {}
    def __init__(self,configfile):
        self._config = self._read_config(configfile)

    def _read_config(self,configfile):
        #config_dict = {}

        with open(configfile,'r') as cf:
            for line in cf:
                mylist = (line.strip()).split("=")
                self.config_dict[mylist[0].strip()] = mylist[1].strip()

        return self.config_dict


class IncomeTaxcalculator(object):

    def __init__(self,conf_dict,userdata):
        self.gongzi_list = self.jisuan_gongzi(conf_dict,userdata)

    def jisuan_gongzi(self,conf_dict,userdata):
        gongzi_list = []
        
        jiaofei_bili = float(conf_dict['YangLao']) + float(conf_dict['YiLiao']) + float(conf_dict['ShiYe']) + float(conf_dict['GongShang']) + float(conf_dict['ShengYu']) + float(conf_dict['GongJiJin'])
        
        shui_qian_gongzi = float(userdata[-1][1])
        if shui_qian_gongzi < float(conf_dict['JiShuL']) :
            she_bao = float(conf_dict['JiShuL']) * jiaofei_bili
        elif shui_qian_gongzi > float(conf_dict['JiShuH']) :
            she_bao = float(conf_dict['JiShuH']) * jiaofei_bili
        else :
            she_bao = shui_qian_gongzi * jiaofei_bili

        ying_na_shui_e = (shui_qian_gongzi - she_bao - 3500)
        if ying_na_shui_e > 80000 :
            ying_na_shui = (ying_na_shui_e * 0.45 - 13505)
        elif ying_na_shui_e > 55000 :
            ying_na_shui = (ying_na_shui_e * 0.35 - 5505)
        elif ying_na_shui_e > 35000 :
            ying_na_shui = (ying_na_shui_e * 0.30 - 2755)
        elif ying_na_shui_e > 9000 :
            ying_na_shui = (ying_na_shui_e * 0.25 - 1005)
        elif ying_na_shui_e > 4500 :
            ying_na_shui = (ying_na_shui_e * 0.20 - 555)
        elif ying_na_shui_e > 1500 :
            ying_na_shui = (ying_na_shui_e * 0.10 - 105)
        elif ying_na_shui_e > 0 :
            ying_na_shui = (ying_na_shui_e * 0.03)
        else :
            ying_na_shui = 0

        shui_huo_gongzi = (shui_qian_gongzi - ying_na_shui - she_bao)

        gongzi_list.append(userdata[-1][0])
        gongzi_list.append(userdata[-1][1])
        gongzi_list.append(str(format(she_bao,".2f")))
        gongzi_list.append(str(format(ying_na_shui,".2f")))
        gongzi_list.append(str(format(shui_huo_gongzi,".2f")))

        return gongzi_list
        #return a list for cun fang shui huo gongzi

# *************
#"""
#class UserData(object):
#
#    def __init__(self,userfile,conf_dict,gongzi_file):
#        self.userdata = self._read_users_data(userfile,conf_dict,gongzi_file)
#
#    def _read_users_data(self,userfile,conf_dict,gongzi_file):
#        userdata = []
#        with open(gongzi_file,'w+') as gf:
#
#            with open(userfile,'r') as uf:
#                for line in uf:
#                    userdata.append((line.strip()).split(","))
#                    #userdata is 2 wei shuzu
#                    income_tax = IncomeTaxcalculator(conf_dict,userdata)
#                    print(income_tax.gongzi_list)
#                    csv.writer(gf).writerow(income_tax.gongzi_list)
#
#
#        return userdata
#"""

def proc1(*args):
    userfile = args[1]
    userdata = []
    with open(userfile,'r') as uf:
        for line in uf:
            userdata.append((line.strip()).split(','))
            queue1.put(userdata)
            print('Send userdata :{}'.format(userdata))
            time.sleep(1)

def proc2(*args):
    conf_dict = args[2]
    #gongzi_list = []
    income_tax = IncomeTaxcalculator(conf_dict,queue1.get())

    queue2.put(income_tax.gongzi_list)
    print('Send gongzi_list :{}'.format(income_tax.gongzi_list))
    time.sleep(1)
def proc3(*args):
    gongzi_file = args[1]
    with open(gongzi_file,'w+') as gf:
        gf.seek(2,0)
        csv.writer(gf).writerow(queue2.get())
        time.sleep(1)






if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print("Usage:{} -c test.cfg -d user.csv -o gongzi.csv".format(sys.argv[0]))
    else:
        chuli_args = Args()
        #print(chuli_args.config_file)
        #print(chuli_args.user_file)
    
        
        chuli_config = Config(chuli_args.config_file)
        #print(chuli_config.config_dict)
        
        #chuli_user = UserData(chuli_args.user_file,chuli_config.config_dict,chuli_args.gongzi_file)
        #print(chuli_user.userdata)

        #Process(target = proc1,args=(queue1,chuli_args.user_file)).start()
        #Process(target = proc2,args=(queue1,queue2,chuli_config.config_dict)).start()
        #Process(target = proc1,args=(queue2,chuli_args.gongzi_file)).start()
        p1 = Process(target = proc1,args=(queue1,chuli_args.user_file))
        p2 = Process(target = proc2,args=(queue1,queue2,chuli_config.config_dict))
        p3 = Process(target = proc1,args=(queue2,chuli_args.gongzi_file))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()



