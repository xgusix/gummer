import db_loader
#Example of analizer
aid = "apt_ips" # Must be unique
name = "TOP Direct connection to IPs"
desc = "Retrieves the top 10 HTTP/S most repeated connections to IP addresses "
desc += "instead of to domains.\n"

def launch(connector):
    query = "select count(*) as Hits, ip_src, url "
    query += "from squid3 "
    query += "where ip_dst = domain "
    query += "group by url "
    query += "order by Hits desc "
    query += "limit 10"
    data = db_loader.db_query(connector, query)
    return data