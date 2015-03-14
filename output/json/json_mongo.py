aid = '202'
name = "Json for mongo"
desc = "Prints the result on the terminal in json format for mongo db\n"

def launch(data):

    json = {}
    for row in data:
        json[row['_id']] = row

    print json