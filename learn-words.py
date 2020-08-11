# import system module
# import sys, re, 
import argparse
import csv
import itertools, random
import datetime
import json
import requests
import webbrowser

# get definition and display in console
def showDefinition1(word):
    r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    # print(r)
    if r.status_code != 200:
        print(f"Error: Cannot find the definition. code={r.status_code}")
        return None
    else:
        js = r.json()
        print(json.dumps(js[0]["meanings"], indent=4))
        return js

# show definition in a web browser
def showDefinition(word, src='google'):
    if src == 'oxford':
        url = f"https://www.oxfordlearnersdictionaries.com/us/definition/english/{word}"
    else:
        url = f"https://www.google.com/search?q=define+{word}"
    webbrowser.open(url)

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

# print(word_list)

n_total =  len(word_list)
print(f"There are {n_total} words.")

start_time = datetime.datetime.now() 
fn_marked = start_time.strftime("%m%d-%H%M%S.txt")
print("The current time is", start_time.strftime("%H:%M:%S")) 

random.shuffle(word_list)

n_questions = 0
n_correct = 0

marked = []

done = 0
counter = 0
for w in word_list:
    counter += 1
    repeat = 1
    while repeat:
        print(f"{counter}/{n_total}----------------\n{w[1]}")
        res = input()
        if len(res) > 0:
            res = res.upper()
            if res[0] == 'M':
                marked.append(w)
                showDefinition(w[1])
                repeat = 0
            elif res[0] == 'Q':
                done = 1
                repeat = 0
            elif res[0] == 'P':
                # marked the previous one
                if counter > 1:
                    marked.append(word_list[counter-2])
                    print(f"{word_list[counter-2][1]} has been marked.")
                else:
                    print(f"There is no prevous word.")
            elif res[0] == 'D':
                showDefinition(w[1])
            elif res[0] == 'O':
                showDefinition(w[1], 'oxford')
        else:
            repeat = 0
        # no else branch
        # if it is empty line, move to the next word
    if done:
        break
    if len(w[2]) > 0:
        print(w[2])

if len(marked) > 0:
    print("Saving ", len(marked), "words to file", fn_marked)
    with open(fn_marked, mode='w') as f_marked:
        for w in marked:
            print(w[1], file=f_marked)

'''
if len(marked) > 0:
    print("Saving ", len(marked), "words to file", fn_marked)
    with open(fn_marked, mode='w' newline='') as f_marked:
        writer = csv.writer(f_marked, 
                delimiter=',', 
                quotechar='"', 
                quoting=csv.QUOTE_MINIMAL)
        for w in marked:
            writer.writerow(w)
'''
