#-*- coding: gb2312

# The word will be peace and quiet

import os, re, sys, shutil



root_dir = os.getcwd()
root_dir = r"D:\!learn\code\linux-4.4.82"
os.chdir(root_dir)




logfile = open("more_readable.txt", "wt")

readonly = True
clean_syscall_parameter_list = False
if 1:
    readonly = False
    os.chdir("./tailored")
else:
    os.chdir("./full")
    clean_syscall_parameter_list = True

files_count = 0


def beauty_syscall_paralist(para_list_str):

    para_list_str = para_list_str[2:] # 去掉开头的", "
    list_para = para_list_str.split(",")
    isType = True;
    final_para_str = "("
    if len(para_list_str): 
        for para in list_para:
            if clean_syscall_parameter_list:
                para = para.strip()
            if isType:
                final_para_str += para
                isType = False
            else:
                if clean_syscall_parameter_list:
                    final_para_str += " "
                final_para_str += (para + ",")
                isType = True
        # 去掉末尾多余的","
        final_para_str = final_para_str[:-1]
    else: # 为空，比如 sched_yield
        final_para_str += ")"
    return final_para_str

# 用 {0,2} 匹配要比 * 快很多耶 ！！！
reg_syscall = re.compile(r"""^(.*)SYSCALL_DEFINE\d
                             \((   [a-zA-Z0-9_]+    )   # function name
                             (   [^)]*\)    )           # parameter list 注意可能为空，所以要用*
                             """, re.VERBOSE|re.MULTILINE)

def replace_all_syscall(item_name, item_path, content):
    global files_count

    need_write_back = False
    start_pos = 0
    #if item_path.find("compat_ioctl.c") == -1:
    #    return need_write_back, content
        
    match1 = reg_syscall.search(content, start_pos)
    while match1:
        start_pos = match1.end()
        #print >> logfile, match1.end() - match1.start()

        begin_str = match1.group(1)
        if begin_str == None:
            begin_str = ""
        if begin_str.endswith("/*") or begin_str.endswith("//"):
            # 即是以/*开头已经注释过的行，不需要再重复注释啦
            # https://docs.python.org/3.1/library/string.html#formatstrings 
            print >> logfile, "{:<46} {:<32} commented".format(item_path, match1.group(2))
        elif begin_str == "" or begin_str == "COMPAT_":

            # group(2) 系统调用名称
            # group(3) para list

            final_para_str = beauty_syscall_paralist(match1.group(3))
            
            sys_call_name = "sys_" + match1.group(2) #
            if begin_str == "COMPAT_":
                sys_call_name = "compat_" + sys_call_name
            print >> logfile, "{:<46} long {}{}".format(item_path, sys_call_name, final_para_str)

            #if item_path.find("posix-timers.c") != -1:
            original_length = len(content)

            # 修改content内容， start_pos 并没有更新，这个细节暂时不会导致错误
            if begin_str == "" or begin_str == "COMPAT_":
                # compat的不要管
                content = content[:match1.start()] + "/*" + content[match1.start():match1.end()] + "*/\nlong "\
                          + sys_call_name + final_para_str + content[match1.end():]
                need_write_back = True
            #print >> logfile, start_pos, " ", str(original_length), " ", str(len(content))
        else:
            print >> logfile, "{} {}".format(item_path, match1.group(0))
            pass
        # 2017年10月09日 bug 一个文件中只能找到一个syscall，
        # 浪费一小时，原因是代码复制粘贴，改漏了
        # 还是用的 reg_static_const_struct.search
        match1 = reg_syscall.search(content, start_pos)

    return need_write_back, content


things = r"""
    __read_mostly
    ____cacheline_aligned
    ____cacheline_aligned_in_smp
    \s__aligned\(\d+\)
"""

reg_list1 = []

def replace_things(item_name, item_path, content):
    #print >> logfile, item_name
    need_write_back = False
    start_pos = 0
    
    for str1 in things.split("\n"):
        str1 = str1.strip()
        if str1:
            reg1 = re.compile(str1)

            match1 = reg1.search(content, start_pos)
            while match1:
            
                if content[match1.start()-2:match1.start()] != "/*":
                    # 已经注释过的不再重复注释
                    content = content[:match1.start()] + "/*" + match1.group(0) + "*/" + content[match1.end():] 
                    need_write_back = True
                start_pos = match1.end()
                
                print >> logfile, item_name, start_pos, content[match1.start()-2:match1.start()], match1.group(0)
                
                
                match1 = reg1.search(content, start_pos)
                #need_write_back = False

    return need_write_back, content

    
def replace_simple_things(item_name, item_path, content):
    global files_count
    need_write_back = False
            
    if -1 != content.find("__read_mostly"):
        files_count += 1
        content = content.replace("__read_mostly", "")

        need_write_back = True

    if -1 != content.find("____cacheline_aligned;"):
        files_count += 1
        content = content.replace("____cacheline_aligned", "")

        need_write_back = True
    if -1 != content.find("____cacheline_aligned_in_smp;"):
        files_count += 1
        content = content.replace("____cacheline_aligned_in_smp", "")

        need_write_back = True
    if item_name == "current.h": # 要在 source insight 里自定义 conditional parsing
        print(item_name)
        if -1 != item_path.find("asm-generic"):
            need_write_back = True
            content = content.replace("#define current get_current()", 
        """
#ifdef WZC_READ_CODE
    struct task_struct *current;
#else
    #define current get_current()
#endif
""")
        else:
            need_write_back = True
            content = content.replace("#define current get_current()", 
        """
#ifdef WZC_READ_CODE
#else
    #define current get_current()
#endif
""")
        
    return need_write_back, content

