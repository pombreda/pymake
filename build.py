cfg = {
  'server': '.\SQLEXPRESS',
	'group': 'test',
	'task': 'migrate',
	'groups': {
		'test': [ 'ADOUtilsTests' ],
		'group2': [ 'db1', 'db2', 'db3' ]
	}
}

import subprocess

def drop_dbs():
	pass

def create_dbs():
	pass

def migrate():
	exec_sql('SELECT GETDATE()')

def script():
	print('executing ' + cfg['task'])

def exec_sql(sql, server=None, database=None):
	server = server or cfg['server']
	group = cfg['group']
	database = database or cfg['groups'][group][0]
	subprocess.check_call([
		'sqlcmd.exe', '-E',
		'-S', server,
		'-d', database,
		'-h', '-1',
		'-Q', sql
	])

if __name__ == '__main__':
	import optparse, inspect

	main_module = __import__('__main__')

	valid_tasks = [x[0] for x  in inspect.getmembers(main_module, inspect.isfunction)]
	valid_groups = cfg['groups'].keys()


	parser = optparse.OptionParser()
	parser.set_defaults(**cfg)
	for prop_name in cfg:
		prop_type = type(cfg[prop_name])
		if prop_type == int:
			parser.add_option('--' + prop_name, dest=prop_name, help='SQL Server instance. Default to %default')
		elif prop_type == str:
			pass
		elif prop_type == bool:
			pass
		parser.add_option('--' + prop_name, dest=prop_name, help='SQL Server instance. Default to %default')

	parser.add_option("-s", dest="server", help='SQL Server instance. Default to %default')
	parser.add_option("-g", dest="group", help='Group name. Default to %default, valid values are ' + ', '.join(valid_groups))
	parser.add_option("-t", dest="task", help='Task name. Default to %default, valid values are ' + ', '.join(valid_tasks))
	(options, args) = parser.parse_args()
	cfg.update(options.__dict__)

	print(cfg)

	task = getattr(main_module, options.task)
	print('ececuting task ' + options.task)
	task()
