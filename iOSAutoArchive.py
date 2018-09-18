
# -*- coding: utf-8 -*-
#! python3
import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import urllib
import urllib.request
import json
import base64
import platform
import time



# Sender
mails_Sender = [
                'xxx0@xx.cn' # [XX<收件人0姓名>]
                ]

# Developer
mails_Developer = [
                   'xxx1@xx.cn' # [XX<收件人1姓名>]
                   , 'xxx2@xx.cn' # [XX<收件人2姓名>]
                   , 'xxx3@xx.cn' # [XX<收件人3姓名>]
                   ]

mails_Tester = [
                'xxx4@xx.cn' # [XX<收件人4姓名>]
                , 'xxx5@xx.cn' # [XX<收件人5姓名>]
                , 'xxx6@xx.cn' # [XX<收件人6姓名>]
                ]


to_Emails = {
    "Sender":       mails_Sender,
    "Developer":    mails_Developer,
    "Tester":       mails_Tester,
    # "Porject":      mails_Porject,
    # "Product":      mails_Product,
    # "UI":           mails_UI,
    # "Boss":         mails_Boss,
}

user_home_path = os.environ['HOME']

tempPrj_dir = os.path.dirname(os.path.abspath(__file__))

project_path = '%s/Desktop/[XX<子路径>]' % user_home_path

scheme_name = 'mixc'
exportOptions_path = '%s/Desktop/[XX<子路径>]/_tool/archive/ExportOptions_enterprise.plist' % user_home_path
temp_path = user_home_path
ipa_dir_save_path = '%s/Desktop' % user_home_path

fir_api_token = '[XX<fir 的 token>]'
fir_app_id = '[XX<fir 的 id>]'

commit_num = '20'

#
base64E = b'eWFuZ2ppY[XX<中间隐藏>]xhbmQuY29tLmNu'
base64P = b'MDlB[XX<中间隐藏>]4NjM4OTky'
smtp_server = '[XX<邮件服务器>].com.cn'

#
log_pre_success = '✅ =====>'
log_pre_failure = '❌ =====>'

#
def pull_project():
    global build_startTimestamp
    build_startTimestamp = time.time()

    print('%s start pull_project' % (log_pre_success))

    os.chdir("%s" % project_path)
    ret = os.system('git pull')
    if ret == 0:
        print('%s pull_project success' % (log_pre_success))

        global current_git_branch
        current_git_branch = os.popen('git symbolic-ref --short -q HEAD').read().replace('\n', '')
        print('current_git_branch: %s' %(current_git_branch))

        change_build()
    else:
        print('%s pull_project failure' % (log_pre_failure))

#
def change_build():
    print('%s start change_build\n' % (log_pre_success))

    filePath = '%s/%s/Info.plist' % (project_path, scheme_name)
    open_r = open(filePath, 'r')
    lines = open_r.readlines()

    lineNum = 0
    for line in lines:
        if '<key>CFBundleVersion</key>' in line:

            nextLine = lines[lineNum + 1]

            index_s = nextLine.find('>')
            index_e = nextLine.rfind('<')
            build_old_local = nextLine[index_s + 1: index_e]
            print('%s build_old_local -> %s' % (log_pre_success, build_old_local))

            build_old_fir = fir_app_Info_in_list()['master_release']['build']
            print('%s build_old_fir -> %s' % (log_pre_success, build_old_fir))

            build_new = str(int(build_old_fir) + 1)
            print('%s build_new -> %s' % (log_pre_success, build_new))

            newLine = nextLine.replace(build_old_local, build_new)

            open_r.close()

            open_r = open(filePath, 'r')
            content = open_r.read()

            content = content.replace(nextLine, newLine)

            open_w = open(filePath, 'w')
            open_w.write(content)
            open_w.close()

            break
        lineNum = lineNum + 1

    clean_project()

#
def clean_project():
    print('%s start clean_project\n' % (log_pre_success))
    ret = os.system('xcodebuild clean')
    if ret == 0:
        print('%s clean_project success' % (log_pre_success))
        build_project()
    else:
        print('%s clean_project failure' % (log_pre_failure))

#
def build_project():
    print('%s start build_project' % (log_pre_success))
    ret = os.system ('xcodebuild -workspace %s.xcworkspace -scheme %s -destination generic/platform=iOS archive -configuration Release ONLY_ACTIVE_ARCH=NO -archivePath %s/%s' % (scheme_name, scheme_name, temp_path, scheme_name))
    if ret == 0:
        print('%s build_project success' % (log_pre_success))
        export_ipa()
    else:
        print('%s build_project failure' % (log_pre_failure))

