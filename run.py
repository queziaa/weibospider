import socket
import time
import sys
import os
import datetime
import subprocess
import requests
import string
import random


dir = '/mnt/hgfs/Distributed/'
encode='UTF-8'
netId = ['32309233','225310',
'32309168','13661X',
'32309276','172357',
'32309188','03001X',
'32309268','040031',
'32309203','300032',
'32309178','063718',
'32309228','202093',
'32309242','170015',
'32309186','183619',
'32309205','150031',
'32309252','243187',
'32309218','121250',
'32309254','100017',
'32309223','026013',
'32309211','273910',
'32309199','183018',
'32309215','130618',
'32309278','273624',
'32309204','131919',
'32309209','116826',
'32309212','160914',
'32309222','165672',
'32309271','102418',
'32309182','262510',
'32309200','27081X',
'32309261','166713',
'32309277','060535',
'32309265','085138',
'32309169','237318']

def find_files_starting(directory,n,ip=False):
    out = []
    if ip:
        for f in os.listdir(directory):
            if ip in f:
                if f.find('_') == -1:
                    continue
                ff = int(f.split('_')[0])
                if ff != n:
                    out.append(f)
    else:
        for f in os.listdir(directory):
            if f.find('_') == -1:
                continue
            ff = int(f.split('_')[0])
            if ff == n:
                out.append(f)
    return out
def read_and_delete_first_line(filename):
    with open(filename, 'r',encoding=encode) as file:
        lines = file.readlines()
    first_line = lines.pop(0).strip()  # read and remove the first line

    with open(filename, 'w',encoding=encode) as file:
        if first_line[0] == 'Q':
            file.write('Q')
            return False
        for line in lines:
            file.write(line)
    return first_line


def read_specific_line(filename, line_number):
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
    response = s.get("https://weibo.com")
    response.encoding = response.apparent_encoding
    html_t = response.text
    # 检测页面是否包含微博用户名
    return html_t.find(uname) != -1

def be(mode,keywords,start_time,end_time,proxy,cookie):
    code414 = 0
    codaHttps = 0
    text = '''def set():
    return{'''
    filename = "./temp/set.py"
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    text = text +  ''''mode':'{}','keywords':'{}','end_time':'{}','start_time':'{}','now':'{}','proxy':'{}','cookie':'{}' '''.format(mode,keywords,end_time,start_time,now,proxy,cookie) + '}'
    if os.path.exists(filename):
        mode = 'w'  # set mode to write to existing file
    else:
        mode = 'x'  # set mode to create new file
    with open(filename, mode,encoding=encode) as f:
        f.write(text)
    
    filename= dir + "output/{}.txt".format(now)
    text = mode+" "+keywords+" "+start_time+" "+end_time+" "+now+" "+proxy+" "+cookie
    if os.path.exists(filename):
        mode = 'w'  # set mode to write to existing file
    else:
        mode = 'x'  # set mode to create new file
    with open(filename, mode,encoding=encode) as f:
        f.write(text)
    # 定义要运行的命令
    command = ['python3', 'run_spider.py']
    filename= dir + "output/{}.log".format(now)
    # 打开一个文件来保存输出
    with open(filename, 'w',encoding=encode) as f:
        # 运行命令并将输出写入文件
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # encode2 = 'gbk'
        encode2 = 'UTF-8'
        for line in iter(process.stdout.readline, b''):
            de = line.decode(encode2)
            f.write(de)
            if '414' in de:
                code414 = code414 + 1
            if 'https' in de:
                codaHttps = codaHttps + 1
            # print(de, end='')
    # 等待命令运行完成
    process.wait()
    return [code414,codaHttps]

def ping_website(website):
    try:
        output = subprocess.check_output("ping -c 1 " + website, shell=True)
        output = output.decode("utf-8")

        if "1 packets transmitted, 1 received" in output:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def connected(ID):
    response = ping_website("weibo.com")
    if response == False:
        random_int = random.randint(0, 29)  # 生成0至30的随机整数
        print("尝试登录校园网",ID)
        filename = "./temp/" + ID + ".json"
        text = '''{"server":"http://172.31.99.50","strict_bind":false,"double_stack":false,"retry_delay":300,"retry_times":1,"n":200,"type":1,"acid":4,"os":"Windows","name":"Windows98","users":[{"username":"'''
        text = text + '''{}","password":"{}","ip":"{}'''.format(netId[random_int*2],netId[random_int*2+1],socket.gethostbyname(socket.gethostname()))
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
        response = requests.get("https://www.ipplus360.com/getIP")
        data = response.json()
        return data['data']
    except Exception as e:
        print("获取IP失败: ",e)
        return None
if __name__ == '__main__':
    index = int(sys.argv[1])
    cookieLose = False
    ipccupy = False
    workNull = False
    code414 = False
    ip = ''
    co = read_specific_line(dir + "cookies.txt", index)
    ID = str(index)
    print('**********************************')
    while True:
        time.sleep(1)
        connected(ID)
        ip = get_data_from_api()
        if ip == None:
            continue
        temp = find_files_starting(dir,index)
        if temp != []:
            if len(temp) > 1:
                print('错误: ID:' + ID + ' 有多个IP文件')
                exit()
            temp = temp[0]
            os.remove(dir + temp)         
        with open(dir + ID + "_" + ip, 'w') as f:
                pass
        temp = find_files_starting(dir,index,ip=ip)
        if temp != []:
            if not ipccupy:
                print('IP ',ip,' 已被占用')
                ipccupy = True
            continue
        else:
            ipccupy = False

        if not read_cookies(co[0],co[1]):
            if not cookieLose:
                print('cookie失效 10s后重试')
                time.sleep(10)
                cookieLose = True
            co = read_specific_line(dir + "cookies.txt", index)
            continue
        else:
            cookieLose = False
        first_line = ''
        if find_files_starting(dir,0) == []:
            if not code414:
                with open(dir + '0_' + ID, 'w') as f:
                    pass
                first_line = read_and_delete_first_line(dir + 'works.txt')  # 读取并删除第一行        
                os.remove(dir + '0_' + ID)
                if first_line == False:
                    if not workNull:
                        print('无任务')
                        workNull = True
                    continue
                else:
                    workNull = False
                print('ID:', ID + ' IP: ' + ip + ' 任务: ', first_line)

            recode = be('tweet_by_user_id',first_line,'0','0','0',co[1])
            if recode[0] >= 4 and recode[1] == 2:
                if not code414:
                    print('414错误 63s后重试')
                    code414 = True
                time.sleep(63)
            else:
                code414 = False
        else:
            print('有未完成任务')
