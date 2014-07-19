# -*- coding: utf8 -*-
__author__ = 'dongdaqing'

import os,codecs,json,shutil
from zipfile import *

class Gen_Channel_Package(object):

    def __init__(self):
        root_path = os.path.dirname(__file__)
        self.pid_file = os.path.join(root_path,'pid_src.txt')
        self.input_ipa_file = os.path.join(root_path,'*.ipa')
        self.ver = 'v3.7_'
        if ('ipad' or 'iPad') in self.input_ipa_file:
            self.ipa_prefix = 'Youku_iPad_'
        else:
            self.ipa_prefix = 'Youku_iPhone_'
        self.channel_ipa_folders = os.path.join(root_path,'channels')
        if not os.path.exists(self.channel_ipa_folders):
            os.mkdir(self.channel_ipa_folders)

    def get_pid_from_file(self,pid_file):
        pid_list=[]
        channel_name = []
        fp = codecs.open(pid_file,'r','utf-8')
        pid_lines = fp.readlines()
        fp.close()
        for line in pid_lines:
            pid = line.split(',')
            pid_list.append(pid[2].strip())
            channel_name.append(pid[0])
        return (channel_name,pid_list)

    def get_settings_file(self,input_ipa_file):
        unzip_file = ZipFile(input_ipa_file,mode='r')
        self.unzip_file = unzip_file
        unzip_file.extractall('.')
        unzip_file.close()
        for name_list in unzip_file.namelist():
            if 'settings.json' in name_list:
                return name_list

    def replace_pid(self,settings_file,pid):
        fp = codecs.open(settings_file,'r','utf-8')
        json_dict = json.load(fp)
        if json_dict.has_key('release'):
            json_dict['release']['pid'] = pid
        output_str = json.dumps(json_dict,ensure_ascii=False)
        output_file = codecs.open(settings_file,'w','utf-8')
        output_file.write(output_str)
        output_file.close()

    def create_ipa(self,channel_name):
        ipa_name = self.channel_ipa_folders+'/'+self.ipa_prefix + self.ver + channel_name + '.ipa'
        zip_file_out = ZipFile(ipa_name,mode='w',compression=ZIP_DEFLATED)
        for file_list in self.unzip_file.namelist():
            zip_file_out.write(file_list)
        zip_file_out.close()

    def remove_unzip_file(self):
        shutil.rmtree(self.unzip_file.namelist()[0])

    def start_package(self):
        channel_name,pid_list = self.get_pid_from_file(self.pid_file)
        print 'start create channel ipas...\n'
        for index in range(len(pid_list)):
            print 'channel name: {0}'.format(channel_name[index])
            print 'channel pid: {0}'.format(pid_list[index])
            settings_file = self.get_settings_file(self.input_ipa_file)
            self.replace_pid(settings_file,pid_list[index])
            self.create_ipa(channel_name[index])
            self.remove_unzip_file()
            print '{0} finished...\n'.format(channel_name[index])

if __name__ == '__main__':

    gen_obj = Gen_Channel_Package()
    gen_obj.start_package()