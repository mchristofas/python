import random
for i in range(20):
    x = random.randint(5, 100)
    print x*10
    x = x*10 
    if x <= 100:
	print "winner!"

