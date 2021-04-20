# Getting root on system boot

## Getting into boot menu

Menu will appear if you press and hold `Shift` during loading Grub, if you boot using BIOS. When your system boots using UEFI, press `Esc`. Either of the two options will work in our case. We've found out it [here](https://askubuntu.com/questions/16042/how-to-get-to-the-grub-menu-at-boot-time).

## Getting the list of available kernels

In order to get a list of available kernels, we just have to press `Tab` when we are in the boot menu. After we press `Tab` we will see only one available kernel named `live`.

## Passing custom boot option

In order for the argument to have the value of interest during kernel loading, it must be set by writing it after the chosen kernel like that: `<kernel> <argument>`. In our case it will be `live init=/bin/bash`. We know it from the official [Debian boot process documentation](https://wiki.debian.org/BootProcess).

After doing that we'll appear in the bash shell under user `root`. **You are root now!**