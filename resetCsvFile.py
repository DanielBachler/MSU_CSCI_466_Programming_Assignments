#Kyle Webster csv reset tool for new games
import csv
import sys

#Reading data to check
def readCsv(file):
    lines = csv.reader(open(file,"r"))
    data = list(lines)
    for i in range(len(data)):
        print(data[i])

#Writes blank board
def writeCsv(file):
    with open(file, mode='w') as out:
        #writes each row from the data
        writer = csv.writer(out, delimiter=',')
        list = [("_"),("_"),("_"),("_"),("_"),("_"),("_"),("_"),("_"),("_")]
        for i in range(10):
            writer.writerow(list)

option = sys.argv[1]
if(option == "0"):
    writeCsv("opponent_board.csv")
else:
    readCsv("opponent_board.csv")
