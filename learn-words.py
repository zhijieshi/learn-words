# import system module
# import sys, re, 
import argparse
import csv
import itertools, random
import datetime
import json
from PyDictionary import PyDictionary

parser = argparse.ArgumentParser(description='Flashcards')
#parser.add_argument('-i', default='500.csv', nargs='?', type=argparse.FileType('r'), help='File name. Default is 500.csv')
# parser.add_argument('--num', type=int, default=0, help='a number.')
parser.add_argument("-i", "--input", default='500.csv', help="File that contains the word list.")

args = parser.parse_args()

fn_words = args.input
start_time = datetime.datetime.now() 
fn_marked = start_time.strftime("%m%d-%H%M%S.csv")
print("The current time is", start_time.strftime("%H:%M:%S")) 

word_list = [] 

with open(fn_words, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    word_list = list(reader)

# print(word_list)

word_list.pop(0)

random.shuffle(word_list)

n_questions = 0
n_correct = 0

dictionary=PyDictionary()
marked = []

last = None
done = 0
for w in word_list:
    print(f"----------------\n{w[1]}")
    repeat = 1
    while repeat:
        repeat = 0
        res = input()
        if len(res) > 0:
            if res.upper()[0] == 'M':
                marked.append(w)
            elif res.upper()[0] == 'P':
                marked.append(last)
                print(f"{last[1]} has been marked.")
                repeat = 1
            elif res.upper()[0] == 'Q':
                done = 1
    if done:
        break
    if len(w[2]) > 0:
        print(w[2])
    else:
        # print("PyDictionary:")
        print(json.dumps(dictionary.meaning(w[1]), indent=4))
    last = w


if len(marked) > 0:
    print("Saving ", len(marked), "words to file", fn_marked)
    with open(fn_marked, mode='w', newline='') as f_marked:
        writer = csv.writer(f_marked, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL)
        for w in marked:
            writer.writerow(w)

