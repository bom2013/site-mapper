import threading
import queue
import argparse
import re
import urllib.request
import urllib.parse

parser = argparse.ArgumentParser(
    prog="site_mapper.py", description='Map site using brute force')
parser.add_argument('url',
                    metavar='url',
                    type=str,
                    help='The Target url')
parser.add_argument('-t',
                    '--thread',
                    action='store', type=int,
                    help='Number of threads', required=False, default=5)
parser.add_argument('-w',
                    '--wordlist',
                    action='store', type=str,
                    help='The wordlist address', required=False, default="all.txt")
parser.add_argument('-e', '--extension', nargs='*', type=str, default=[], required=False, help="List of file extensions to brute force trying")

def create_wordlist_queue(dir):
    try:
        words_queue = queue.Queue()
        with open(dir, 'r') as f:
            raw_words = f.readlines()
            for word in raw_words:
                words_queue.put(word.rstrip())
    except FileNotFoundError:
        raise FileNotFoundError("The wordlist file doesn't exist")
    return words_queue


def brute_map(target_url, words_queue, subdir_filter=None, extensions=None):
    while not words_queue.empty():
        word = words_queue.get()
        subdir_list = []
        # Add the basic url, if the word isn't extension add '/'
        if "." in word:
            subdir_list.append(f"/{word}")
        else:
            subdir_list.append(f"/{word}/")

        # Add all bruteforce extension
        if extensions:
            for ext in extensions:
                subdir_list.append(f"/{word}.{ext}")

        # Filter subdir acourding to regex
        if subdir_filter:
            pattern = re.compile(subdir_filter)
            subdir_list = list(filter(lambda w: pattern.match(w), subdir_list))

        # Iterate over our list of urls
        for subdir in subdir_list:
            full_url = f"{target_url}{urllib.parse.quote(subdir)}"
            if "CVS" in full_url:
                a=1
            try:
                response = urllib.request.urlopen(full_url)
                if len(response.read()):
                    print(f"[{response.code}] => {full_url}")
            except urllib.request.URLError as e:
                if hasattr(e, 'code') and e.code != 404:
                    print(f"~[{e.code}] => {full_url}")

def main(args):
    word_queue = create_wordlist_queue(args.wordlist)
    for i in range(args.thread):
        t = threading.Thread(target=brute_map,args=(args.url, word_queue,None, args.extension,))
        t.start()
    '''
    word_queue = create_wordlist_queue('all.txt')
    for i in range(10):
        t = threading.Thread(target=brute_map,args=("https://algoritmim.co.il", word_queue,None, [],))
        t.start()
    '''

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    main(args)
