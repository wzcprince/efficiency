#-*- coding: gb2312

# The word will be peace and quiet

import os, shutil, re

logfile = open("test_more_readable.txt", "wt")

readonly = True
clean_syscall_parameter_list = False
if 1:
    readonly = False
    os.chdir("./tailored")
else:
    os.chdir("./full")
    clean_syscall_parameter_list = True

files_count = 0


def replace_aligned(item_name, item_path, content):
    #print >> logfile, item_name
    need_write_back = False
    start_pos = 0
    
    reg_aligned = re.compile(r""" __aligned\(\d+\)""") # ע���ַ�����ĵ�һ��Ҫ���ո�
    
    match1 = reg_aligned.search(content, start_pos)
    while match1:
    
        if content[match1.start()-2:match1.start()] != "/*":
            content = content[:match1.start()] + "/*" + match1.group(0) + "*/" + content[match1.end():] 
            need_write_back = True
        start_pos = match1.end()
        
        print >> logfile, item_name, start_pos, content[match1.start()-2:match1.start()], match1.group(0)
        
        
        match1 = reg_aligned.search(content, start_pos)
        #need_write_back = False

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
            need = False # ���ֻ��һ��  need_write_back ����bug���ϵ�True�ᱻ�µ�False���ǵ� 2017��10��08�� bug


            if 1: # �滻 
                need, content = replace_aligned(item_name, item_path, content)
                need_write_back |= need

            if not readonly and need_write_back:
                f1 = open(item_path, "wt")
                f1.write(content)
                f1.close()


#iterate_files(".")

print "files_count:" + str(files_count)


logfile.close()

os.system("pause")


