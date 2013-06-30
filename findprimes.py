
#resource efficient way to find prime numbers
#we use multiplication instead of division because it's more efficient

import math
import sys
import sqlite3
import os

here = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(here, 'primes.db'))
sql = "create table if not exists primes(num integer primary key not null); create table if not exists lr(lr integer not null);"
db.executescript(sql)
db.commit()
cursor=db.cursor()

n=int(sys.argv[1]) #scan numbers up to here
primes=[]
cursor.execute("select lr from lr order by lr desc")
data = cursor.fetchone()
if data is None :
    lr = 0 
else:
    lr = data[0]
print "Largest range calculated is " + str(lr)

if n < lr: cursor.execute("select num from primes where num <= ? order by num asc", [n])
else: cursor.execute("select num from primes order by num asc")
data = cursor.fetchall()
for d in data:
    primes.append(d[0])

if n > lr: #we have to do some work on this one
    nums = [1 if i in primes else 0 for i in range(1,lr+1) ]
    nums += [1 for i in range(lr+1,n+1)]
    #nums= [1 for i in range(1,n+1)] #less efficient
    print "Finding all prime numbers in range 1 to (not including) " + str(n)

    for i in range(1,n):
        if nums[i]==1:
            #this is a prime
            if i>=lr: primes.append(i)
            if i>1:
                c=int(math.ceil(lr/i))
                if c==0: c=1
                #print "c = " + str(c) + " i = " + str(i)
                while c*i < n:
                    #print "Index = " + str(c*i)
                    nums[c*i]=0
                    c+=1


prntstr="Primes in range 1 to " + str(n) + " are: "
sql=""
for p in primes:
    prntstr+= str(p) + ", "
    if p > lr:
        sql+="insert into primes (num) values ('" + str(p) + "'); "


if n > lr:
    print "Saving results to database"
    db.executescript(sql)
    if lr>0: db.execute('update lr set lr=?', [n])
    else: db.execute('insert into lr (lr) values (?)', [n])
    db.commit()

print prntstr
print "There are " + str(len(primes)) + " primes in range 1, " + str(n)
