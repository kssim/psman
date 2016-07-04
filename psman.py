import subprocess
from collections import namedtuple

class Psman(object):

	pid = -1
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
		self.stat_file_field = self.get_process_info()


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
		with open('/proc/%s/stat' % self.pid, 'rb') as f:
			values = f.readline().split()[1:]

		return namedtuple('ProcessData', self.stat_file_field)._make(tuple(values))


	## Outer method
	def get_process_name(self):
		return self.stat_file_field.p_name

	def print_process_info(self):
		print ('name : %s' % self.stat_file_field.p_name)
		print ('pid : %s' % self.pid)
		print ('state : %s' % self.stat_file_field.p_status)
		print ('parent pid : %s' % self.stat_file_field.ppid)
		print ('process group id : %s' % self.stat_file_field.pgrp)
		print ('process session id : %s' % self.stat_file_field.session)

