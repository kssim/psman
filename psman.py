import subprocess
import os.path
from collections import namedtuple

PROCESS_STAT_PATH = '/proc/%s/stat'

class Psman(object):

	pid = -1
	stat_data = None
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
		self.pid = self.get_pid(pinfo) if type(pinfo) is str else pinfo
		self.stat_data = self.get_process_info()


	## Inner method
	def get_pid(self, process_name):
		try:
			process_id = subprocess.check_output(['pidof', process_name]).strip()
		except subprocess.CalledProcessError:
			print ('The process name is not vaild.')
			return -1
		else:
			return process_id

	def get_process_info(self):
		if self.pid == -1:
			return None

		stat_path = PROCESS_STAT_PATH % self.pid
		if os.path.exists(stat_path) == False:
			return None

		with open(stat_path, 'rb') as f:
			values = f.readline().split()[1:]

		return namedtuple('ProcessData', self.stat_file_field)._make(tuple(values))


	## Outer method
	def check_process_data(self):
		return stat_data

	def get_process_name(self):
		return self.stat_data.p_name

	def print_process_info(self):
		print ('=================================================================================================')
		print ('Name : %s' % self.stat_data.p_name)
		print ('Pid : %s' % self.pid)
		print ('State : %s' % self.stat_data.p_status)
		print ('Parent pid : %s' % self.stat_data.ppid)
		print ('Process group id : %s' % self.stat_data.pgrp)
		print ('Process session id : %s' % self.stat_data.session)
		print ('Controlling terminal of the process : %s' % self.stat_data.tty_nr)
		print ('ID of the foreground process group : %s' % self.stat_data.tpgid)
		print ('Kernel flags word of the process : %s' % self.stat_data.flags)
		print ('Minor faults the process has made : %s' % self.stat_data.minflt)
		print ('Minor faults the process\'s waited-for children have made : %s' % self.stat_data.cminflt)
		print ('Major faults the process has made : %s' % self.stat_data.majflt)
		print ('Major faults the process\'s waited-for children have made : %s' % self.stat_data.cmajflt)
		print ('Time that this process has been scheduled in user mode : %s' % self.stat_data.utime)
		print ('Time that this process has been scheduled in kernel mode : %s' % self.stat_data.stime)
		print ('Time that this process\' waited-for children have been scheduled in user mode : %s' % self.stat_data.cutime)
		print ('Time that this process\' waited-for children have been scheduled in kernel mode : %s' % self.stat_data.cstime)
		print ('For processes running a real-time scheduling policy : %s' % self.stat_data.priority)
		print ('Nice value : %s' % self.stat_data.nice)
		print ('Number of threads : %s' % self.stat_data.num_threads)
		print ('The time of jiffies : %s' % self.stat_data.itrealvalue)
		print ('The time the process started after system boot : %s' % self.stat_data.start_time)
		print ('Virtual memory size : %s' % self.stat_data.v_size)
		print ('Resident set size : %s' % self.stat_data.rss)
		print ('Current soft limit : %s' % self.stat_data.rss_lim)
		print ('Address above which program text can run : %s' % self.stat_data.start_code)
		print ('Address below which program text can run : %s' % self.stat_data.end_code)
		print ('Address of the start of the stack : %s' % self.stat_data.start_stack)
		print ('Current value of ESP : %s' % self.stat_data.kstk_esp)
		print ('Current EIP : %s' % self.stat_data.kstk_eip)
		print ('The bitmap of pending signals : %s' % self.stat_data.signal)
		print ('The bitmap of blocked signals : %s' % self.stat_data.blocked)
		print ('The bitmap of ignored signals : %s' % self.stat_data.sig_ignore)
		print ('The bitmap of caught signals : %s' % self.stat_data.sig_catch)
		print ('The \'channel\' in which the process is waiting : %s' % self.stat_data.wchan)
		print ('Number of pages swapped : %s' % self.stat_data.nswap)
		print ('Cumulative nswap for child process : %s' % self.stat_data.cnswap)
		print ('Signal to be sent to parent when we die : %s' % self.stat_data.exit_signal)
		print ('CPU number last executed on : %s' % self.stat_data.processor)
		print ('Real-time scheduling priority : %s' % self.stat_data.rt_priority)
		print ('Scheduling policy : %s' % self.stat_data.policy)
		print ('Aggregated block I/O delays : %s' % self.stat_data.delayacct_blkio_ticks)
		print ('Guest time of the process : %s' % self.stat_data.guest_time)
		print ('Guest time of the process\'s children : %s' % self.stat_data.cguest_time)
		print ('Address above which program initialized : %s' % self.stat_data.start_data)
		print ('Address below which program initialized : %s' % self.stat_data.end_data)
		print ('Address above which program heap can be expanded : %s' % self.stat_data.start_brk)
		print ('Address above which program command-line arguments : %s' % self.stat_data.arg_start)
		print ('Address below which program command-line arguments : %s' % self.stat_data.arg_end)
		print ('Address above which program environment : %s' % self.stat_data.env_start)
		print ('Address below which program environment : %s' % self.stat_data.env_end)
		print ('The thread\'s exit status : %s' % self.stat_data.exit_code)
		print ('=================================================================================================')
