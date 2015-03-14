aid = '201'
name = "Json"
desc = "Prints the result on the terminal in json format.\n"

def launch(data):

	desc = data.description
	rows = data.fetchall()
	json = {}
	for i in range (0,len(rows)):
		row = {}
		for j in range(0, len(rows[i])):
			row[desc[j][0]] = rows[i][j]
		json[i] = row

	print json	