reg_LIST_HEAD = re.compile(r".*static LIST_HEAD\((.*)\).*")
def replace_LIST_HEAD(content):
    need_write_back = False
    start_pos = 0
    match1 = reg_LIST_HEAD.search(content, start_pos)
    while match1:
        print >> logfile, match1.group(0)
        print >> logfile, match1.group(1)

        # 跳过上次搜索到的这个结果，看看文件中是否还有其他的
        start_pos = match1.end()
        
        print >> logfile, item_path, " start_pos: ", start_pos

        if match1.group(0).startswith("//"):
            # 表示我已经把它替换好了
            # 必须更新match呀，要不然死循环了
            match1 = reg_LIST_HEAD.search(content, start_pos)
            continue
        else:
            #print >> logfile, item_path
            replace1 = "//" + match1.group(0) + "\nstatic struct list_head " + match1.group(1) + " = LIST_HEAD_INIT(" + match1.group(1) + ");"
            print >> logfile, replace1
            content = content.replace(match1.group(0), replace1)

            need_write_back = True
            
            # 必须更新match呀，要不然死循环了
            match1 = reg_LIST_HEAD.search(content, start_pos)
    return need_write_back, content

reg_static_const_struct = re.compile(r"(/\*){0-1}static const struct [a-zA-Z0-9_ ]+;")
def replace_static_const_struct(content):
    global files_count
    need_write_back = False
    start_pos = 0
    match1 = reg_static_const_struct.search(content, start_pos)
    while match1:
        start_pos = match1.end()
        print >> logfile, str(start_pos) + ":", match1.group(0)
        if match1.group(1):
            # 即是以/*开头已经注释过的行，不需要再重复注释啦
            print >> logfile, "commented"
            pass
        else:
            need_write_back = True
            content = content.replace(match1.group(0), "/*" + match1.group(0) + "*/")

        match1 = reg_static_const_struct.search(content, start_pos)

    return need_write_back, content

# DEFINE_PER_CPU
def replace_per_cpu(item_name, item_path, content):
    # ● 要忽略 percpu-defs.h 文件 
    # ● 不能处理带 # 的行，例如：
    #          static DEFINE_PER_CPU_SHARED_ALIGNED(struct rcu_data, sname##_data);
    
    need_write_back = False
    if item_name == "percpu-defs.h":
        return False, content
        
    print item_name
    # (?:...)  https://docs.python.org/2.7/library/re.html
    reg1 = re.compile(r"(/\*){0-1}(static ){0-1}DEFINE_PER_CPU\((.*),(.*)\);")
    # 2017年12月25日 晕晕 搞不定 (static ){0-1} 啊
    # 2017年12月25日 晕晕 搞不定 (/\*){0-1} 啊
    # ^和re.MULTILINE很关键，要不然会从一行的中间开始匹配，效果就是乱七八糟了
    reg1 = re.compile(r"^(.*)DEFINE_PER_CPU\((.*),(.*)\);", re.MULTILINE)
    # "^(/\*){0-1}(static ){0-1}DEFINE_PER_CPU\((.+),(.+)\);" 就是不行，郁闷啊
    reg1 = re.compile(r"^(/\*)?(static )?DEFINE_PER_CPU\((.+),(.+)\);", re.MULTILINE)
    
    start_pos = 0
    match1 = reg1.search(content, start_pos)
    while match1:
        print item_name + " match1 ",
        start_pos = match1.end()
        
        if match1.group(0).find("#") != -1:
            ## ● 不能处理带 # 的行
            continue
        elif match1.group(1) and match1.group(1) [0:2] == "/*":
            # 即是以/*开头已经注释过的行，不需要再重复注释啦
            print "commented"
            pass
        else:
            need_write_back = True
            new_str = "/*" + match1.group(0) + "*/  // !!! per cpu !!!" + "\n"
            if match1.group(2):
                new_str += match1.group(2)  # static可能没有
            new_str += match1.group(3) + " /*per_cpu*/"
            new_str += match1.group(4) + ";"

            content = content.replace(match1.group(0), new_str)
            start_pos = match1.start() + len(new_str) ## great !!!!
            print "to replace new_str:" + new_str
            
        match1 = reg1.search(content, start_pos)
    
    return need_write_back, content
    
    
    
def iterate_files(dir1):
    global files_count

    for item_name in os.listdir(dir1):
        item_path = dir1 + "/" + item_name
        if os.path.isdir(item_path):
            iterate_files(item_path)
        elif os.path.isfile(item_path):
            f1 = open(item_path, "rt")
            content = f1.read()
            f1.close()
            need_write_back = False
            need = False # 如果只用一个  need_write_back 会有bug，老的True会被新的False覆盖掉 2017年10月08日 bug

            if 0: 
                # 想办法 把 函数 inet_sk_rebuild_header tcp_v4_conn_request tcp_v4_syn_recv_sock 的声明注释掉
                # 避免source insight 报 multiple definition
                pause 
            if 0: # 替换 
                need, content = replace_things(item_name, item_path, content)
                need_write_back |= need

            if 0: # 替换 
                need, content = replace_all_syscall(item_name, item_path, content)
                need_write_back |= need

            if 0: # 替换 static LIST_HEAD
                need, content = replace_LIST_HEAD(content)
                need_write_back |= need

            if 0: # 替换 static const struct vm_operations_struct shmem_vm_ops;
                need, content = replace_static_const_struct(content)
                need_write_back |= need
            if 1: # 替换 DEFINE_PER_CPU
                need, content = replace_per_cpu(item_name, item_path, content)
                need_write_back |= need


            if not readonly and need_write_back:
                f1 = open(item_path, "wt")
                f1.write(content)
                f1.close()


iterate_files(".")

print "files_count:" + str(files_count)


logfile.close()

