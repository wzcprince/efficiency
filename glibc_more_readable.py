#-*- coding: gb2312

# The word will be peace and quiet

import os, shutil, re,subprocess,sys


os.chdir(r"D:\!learn\code\glibc")

# https://docs.python.org/2.7/library/subprocess.html#subprocess.Popen.stdin
ptee = subprocess.Popen("tee " + os.path.basename(__file__) + ".txt", stdin=subprocess.PIPE)
sys.stdout = ptee.stdin

os.chdir(r"./glibc-2.23")




files_count = 0


reg_LIST_HEAD = re.compile(r"^.*static LIST_HEAD \((.*)\).*", re.MULTILINE)
def replace_LIST_HEAD(content):
    need_write_back = False
    start_pos = 0
    match1 = reg_LIST_HEAD.search(content, start_pos)
    while match1:
        print match1.group(0)
        print match1.group(1)

        # �����ϴ����������������������ļ����Ƿ���������
        start_pos = match1.end()
        
        if match1.group(0).startswith("//"):
            # ��ʾ���Ѿ������滻����
            # �������matchѽ��Ҫ��Ȼ��ѭ����
            match1 = reg_LIST_HEAD.search(content, start_pos)
            continue
        else:

            replace1 = "//" + match1.group(0) + "\nstatic struct list_head " + match1.group(1) + " = LIST_HEAD_INIT(" + match1.group(1) + ");"
            print replace1
            content = content.replace(match1.group(0), replace1)

            need_write_back = True
            
            # �������matchѽ��Ҫ��Ȼ��ѭ����
            match1 = reg_LIST_HEAD.search(content, start_pos)
    return need_write_back, content


dirs_to_delete = r"""
    ./rt
"""

# tst��ͷ���ļ��ǵ�Ԫ��������
# SPARC������Դ���ڿ����䴦�����ܹ���Scalable Processor ARChitecture������д����һ��RISCָ��ܹ���������1985����̫��΢ϵͳ����ƣ�Ҳ��SPARC���ʹ�˾��ע���̱�֮һ��
# ./ ��ôдҲͦ�õģ�Ҳ����д�� \./ 
files_to_delete = r"""
    .*/tst.*
    .*/sparc/.*
    ./io/mkfifo.c
    ./io/xmknod.c

    ./sysdeps/arm/.*
    ./sysdeps/alpha/.*
    ./sysdeps/aarch64/.*
    ./sysdeps/microblaze/.*
    ./sysdeps/hppa/.*
    ./sysdeps/sh/.*
    ./sysdeps/nios2/.*
    ./sysdeps/tile/.*
    ./sysdeps/m68k/.*
    ./sysdeps/mach/hurd/.*
    ./sysdeps/ia64/.*
    ./sysdeps/s390/.*
    ./sysdeps/mips/.*
    ./sysdeps/powerpc/.*


    ./sysdeps/unix/sysv/linux/arm/.*
    ./sysdeps/unix/sysv/linux/alpha/.*
    ./sysdeps/unix/sysv/linux/aarch64/.*
    ./sysdeps/unix/sysv/linux/microblaze/.*
    ./sysdeps/unix/sysv/linux/hppa/.*
    ./sysdeps/unix/sysv/linux/sh/.*
    ./sysdeps/unix/sysv/linux/nios2/.*
    ./sysdeps/unix/sysv/linux/tile/.*
    ./sysdeps/unix/sysv/linux/m68k/.*
    ./sysdeps/unix/sysv/linux/mach/hurd/.*
    ./sysdeps/unix/sysv/linux/ia64/.*
    ./sysdeps/unix/sysv/linux/s390/.*
    ./sysdeps/unix/sysv/linux/mips/.*
    ./sysdeps/unix/sysv/linux/powerpc/.*

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
        elif os.path.isfile(item_path):
            pass
            if should_del(item_path, list_file_regs):
                os.remove(item_path)
                print "os.remove(item_path):" + item_path
                continue
            #f1 = open(item_path, "rt")
            #content = f1.read()
            #f1.close()

            need_write_back = False
            f1 = open(item_path, "rt")
            content = f1.read()
            f1.close()

            need, content = replace_LIST_HEAD(content)
            need_write_back |= need


            if need_write_back:
                f1 = open(item_path, "wt")
                f1.write(content)
                f1.close()



iterate_files(".")

print "files_count:" + str(files_count)

sys.stdout.flush()
ptee.kill()

