#-*- coding: gb2312

import os, shutil




root_dir = os.getcwd()
root_dir = r"D:\!learn\code\linux-4.4.82"


# https://docs.python.org/2.7/library/subprocess.html#subprocess.Popen.stdin
ptee = subprocess.Popen("tee " + __file__ + ".txt", stdin=subprocess.PIPE)
sys.stdout = ptee.stdin



src_path = root_dir + r"\full" + "\\"
dst_path = root_dir + r"\tailored" + "\\"

# @表示目录下的所有regular 文件
gl_subpaths = r"""
    arch\x86
    block

    drivers\vhost
    drivers\virtio
    
    drivers\net\ethernet\i825xx\82596.c
    
    drivers\net\loopback.c
    drivers\net\tun.c
    drivers\net\veth.c
    drivers\net\virtio_net.c
    drivers\net\vxlan.c
    drivers\net\ethernet\intel\e1000e
    
    fs\@
    fs\ext2
    fs\ext4
    fs\kernfs
    fs\proc
    fs\ramfs
    fs\squashfs
    fs\sysfs

    include\asm-generic
    include\linux
    include\net\netfilter
    include\net\netns
    include\net\@
    include\uapi\asm-generic
    include\uapi\linux
    include\@

    init
    ipc
    kernel
    lib
    mm
    net\@
    net\8021q
    net\bridge
    net\core
    net\ethernet
    net\ipv4
    net\ipv6
    net\netfilter
    net\netlink
    net\openvswitch
    net\packet
    net\sched
    net\unix

    """

def rcopy(commands):
    #os.startfile(r"C:\Windows\System32\cmd.exe /c " + commands) 
    #os.startfile(r'C:\Windows\System32\Robocopy.exe '  + '', "open") 
    import subprocess
    # 不等待子进程结束
    p1 = subprocess.Popen('C:\Windows\System32\Robocopy.exe ' + commands + '')
    print "p1.pid: " + str(p1.pid)
    #os.system(commands)

def copy_file(commands):
    import subprocess
    # 不等待子进程结束
    p1 = subprocess.Popen('cmd.exe /c echo F | xcopy /Y ' + commands + '')
    print "p1.pid: " + str(p1.pid)
    
    
def copy_files(subpaths):
    for subpath in subpaths.split():
        subpath = subpath.strip()
        if subpath:
            real_sub_path = subpath
            if subpath.endswith("@"):
                real_sub_path = subpath[0:len(subpath)-1]
                
            if os.path.isdir(src_path + real_sub_path):
                rcopy(" " + src_path + real_sub_path + " " + dst_path + real_sub_path + " /XF * /XD * " )
                os.chdir(src_path + real_sub_path)

                if subpath.endswith("@"):
                    pass

                    # 复制目录中所有的regular file
                    # /MIR :: MIRror a directory tree (equivalent to /E plus /PURGE).
                    rcopy(" " + src_path + real_sub_path + " " + dst_path + real_sub_path + "  /MIR /XD *   /MT:36" )
                
                else:
                    # 复制目录中所有的文件及子目录
                    rcopy(" " + src_path + real_sub_path + " " + dst_path + real_sub_path + " *.* /MIR /MT:36" )

                os.chdir(root_dir)
                os.system("echo " + subpath)
            else:
                copy_file(" " + src_path + real_sub_path + " " + dst_path + real_sub_path )
                


# 删掉影响阅读的多余的文件
redundant = r"""
    mm\nobootmem.c
    mm\nommu.c
    net\ipv4\tcp_bic.c 
    
    """

dirs_to_delete = r"""
    arch\x86\ia32
"""

files_to_delete = r"""
    mm\nobootmem.c
    mm\nommu.c
    net\ipv4\tcp_bic.c 
"""

def delete_redundant():
    print ("delete_redundant")
    for lines in dirs_to_delete.split("\n"):
        print lines
        subpath = lines.strip()
        if len(subpath) and os.path.exists(dst_path + subpath):
            print dst_path + subpath
            shutil.rmtree(dst_path + subpath)
    for lines in files_to_delete.split("\n"):
        print lines
        subpath = lines.strip()
        if len(subpath) and os.path.exists(dst_path + subpath):
            print dst_path + subpath
            #os.system("del  /F /Q " + dst_path + subpath)
            os.remove(dst_path + subpath)
    

# copy_files(gl_subpaths)
temp_ = r"""
    drivers\vhost
    drivers\virtio
    
    drivers\net\ethernet\i825xx\82596.c
    
    drivers\net\loopback.c
    drivers\net\tun.c
    drivers\net\veth.c
    drivers\net\virtio_net.c
    drivers\net\vxlan.c
    drivers\net\ethernet\intel\e1000e

    
"""
copy_files( temp_)

#print ("delete_redundant")
#delete_redundant()

os.system("pause")

ptee.kill()
