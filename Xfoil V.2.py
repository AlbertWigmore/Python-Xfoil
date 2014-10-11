__author__ = 'Albert'

import glob
import csv
from subprocess import *
from itertools import product
from os import remove
from multiprocessing import Pool


def dir_list():
    files = []
    for file in glob.glob('NACA*'):
        files.append(file)
    return(files)


def naca4():
    naca4list = map(lambda x: "NACA %i%i%i" %x ,product(range(10), range(10), range(15,26)))
    naca4list = list(set(naca4list)-{x[:9] for x in dir_list()})
    naca4list.sort()
    return naca4list


def naca5():
    naca5list = map(lambda x: "NACA %i%i%i%i" %x, product(range(0,3), range(0,6), range(1), range(15,26)))
    naca5list = list(set(naca5list)-{x[:10] for x in dir_list()})
    naca5list.sort()
    return naca5list


def command_generation():
    print("---------------------------\n Xfoil Data Generator V2\n Author = Albert Wigmore\n---------------------------\n\n")

    Re = input("Enter Re     <return = default(7e5)>:")
    mach = input("Enter Mach     <return = default(0)>:")

    if Re == "\n":
        Re = 7e5
    if mach == "\n":
        mach = 0



    commands = [" "]



def data_generation(naca):
    cmd = r"C:\Users\Albert\Desktop\XFOIL6.99\xfoil"

    xfoil = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=True, bufsize=-1, universal_newlines=True)

    xfoil.stdin.write("\n".join(["PLOP", "G F", "", naca, "OPER","ITER 100", "visc", "67e4", "PACC", naca, "", "alfa 0", "PACC", "", "QUIT", ""]))
    xfoil.stdin.close()

    try:
        check = 0
        for line in xfoil.stdout:
            #print(line)
            if line == " Polar accumulation disabled\n":
                check += 1
            elif "VISCAL:  Convergence failed" in line:
                check += 1
                #print("Convergence Failed on: %s" % naca)
                remove(naca)
                #print("Deleted %s" %naca)
                xfoil.wait(5)
        if check >= 1:
            #print ("%s DONE" %naca)
            pass
    except:
        xfoil.terminate()

        print()

def file_generation():
    nacalist = dir_list()
    nacalist.sort()
    data = dict()
    with open('data.csv', "w", newline='') as csvfile:
        for naca in nacalist:
            with open(naca, "r") as file:
                print(naca)
                data[naca] = [(float(x[1]), float(x[2])) for x in [x.split() for x in file.readlines()[12:13]]] # Need to edit for test conditions, will have to read in all


        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(["NACA AEROFOIL", "Cl", "Cd",  "L/D", "Cd0"]) # Need to edit for test conditions

        for x in data.keys():
            print("%s ADDED TO CSV" %x)
            print(x, data[x][0][0], data[x][0][1])
            writer.writerow([x, data[x][0][0], data[x][0][1]])

    with open('failed.csv', "w", newline='') as csvfile:
        for failed in (naca4()+naca5()):
            print(failed)
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow([failed])




if __name__ == '__main__':
    #command_generation()
    procceses = Pool()
    #procceses.map(data_generation, naca4()+naca5())

    count = 0
    total = float(len(naca5()+naca4()))
    for x in procceses.imap_unordered(data_generation, naca4()+naca5()):
        count +=1
        print("Percentage Complete = %.2f%%"%(100*count/total))
        #call('cls', shell = True)

    file_generation()
    print("COMPLETED")

    print("UNCOMPLETED = %i" %(len(naca5()) + len(naca4())))