#!/usr/bin/env python

import sys
from psman import Psman
from optparse import OptionParser
from utils import Logger

def main():
    parser = OptionParser('Usage: %prog -n <process name>')
    parser.add_option('-n', '--name', dest='process_name', type='string', help='process name')
    parser.add_option('-p', '--pid', dest='process_id', type='int', help='process id')
    parser.add_option('-s', '--show', dest='show_process_info', action='store_true', help='show process information')
    parser.add_option('-c', '--check', dest='checked', action="store_true", help='process alive check')
    parser.add_option('-i', '--interval', dest='interval', type='int', help='process check interval (default 10s)')
    parser.add_option('-r', '--recursive', dest='recursive_start', action="store_true", help='process check and recursive start')
    parser.add_option('-v', '--verbose', dest='verbose', action="store_true", help='Verbose mode')

    (options, args) = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        exit(1)

    if options.process_name is None and options.process_id is None:
        print ('Please input process id or process name, you want to manage.')
        exit(1)

    Logger().set_verbose_mode(options.verbose)

    pinfo = options.process_name if options.process_name is not None else options.process_id
    p = Psman(pinfo)

    if p.exist_process_info() == False:
        print ('There is no process data.')
        exit(1)

    if options.interval is not None:
        p.set_process_check_interval(options.interval)


    if options.show_process_info == True:
        p.print_process_info()
    elif options.checked == True:
        p.check_process(options.recursive_start)
    else:
        p.print_brief_process_info()


if __name__ == '__main__':
    main()
