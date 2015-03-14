import logging
import glob
import sys
import os

logger = logging.getLogger('gummerlog')

def load_module(module, directory):
	try:
		module = __import__(module, fromlist = [directory])
	except Exception, e:
		msg = "There was an error loading the module %s: %s" % (module, e)
		logger.error(msg)

	return module

def get_module_dic(module):
	dic_mod = {}
	for attribute in dir(module):
		if (not callable(getattr(module,attribute)) 
				and attribute.find('__') == -1):
			dic_mod[attribute] = getattr(module,attribute)

	return dic_mod

def get_modules(directory):
	modules = []

	if sys.platform.find("win") != -1:
		split = '\\'
	else:
		split = '/'
	
	for file1 in os.listdir(directory):
		folder = "%s%s%s" % (directory, split, file1)

		if os.path.isdir(folder):

	 		for file2 in os.listdir(folder):

	 			if file2.endswith(".py") and file2 != '__init__.py':

	 				file2 = "%s%s%s" % (folder, split, file2)
	 				module = file2.replace(split,'.')[:-3]
	 				module = load_module(module, directory)

	 				dic_mod = get_module_dic(module)

	 				if dic_mod != {}:
						modules.append(dic_mod)
					else:
						msg = ("There was an error loading the module %s: %s" 
							% (module, e))
						logger.error(msg)
	return modules

def get_module(directory, module_id):
	module_ret = None
	if sys.platform.find("win") != -1:
		split = '\\'
	else:
		split = '/'
	
	for file1 in os.listdir(directory):
		folder = "%s%s%s" % (directory, split, file1)
		if os.path.isdir(folder):

	 		for file2 in os.listdir(folder):

	 			if file2.endswith(".py") and file2 != '__init__.py':
	 				file2 = "%s%s%s" % (folder, split, file2)
	 				module = file2.replace(split,'.')[:-3]
	 				module = load_module(module, directory)
	 				try:
	 					if getattr(module, 'aid') == module_id:
	 						module_ret = module
	 						break
	 				except:
	 					pass

	 	if module_ret != None:
	 		break
	return module_ret