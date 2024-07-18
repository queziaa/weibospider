import socket
import time
import sys
import os
import datetime
import subprocess
import requests
import string
import random
import time
import threading
import re


dir = '/mnt/hgfs/Distributed/'
encode='UTF-8'
MAXthreadVALUE = 1
CORETIME = 0.1
MAXthread = threading.Semaphore(MAXthreadVALUE)
netId = ['32309233','225310','32309245','122957','32309248','170039','32309264','06061X','32309208','018335','32309258','154615','32309237','260047','32309168','13661X','32309276','172357','32309188','03001X','32309268','040031','32309203','300032','32309244','278114','32309178','063718','32309228','202093','32309242','170015','32309186','183619','32309205','150031','32309252','243187','32309218','121250','32309206','290219','32309254','100017','32309223','026013','32309225','272967','32309211','273910','32309199','183018','32309215','130618','32309278','273624','32309204','131919','32309209','116826','32309212','160914','32309222','165672','32309271','102418','32309182','262510','32309200','27081X','32309261','166713','32309277','060535','32309265','085138','32309195','084819','32309169','237318','32309227','091214','32309210','192019','32309251','261513','32309250','101834','32309189','242473','32309247','22541X','32309275','013713','32309272','100554','32309235','02551X','32309196','146812','32309187','190616','32309197','221212','32309207','17305X','32309201','275415','32309262','174199','32309190','080140','32309243','300310','32309192','231029','32309193','252724','32309263','023910','32309226','132617','32309177','073011','32309219','047346','32309230','100626','32309231','110031','32309234','113032','32309279','296915','32309260','032822','32309236','306413','32309238','270512','32309213','034413','32309172','260599','32309273','290627','32309166','050051','32309246','30771X','32309221','104221','32309255','031130','32309176','141013','32309185','284514','32309240','203515','32309202','010010','32309171','284671','32309266','231198','32309198','300513','32309170','109391','32309253','134767','32309175','123875','32309165','220023','32309224','062532','32309229','120119','32309184','060011','32309217','015619','32309174','087819','32309269','270010','32309256','105228','32309274','256109','32309257','081213','32309180','173916','32309194','031212','32309267','143919','32309191','230075','32309259','146410','32309181','160261','32309249','106036','32309214','08131X','32309220','22071X','32309270','096625','32309179','010025','32309239','246640','32309216','141019','32309183','291614','32309173','261213','32309232','080013','32309167','112028']
work_filesSet = []
cache = []
def find_files_starting(directory,n,ip=False):
    out = []
    if ip:
        for f in os.listdir(directory):
            if f.find('_') == -1:
                continue
            ff = f.split('_')[1]
            if ip == ff:
                ff = int(f.split('_')[0])
                if ff != n:
                    out.append(f)
    else:
        for f in os.listdir(directory):
            if f.find('_') == -1:
                continue
            tt = f.split('_')[0]
            if tt == 'ip':
                continue
            ff = int(tt)
            if ff == n:
                out.append(f)

    print("@@@Files found:", out)
    return out

def read_and_delete_first_line(dir,log):
    global work_filesSet
    global cache
    if cache != []:
        # return cache.pop(0)
        return True

    if work_filesSet == []:
        for item in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, item)) and item.startswith('work'):
                work_filesSet.append(dir + item)
    if not work_filesSet:
        print("@@@No 'works' files found.",log)
        return False
    filename = random.choice(work_filesSet)
    print("@@@Reading file", work_filesSet,filename,log)
    if not os.path.exists(filename):
        work_filesSet.remove(filename)
        print("@@@File", filename, "has been removed.",log)
        return False
    print("@@@Reading file", filename,log)
    with open(filename, 'r',encoding=encode) as file:
        lines = file.readlines()
    if not lines or not lines[0].strip():
        print("@@@The first line is empty.",log)
        if len(lines) == 0:  # the file is empty after removing the first line
            os.remove(filename)
            print(f"@@@File {filename} has been removed.",log)
            return False
        else:
            lines.pop(0)  # remove the first line
            with open(filename, 'w',encoding=encode) as file:
                file.writelines(lines)
            print('@@@Delete blank line',log)
            return False
        
    with open(filename, 'r',encoding=encode) as file:
        lines = file.readlines()
    try:
        # first_line = lines.pop(0).strip()  # read and remove the first line
        cache = []
        for i in range(30):
            if len(lines) == 0:
                break
            cache.append(lines.pop(0).strip())
    except Exception as e:
        return False
    with open(filename, 'w',encoding=encode) as file:
        file.writelines(lines)
    # return cache.pop(0)
    return True


