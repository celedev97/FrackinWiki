
logFile = open('log.txt','w')

def log(*args, sep=' ', end='\n'):
    output = sep.join(map(lambda arg:str(arg),args))+end
    logFile.write(output)
    logFile.flush()
    print(output,end='')