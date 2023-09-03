from datetime import datetime

#printMeFirst function generate the string of my name and the current time
#@pram name,className
#@return result
def printMeFirst(name, className):
    """
    Call the system datetime library to get current time
    and print out the current time
    """
    currentTime = datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
    result = name+" - "+className+"\n"+currentTime
    return result
