# import system module
# import sys, re, 
import argparse
import csv
import itertools, random
import datetime
import json
import requests
# from PyDictionary import PyDictionary

def getDefinition(word):
    r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    # print(r)
    if r.status_code != 200:
        return None
    else:
        return r.json()

parser = argparse.ArgumentParser(description='Flashcards')
# parser.add_argument('--num', type=int, default=0, help='a number.')
parser.add_argument("input", default='500.csv', help="File that contains the word list.")

args = parser.parse_args()

fn_words = args.input
word_list = [] 

if fn_words.endswith(".csv"):
    # CSV file. 
    # three columns
    # tag, word, definition
    with open(fn_words, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader: 
            if len(line) != 3:
                print(line)
                raise ValueError("The row does not have exactly 3 columns.")
#    word_list.pop(0)
else:
    # txt file
    # one word a line
    with open(fn_words, encoding='utf-8') as f:
        for line in f:
            word_list.append(['', line.rstrip(), ''])

print(word_list)

n_total =  len(word_list)
print(f"There are {n_total} words.")

start_time = datetime.datetime.now() 
fn_marked = start_time.strftime("%m%d-%H%M%S.csv")
print("The current time is", start_time.strftime("%H:%M:%S")) 

random.shuffle(word_list)

n_questions = 0
n_correct = 0

marked = []

last = None
done = 0
counter = 0
for w in word_list:
    counter += 1
    print(f"{counter}/{n_total}----------------\n{w[1]}")
    repeat = 1
    while repeat:
        repeat = 0
        res = input()
        if len(res) > 0:
            if res.upper()[0] == 'M':
                marked.append(w)
            elif res.upper()[0] == 'P':
                marked.append(last)
                print(f"{last[0]} has been marked.")
                repeat = 1
            elif res.upper()[0] == 'Q':
                done = 1
    if done:
        break
    if len(w[2]) > 0:
        print(w[2])
    else:
        # print("PyDictionary:")
        d = getDefinition(w[1])
        if d:
            print(json.dumps(d[0]["meanings"], indent=4))
        else:
            print("Error: Cannot find the definition.")
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

