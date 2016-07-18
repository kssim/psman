import subprocess
import os.path
import time
from collections import namedtuple
from utils import Logger

PROCESS_STAT_PATH = '/proc/%s/stat'
PROCESS_CMDLINE_PATH = '/proc/%s/cmdline'

class Psman(object):

    process_check_interval = 10
    pid = []
    process_cmdline = []
    stat_data = []
    stat_file_field = ['p_name', 'p_status', 'ppid', 'pgrp', 'session', 'tty_nr', 'tpgid',
                    'flags', 'minflt', 'cminflt', 'majflt', 'cmajflt', 'utime', 'stime',
                    'cutime', 'cstime', 'priority', 'nice', 'num_threads', 'itrealvalue',
                    'start_time', 'v_size', 'rss', 'rss_lim', 'start_code', 'end_code',
                    'start_stack', 'kstk_esp', 'kstk_eip', 'signal', 'blocked',
                    'sig_ignore', 'sig_catch', 'wchan', 'nswap', 'cnswap', 'exit_signal',
                    'processor', 'rt_priority', 'policy', 'delayacct_blkio_ticks',
                    'guest_time', 'cguest_time', 'start_data', 'end_data', 'start_brk',
                    'arg_start', 'arg_end', 'env_start', 'env_end', 'exit_code']

    def __init__(self, pinfo):
        if type(pinfo) is str:
            self.pid = self.get_pid(pinfo)
        else:
            self.pid.append(pinfo)

        self.set_process_info()
        self.set_process_cmdline()


    ## Inner method
    def get_pid(self, process_name):
        try:
            process_id = subprocess.check_output(['pidof', process_name]).strip().split(' ')
        except subprocess.CalledProcessError:
            print ('The process name is not vaild.')
            return []
        else:
            return process_id

    def set_process_info(self):
        for i, pid in enumerate(self.pid):
            stat_path = PROCESS_STAT_PATH % pid
            if os.path.exists(stat_path) == False:
                continue

            with open(stat_path, 'rb') as f:
                values = f.readline().split()[1:]

            self.stat_data.append(namedtuple('ProcessData', self.stat_file_field)._make(tuple(values)))

    def set_process_cmdline(self):
        for pid in self.pid:
            cmdline_path = PROCESS_CMDLINE_PATH % pid
            if os.path.exists(cmdline_path) == False:
                continue

            with open(cmdline_path, 'rb') as f:
                self.process_cmdline.append(f.readline().replace('\0', ' '))

    def update_process_info(self, index, process_name):
        stat_path = PROCESS_STAT_PATH % self.pid[index]
        if os.path.exists(stat_path) == False:
            return False

        with open(stat_path, 'rb') as f:
            values = f.readline().split()[1:]

        self.stat_data[index] = namedtuple('ProcessData', self.stat_file_field)._make(tuple(values))
        return True

    def restart_process(self, index):
        print ('Restart process')
        pid = subprocess.Popen(self.process_cmdline[index].split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).pid
        self.pid[index] = pid

    def delete_dead_process(self, index):
        self.stat_data.pop(index)
        self.pid.pop(index)
        self.process_cmdline.pop(index)



    ## Outer method
    def exist_process_info(self):
        return False if len(self.stat_data) == 0 else True

    def set_process_check_interval(self, interval):
        self.process_check_interval = interval

    def check_process(self, recursive_start):
        Logger().psman_log('Start check process...')

        while True:
            for i, data in enumerate(self.stat_data):
                print ('\'%s(%s)\' process status is \'%s\'.' % (data.p_name, self.pid[i], data.p_status))
                update_result = self.update_process_info(i, data.p_name)

                if update_result == True:
                    continue

                if recursive_start == None or recursive_start == False:
                    print ('Process%s died.' % data.p_name)
                    self.delete_dead_process(i)
                    continue

                self.restart_process(i)

            if len(self.stat_data) == 0:
                break

            time.sleep(self.process_check_interval)

        Logger().psman_log('Stop check process...')

    def print_brief_process_info(self):
        for i, data in enumerate(self.stat_data):
            print ('=================================================================================================')
            print ('Name : %s' % data.p_name)
            print ('Pid : %s' % self.pid[i])
            print ('State : %s' % data.p_status)
            print ('cmdline : %s' % self.process_cmdline[i])
            print ('=================================================================================================')

    def print_process_info(self):
        for i, data in enumerate(self.stat_data):
            print ('=================================================================================================')
            print ('Name : %s' % data.p_name)
            print ('Pid : %s' % self.pid[i])
            print ('State : %s' % data.p_status)
            print ('cmdline : %s' % self.process_cmdline[i])
            print ('Parent pid : %s' % data.ppid)
            print ('Process group id : %s' % data.pgrp)
            print ('Process session id : %s' % data.session)
            print ('Controlling terminal of the process : %s' % data.tty_nr)
            print ('ID of the foreground process group : %s' % data.tpgid)
            print ('Kernel flags word of the process : %s' % data.flags)
            print ('Minor faults the process has made : %s' % data.minflt)
            print ('Minor faults the process\'s waited-for children have made : %s' % data.cminflt)
            print ('Major faults the process has made : %s' % data.majflt)
            print ('Major faults the process\'s waited-for children have made : %s' % data.cmajflt)
            print ('Time that this process has been scheduled in user mode : %s' % data.utime)
            print ('Time that this process has been scheduled in kernel mode : %s' % data.stime)
            print ('Time that this process\' waited-for children have been scheduled in user mode : %s' % data.cutime)
            print ('Time that this process\' waited-for children have been scheduled in kernel mode : %s' % data.cstime)
            print ('For processes running a real-time scheduling policy : %s' % data.priority)
            print ('Nice value : %s' % data.nice)
            print ('Number of threads : %s' % data.num_threads)
            print ('The time of jiffies : %s' % data.itrealvalue)
            print ('The time the process started after system boot : %s' % data.start_time)
            print ('Virtual memory size : %s' % data.v_size)
            print ('Resident set size : %s' % data.rss)
            print ('Current soft limit : %s' % data.rss_lim)
            print ('Address above which program text can run : %s' % data.start_code)
            print ('Address below which program text can run : %s' % data.end_code)
            print ('Address of the start of the stack : %s' % data.start_stack)
            print ('Current value of ESP : %s' % data.kstk_esp)
            print ('Current EIP : %s' % data.kstk_eip)
            print ('The bitmap of pending signals : %s' % data.signal)
            print ('The bitmap of blocked signals : %s' % data.blocked)
            print ('The bitmap of ignored signals : %s' % data.sig_ignore)
            print ('The bitmap of caught signals : %s' % data.sig_catch)
            print ('The \'channel\' in which the process is waiting : %s' % data.wchan)
            print ('Number of pages swapped : %s' % data.nswap)
            print ('Cumulative nswap for child process : %s' % data.cnswap)
            print ('Signal to be sent to parent when we die : %s' % data.exit_signal)
            print ('CPU number last executed on : %s' % data.processor)
            print ('Real-time scheduling priority : %s' % data.rt_priority)
            print ('Scheduling policy : %s' % data.policy)
            print ('Aggregated block I/O delays : %s' % data.delayacct_blkio_ticks)
            print ('Guest time of the process : %s' % data.guest_time)
            print ('Guest time of the process\'s children : %s' % data.cguest_time)
            print ('Address above which program initialized : %s' % data.start_data)
            print ('Address below which program initialized : %s' % data.end_data)
            print ('Address above which program heap can be expanded : %s' % data.start_brk)
            print ('Address above which program command-line arguments : %s' % data.arg_start)
            print ('Address below which program command-line arguments : %s' % data.arg_end)
            print ('Address above which program environment : %s' % data.env_start)
            print ('Address below which program environment : %s' % data.env_end)
            print ('The thread\'s exit status : %s' % data.exit_code)
            print ('=================================================================================================')