#
def export_ipa():
    print('%s start export_ipa' % (log_pre_success))
    global ipa_dir_path
    ipa_dir_name_temp = time.strftime('mixc_%m-%d_%H-%M-%S', time.localtime(time.time()))
    ipa_dir_temp = '%s/%s' % (temp_path, ipa_dir_name_temp)

    ret0 = os.system ('xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s -exportOptionsPlist %s' % (temp_path, scheme_name, ipa_dir_temp, exportOptions_path))

    if ret0 == 0:
        print('%s export_ipa success' % (log_pre_success))

        ipa_dir_name = time.strftime('mixc_%m-%d_%H-%M-%S', time.localtime(time.time()))
        ipa_dir_path = '%s/%s' % (ipa_dir_save_path, ipa_dir_name)
        ret1 = os.system ('mv %s %s' % (ipa_dir_temp, ipa_dir_path))
        if ret1 == 0:
            print('%s mv export_ipa dir success' % (log_pre_success))

            ret2 = os.system('rm -r -f %s/%s.xcarchive' % (temp_path, scheme_name))
            if ret2 == 0:
                print('%s rm .xcarchive success' % (log_pre_success))

                ret3 = os.system('rm -r -f %s' % ipa_dir_temp)
                if ret3 == 0:
                    print('%s rm ipa_dir_temp success' % (log_pre_success))
                    upload_fir()
                else:
                    print('%s rm ipa_dir_temp failure' % (log_pre_failure))
            else:
                print('%s rm .xcarchive failure' % (log_pre_failure))
        else:
            print('%s mv export_ipa dir failure' % (log_pre_failure))
    else:
        print('%s export_ipa failure' % (log_pre_failure))

