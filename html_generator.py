import json
import re
from jsmin import jsmin

def loadJsonData(fileName):
    with open(fileName) as js_file:
        contents = js_file.read()
        #analyzing inside strings
        contents = contents.split('"')
        for i in range(1,len(contents),2):
            #clearing \n inside strings
            contents[i] = contents[i].replace('\n','\\n')
            #converting comments inside strings to not comments
            contents[i] = contents[i].replace('//','SLASH')
        contents = '"'.join(contents)       

        #clearing comments
        contents = re.sub(r"\/\/.*",'',contents)#//comment
        contents = re.sub(r"\/\*[^*]*\*\/",'',contents)#/*comment*/

        
        

        #parsing json
        return json.loads(contents)

def parse(fileName):
    output = ""
    data = loadJsonData(fileName)
    output+=''+data['shortdescription']+'\n'
    output+=descriptionFormat(data['description'])
    return output, data

def parse_item(fileName):
    output, data = parse(fileName)
    return output, data

def parse_head(fileName):
    output, data = parse(fileName)
    return output, data

def parse_chest(fileName):
    output, data = parse(fileName)
    return output, data

def parse_recipe(fileName):
    output, data = parse(fileName)
    return output, data

def descriptionFormat(description):
    return re.sub('\\^([^;]*);([^^]*)\\^reset;','<span style="color:$1;">$2</span>',description)

