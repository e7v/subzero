#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''subdomain bruteforcer. uses dns.resolver + dig to check for results. '''

import dns.resolver 
import argparse
import threading
import certscan
import dig
__author__ = 'e7v'
__version__ = '0.2B Clint Eastwood'
__url__='https://github.com/e7v/subzero'
__description__='''
___________________________________________
Subzero, a subdomain bruteforcer.
Version: '''+__version__+'''
Author: '''+__author__+'''
Github: '''+__url__+'''
___________________________________________
'''
__epilog__='''
example:
  subzero domain.com
  subzero domain.com -w wordlist.txt -o output.txt
  '''

#global variables
global args
log = []
count = 0
wordlist = []
wordlist_size = 0 

 

def main():
    global count
    while len(wordlist) > 0:
        target = wordlist.pop() + '.' + args['domain']
        for success in dig.check(target, True):
            log.append(success)
        count += 1
        print('\rComplete: {} / {}'.format(count, wordlist_size), end='')
    
if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description=__description__,
                                    prog='subzero',
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog=__epilog__)
    #parser.add_argument('-d','--domain', help='Domain', required=True)
    parser.add_argument('domain', help='target to scan, like domain.com')
    parser.add_argument('-w','--wordlist', help='Wordlist', default='wordlists/subdomains.txt', required=False)
    parser.add_argument('-v','--verbose', help='Verbose', required=False, action='store_true', default=True)
    parser.add_argument('-o','--output', help='Output file', required=False, default=False)
    parser.add_argument('-t','--threadcount', help='Number of Threads', required=False, default=100)    
    
    args = vars(parser.parse_args())
    threads = []
    
    header = '''\033[94m      
            ,gg,                                                                     
           i8""8i               ,dPYb,                                               
           `8,,8'               IP'`Yb                                               
            `88'                I8  8I                                               
            dP"8,               I8  8'                                               
           dP' `8a  gg      gg  I8 dP        ,gggg,   ,ggg,    ,gggggg,    ,ggggg,   
          dP'   `Yb I8      8I  I8dP   88gg d8"  Yb  i8" "8i   dP""""8I   dP"  "Y8ggg
      _ ,dP'     I8 I8,    ,8I  I8P    8I  dP    dP  I8, ,8I  ,8'    8I  i8'    ,8I  
      "888,,____,dP,d8b,  ,d8b,,d8b,  ,8I,dP  ,adP'  `YbadP' ,dP     Y8,,d8,   ,d8'  
      a8P"Y88888P" 8P'"Y88P"`Y88P'"Y88P"'8"   ""Y8d8888P"Y8888P      `Y8P"Y8888P"    
                                               ,d8I'         fastest in the west                           
                                             ,dP'8I                                  
                                            ,8"  8I                                  
                                            I8   8I                                  
                                            `8, ,8I                                  
                                             `Y8P"                                   \033[0m\n'''
    print(header)
    if args['domain']:
        wordlist = open(args['wordlist'], 'r').readlines()
        wordlist = [i.strip() for i in wordlist]
        wordlist.reverse()
        wordlist_size = len(wordlist)
        threadcount = int(args['threadcount'])

        
        for i in range(threadcount):
            try:
                t = threading.Thread(target=main, daemon=True)
                threads.append(t)
                t.start()
            except:
                print('threading error')
    else:
        print("Usage: subzero.py -d [domain]")
        
        
    while True:
        if count < wordlist_size: 
            pass
        else:                
            print('\r\n')
            print('\n\nScanning certs...')
            
            certs = []
            certs2 = []
            for i in certscan.main(args['domain'],False):
                certs.append(i)
            for i in certs:
                for x in dig.check(i,True,False):
                    certs2.append(x)
            for i in certs2:
                if args['verbose']:
                    print(i)
            if args['output']:
                logfile = open(args['output'],'w')
                #remove duplicates
                deDuped = []
                log = certs2 + log
                for record in log:
                    if record not in deDuped:
                        deDuped.append(record)
                for i in deDuped: 
                    logfile.write(i+'\n')
            break