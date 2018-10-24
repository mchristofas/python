#!/usr/bin/ python
# login to dac module?
# mchristofas 10/12/18

import os
import paramiko

os.system('clear')
with open('daclist.txt', 'r') as f:
    for ip in f:
        ip = str.rstrip(ip)
        port = 22
        username = 'acc4000d'
        password = 'ippv4000'


        cmd = 'hostname'
        cmda = 'uptime'
        cmdb= 'cat /etc/SuSE-release'
        cmdc = 'cat /etc/redhat-release'


        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password, timeout=4)

            stdin, stdout, stderr = ssh.exec_command(cmd)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            resp = resp.strip('\n')
            print
            print ip, " ", resp

            stdin, stdout, stderr = ssh.exec_command(cmda)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            resp = resp.lstrip()
            resp = resp.strip('\n')
            print resp

            stdin, stdout, stderr = ssh.exec_command(cmdb)
            outlines = stdout.readlines()
            resp = ''.join(outlines)

            print resp

            stdin, stdout, stderr = ssh.exec_command(cmdc)
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            print resp

        except:
            print "not online\n"
