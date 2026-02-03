import json
import csv
json1 ={
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}

DIC=json.dumps(json1)
print(type(DIC))

dict1 = json.loads(DIC)
print(type(dict1))

employee = [{'Name': 'Satyam', 'Role': 'Developer', 'Company': "Scaler"},
            {'Name': 'Shivam', 'Role': 'Programmer', 'Company': "InterviewBit"},
            {'Name': 'Jack', 'Role': 'Manager', 'Company': "Google"}]


header = ["Name", "Role", "Company"]
with open('test.csv', 'w') as file:

    writer = csv.DictWriter(file,fieldnames=header)
    writer.writeheader()
    for row in employee:
        writer.writerow(row)

data = csv.reader(open('test.csv'))
print(list(data))



def read_in_chunk(fil1):
    while True:
      line= fil1.readline()
      if not line:
          break
      else:
           yield  line
with open('test.csv','r') as file:
    gen=read_in_chunk(file)
    print(next(gen))