def read_specific_line(filename, line_number):
    line_number = line_number%4
    if line_number == 0:
        line_number = 4
    line_number = (line_number - 1) * 2 + 1
    with open(filename, 'r',encoding=encode) as file:
        lines = file.readlines()
        return [lines[line_number - 1].strip(),lines[line_number].strip()]


def read_cookies(uname, f):
    dict = {item.split('=')[0]: item.split('=')[1] for item in f.split('; ')}
    end = []
    for cookie in dict:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie,
            'value': dict[cookie],
            'expires': '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        end.append(cookie_dict)
    s = requests.Session()
    for cookie in end:
        s.cookies.set(cookie['name'], cookie['value'])
    try:
        # response = s.get("https://weibo.com")
        # 限制时间为2s
        response = s.get("https://weibo.com", timeout=2)
    except :
        return False
    response.encoding = response.apparent_encoding
    html_t = response.text
    # 检测页面是否包含微博用户名
    return html_t.find(uname) != -1

# 函数 在300至200次调用后返回 1 次true 之外一直返回false
random_true_count = (2*MAXthreadVALUE - 1) * -1
def random_true():
    global random_true_count
    if random_true_count < 0:
        random_true_count += 1
        if random_true_count >= 0:
            random_true_count = 400
        return True
    else:
        random_true_count -= random.randint(1, 2)
        if random_true_count < 0:
            random_true_count = (2*MAXthreadVALUE - 1) * -1
        return False


def be(mode,keywords,start_time,end_time,proxy,cookie):
    code = {}
    codaHttps = 0
    # text = '''def set():
    # return{'''
    text = '{'
    # filename = "./temp/set.py"
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    text = text +  ''''mode':'{}','keywords':'{}','end_time':'{}','start_time':'{}','now':'{}','proxy':'{}','cookie':'{}' '''.format(mode,keywords,end_time,start_time,now,proxy,cookie) + '}'
    # if os.path.exists(filename):
        # Fmode = 'w'  # set mode to write to existing file
    # else:
        # Fmode = 'x'  # set mode to create new file
    # with open(filename, Fmode ,encoding=encode) as f:
        # f.write(text)
    
    filename= dir + "output/{}_{}_{}_{}_{}.txt".format(keywords,end_time,start_time,now,mode)
    outlog = mode+" "+keywords+" "+start_time+" "+end_time+" "+now+" "+proxy+" "+cookie
    if os.path.exists(filename):
        Fmode = 'w'  # set mode to write to existing file
    else:
        Fmode = 'x'  # set mode to create new file
    with open(filename, Fmode,encoding=encode) as f:
        f.write(outlog)
    # 定义要运行的命令
    command = ['python3', 'run_spider.py', keywords,text,dir]
