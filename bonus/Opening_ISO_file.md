# Opening the file system of the ISO file

## Opening the given ISO file

To open the given ISO file we need to mount it to any mount point like that [(Source)](https://linuxize.com/post/how-to-mount-iso-file-on-linux/):

    sudo mount <path_to_the_iso_file> <path_to_the_mount_point> -o loop

**Important:** you'd better have access to root on the system on which you will be doing this for sake of simplicity of the process. [(Source)](https://unix.stackexchange.com/questions/32008/how-to-mount-an-image-file-without-root-permission)


## Find a compressed file system

Apparently the ISO image given to us is a LiveCD. So, according to the first answer [here](https://unix.stackexchange.com/questions/287446/what-is-filesystem-squashfs-and-why-does-it-take-so-long-to-load-on-to-bootable) we should definitely try to find something with `.squashfs` extension, ideally file named exactly `filesystem.squashfs`. We can do this using `find <path_to_the_mount_point> -name "filesystem.squashfs"` command. The result of running this command is that we find the file we want.

## Decompressing the squashfs file system

We cannot decompress the `filesystem.squashfs` file directly, as the image is mounted in mode 'readonly', so, we need to copy it somewhere else. After copying it, we must check that we have installed the `unsquashfs` utility. If so, we can use the `unsquashfs` utility on the copy of the `filesystem.squashfs` file. [(Source)](https://stackoverflow.com/questions/2806432/reading-a-squashfs-archive)

## Trying to find a decrypted password from any user

Maybe password will be in the `.bash_history` file. If it turns out that this is the case, then we are very lucky. To do that we can execute next command:

    find squashfs-root -name ".bash_history" -exec cat {} \;
    
 Okay, we've found all `.bash_history` files, and even printed out their content. But there are more than a thousand lines of commands. Let's make our work simpler. Shall we?

    find squashfs-root -name ".bash_history" -exec cat {} \; | grep -A 1 "laurie\|zaz\|root\|lmezard\|thor"

We now have less than a third of all the content of the files we are interested in. After running our eyes over the lines we received, we find one that is of great interest to us. Something like a password from the user `zaz`. Actually, that's what password is.

**We've got to the zaz user! Now you should proceed to the 1st writeup.**

## What to do next?

If you want it to be short and simple - proceed to the [Dirty COW writeup](https://github.com/MrOnimus/42_boot2root/blob/master/bonus/Dirty_COW.md). By following this path, you will come along the **Bonus way #1**:

![Bonus way #1](https://drive.google.com/uc?export=view&id=1eUNJ5Mz21R8t2LFoC3ybnX-dVSGYO_oy)

Of course, you can choose another path. Proceed to the `zaz` path of the [Main way #1](https://github.com/MrOnimus/42_boot2root/blob/master/writeup1) to make it long, hard, and funny. By following this path, you will come along the **Bonus way #2**:

![Bonus way #2](https://drive.google.com/uc?export=view&id=1KkWnnjpG7Bo9byMjtoz8TyJy8fT1mtPl)