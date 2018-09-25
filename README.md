注: 
下文内容及代码中出现的 [XX<...>] 为敏感信息不便写出, 或不同项目的配置项, 实际使用中参考替换即可.
为了更详细说明细节及功能, 下文代码进行了详细注释说明.
`iOSAutoArchive` 源代码已上传 `github`, [点击传送](https://github.com/augsun/iOSAutoArchive).

### 先看看分发出去的邮件内容:
```
# 邮件标题: 
iOS_<3.0.1(384)>_<3.0.0_fix>_<09-14 18:31>

# 邮件内容
Dear all:

最新 [XX<应用名称>]_iOS_客户端 项目已打包完毕，可前往安装！
http://fir.im/[XX<应用对应的 path>]?release_id=5b9b8e1bca87a844aa4dccaa

version: 3.0.1
build: 384
build_time_cost: 06m27s
release_type: inhouse
created_at: 2018-09-14 18:31:55
git_branch: 3.0.0_fix
os_platform: Darwin-17.7.0-x86_64-i386-64bit
xcodebuild_version: Xcode 9.4.1 Build version 9F2000
python_version: 3.6.5

send_to_department(s): Sender, Developer, Tester.

--------------------------------------------------

附最近 20 个提交修改:

* 64c8122bee 2018-09-14 18:25:06 augsun:
| no message
|
* bea971d9b2 2018-09-14 18:09:49 augsun:
| - 创意课堂申请退款页面和多件购买申请退款页面，这个文案修改为“7-15个工作日内完成退款，0手续费”.
|
* aac384221b 2018-09-06 16:53:10 augsun:
| - 秒杀列表按钮不能点击问题.
|
*   d04886489b 2018-09-06 14:45:52 augsun:
|\  Merge remote-tracking branch 'origin/mixc_TencentLBS' into 3.0.0_fix
| |
| * bec89d2fa7 2018-08-28 14:46:29 augsun:
| | - 添加腾讯 LBS SDK.
| |
* | a8e1fcb322 2018-09-06 14:27:56 augsun:
| | no message
| |
* | a120a0372c 2018-09-06 14:08:30 augsun:
| | - APP 激活后 商品详情自动刷新(倒计时刷新).
| |
* | ec15cfa5f9 2018-09-06 14:04:51 augsun:
| | - 事件 300006 添加参数 name.
| |
* | 3c54c337dc 2018-09-05 15:27:30 augsun:
| | - 退款埋点 104208 -> 104209.
| |
* | 1146477299 2018-09-05 14:15:15 augsun:
| | - 好物列表没有 banner 时隐藏.
| |
* | f0692d7d11 2018-09-05 14:01:04 augsun:
| | - 套餐列表选中套餐后可以取消选中.
| |
* | bda9a976d0 2018-09-03 15:13:52 augsun:
| | - 万象时间导航条颜色问题.
| |
* | 4906de37df 2018-09-03 11:51:09 augsun:
| | - 修复商品无限制购买数量时下单页.
| |
* | 4590e33b22 2018-09-03 11:36:29 Sun_MBP:
| | no message
| |
* | 17c30375b0 2018-08-31 16:53:27 Sun_MBP:
| | no message
| |
* | f4963fefd5 2018-08-31 16:14:44 Sun_MBP:
| | no message
| |
* | 4a4a78eb43 2018-08-31 16:11:53 augsun:
| | no message
| |
* |   34fb92c197 2018-08-31 13:47:14 Sun:
|\ \  Merge remote-tracking branch 'origin/2.9.0_多件购买' into deve
| | |
| * | be3d5c5bdb 2018-08-31 10:07:07 augsun:
| | | no message
| | |
* | |   2349b368a3 2018-08-30 16:46:17 Sun:
|\ \ \  Merge remote-tracking branch 'origin/2.9.0_多件购买' into deve
| |/ /

...

--------------------------------------------------

注:

- 测试第三方相关功能时<第三方支付及第三方分享回调的情况>, 请删除 AppStore 下载的正式版本, 以保证第三方能正确回调回[XX<应用名称>].

- 若没收到该最新邮件, 可从如下固定地址下载最新测试包<建议收藏该地址>(上面带 release_id 的地址可用于日后安装旧版本, 如回退验证.):
http://fir.im/[XX<fir上的固定地址>]

- 若还希望添加其它信息, 可将需要的相关信息回复该邮件, 可行的话将在后续进行完善.

- 安装后点击打开若遇到证书信任弹框问题时, 请移步苹果官方进一步了解 <在 iOS 上安装自定企业级应用>.
请点击传送: https://support.apple.com/zh-cn/HT204460

- 该邮件为自动打包后发出, 若无需收到该邮件, 回复说明即可.

--------------------------------------------------

Sun [XX<姓名>]
[XX<公司>] [XX<部门>] 电商组
```
以上是打包分发出去收件人收到的邮件格式样式, 接下来详细阐述实现细节.
#### 一, 配置基本信息
##### 1, 收件人
收件人以部门组划分, 比如 [开发组人员] [测试组人员] [项目组人员] ..., 这样划分是为了灵活配置以分发给需要的组人员, 比如测试阶段需要频繁打包给测试人员, 那么邮件只需要发给测试组人员, 验收阶段, 同时也要发给项目 产品 UI 或 Boss 人员, 那么收件人员分组的好处就是可以达到灵活配置.
```
# Sender
mails_Sender = ['xxx0@xx.cn'] # [XX<发件人0姓名>]

# Developer
mails_Developer = [
      'xxx1@xx.cn' # [XX<收件人1姓名>]
    , 'xxx2@xx.cn' # [XX<收件人2姓名>]
    , 'xxx3@xx.cn' # [XX<收件人3姓名>]
]

# Tester
mails_Tester = [
      'xxx4@xx.cn' # [XX<收件人4姓名>]
    , 'xxx5@xx.cn' # [XX<收件人5姓名>]
    , 'xxx6@xx.cn' # [XX<收件人6姓名>]
]
...

# 灵活配置部分 打包的时候指定需要发送的组人员
to_Emails = {
    "Sender":       mails_Sender, # 发送者
    "Developer":    mails_Developer, # 开发人员
    "Tester":       mails_Tester, # 测试人员
    # "Porject":      mails_Porject, # 项目
    # "Product":      mails_Product, # 产品
    # "UI":           mails_UI, # UI
    # "Boss":         mails_Boss, # Boss
}

```
##### 2, 项目目录路径及打包的临时缓存目录路径配置
```
# 用户主目录路径
user_home_path = os.environ['HOME']
# 当前 py 文件路径
tempPrj_dir = os.path.dirname(os.path.abspath(__file__))
# 项目路径
project_path = '%s/Desktop/[XX<子路径>]' % user_home_path
# 项目 scheme
scheme_name = '[XX<scheme名称>]'
# 打包时需要的 exportOptions 路径
exportOptions_path = '%s/Desktop/[XX<子路径>]/_tool/archive/ExportOptions_enterprise.plist' % user_home_path
# 缓存临时目录
temp_path = user_home_path
# 导出的 ipa 目录
ipa_dir_save_path = '%s/Desktop' % user_home_path
```
##### 3, fir 配置
```
fir_api_token = '[XX<fir 的 token>]'
fir_app_id = '[XX<fir 的 id>]'
```
##### 4, git 配置
```
# 最近 git 修改条数
commit_num = '20'
```
##### 5, 发件人邮箱配置
```
# 发件人邮箱和密码 <为了不明文被感知 进行了 base64 编码存放, 发邮件的时候进行反编码即可>
base64E = b'eWFuZ2ppY[XX<中间隐藏>]xhbmQuY29tLmNu'
base64P = b'MDlB[XX<中间隐藏>]4NjM4OTky'
# 邮件对应服务器 SMTP
smtp_server = '[XX<邮件服务器>].com.cn'
```
##### 6, 其它
```
# 定义日志输出样式
log_pre_success = '✅ =====>'
log_pre_failure = '❌ =====>'
```
#### 二, 功能实现代码
##### 1, 拉取代码 <pull_project>
```Python
def pull_project():
#开始打包的时间
    global build_startTimestamp
    build_startTimestamp = time.time()

    print('%s start pull_project' % (log_pre_success))

    os.chdir("%s" % project_path)
# 拉取最新代码
    ret = os.system('git pull')
    if ret == 0:
        print('%s pull_project success' % (log_pre_success))
# 获取 git 分支名称
        global current_git_branch
        current_git_branch = os.popen('git symbolic-ref --short -q HEAD').read().replace('\n', '')
        print('current_git_branch: %s' %(current_git_branch))

        change_build()
    else:
        print('%s pull_project failure' % (log_pre_failure))
```
注: 初次拉取代码前, 请用 SourceTree 对仓库进行一次 pull 和 push, 或手动做远程分支关联, 否则会出现如下情况:
```
Suns-iMac:merchant sun$ git pull
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details.

    git pull <remote> <branch>

If you wish to set tracking information for this branch you can do so with:

    git branch --set-upstream-to=origin/<branch> master

```

##### 2, 修改项目 build 号 <change_build>
注:
1,
请保证 fir 上最新的 build 格式为 (xxx) 整数形式的 build 号. 如: 101.
因为此步骤会自动取得 fir 上的最新 build 号, 并为此次打包的 build 加 1.
如: 当前 fir 上的 build 号为 101, 那么此次打包后上传 fir 的包 build 为 102.
2, 当前 xcode 里 Build 设置的值请设置为整数, 如 99.
3, 目前对于 build 版本格式只兼容整数 build 号, 即 build 里不应该出现 ".", 如: 2.3.0.
```
def change_build():
    print('%s start change_build\n' % (log_pre_success))
#打开 Info.plist 文件 进行 build 的修改
    filePath = '%s/%s/Info.plist' % (project_path, scheme_name)
    open_r = open(filePath, 'r')
    lines = open_r.readlines()

    lineNum = 0
#遍历行
    for line in lines:
# build 所在行
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
```
##### 3, clean项目 <clean_project>
```
def clean_project():
    print('%s start clean_project\n' % (log_pre_success))
    ret = os.system('xcodebuild clean')
    if ret == 0:
        print('%s clean_project success' % (log_pre_success))
        build_project()
    else:
        print('%s clean_project failure' % (log_pre_failure))
```
##### 4, 编译项目 <build_project>
```
def build_project():
    print('%s start build_project' % (log_pre_success))
# 执行编译命令 <编译哪个 scheme, 临时缓存目录, 缓存文件名称>
    ret = os.system ('xcodebuild -workspace %s.xcworkspace -scheme %s -destination generic/platform=iOS archive -configuration Release ONLY_ACTIVE_ARCH=NO -archivePath %s/%s' % (scheme_name, scheme_name, temp_path, scheme_name))
    if ret == 0:
        print('%s build_project success' % (log_pre_success))
        export_ipa()
    else:
        print('%s build_project failure' % (log_pre_failure))
```
##### 5, 导出 ipa <export_ipa>
```
def export_ipa():
    print('%s start export_ipa' % (log_pre_success))
    global ipa_dir_path
# 指定导出 ipa 的名称
    ipa_dir_name_temp = time.strftime('mixc_%m-%d_%H-%M-%S', time.localtime(time.time()))
    ipa_dir_temp = '%s/%s' % (temp_path, ipa_dir_name_temp)
# 执行 导出命令
    ret0 = os.system ('xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s -exportOptionsPlist %s' % (temp_path, scheme_name, ipa_dir_temp, exportOptions_path))

# 导出后删除相关 build 缓存文件或目录
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
```
##### 6, 上传 fir <upload_fir>
```
def upload_fir():
    os.chdir("%s" % project_path)
# 获取 git 最近提交修改内容
    cmd_str = 'git log  --graph --pretty=format:\"%h %cd:%n%s%n\" --date=format:\"%m-%d %H:%M\"' + " -%s" % (commit_num)
    commit_msg = os.popen(cmd_str).read()
    commit_msg = "git_branch: %s \n" % (current_git_branch) + \
                 "附最近 %s 个提交修改:\n\n%s" % (commit_num, commit_msg)

    print('%s start upload_fir' % (log_pre_success))
    ipa_path = '%s/%s.ipa' % (ipa_dir_path, scheme_name)
# 执行 fir 上传
    ret = os.system('/usr/local/bin/fir p %s -T %s -c \"%s\"' % (ipa_path, fir_api_token, commit_msg))
    if ret == 0:
        print('%s upload_fir success' % (log_pre_success))
        ret3 = os.system('rm -r -f %s' % ipa_dir_path)
        send_mail()
    else:
        print('%s upload_fir failure' % (log_pre_failure))
```
上传 fir 后, 所有本地缓存文件都会删除, 不用担心留存磁盘占用空间.
##### 7, 发送邮件 <send_mail>
```
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
    app_info_str =  'version: %s' % (version) + \ # 版本号
                    '\nbuild: %s' % (build) + \ # build 号
                    '\nbuild_time_cost: %02dm%02ds' % (build_time_cost_m, build_time_cost_s) + \ # 整个打包过程花费的时间
                    '\nrelease_type: %s' % (master_release['release_type']) + \ # 打包类型
                    '\ncreated_at: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', created_at_Array)) + \ # 打包时间
                    '\ngit_branch: %s' % (current_git_branch) + \ # 打包所在分支
                    '\nos_platform: %s' % (platform.platform()) + \ # 系统平台
                    '\nxcodebuild_version: %s' % (xcodebuild_version) + \ # Xcode 版本
                    '\npython_version: %s\n' % (platform.python_version()) + \ # python 版本
                    '\nsend_to_department(s): %s\n' % (temp_department_names) # 邮件发送给了哪些组成员

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
```
##### 8, 其它功能函数 <>
用于数据处理及从 fir 获取应用相关信息.
```
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

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
```
#### 三, 一键打包
在终端执行 `python3 iOSAutoArchive.py` 即可.
```
augsuns-MBP:Desktop augsun$ python3 iOSAutoArchive.py
```
或配置到持续集成工具中执行.

- 以上内容及 Python 代码略拙, 不足之处, 欢迎指正.