####################################################################################
    # 打开一个文件来保存输出
    with open(filename.replace('txt','log'), 'w',encoding=encode) as f:
        # 运行命令并将输出写入文件
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # encode2 = 'gbk'
        encode2 = 'UTF-8'
        for line in iter(process.stdout.readline, b''):
            de = line.decode(encode2)
            f.write(de)
            if 'wled (' in de:
                codaHttps = codaHttps + 1
                de = de.split('led (')[1]
                de = de.split(') <')[0]
                if len(de) <5:
                    if de in code:
                        code[de] = code[de] + 1
                    else:
                        code[de] = 1
        #将网络结果code写入文件
        f.write(str(code))
    process.wait()
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # # encode2 = 'gbk'
    # encode2 = 'UTF-8'
    # for line in iter(process.stdout.readline, b''):
    #     de = line.decode(encode2)
    #     if de[0] == '2':
    #         if 'Crawled' in de:
    #             codaHttps = codaHttps + 1
    #             de = de.split('<')[0]
    #             de = de.split('Crawled')[1]
    #             de = de.replace(' ','')
    #             de = de[1:-1]
    #             if len(de) <5:
    #                 if de in code:
    #                     code[de] = code[de] + 1
    #                 else:
    #                     code[de] = 1
    #将网络结果code写入文件
    with open(filename, 'a',encoding=encode) as f:
        f.write(str(code))
    return [code,codaHttps]

def ping_website(website):
    try:
        output = subprocess.check_output("ping -c 1 -w 1 " + website, shell=True)
        output = output.decode("utf-8")

        if "1 packets transmitted, 1 received" in output:
            return True
        else:
            return False
    except Exception as e:
        print("@@@No Internet connection")
        return False

def find_ipv4_addresses(string):
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    for i in re.findall(pattern, string):
        if i != '127.0.0.1':
            return i
        
def connected(ID):
    random_int = random.randint(0, len(netId)/2-1)
    print("@@@Attempting to log in to the campus network U&P: ",netId[random_int*2],netId[random_int*2+1])
    output = subprocess.check_output("ip a", shell=True)
    output = output.decode("utf-8")
    innerIP = find_ipv4_addresses(output)
    filename = "./temp/" + ID + ".json"
    text = '''{"server":"http://172.31.99.50","strict_bind":false,"double_stack":false,"retry_delay":300,"retry_times":1,"n":200,"type":1,"acid":4,"os":"Windows","name":"Windows98","users":[{"username":"'''
    text = text + '''{}","password":"{}","ip":"{}'''.format(netId[random_int*2],netId[random_int*2+1],innerIP)
    text = text + '''"}]}'''
    if os.path.exists(filename):
        mode = 'w'  # set mode to write to existing file
    else:
        mode = 'x'  # set mode to create new file
    with open(filename, mode, encoding=encode) as f:
        f.write(text)
    response = os.popen("./sdusrun1 login -c " + filename).read()
    return response

def get_data_from_api():
    try:
        response = requests.get("https://www.ipplus360.com/getIP",timeout=(2,3))
        data = response.json()
        return data['data']
    except Exception as e:
        print("@@@Failed to obtain IP address BY http API")
        return None
    
