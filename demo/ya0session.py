import random
import sys
import urllib
#import urllib2
import sys
import threading
import package_gen_demo 
#url = "http://yax.ymcnetwork.com/track"
url = "http://10.1.1.33:3000/import"
#users = file("users.txt","r")


users = open("users.txt",'r').readlines()
#count = len(users)

for x in range(1,31):
	
	print "current day",x
	
	for i in range(random.randint(1,x)):



		current_user_1 = random.choice(users)
		current_user = current_user_1.strip('\n')
		for e in range(random.randint(1,5)):	# one user launch game 1 to 5 time per day
	
			date_1 = [2014,6,x]
			time_1 = [random.randint(5,23),30,00]	# users launch time between (5am to 23pm)
		#random_id = str(random.randint(1,500))
			data = package_gen_demo.package_generator("YA0session","2.0.2","8416e32af87f11e284c212313b0ace15",date_1,time_1,current_user)
		#print data

		
			rex = urllib.urlopen(url,data)
		#print rex.read()




open("users.txt",'r').close()


		

