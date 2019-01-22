#!/usr/bin/env python3
import sys
import csv
import os
import getopt
import configparser
import datetime


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
class myConfig(object):
    def __init__(self,cityname,configfile):
        self.config_dict = {}
        self.my_config = self.read_config(cityname,configfile)

    def read_config(self,cityname,configfile):
        cf = configparser.ConfigParser()
        cf.read(configfile)
        self.config_dict = dict(cf.items(cityname))

        return self.config_dict


class IncomeTaxcalculator(object):

    def __init__(self,conf_dict,userdata):
        self.gongzi_list = self.jisuan_gongzi(conf_dict,userdata)

    def jisuan_gongzi(self,conf_dict,userdata):
        gongzi_list = []
        
        jiaofei_bili = float(conf_dict['yanglao']) + float(conf_dict['yiliao']) + float(conf_dict['shiye']) + float(conf_dict['gongshang']) + float(conf_dict['shengyu']) + float(conf_dict['gongjijin'])
        
        shui_qian_gongzi = float(userdata[-1][1])
        if shui_qian_gongzi < float(conf_dict['jishul']) :
            she_bao = float(conf_dict['jishul']) * jiaofei_bili
        elif shui_qian_gongzi > float(conf_dict['jishuh']) :
            she_bao = float(conf_dict['jishuh']) * jiaofei_bili
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
        t = datetime.datetime.now()
        gongzi_list.append(t.strftime("%Y-%m-%d %H:%M:%S"))

        return gongzi_list
        #return a list for cun fang shui huo gongzi


class UserData(object):

    def __init__(self,userfile,conf_dict,gongzi_file):
        self.userdata = self._read_users_data(userfile,conf_dict,gongzi_file)

    def _read_users_data(self,userfile,conf_dict,gongzi_file):
        userdata = []
        with open(gongzi_file,'w+') as gf:

            with open(userfile,'r') as uf:
                for line in uf:
                    userdata.append((line.strip()).split(","))
                    #userdata is 2 wei shuzu
                    income_tax = IncomeTaxcalculator(conf_dict,userdata)
                    print(income_tax.gongzi_list)
                    csv.writer(gf).writerow(income_tax.gongzi_list)


        return userdata





if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print("Usage:{} -C cityname -c test.cfg -d user.csv -o gongzi.csv".format(sys.argv[0]))
    else:
        #chuli_args = Args()
        #print(chuli_args.config_file)
        #print(chuli_args.user_file)
        
        myoptlist,myargs = getopt.getopt(sys.argv[1:],"C:c:d:o:")
        #print("myoptlist = {}\nmyargs = {}".format(myoptlist,myargs))
        myargs_dict = {}
        myargs_dict = dict(myoptlist)
        #print("myargs_dict = {} ".format(myargs_dict))
        #print("myargs_dict['-C'] = {} ".format(myargs_dict['-C']))
        
        chuli_config = myConfig(myargs_dict['-C'].upper(),myargs_dict['-c'])
        #print("chuli_config.config_dict = {}".format(chuli_config.config_dict))
        
        #chuli_config = Config(chuli_args.config_file)
        #print(chuli_config.config_dict)
        
        #chuli_user = UserData(chuli_args.user_file,chuli_config.config_dict,chuli_args.gongzi_file)
        #print(chuli_user.userdata)
        #print("****************")
        #print(myargs_dict['-d'])
        #print(chuli_config.config_dict)
        #print(myargs_dict['-o'])
        #print("^^^^^^^^^^^^^^^^")
        chuli_user = UserData(myargs_dict['-d'],chuli_config.config_dict,myargs_dict['-o'])
        #print(chuli_user.userdata)





