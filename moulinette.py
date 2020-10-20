#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import subprocess
import requests
import sys
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://nsa.epitest.eu"

def check_argument(argv):
    if len(sys.argv) != 2:
        usage(argv)

def usage(argv):
    print(argv[0] + " : slug is require")
    sys.exit(84)

def cmd_execute(cmd, steep):
    print ("<> STEEP "+ str(steep) + " <>")
    print("\n\ncommande :")
    print(cmd)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    result = stdout.decode("utf-8")
    print("\n\nresultat:")
    print(result)
    return (result)

def check_sudo():
    if os.geteuid() == 0 :
        return True
    return False

if __name__ == '__main__':

    if check_sudo() == False:
        print("[-] You need admin rights")
        sys.exit(84)
    check_argument(sys.argv)
    slug = sys.argv[1]
    login = False
    while login == False :
        username = "USERNAME EPITECH"
        try:
            password = "PASSWORD EPITECH"
        except Exception as error:
            print('ERROR', error)
        try:
            payload = {'slug' : slug}
            response = requests.post(url + '/api/login', verify=False, auth=(username, password), json=payload)
            print(response)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(str(e))
            exit(84)
        if response.status_code == 200:
            login = True
        elif response.status_code == 403:
            print(str(response.status_code) + " " + response.json()['error'])
        else:
            print(response.json()['error'])
            sys.exit(84)

    data = response.json()
    print(data)
    token = data['security']['token']
    left = data['left']

    print ("il te reste %d essaie mais tranquille" %(left))
    print ("tester gratuitement (Y/N) ?")
    x = input().upper()

    if len(x) == 0 or x[0] != "Y":
        print ("Good bye !")
        sys.exit(84)
    result = []
    for index, cmd in enumerate(data['cmd']):
        steep = cmd_execute(cmd, index + 1)
        print("Step suivante (Y/N)")
        x = input().upper()
        if len(x) == 0 or x[0] !="Y":
            print("Bonne Piscine")
            sys.exit(84)
        result.append([cmd, steep])
    payload = {'content': result, 'slug' : slug}
    print("\nJSON final: ")
    print(result)
    
    
    #envoyer information au server
    # build = requests.post(url + '/api/build', verify=False, json=payload, auth=(username, token))
    # print (build.json())
