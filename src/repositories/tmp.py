#!/usr/bin/env python3
import re, os, sys
root = '/'
output = '''Filesystem     Type      Size  Used Avail Use% Mounted on
udev           devtmpfs  1.9G     0  1.9G   0% /dev
tmpfs          tmpfs     389M  780K  388M   1% /run
/dev/nvme0n1p1 ext4       20G  5.2G   15G  27% /
tmpfs          tmpfs     1.9G     0  1.9G   0% /dev/shm
tmpfs          tmpfs     5.0M     0  5.0M   0% /run/lock
tmpfs          tmpfs     1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/loop0     squashfs   88M   88M     0 100% /snap/core/5328
/dev/loop1     squashfs   13M   13M     0 100% /snap/amazon-ssm-agent/495
/dev/loop2     squashfs   91M   91M     0 100% /snap/core/6405
/dev/loop3     squashfs   18M   18M     0 100% /snap/amazon-ssm-agent/1068
tmpfs          tmpfs     389M     0  389M   0% /run/user/1000
/dev/loop4     squashfs   92M   92M     0 100% /snap/core/6531'''
pattern = re.compile(r'\s+(\d+\.?\d+[A-Z]).+\s+(\d+\.?\d+[A-Z])\s+\d+%\s+{}?[\n]?$'.format(root))
for line in output.split('\n'):
       result = [(match.group(1), match.group(2)) for match in pattern.finditer(line)]
       if result:
             print(result[0])
