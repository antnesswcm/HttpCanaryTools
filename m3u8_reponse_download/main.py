# HC-request Extract the m3u8-V1.0
import os


def readText(_text_path):                                           # 读取文本文件第一行内容，形参为文件绝对路径
    file = open(_text_path, mode='rt', encoding='utf-8')            # rt为默认的打模式，即只读文本
    text = file.readline()
    file.close()
    return text                                                     # 返回文本第一行内容


def formatText(_old_text):                                          # 对字符串格式化，形参为一行字符串
    new_text = _old_text[4:-10] + '\n'                              # 截取字符串开头“GET ”和结尾“ HTTP1/1”并加入换行
    return new_text                                                 # 返回处理后的字符串


def list2Aggregate(_in_list):                                       # 将列表转化为集合，形参为列表
    return set(_in_list)                                            # 用set()集合创建命令直接接受列表并返回，达到元素去重


def WriteFile(_in_aggregate):                                       # 将序列写入文本文件，形参为集合
    out_path = root_path                                            # 将外部参数“根路径”导入
    # 调用os模块组合路径并保存为path，供调用
    file = open(path := os.path.join(out_path, 'outfile.txt'), mode='w', encoding='utf-8')  # “w”为覆盖写入,会丢失所有原数据
    file.writelines(_in_aggregate)                                  # writelines不会自动添加换行，需要输入的序列元素自带换行
    file.close()                                                    # 关闭文件，必须操作
    print("数据保存成功！地址: {}".format(os.path.abspath(path)))      # 打印path的绝对路径，os转化调用好像不需要了
    # 此函数为动作函数，没有返回值


# 提示信息
sample = """
# =======================================使用说明=============================================
# 
# 此脚本为提取 HttpCanary 导出数据中所有 request.hcy 的第一行的m3u8地址
# 作者: 酷安: @王糙米              github地址: https://github.com/antnesswcm/HttpCanaryTools
# 运行环境: python3.8 (3.6没测试可能报错)  在终端中运行(cmd窗口) 其他环境不一定可以拖拽文件夹
# 使用到的库： os 
# ===========================================================================================
# 文件夹参考示例:
# 
#  HttpCanary                         //工作目录
#     ├─任务1                        //任务目录
#     │  └─项目1                     //项目目录
#     │       request.hcy    <---这个就是提取m3u8地址的文件了，玩HttpCanary应该知道吧
#     │       request.json
#     │       response.hcy
#     │       response.json
#     │       response_body.bin
#     │
#     ├─任务2
#     │  ├─项目1
#     │  ├─项目2
#     │  └─项目3
#     └─任务3
#         ├─项目1
#         ├─项目2
#         └─项目3
# ******文件夹名字不需要一样，但需要3个层级！！！******
# ******第3个目录的request.hcy文件名不能不一样！！！******
# ===========================================================================================
# request.hcy的第一行如下类才能提取成功：
# GET http://www.antnesswcm.com/happy.m3u8 HTTP/1.1
# 提取出 http://www.antnesswcm.com/happy.m3u8 地址并保存到 HttpCanary/outfile.txt 文件(默认就是)
# 保存地址在程序结束后也会生成哒~
# 
# 脚本注释写的很全啦~有需求可以自己改，或者求助me~
# 酷安: @王糙米 邮箱: antnesswcw@gmail.com
# ===========================================================================================
# 脚本没有写什么input检测，请按照使用说明操作，要终止就关闭窗口！
# ===========================================================================================
"""

DL_path = "N_m3u8DL-CLI_v2.9.7.exe"
baseUrl = "http://cncdn.mysunhan.com/"
headers = "Host:cncdn.mysunhan.com|User-Agent:stagefright/1.2 (Linux;Android 11)"
proxyAddress = "http://127.0.0.1:10809"
other = "--enableDelAfterDone"
if __name__ == '__main__':                                          # 脚本的执行入口
    # print(sample)                                                   # 打印提示信息
    root_path = input("(可拖拽)工作文件夹路径(回车继续): ")                      # 工作地址输入获取
    # root_path = r"工作地址绝对路径"                                            # 这是内部定义的地址，定义后注释上行
    # 任务读取
    task = os.listdir(root_path)                                    # 调用listdir获取一级子目录和文件(此处返回应无文件)，返回列表
    print("读取成功！任务数: {task_num!s}".format(task_num=len(task)))  # 此处返回的应为子目录数
    print("-" * 40)
    # 任务处理
    url_list = []                                                   # 初始化空列表，用于接收formatText处理的字符串
    num = 0                                                         # 初始化“任务”计数器
    for item in task:                                               # 对每一个任务目录进行处理
        num += 1                                                    # 任务计数器update
        print("第{}个任务开始".format(num))
        item_path = os.path.join(root_path, item)                   # 调用os拼接出每一个任务地址绝对路径
        threads = os.listdir(item_path)                             # 调用listdir获取任务目录下的项目目录，返回项目列表
        print("加载成功！项目数: {thread_num!s}".format(thread_num=len(threads)))   # 统计项目数
        print("开始处理！")
        # 项目处理
        for thread in threads:                                      # 循环处理每一个项目
            thread_path = os.path.join(item_path, thread)           # 调用os拼接出每一个项目地址绝对路径
            text_path = thread_path + r"\request.hcy"               # 此路径为项目中request.hcy的绝对路径，共readText调用
            # print(text_path)
            url = formatText(readText(text_path))                   # 读取text_path路径文本第一行并格式化
            # print(url)
            # m3u8 检测
            if url[-6:-1] == ".m3u8":                               # 截取文本末尾5个字符(跳过换行符)与“.m3u8”匹配
                if url in url_list:
                    continue
                else:
                    url_list.append(url)
                    m3u8_path = thread_path + r"\response_body.bin"

                    if os.path.isfile(m3u8_path):
                        command = "{} {} --baseUrl \"{}\" --headers \"{}\" --proxyAddress \"{}\" {}".format(DL_path,
                                                                                                            m3u8_path,
                                                                                                            baseUrl,
                                                                                                            headers,
                                                                                                            proxyAddress,
                                                                                                            other)
                        os.system(command)
            # 项目处理结束
        print("任务{}处理完成！".format(num))                                           # 任务完成提示
        print("-" * 40)
        # 任务处理结束
    print("*" * 53)
    print("*" * 53)
    aggregate = list2Aggregate(url_list)                            # 将URL列表去重
    print("任务完成！共解析m3u8链接{0!s}条, 重复链接{1!s}条, 有效链接{2!s}条".format(len(url_list), len(url_list) - len(aggregate), len(aggregate)))
    print("*" * 53)
    print("正在保存链接.....")
    WriteFile(aggregate)                                            # 将链接保存至outfile.txt文件
    os.system('pause')                                              # 等待用户关闭
