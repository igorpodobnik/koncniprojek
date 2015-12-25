__author__ = 'Franko'



datum  = "5.5.1983"
datum2 = "12.12.1983"
datum3 = "5.12.1983"
datum4 = "12.5.1983"
datumi=["5.5.1983","12.12.1983","5.12.1983","12.5.1983","5,5,200"]

c="."
prvi=[pos for pos, char in enumerate(datum) if char == c]
prvi2=[pos for pos, char in enumerate(datum2) if char == c]
prvi3=[pos for pos, char in enumerate(datum3) if char == c]
prvi4=[pos for pos, char in enumerate(datum4) if char == c]
print prvi
print prvi2
print prvi3
print prvi4
prva = 1
druga = 2
tretja = 3
cetrta = 4
peta = 5

if prva in prvi:
    print "Yes"

"""
dan = int(i[:2])
mesec = int(i[5:7])
dan = int(i[8:10])
"""


for i in datumi:
    rezultat="ok"
    pozicije=[pos for pos, char in enumerate(i) if char == c]
    if prva in pozicije:
        if tretja in pozicije:
            dan = int(i[:1])
            mesec = int(i[2:3])
            leto = int(i[4:8])
        elif cetrta in pozicije:
            dan = int(i[:1])
            mesec = int(i[2:4])
            leto = int(i[5:9])
        else:
            rezultat = "ponovi"
    elif druga in pozicije:
        if peta in pozicije:
            dan = int(i[:2])
            mesec = int(i[3:5])
            leto = int(i[6:10])
        elif cetrta in pozicije:
            dan = int(i[:2])
            mesec = int(i[3:4])
            leto = int(i[5:9])
        else:
            rezultat = "ponovi"
    else:
        rezultat = "ponovi"
    print "---"
    print i
    print dan
    print mesec
    print leto
    print rezultat




def vnosdatuma(datum):
    rezultat="ok"
    pozicije=[pos for pos, char in enumerate(datum) if char == c]
    if prva in pozicije:
        if tretja in pozicije:
            dan = int(datum[:1])
            mesec = int(datum[2:3])
            leto = int(datum[4:8])
        elif cetrta in pozicije:
            dan = int(datum[:1])
            mesec = int(datum[2:4])
            leto = int(datum[5:9])
        else:
            rezultat = "ponovi"
    elif druga in pozicije:
        if peta in pozicije:
            dan = int(datum[:2])
            mesec = int(datum[3:5])
            leto = int(datum[6:10])
        elif cetrta in pozicije:
            dan = int(datum[:2])
            mesec = int(datum[3:4])
            leto = int(datum[5:9])
        else:
            rezultat = "ponovi"
    else:
        rezultat = "ponovi"
    return rezultat,dan,mesec,leto

datum  = "5.5.1983"
datum2 = "12.12.1983"
datum3 = "5.12.1983"
datum4 = "12.5.1983"
rez,d,m,l = vnosdatuma(datum)
print "--"
print rez
print d
print m
print l

print "yes"
print ("hehe %s hehe %s" %(prva,druga))