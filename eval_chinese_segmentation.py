"""
USE: python <PROGNAME> (options) GOLD-FILE OUTPUT-FILE
OPTIONS:
    -h : print this help message and exit
"""
################################################################
# Этот импорт делает print() функцией даже в Python 2
from __future__ import print_function
import sys, re, getopt, io

################################################################
# Command line options handling, and help

def printHelp():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    
    print('-' * 60, file=sys.stderr)
    print(help, file=sys.stderr)
    print('-' * 60, file=sys.stderr)
    sys.exit()
    
try:
    opts, args = getopt.getopt(sys.argv[1:], 'h')
    opts = dict(opts)
except getopt.GetoptError:
    printHelp()

if '-h' in opts:
    printHelp()

if len(args) != 2:
    print("\n** ERROR: must specify precisely two input files! **", file=sys.stderr)
    printHelp()

################################################################
# Read in all lines of gold-standard and system results

try:
    # io.open работает и в Python 2, и в Python 3 с кодировкой
    with io.open(args[0], 'r', encoding='utf-8') as gold_in:
        gold_lines = gold_in.readlines()
        
    with io.open(args[1], 'r', encoding='utf-8') as result_in:
        result_lines = result_in.readlines()

# Перехватываем и IOError (Py2), и OSError (Py3) для надежности
except (IOError, OSError) as e:
    # Используем % форматирование вместо f-строк для совместимости
    print("\n** ERROR: File not found or error reading: %s **" % e, file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print("\n** ERROR: %s **" % e, file=sys.stderr)
    sys.exit(1)
    
if len(result_lines) != len(gold_lines):
    print("\n** ERROR: gold-std and results files differ in num of lines **", file=sys.stderr)
    printHelp()

################################################################
# Converts segmented sentence to set of tokens, each marked with 
# character offset position

def get_words_sequenced(line):
    words = set()
    posn = 0
    for word in line.split():
        words.add((posn, word))
        posn += len(word)
    return words

################################################################
# Score all lines

gold_word_count = 0
correct_words = 0
correct_sentences = 0

for i in range(len(gold_lines)):
    gold_words = get_words_sequenced(gold_lines[i])
    result_words = get_words_sequenced(result_lines[i])
    
    gold_word_count += len(gold_words)
    correct_words += len(gold_words & result_words)
    
    if gold_words == result_words:
        correct_sentences += 1

################################################################
# Print results

print("")
print("Total correct words:", correct_words)
print("Total gold-std words:", gold_word_count)

if gold_word_count > 0:
    word_acc = 100.0 * correct_words / gold_word_count
    print("Word-level accuracy: %.2f%%" % word_acc)
else:
    print("Word-level accuracy: N/A")

if len(gold_lines) > 0:
    sent_acc = 100.0 * correct_sentences / len(gold_lines)
    print("Sentence-level accuracy: %.2f%%" % sent_acc)
else:
    print("Sentence-level accuracy: N/A")