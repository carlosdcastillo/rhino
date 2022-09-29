* What is this?

This is my simple backup script that I point to the directories where I'm writing code (to prevent losing uncommited changes) and avoid overwriting binary files that are output by my programs (such as Pytorch models). It operates by copying them to another location on a fixed schedule and out of the way. I mess up and remove, overwrite/damage a file about once every few months, this script prevents me from losing large amounts of work. I usually run this software on my Mac, and I write code on Linux GPU workstation/server. The code is authoritative.

You should also use version control and other more definitive forms of backup.
