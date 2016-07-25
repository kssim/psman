# psman
This program allows you to easily manage your Linux process.

And also it provides the ability to monitor the specific process.


# Currently
Currently under development.




# Usage
## Basic usage
<pre>
Usage: main.py -n <process name>

Options:
	-h, --help            show this help message and exit
	-n PROCESS_NAME, --name=PROCESS_NAME process name
	-p PROCESS_ID, --pid=PROCESS_ID process id
	-s, --show            show process information
	-c, --check           process alive check
	-i INTERVAL, --interval=INTERVAL process check interval (default 10s)
	-r, --recursive       process check and recursive start
	-v, --verbose         Verbose mode
</pre>


## Show process info
<pre>
# ./main.py -n cron
=================================================================================================
Name : (cron)
Pid : 407
State : S
cmdline : /usr/sbin/cron -f
=================================================================================================
</pre>

<pre>
# ./main.py -n cron -s
=================================================================================================
Name : (cron)
Pid : 407
State : S
cmdline : /usr/sbin/cron -f
Parent pid : 1
Process group id : 407
Process session id : 407
Controlling terminal of the process : 0
ID of the foreground process group : -1
Kernel flags word of the process : 1077944576
Minor faults the process has made : 12339
Minor faults the process's waited-for children have made : 1236964
Major faults the process has made : 1
Major faults the process's waited-for children have made : 152
Time that this process has been scheduled in user mode : 2
Time that this process has been scheduled in kernel mode : 60
Time that this process' waited-for children have been scheduled in user mode : 342
Time that this process' waited-for children have been scheduled in kernel mode : 184
For processes running a real-time scheduling policy : 20
Nice value : 0
Number of threads : 1
The time of jiffies : 0
The time the process started after system boot : 2156
Virtual memory size : 30498816
Resident set size : 650
Current soft limit : 18446744073709551615
Address above which program text can run : 1
Address below which program text can run : 1
Address of the start of the stack : 0
Current value of ESP : 0
Current EIP : 0
The bitmap of pending signals : 0
The bitmap of blocked signals : 0
The bitmap of ignored signals : 0
The bitmap of caught signals : 65537
The 'channel' in which the process is waiting : 18446744073709551615
Number of pages swapped : 0
Cumulative nswap for child process : 0
Signal to be sent to parent when we die : 17
CPU number last executed on : 1
Real-time scheduling priority : 0
Scheduling policy : 0
Aggregated block I/O delays : 0
Guest time of the process : 0
Guest time of the process's children : 0
Address above which program initialized : 0
Address below which program initialized : 0
Address above which program heap can be expanded : 0
Address above which program command-line arguments : 0
Address below which program command-line arguments : 0
Address above which program environment : 0
Address below which program environment : 0
The thread's exit status : 0
=================================================================================================
</pre>


## Check process
<pre>
./main.py -n cron -c
'(cron)(407)' process status is 'S'.
</pre>

<pre>
./main.py -n cron -c -i 5
'(cron)(407)' process status is 'S'.
</pre>

<pre>
./main.py -n cron -c -r
'(cron)(407)' process status is 'S'.
</pre>