#
def upload_fir():
    os.chdir("%s" % project_path)
    cmd_str = 'git log  --graph --pretty=format:\"%h %cd:%n%s%n\" --date=format:\"%m-%d %H:%M\"' + " -%s" % (commit_num)
    commit_msg = os.popen(cmd_str).read()
    commit_msg = "git_branch: %s \n" % (current_git_branch) + \
                 "附最近 %s 个提交修改:\n\n%s" % (commit_num, commit_msg)

    print('%s start upload_fir' % (log_pre_success))
    ipa_path = '%s/%s.ipa' % (ipa_dir_path, scheme_name)
    ret = os.system('/usr/local/bin/fir p %s -T %s -c \"%s\"' % (ipa_path, fir_api_token, commit_msg))
    if ret == 0:
        print('%s upload_fir success' % (log_pre_success))
        ret3 = os.system('rm -r -f %s' % ipa_dir_path)
        send_mail()
    else:
        print('%s upload_fir failure' % (log_pre_failure))

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail():
    print('%s start send_mail...' % (log_pre_success))
    download_URL = fir_download_URL()
    master_release_downloadURL = fir_master_release_downloadURL()

    app_Info_in_list = fir_app_Info_in_list()
    master_release = app_Info_in_list['master_release']
    created_at = master_release['created_at']
    created_at_Array = time.localtime(created_at)
    created_at_Time = time.strftime('%m-%d %H:%M', created_at_Array)

    os.chdir("%s" % project_path)
    cmd_str = 'git log --graph --pretty=format:\"%h %cd %an:%n%s%n\" --date=format:\"%Y-%m-%d %H:%M:%S\"' + ' -%s' % (commit_num)
    commit_msg = os.popen(cmd_str).read()
    commit_msg = "附最近 %s 个提交修改:\n\n%s" % (commit_num, commit_msg)

    version = master_release['version']
    build = master_release['build']
    xcodebuild_version = os.popen('xcodebuild -version').read().replace('\n', ' ', 1).replace('\n', '')

    temp_to_Emails_group_names = []
    temp_to_Emails = []
    temp_to_Emails_logs= []
    for key in to_Emails:
        temp_to_Emails_group_names.append(key)
        temp_to_Emails += to_Emails[key]

        temp_to_Emails_logs.append(key + ': ' + ', '.join(to_Emails[key]) + '.')

    temp_department_names = ', '.join(temp_to_Emails_group_names) + '.'
    temp_to_Emails_logs_str = '\n'.join(temp_to_Emails_logs)

    build_endTimestamp = time.time()
    build_time_cost = build_endTimestamp - build_startTimestamp
    build_time_cost_m = build_time_cost / 60
    build_time_cost_s = build_time_cost % 60

    global app_info_str
    app_info_str =  'version: %s' % (version) + \
                    '\nbuild: %s' % (build) + \
                    '\nbuild_time_cost: %02dm%02ds' % (build_time_cost_m, build_time_cost_s) + \
                    '\nrelease_type: %s' % (master_release['release_type']) + \
                    '\ncreated_at: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', created_at_Array)) + \
                    '\ngit_branch: %s' % (current_git_branch) + \
                    '\nos_platform: %s' % (platform.platform()) + \
                    '\nxcodebuild_version: %s' % (xcodebuild_version) + \
                    '\npython_version: %s\n' % (platform.python_version()) + \
                    '\nsend_to_department(s): %s\n' % (temp_department_names)

    text = 'Dear all:\n\n最新 [XX<应用名称>]_iOS_客户端 项目已打包完毕，可前往安装！' + \
            '\n' + master_release_downloadURL + \
            '\n\n' + \
            app_info_str + \
            '\n--------------------------------------------------' + \
            '\n\n' + commit_msg + '\n...'\
            '\n\n--------------------------------------------------' + \
            '\n\n注:' + \
            '\n\n- 测试第三方相关功能时<第三方支付及第三方分享回调的情况>, 请删除 AppStore 下载的正式版本, 以保证第三方能正确回调回一点万象.' + \
            '\n\n- 若没收到该最新邮件, 可从如下固定地址下载最新测试包<建议收藏该地址>(上面带 release_id 的地址可用于日后安装旧版本, 如回退验证.):' + \
            '\n  ' + download_URL + \
            '\n\n- 若还希望添加其它信息, 可将需要的相关信息回复该邮件, 可行的话将在后续进行完善.' + \
            '\n\n- 安装后点击打开若遇到证书信任弹框问题时, 请移步苹果官方进一步了解 <在 iOS 上安装自定企业级应用>.' + \
            '\n  请点击传送: https://support.apple.com/zh-cn/HT204460' + \
            '\n\n- 该邮件为自动打包后发出, 若无需收到该邮件, 回复说明即可.' + \
            '\n\n--------------------------------------------------' + \
            '\n\nSun [XX<姓名>]\n[XX<公司>] [XX<部门>] 电商组'

    eMail = base64.b64decode(base64E).decode()
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = _format_addr('Sun <%s>' % eMail)
    msg['To'] = ','.join(temp_to_Emails)
    msg['Subject'] = Header('iOS_<%s(%s)>_<%s>_<%s>' % (version, build, current_git_branch, created_at_Time), 'utf-8').encode()

    try:
        server = smtplib.SMTP()
        server.connect(smtp_server, 25)
        server.login(eMail, base64.b64decode(base64P).decode())
        server.sendmail(eMail, temp_to_Emails, msg.as_string())
        server.quit()

        print('send_mail to:\n%s' %(temp_to_Emails_logs_str))

        print('%s send_mail success' % (log_pre_success))
    except smtplib.SMTPException:
        print('%s send_mail failure' % (log_pre_failure))

#
def fir_app_Info_in_list():
    global fir_app_Info_in_list_temp
    if 'fir_app_Info_in_list_temp' in globals():
        return fir_app_Info_in_list_temp
    else:
        url = 'http://api.fir.im/apps?api_token=%s' % (fir_api_token)
        res = urllib.request.urlopen(url).read()
        appInfoObj = json.loads(res)

        items = appInfoObj['items']

        for item in items:
            id = item['id']
            if id == fir_app_id:
                return item

def fir_app_Info():
    global fir_app_Info_temp
    if 'fir_app_Info_temp' in globals():
        return fir_app_Info_temp
    else:
        url = 'http://api.fir.im/apps/%s?api_token=%s' % (fir_app_id, fir_api_token)
        res = urllib.request.urlopen(url).read()
        fir_app_Info_temp = json.loads(res)
        return fir_app_Info_temp

def fir_download_URL():
    appInfo = fir_app_Info()
    master_release_id = appInfo['master_release_id']
    short = appInfo['short']
    downloadURL = 'http://fir.im/%s' % (short)
    return downloadURL

def fir_master_release_downloadURL():
    appInfo = fir_app_Info()
    downloadURL = fir_download_URL()
    master_release_id = appInfo['master_release_id']
    master_release_downloadURL = '%s?release_id=%s' % (downloadURL, master_release_id)
    return master_release_downloadURL

def fir_master_release_build():
    appInfo = fir_app_Info()
    downloadURL = fir_download_URL()
    master_release_id = appInfo['master_release_id']
    master_release_downloadURL = '%s?release_id=%s' % (downloadURL, master_release_id)
    return master_release_downloadURL

def main():
    pull_project()



main()









