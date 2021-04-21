# Dirty Cow exploit

## How to start?

Need to do steps from [Main way #1](https://github.com/MrOnimus/42_boot2root/blob/master/writeup1.md) to start with `laurie` user, or steps from [Opening ISO file](https://github.com/MrOnimus/42_boot2root/blob/master/bonus/Opening_ISO_file.md) to start with `zaz` user.

## Exploring the possibility of privilege escalation

When we have access to laurie, or, again, any other user - we can check linux-core version with `uname -r` command, Ubuntu version with `lsb_release -a` command, and than try to find out if any exploit to privilege escalation exist.

And there is [one](https://www.exploit-db.com/exploits/40839) (actually more than one, but this exploit execute without problems first).

You just need to:
1. Copy its source code into c file;
2. Compile it with `gcc -pthread exploit.c -o exploit -lcrypt`;
3. Run the resulting executable.

After that you will have user 'firefart' with password you choose.
Just add `su firefart` (execute it, not just paste it into your CLI). **You are root now!**
