import db_loader
#Example of analizer
aid = "apt_size" # Must be unique
name = "TOP biggest requests"
desc = "Retrieves TOP 10 biggest requests.\n"

def launch(connector):
    query = "select time, sz_request, ip_src, url "
    query += "from squid3 "
    query += "order by sz_request desc "
    query += "limit 10"
    data = db_loader.db_query(connector, query)
    return data