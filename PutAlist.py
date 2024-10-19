import requests
import re,os,json
from urllib.parse import quote
def get_token(user,passwd):
    url=pre_fix+"/api/auth/login"
    data={
      "username": user,
      "password": passwd
    }
    res = requests.post(url,json=data)
    token=json.loads(res.text).get("data").get("token")
    os.environ['TOKEN']=token
    return token

def put_file(file_path,path):

    url = pre_fix+"/api/fs/put"
    boundary = ''
    payload = ''
    with open(file_path,"rb") as f:
        content=f.read()
    # file_path=
    path=path+file_name
    header = {
       'Authorization':os.environ['TOKEN'],
       'Content-Length': str(len(content)),
       'File-Path': quote(path),
       'As-Task': 'true',
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarylFuwOB1pQ9f4hvRh',
       'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    res = requests.put(url, data=content, headers=header)
    res2 = res.text
    return file_name + "上传成功"
def traverse_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # 在此处添加对文件的处理逻辑
            file_list.append(file_path)
        else:
            traverse_folder(file_path)  # 递归遍历子文件
def split_string(s):
    # 使用正则表达式来分割字符串，包括'/'和'\'
    parts = re.split(r'[\\/]', s)

    # 去除空字符串，除非字符串本身就是空的
    parts = [part for part in parts if part != ""]

    return parts

if __name__ == '__main__':
    """本代码适用于挂载夸克网盘，理论上都适用"""
    from dotenv import load_dotenv
    load_dotenv()
    pre_fix = os.getenv("PRE_FIX")
    user,passwd=os.getenv("USER_NAME"),os.getenv("PASS_WORD")
    token=get_token(user,passwd)
    basedir = os.getenv("BASE_DIR")
    file_list = []
    traverse_folder(basedir)
    Alist_Path=os.getenv("ALIST_PATH")
    if Alist_Path is None:
        """ 这段是我自己用Alist补充路径 录制直播间自动上传"""
        for file in file_list:
            pt_name,zb_name,file_name=split_string(file)[-3],split_string(file)[-2],split_string(file)[-1]
            if file_name.endswith("mp4"):
                data = file_name.split("_")[-3]
                path = "/{pt_name}/{zb_name}/{data}/{file_name}".format(pt_name=pt_name
                                                                    ,zb_name=zb_name
                                                                    ,data=data
                                                                    ,file_name=file_name)
                put_file(file,path)
                os.remove(file)
    else:
        """自己设置Alist 路径之后用这段就可以了"""
        for file in file_list:
            file_name=split_string(file)[-1]
            path = Alist_Path+file_name
            put_file(file,path)
            os.remove(file)