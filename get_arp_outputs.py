#!/usr/bin/env python
# coding: utf-8
# In[1]:
import os
import re
from datetime import datetime
import textfsm
import pandas as pd
# In[2]:
def get_value(key):
    ''' gets variable values from settings file.
        MAKE SURE TO PUT THE RIGHT SETTINGS FILE PATH '''
    key = key
    plog(f'getting value {key}..')
    try:
        key = key
        with open("find_arp_outputs_settings.txt") as settings_file:
                settings_file = settings_file.read()
        if '#' in settings_file.split(key)[0].split("\n")[-1]:
            msg = 'value is commented out'
            plog(msg)
            return None
        else:
            #var = settings_file.split(key)[1].split("\n")[0].strip(" ").strip("\"").strip("\'")
            #plog(key)
            unstriped = settings_file.split(key)[1].split("\n")[0].strip()
            #plog(unstriped[0])
            if unstriped.lower()[0] ==  '[' and unstriped.lower()[-1] == ']':
                var1 = unstriped.strip('[').strip(']').split(',')
                var = [e.strip().strip("'").strip('"') for e in var1]
                return var
            elif '"' == unstriped[0]  or '"' == unstriped[-1] or "'" == unstriped[0]  or "'" == unstriped[-1]:
                #plog("is string")
                var = unstriped.strip("\"").strip("\'")
                return var
            elif  unstriped.isnumeric():
                var = int(unstriped)
                return var
            elif unstriped.lower() == 'true':
                var = True
                return var
            elif unstriped.lower() ==  'false':
                var = False
                return var
            else:
                plog(f"{unstriped} -invalid variable set in settings")
    except Exception as e:
        try:
            plog(f'EXCEPTION ERROR - get_value() - {e}')
        except:
            plog(f'EXCEPTION ERROR - get_value() - {e}') 
# In[5]:
def plog(string, log_only=False):
    """prints and logs string"""
    root = os.getcwd()
    global session_id #so it wont have to create multiple text file for every plog call. this will ensure that only one text file will be generated for every session.
    string = str(string)
    if log_only == False: #prints if log_only is false default is false
        print(string)
    try:
        session_id = session_id # checks if session_id is defined 
    except:
        from datetime import datetime
        date_now = datetime.now().strftime("%m-%d-%y_%H%M%S")  # defines the session id
        session_id = str(date_now)
    output_folder = r'print_log\\'	# this is the log folder path
    try:
        if os.path.exists(output_folder): # checks if folder already exist, if not the it will create one
            pass
        else:	
            os.mkdir(output_folder)
    except:
        #import os
        if os.path.exists(output_folder): 
            pass
        else:	
            os.mkdir(output_folder)
    with open(f'{root}\\{output_folder}/plog_{session_id}.txt', 'a') as f: #saves the string in the text file 
        f.write(string)
        f.write('\n')
    return
# In[3]:
def current_dir_folder_lister(path):
    """lists the folders in a dir FIRST LEVEL ONLY"""
    path = path 
    current_listdir = os.listdir(path)
    plog(f'listing files in folder {path}')
    #plog(current_dir_list)
    folder_list = []
    for obj in current_listdir: 
        obj_path = f'{path}\\{obj}'  
        if os.path.isdir(obj_path): 
            #plog(obj_path)
            folder_list.append(obj_path)
    return folder_list
def directory_folder_lister(root_path):
    """lists all the folder and subfolder in a directory"""
    root_path = root_path
    list_of_folders = current_dir_folder_lister(root_path)    
    dir_map = [list_of_folders]
    for list_of_folders in dir_map:
        for folder in list_of_folders:
                #plog(current_dir_folder_lister(folder))
                dir_map.append(current_dir_folder_lister(folder))
    return dir_map
def get_text_log_files(device_outputs_folder):
    """gets all the text and log file's path from device_outputs_folder"""
    plog(f"getting all the text and log file's path from device_outputs_folder")
    device_outputs_folder = device_outputs_folder
    folders = []
    folders.append([[device_outputs_folder]])
    folders.append(directory_folder_lister(device_outputs_folder))
    folders_clean = []
    for folder_list in folders:
        for folder_l in folder_list:
            plog(folder_l)
            for folder_path in folder_l:
                #plog(folder_path)
                folders_clean.append(folder_path)
    all_device_output_files = []
    for device_outputs_folder in folders_clean:
        device_output_files = os.listdir(device_outputs_folder)
        #plog(device_output_files)
        for file in device_output_files:
            file = f'{device_outputs_folder}\\{file}'
            if os.path.isfile(file):
                #plog(file)
                if 'log' in file.split('.') or 'txt' in file.split('.'):
                    all_device_output_files.append(file)
    return all_device_output_files
# In[4]:
def get_hostname_from_output_text(file,file_name):
    '''get_hostname_from_output_text'''
    file_name =file_name 
    file = file
    plog(f'get_hostname_from_output_text')
    if 'show' in file and '#' in file:
        hostname = file.split('show')[0].split('\n')[-1].split('#')[0]
    else:
        hostname = f'invalid file--{file_name}'
    plog(f'\t{hostname}')
    return hostname
def store_all_output_text_in_dict(device_outputfiles):
    '''store_all_output_text_in_dict'''
    plog(f'stores all ouput text in a dictionary')
    output_dict = {}
    for file_name in device_outputfiles:
        with open(file_name) as f:
            file = f.read()
        hostname = get_hostname_from_output_text(file,file_name)
        output_dict[hostname.strip()] = file
    return output_dict
