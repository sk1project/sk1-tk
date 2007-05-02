#! /usr/bin/env python
 
# sK1 - A Python & Tcl/Tk based vector graphics editor for prepress
# Copyright (C) 2003-2007 by Igor E. Novikov

# Skencil - A Python-based interactive drawing program
# Copyright (C) 1998, 1999, 2000, 2001, 2002, 2003, 2005 by Bernhard Herzog 

def parse_cmd_line():
    setup = None
    argv = sys.argv[1:]
    flags = {}
    flags['standard'] = {'prefix': '/usr/local/', 'destdir':''}
    flags['pax'] = {'XSHM': ''}
    flags['intl'] = {'files': ''}
    flags['sketch'] = {'imaging-include':
                       os.path.join(sys.prefix, 'include',
                                    'python' + sys.version[:3])}
    flags['tk'] = {'autoconf': 0, 'flags': ''}
    flags['make_defs'] = []
    if len(argv) == 0:
        command = 'help'
    else:
        command = argv[0]
        if command in ('-h', '--help'):
            command = 'help'
        del argv[0]
    for arg in argv:
        if '=' in arg:
            arg, value = split(arg, '=', 1)
        else:
            value = None
        if arg == '--prefix':
            if value is None:
                print 'Value required for option --prefix'
                sys.exit(1)
            flags['standard']['prefix'] = value
        elif arg == '--dest-dir':
            flags['standard']['destdir'] = value
        elif arg == '--python-setup':
            setup = value
        elif arg == '--pax-no-xshm':
            flags['pax']['XSHM'] = '-DPAX_NO_XSHM'
        elif arg == '--imaging-include':
            if value is None:
                print 'Value required for option --imaging-include'
                sys.exit(1)
            flags['sketch']['imaging-include'] = value
        elif arg == '--with-nls':
            flags['intl']['files'] = 'intl intl.c'
        elif arg == '--tk-flags':
            flags['tk']['flags'] = value
        elif arg == '--tk-autoconf':
            flags['tk']['autoconf'] = 1
        elif arg in ('-h', '--help'):
            command = 'help'
        elif arg[0] != '-' and value:
            flags['make_defs'].append(pipes.quote(arg + '=' + value))
        else:
            sys.stderr.write('Unknown option %s\n' % arg)
            sys.exit(1)
    return command, flags, setup
	
def main():
	command, flags, setup = parse_cmd_line()

if __name__ == '__main__':
	main()