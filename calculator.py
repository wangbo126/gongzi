#!/usr/bin/env python3
import sys
import csv
import os

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
    def __init__(self,configfile):
        self._config = self._read_config(configfile)

    def _read_config(self,configfile):
        config_dict = {}

        with open(configfile,'r') as cf:
            for line in cf:
                mylist = (line.strip()).split("=")
                self.config_dict[mylist[0]] = mylist[1]

        return self.config_dict

class UserData(object):

    def __init__(self,userfile):
        self.userdata = self._read_users_data(self,userfile)

    def _read_users_data(self,userfile):
        userdata = []
        with open(userfile,'r') as uf:
            for line in uf:
                userdata.append((line.strip()).split(","))
                #userdata is 2 wei shuzu
        return userdata

class IncomeTaxcalculator(object):

    def calc_for_all_userdata(self,userdata):
        pass






if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print("Usage:{} -c test.cfg -d user.csv -o gongzi.csv".format(sys.argv[0]))
    else:
        chuli_args = Args()
        #print(chuli_args.config_file)





