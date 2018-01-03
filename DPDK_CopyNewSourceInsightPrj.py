
import os,shutil

old_name = "dpdk-stable-17.05.2-20L3Fwd"
new_name = "dpdk-stable-17.05.2-34VMDQ"


if old_name != new_name:
    shutil.copytree("./" + old_name, "./" + new_name)
    os.chdir("./" + new_name)
    list_fnames = os.listdir("./")
    for fname in list_fnames:
        if fname.find(old_name) != -1:
            new_fname = fname.replace(old_name, new_name)
            os.rename(fname, new_fname)
