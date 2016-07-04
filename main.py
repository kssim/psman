#!/usr/bin/env python

import sys
from psman import Psman
from optparse import OptionParser


def main():
	parser = OptionParser('Usage: %prog -n <process name>)')
	parser.add_option('-n', '--name', dest='process_name', type='string', help='process name')
	parser.add_option('-p', '--pid', dest='process_id', type='int', help='process id')
	parser.add_option('-s', '--show', dest='show_process_info', action='store_true', help='show process information.')

	(options, args) = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		exit(1)

	if options.process_name is None and options.process_id is None:
		print ('Please input process id or process name, you want to manage.')
		exit(1)

	pinfo = options.process_name if options.process_name is not None else options.process_id
	p = Psman(pinfo)

	if options.show_process_info == True:
		p.print_process_info()
	else:
		print ('process name : %s' % p.get_process_name())
		print ('process id : %s' % p.pid)


if __name__ == '__main__':
	main()
