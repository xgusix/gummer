import db_loader
aid = "apt_time" 
name = "TOP longest connections"
desc = "Retrieves TOP 10 IPs with the longest connections.\n"

def launch(connector):
    query = "select max(duration) as time, ip_src, url "
    query += "from squid3 "
    query += "group by ip_src, url "
    query += "order by time desc "
    query += "limit 10"
    data = db_loader.db_query(connector, query)
    return data