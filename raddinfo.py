#!/usr/bin/ python
# login to dac module?
# mchristofas 10/12/18

import os
import paramiko

os.system('clear')
with open('radds.txt', 'r') as f:
    for ip in f:
        ip = str.rstrip(ip)
        port = 22
        username = 'radd6000'
        password = 'ippv4000'


        cmd = 'hostname'
        cmda = 'uptime'
        cmdb= 'cat /etc/SuSE-release'
        cmdd= 'sudo dmidecode |grep Product'


        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password, timeout=4)

            stdin, stdout, stderr = ssh.exec_command(cmd)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            resp = resp.strip('\n')
            print()
            print(ip, " ", resp)

            stdin, stdout, stderr = ssh.exec_command(cmda)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            resp = resp.lstrip()
            resp = resp.strip('\n')
            print(resp)

            stdin, stdout, stderr = ssh.exec_command(cmdb)
            outlines = stdout.readlines()
            resp = ''.join(outlines)

            print(resp)

            stdin, stdout, stderr = ssh.exec_command(cmdd)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            print(resp)

        except:
            print("not online\n")
        ssh.close()
