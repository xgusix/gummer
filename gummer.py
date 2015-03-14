from load_mod import *
import argparse
import logging

DEFAULT_OUTPUT = '101'

def init():

	logger = set_up_log()

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--list_anal", action='store_true',
		help="List analyzers.")
	parser.add_argument("-ldb", "--list_databases", action='store_true',
		help="List db connectors.")
	parser.add_argument("-lo", "--list_outputs", action='store_true',
		help="List possible output formats.")
	parser.add_argument("-lc", "--list_collectors", action='store_true',
		help="List collectors.")
	parser.add_argument("-a", "--analyzer", nargs=1,
		help="ID of the analyzer to use.")
	parser.add_argument("-db", "--dbconnector", nargs=1,
		help="ID of the database connector to use.")
	parser.add_argument("-o", "--output", nargs=1,
		help="ID of the output to use.")
	parser.add_argument("-c", "--collector", nargs=1,
		help="ID of the collector to use.")
	
	return parser, logger

def set_up_log():

	logger = logging.getLogger('gummerlog')
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	filelog = logging.FileHandler('log/gummer.log')
	filelog.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	consolelog = logging.StreamHandler()
	consolelog.setLevel(logging.ERROR) #Change to ERROR before the release
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
	filelog.setFormatter(formatter)
	consolelog.setFormatter(formatter)
	# add the handlers to logger
	logger.addHandler(consolelog)
	logger.addHandler(filelog)
	return logger

def print_options(option):
	try:
		logger.debug('Entering function print_options.')
		attributes = get_modules(option)
		#Sort attributes:
		attributes = sorted(attributes, key=lambda k: k['aid'])
		for attribute in attributes:
			try:
				print "[%s] %s" % (attribute['aid'], attribute['name'])
				print "\t%s" % (attribute['desc'])

			except Exception, e:
				msg = "There was an error loading the module %s: %s"  % (attribute, e)
				logger.error(msg)
	except Exception, e:
		msg = "There was an error loading the module %s: %s"  % (option, e)
		logger.error(msg)
		exit(1)


if __name__ == '__main__':
	
	parser, logger = init()

	args = parser.parse_args()

	if args.list_anal:
		print_options("analyzers")
		exit(0)
	elif args.list_databases:
		print_options("db_connectors")
		exit(0)
	elif args.list_collectors:
		print_options("collectors")
		exit(0)
	elif args.list_outputs:
		print_options("output")
		exit(0)
	elif args.analyzer and args.dbconnector:
		flag = 0

		analyzer = get_module("analyzers", args.analyzer[0])
		if analyzer == None:
			flag += 1
			msg = "Cannot find the analyzer: %s" % (args.analyzer[0])
			logger.error(msg)


		connector = get_module("db_connectors", args.dbconnector[0])
		if connector == None:
			flag += 1
			msg = "Cannot find the connector: %s" % (args.dbconnector[0])
			logger.error(msg)

		if not args.output:
			output = get_module("output", DEFAULT_OUTPUT)
		else:
			output = get_module("output", args.output[0])

		if output == None:
			flag += 1
			msg = "Cannot find the output: %s" % (args.output[0])
			logger.error(msg)

		if flag:
			exit(-1)

		data = analyzer.launch(connector)
		try:
			output.launch(data)
		except Exception, e:
			msg = "There was an error processing the output: %s"  % (e)
			logger.error(msg)
			exit(1)

	elif args.collector and args.dbconnector:
		flag = 0

		collector = get_module("collectors", args.collector[0])
		if collector == None:
			flag += 1
			msg = "Cannot find the collector: %s" % (args.collector[0])
			logger.error(msg)


		connector = get_module("db_connectors", args.dbconnector[0])
		if connector == None:
			flag += 1
			msg = "Cannot find the connector: %s" % (args.dbconnector[0])
			logger.error(msg)

		if flag:
			exit(-1)

		data_s, data_f = collector.launch(connector)
		msg = "Insertions succeded/Insertions failed: %d/%d" % (data_s, data_f) 
		logger.info(msg)

	else:
		print parser.print_usage()