def task(Wmode,keyWord,co,ip,ID):
    start_time = '0'
    end_time = '0'
    if Wmode == 'tweet_by_keyword':
        keyWord = keyWord.split('/')
        start_time = keyWord[1]
        end_time = keyWord[2]
        keyWord = keyWord[0]
    else:
        keyWord = keyWord
        start_time = '0'
        end_time = '0'
        
    recode = be(Wmode,keyWord,start_time,end_time,'0',co[1])
    print('@@@ID:', ID + ' IP: ' + ip + ' Task: ', first_line,'mode: ', Wmode, ' result: ', recode,' thread: ',MAXthread._value,'-',MAXthreadVALUE)
    if '414' in recode[0]:
        print('@@@414 error 120s retry',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
        time.sleep(120)
    MAXthread.release()

if __name__ == '__main__':
    if type(sys.argv[1])==str:
        index = int(sys.argv[1])
    else:
        index = sys.argv[1]
    cookieLose = False
    ipccupy = False
    workNull = False
    ip = ''
    co = read_specific_line(dir + "cookies.txt", index)
    ID = str(index)
    print('@@@**********************************')
    while True:
        MAXthread.acquire()
        time.sleep(CORETIME)
        if random_true(): 
            if ping_website("weibo.com") == False:
                print('@@@No Internet connection',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
                connected(ID)
                time.sleep(5)
                MAXthread.release()
                random_true_count = (2*MAXthreadVALUE - 1) * -1
                continue
            temp = get_data_from_api()
            if temp == None:
                MAXthread.release()
                random_true_count = (2*MAXthreadVALUE - 1) * -1
                continue
            elif ip != temp:
                # 搜 dir 下面所有 ip_ 开头的文件
                fileList = []
                for f in os.listdir(dir):
                    if f.find('ip_') == 0:
                        fileList.append(f)
                for f in fileList:
                    f = f.split('_')
                    if f[1] == temp and f[2] != ID:
                        print('@@@IP ',temp,' Already occupied',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
                        exit()
                
                for f in os.listdir(dir):
                    if f.find('ip_' + ID) == 0:
                        os.remove(dir + f)
                ip = temp
                with open(dir + 'ip_' + ID + '_' + ip, 'w') as f:
                    pass

                # ipfilename = dir + 'ip_' + ID + '_' + ip
                # with open(dir + , 'w') as f:
                    # pass
        
        if not read_cookies(co[0],co[1]):
            # if not cookieLose:
            print('@@@Cookie fails after 10s retry',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
                # cookieLose = True
            time.sleep(10)
            co = read_specific_line(dir + "cookies.txt", index)
            MAXthread.release()
            continue
        else:
            cookieLose = False        

        # ipFile = find_files_starting(dir,index)
        # filedir = ID + "_" + ip
        # if ipFile != []:
        #     if len(ipFile) > 1:
        #         print('@@@error: ID:' + ID + ' This ID has multiple IP files',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
        #         exit()
        #     ipFile = ipFile[0]
        #     if ipFile != filedir:
        #         os.remove(dir + ipFile)         
        #         with open(dir + filedir, 'w') as f:
        #                 pass
        # else:
        #     with open(dir + filedir, 'w') as f:
        #             pass
        
        # if find_files_starting(dir,index,ip=ip) != []:
        #     if not ipccupy:
        #         print('@@@IP ',ip,' Already occupied',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
        #         ipccupy = True
        #     time.sleep(5)
        #     MAXthread.release()
        #     continue
        # else:
        #     ipccupy = False
        

        
        first_line = ''
        if len(cache)!= 0 or  find_files_starting(dir,0) == []:
            if len(cache)== 0:
                with open(dir + '0_' + ID, 'w') as f:
                    pass
                logtemp = ' thread: ' + str(MAXthread._value) + '-' + str(MAXthreadVALUE)
                first_line = read_and_delete_first_line(dir,logtemp)  # 读取并删除第一行        
                if first_line == False:
                    if not workNull:
                        print('@@@No task',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
                        time.sleep(2)
                        workNull = True
                    os.remove(dir + '0_' + ID)
                    MAXthread.release()
                    continue
                else:
                    workNull = False
                os.remove(dir + '0_' + ID)
            first_line = cache.pop(0)
                
            # first_line = first_line.split('@')
            # Wmode = first_line[0]
            # Wmode = 'follow'
            Wmode = 'comment'
            # Wmode = 'repost'
            keyWord = first_line
            # keyWord = first_line[1]

            print('@@@ID:', ID + ' IP: ' + ip + ' Task: ', keyWord, 'mode: ', Wmode,' thread: ',MAXthread._value,'-',MAXthreadVALUE)
            t1 = threading.Thread(target=task, args=(Wmode,keyWord,co,ip,ID)).start()
            # task(Wmode,keyWord,co,ip,ID)
        else:
            print('@@@Other programs after reading the task list, review after 5 seconds',' thread: ',MAXthread._value,'-',MAXthreadVALUE)
            time.sleep(5)
            MAXthread.release()