def textfsm_the_response(text):   
    text = text
    with open(r"textfsm\\cisco_ios_show_ip_arp.textfsm") as template: 
        re_table = textfsm.TextFSM(template)
        #print(re_table)
    extracted_data = re_table.ParseText(text)
    return extracted_data
def textfsm_the_response_2(text):   
    text = text
    with open(r"textfsm\\cisco_ios_show_ip_arp_2.textfsm") as template: 
        re_table = textfsm.TextFSM(template)
        #print(re_table)
    extracted_data = re_table.ParseText(text)
    return extracted_data
# In[5]:
def main_process(output_dict):
    main_data = []
    output_dict =output_dict
    match_list = []
    no_match_list = []
    arp_data_list = []
    for hostname, text in output_dict.items():    
        try:
            comnd = 0
            arp_patt = "#\s*[sS][hH]\S*\s+[iI][pP]\s+[aA][rR][pP].*" #<<<<< ReGEX for all shortcut of show arp
            arp_match = re.findall(arp_patt , text)
            if len(arp_match) == 0:
                no_match_list.append([hostname, "No arp data found!!!"])
                #continue
            else:
                ############################################################################## match
                for cmd in arp_match:
                    #
                    #print(hostname)
                    #print(cmd)
                    text2 = text.split(cmd)[1].split(f'{hostname}#')[0]
                    ex_dat = textfsm_the_response(text2)
                    #print(len(ex_dat))
                    if len(ex_dat) == 0:
                        ex_dat = textfsm_the_response_2(text2)
                    #print(ex_dat)
                    for line in ex_dat:
                        line.insert(0, cmd)
                        line.insert(0, hostname)
                        #print(line)
                        main_data.append(line)
                ########################################################################################
                match_list.append([hostname, "Found!"])
            arp_data_list.append("_"*80)
            arp_data_list.append(hostname)
            for arp_comm in arp_match:
                try:
                    arp_comm = arp_comm.split("#")[1] 
                except:
                    pass
                arp_data = text.split(arp_comm)[1].split(f"{hostname}#")[0]
                if '% Invalid input detected' in arp_data or "" == arp_data:
                    arp_data = "\nno data"
                try:
                    arp_data = arp_data.split("D - Static Adjacencies attached to down interface")[1]
                except:
                    pass
                #plog(root,hostname)
                #plog(root,arp_match[0] + arp_data)
                #arp_data_list.append(str(arp_match))
                arp_data_list.append(arp_comm + arp_data)
                arp_data_list.append("-----------------")
        except Exception as e:
            plog(e)
    return match_list,no_match_list,arp_data_list, main_data
# In[6]:
def process_output(match_list,no_match_list,arp_data_list,main_data):
    main_data = main_data
    match_list =match_list
    no_match_list =no_match_list
    arp_data_list =arp_data_list
    plog('\n\n')
    plog("_"*80)
    plog('saving..')
    temp_arp_output = []
    temp_arp_output_no_match_list = []
    temp_arp_output.append('\n'.join(arp_data_list))
    for dat in no_match_list:
        match_list.append(dat)
    from tabulate import tabulate
    temp_arp_output.append(tabulate(match_list, headers = ["HOSTNAME", "ARP COMMAND"], tablefmt= "orgtbl"))
    temp_arp_output_no_match_list.append(tabulate(no_match_list, headers = ["HOSTNAME", "ARP COMMAND"], tablefmt= "orgtbl"))
    final_arp_output = '\n'.join(temp_arp_output)
    plog(final_arp_output)
    date_now = datetime.now().strftime("%m-%d-%y_%H-%M-%S")
    out_file_name = f'show_ip_arp_DATA'
    out_file_name_2 = f'NO_MATCH_DATA'
    if os.path.exists('results'): 
        pass
    else:	
        os.mkdir('results')
    '''with open(f'results\\{out_file_name}.txt', 'w') as f:
        f.write(final_arp_output)
    with open(f'results\\{out_file_name_2}.txt', 'w') as f:
        f.write('\n'.join(temp_arp_output_no_match_list))'''
    dict_of_df = {}
    dict_of_df['MAIN REPORT'] =pd.DataFrame(main_data, columns=['HOSTNAME', 'COMMAND', 'IP ADDRESS', 'AGE', 'MAC ADDRESS', 'INTERFACE' ])
    dict_of_df['NO MATCH REPORT'] =pd.DataFrame(no_match_list, columns=['HOSTNAME', 'STATUS'])
    writer = pd.ExcelWriter("results\\arp_report.xlsx")
    for k,v in dict_of_df.items():
        v.to_excel(writer, sheet_name=k, index= False)
    writer.close()
    plog('saved..')
    plog(out_file_name)
# # MAIN
# In[7]:
device_outputs_folder= get_value('inpt_path=') #GET THE PATH TO OUTPUT FOLDERS
device_outputfiles = get_text_log_files(device_outputs_folder) #LIST THE ABSOLUTE PATH OF EACH .LOG .TXT FILE
#plog(len(device_outputfiles))
output_dict = store_all_output_text_in_dict(device_outputfiles) #STORE ALL THE OUTPUT TEXT IN DICTIONARY WITH HOSTNAMES AS KEYS
#plog(len(output_dict))
# In[8]:
match_list,no_match_list,arp_data_list,main_data = main_process(output_dict) #main process
process_output(match_list,no_match_list,arp_data_list,main_data) #output
