days = ["mon", "tues", "weds", "thurs", "fri"]

#what's the second day of the week?
#recall, indices start at zero
day2 = days[1]  # "tues"

#add the weekend
days.append("sat")
days.append("sun")  
# days is now ["mon", "tues", "weds", "thurs", "fri", "sat", "sun"]

#I don't like Mondays!
days.pop(0)
# days is now ["tues", "weds", "thurs", "fri", "sat", "sun"]

#We can remove from the end too
days.pop()
# days is now ["tues", "weds", "thurs", "fri", "sat"]

