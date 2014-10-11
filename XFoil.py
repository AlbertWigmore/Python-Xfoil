__author__ = 'Albert'


import glob, csv
from subprocess import *
from itertools import product
from os import remove


def dir_list():
    files = []
    for file in glob.glob('*'):
        files.append(file)
    return(files)


def naca4(test_condition):
    naca4list = map(lambda x: "NACA %i%i%i" %x ,product(range(10), range(10), range(15,26)))
    naca4list = list(set(naca4list)-{x[:9] for x in dir_list() if "-" + test_condition in x})
    naca4list.sort()
    return naca4list


def naca5(test_condition):
    naca5list = map(lambda x: "NACA %i%i%i%i" %x, product(range(10), range(10), range(1), range(15,26)))
    naca5list = list(set(naca5list)-{x[:10] for x in dir_list() if "-" + test_condition in x})
    naca5list.sort()
    return naca5list


def data_generation(nacalist, test_condition):
    i = 0
    failed = 0
    cmd = r"C:\Users\Albert\Desktop\XFOIL6.99\xfoil"
    for naca in nacalist:
        xfoil = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=True, bufsize=-1, universal_newlines=True)

        if test_condition == "12":
            xfoil.stdin.write("\n".join(["PLOP", "G F", "", naca, "OPER","ITER 10", "visc", "65e4", "mach", "0", "PACC", naca+"-12", "", "alfa 0", "cl 0.5", "PACC", "", "QUIT", ""]))
        elif test_condition == "3":
            xfoil.stdin.write("\n".join(["PLOP", "G F", "", naca, "OPER","ITER 10", "visc", "10e5", "mach", "0", "PACC", naca+"-3", "", "cl 0", "PACC", "", "QUIT", ""]))

        xfoil.stdin.close()

        try:
            for line in xfoil.stdout:
                #print(line)
                if line == " Polar accumulation disabled\n":
                    i += 1
                    #print("Percentage Done :  %.2f%%" % (100*(i/float(len(nacalist)))))
                    #print("%s DONE" %naca)
                elif "VISCAL:  Convergence failed" in line:
                    #print("Convergence Failed on: %s" % naca)
                    failed += 1

                    if test_condition == "12":
                        remove(naca+"-12")
                        #print("Deleted %s-12" %naca)

                        #xfoil = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=True, bufsize=-1, universal_newlines=True)
                        #xfoil.stdin.write("\n".join(["PLOP", "G F", "", naca, "PANE", "OPER","ITER 10", "visc", "65e4", "mach 0.0588", "PACC", naca+"-12", "", "alfa 0", "!", "!", "!", "!", "!", "!", "!", "!", "!", "!", "cl 0.5", "!", "!", "!", "!", "!", "!", "!", "!", "!", "!",  "PACC", "", "QUIT", ""]))
                        #print("Tried again for 12: %s" %naca)

                    elif test_condition == "3":
                        remove(naca+"-3")
                        #print("Deleted %s-3" %naca)

                        #xfoil = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=True, bufsize=-1, universal_newlines=True)
                        #xfoil.stdin.write("\n".join(["PLOP", "G F", "", naca, "PANE", "OPER","ITER 10", "visc", "975e3", "mach 0.0882", "PACC", naca+"-3", "", "cl 0", "!", "!", "!", "!", "!", "!", "!", "!", "!", "!", "PACC", "", "QUIT", ""]))
                        #print("Tried again for 3: %s" %naca)


        except: pass

        xfoil.wait(5)
    print("Amount Failed = %i"% failed)

def file_generation():
    nacalist = list(set(dir_list()) - {"data.csv", "XFoil.py", ".idea"})
    nacalist.sort()
    data12 = dict()
    data3 = dict()
    with open('data.csv', "w", newline='') as csvfile:
        for naca in nacalist:
            with open(naca, "r") as file:
                if "-12" in naca:
                    print(naca)
                    data12[naca[:-3]] = [(float(x[1]), float(x[2])) for x in [x.split() for x in file.readlines()[12:14]]]
                elif "-3" in naca:
                    print(naca)
                    data3[naca[:-2]] = file.readlines()[12].split()[2]

        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(["NACA AEROFOIL", "Cl", "Cd",  "L/D", "Cd0"])
        for x in data12.keys() & data3.keys():
            print(x)
            writer.writerow([x, data12[x][0][0], data12[x][0][1], (data12[x][1][0]/data12[x][1][1]), data3[x]])





#vel = input("Enter Velocity m/s: ")
#rho = input("Enter Air Density: ")
#dyn_visc = input("Enter Dynamic Viscosity: ")

test_condition = None
while test_condition != "12" and test_condition != "3":
    test_condition = input("Enter Test Condition (12 or 3): ")

data_generation(naca4(test_condition), test_condition)
data_generation(naca5(test_condition), test_condition)
file_generation()

#print(list(naca4()))
#print(list(naca5()))
print("Complete!")