#-*- coding: gb2312

# The word will be peace and quiet

import os, shutil, re

logfile = open("more_readable.txt", "wt")

readonly = True
clean_syscall_parameter_list = False
if 1:
    readonly = False
    clean_syscall_parameter_list = True
else:
    os.chdir("./full")

files_count = 0


things = r"""
    /*__rte_cache_aligned*/
    __rte_aligned\(PROD_ALIGN\)
    __rte_aligned\(CONS_ALIGN\)
    __attribute__\(\(always_inline\)\)
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

    

files_count = 0

dirs_to_delete = r"""

    .*/arch/arm
    .*/arch/ppc_64
"""

# ./ 这么写也挺好的，也不用写成 \./ 
files_to_delete = r"""

"""

def get_reg_list_to_del(reg_list_str):
    list_regs = []
    for reg in reg_list_str.split("\n"):
        reg = reg.strip()
        if len(reg):
            list_regs.append(reg)
    return list_regs

list_dir_regs = get_reg_list_to_del(dirs_to_delete)
print list_dir_regs
list_file_regs = get_reg_list_to_del(files_to_delete)
print list_file_regs

def should_del(item_path, list_regs):
    for reg in list_regs:
        if re.match(reg, item_path):
            return True
    return False


    
def iterate_files(dir1):
    global files_count

    for item_name in os.listdir(dir1):
        item_path = dir1 + "/" + item_name
        if os.path.isdir(item_path):
        
            if should_del(item_path, list_dir_regs):
                #os.rmdir(item_path)
                shutil.rmtree(item_path)
                print "os.rmdir(item_path):" + item_path
                continue
                
            iterate_files(item_path)
        elif os.path.isfile(item_path) and item_path[-3:] != ".py":
            if should_del(item_path, list_file_regs):
                os.remove(item_path)
                print "os.remove(item_path):" + item_path
                continue 
            print item_path[-3:]
            f1 = open(item_path, "rt")
            content = f1.read()
            f1.close()
            need_write_back = False
            need = False # 如果只用一个  need_write_back 会有bug，老的True会被新的False覆盖掉 2017年10月08日 bug

            if 0: 
                # 想办法 把 函数 inet_sk_rebuild_header tcp_v4_conn_request tcp_v4_syn_recv_sock 的声明注释掉
                # 避免source insight 报 multiple definition
                pause 
            if 1: # 替换 
                need, content = replace_things(item_name, item_path, content)
                need_write_back |= need


            if not readonly and need_write_back:
                f1 = open(item_path, "wt")
                f1.write(content)
                f1.close()


iterate_files(".")

print "files_count:" + str(files_count)


logfile.close()

