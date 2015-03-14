import load_mod
import logging
import time

logger = logging.getLogger('gummerlog')

def db_query(db_connector, query):
	msg = "Connecting to db: %s" % (db_connector.aid)
	logger.debug(msg)
	msg = "Sending query \"%s\" to \"%s\"" % (query, db_connector.name)
	logger.info(msg)

	# TODO:
	# Test and implement for Windows systems
	start = time.clock()
	data = None
	try:
		data = db_connector.launch(query)
		end = time.clock()
		elapsed = end - start
		msg = "Query finished in %s seconds" % elapsed
		logger.info(msg)
	except Exception, e:
		msg = "There was an error executing the query: %s"  % (e)
		logger.error(msg)

	return data