# Dirty Cow exploit

When we have access to laurie - we can go the way the creators intended or we can check linux-core version *uname -r* and Ubuntu version *lsb_release -a*, and try to find out if any exploit to privilege escalation exist.
And there is one (actually more than one, but this exploit execute without problems first) * https://www.exploit-db.com/exploits/40839 *
You just need to copy it into c file, compile with * gcc -pthread exploit.c -o exploit -lcrypt * and run
After that you will have user 'firefart' with password you choose.
*su firefart* - you are root now.