import inspect, sys, traceback, System

def main():
	try:
		build_module = get_main_module()
		args = sys.argv[1:]

		tasks = parse_args(build_module, args)

		dump_cfg()

		for task in tasks:
			cprint('Executing %s' % task, 'Cyan')
			task_fn = getattr(build_module, task)
			task_fn()
		cprint('\nBuild Succeeded!', 'Green')
	except:
		cprint('\nBuild Failed!\n', 'Red')
		print(traceback.format_exc())
		sys.exit(1)

def get_main_module():
	return __import__('__main__')

def parse_args(build_module, args):
	arg_name = None
	tasks = []
	for arg in args:
		if arg.startswith('--'):
			arg_name = arg[2:]
		elif arg_name:
			arg_type = type(getattr(build_module, arg_name, ''))
			setattr(build_module, arg_name, arg_type(arg))
			arg_name = None
		else:
			tasks.append(arg)
	return tasks

def cprint(message, fg, end='\n'):
	System.Console.ForegroundColor = getattr(System.ConsoleColor, fg)
	sys.stdout.write(message)
	sys.stdout.write(end)
	System.Console.ResetColor()

def dump_cfg():
	build_module = get_main_module()

	names = [n for n in dir(build_module) if not n.startswith('_') and type(getattr(build_module, n)) in [str, int, bool]]

	pad = max([len(x) for x in names])

	for name in names:
		cprint(name.rjust(pad) + ': ', 'White', '')
		print(getattr(build_module, name))
