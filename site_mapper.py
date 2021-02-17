# Auther: Noam Ben Shlomo(bom2013)
# This code is based on code in the great book "Black hat python"
# https://www.amazon.com/Black-Hat-Python-Programming-Pentesters/dp/1593275900

import threading
import urllib.request
import urllib.parse
import requests
from queue import Queue
from argparse import ArgumentParser

# The amount of threads created
number_of_threads = 0

# Locks so that the threads can use the counters and write to same file if needed
filter_counter_lock = threading.Lock()
counter_lock = threading.Lock()
number_of_threads_counter_lock = threading.Lock()
file_lock = threading.Lock()

# Counters
counter = 0
filtered_counter = 0
number_of_threads_finish_counter = 0
file_object = None


def create_argparser() -> ArgumentParser:
    """Create the arg parser"""
    parser = ArgumentParser(prog="site_mapper.py",
                            description='Map site using brute force')
    # Target url
    parser.add_argument('url',
                        metavar='url',
                        type=str,
                        help='The Target url')
    # Number of Threads - optional
    parser.add_argument('-t',
                        '--thread',
                        required=False,
                        type=int,
                        action='store',
                        default=5,
                        help='Number of threads')
    # The word file address - optional
    parser.add_argument('-w',
                        '--wordfile',
                        required=False,
                        type=str,
                        action='store',
                        default="all.txt",
                        help='The word file address')
    # Export file address - optional
    parser.add_argument('-f',
                        '--file',
                        required=False,
                        type=str,
                        action='store',
                        help="Export data to file")
    # Full name status code number - optional
    parser.add_argument('-s',
                        '--status',
                        required=False,
                        action='store_true',
                        help='Show status code name')
    # Remove non-200 status code response - optional
    parser.add_argument('-r',
                        '--remove',
                        required=False,
                        action='store_true',
                        help='Remove non-200 results')
    # Extensions to brute check - optional
    parser.add_argument('-e',
                        '--extension',
                        required=False,
                        type=str,
                        nargs='*',
                        default=[],
                        help="List of file extensions to brute force trying")
    return parser


def create_word_queue(dir) -> Queue:
    """Create the word queue"""
    try:
        words_queue = Queue()
        with open(dir, 'r') as f:
            raw_words = f.readlines()
            for word in raw_words:
                words_queue.put(word.rstrip())
    except FileNotFoundError:
        raise FileNotFoundError("The word file doesn't exist")
    return words_queue


def update_counter():
    global counter
    with counter_lock:
        counter += 1


def update_filter_counter():
    global filtered_counter
    with filter_counter_lock:
        filtered_counter += 1


def inform_new_url_available(code, url, file=None, remove_non200=False, status_code_name=False) -> bool:
    """Inform(print\write to file) new url available"""
    # Get extended status code(status code + full name)
    extended_code = str(code)
    if status_code_name:
        try:
            extended_code += f" {requests.status_codes._codes[code][0]}"
        except KeyError:  # Unknown status code
            extended_code += " ?"

    # Create full message
    message = f"[{extended_code}] => {url}"

    # Handle non 200 status code response
    if str(code) != "200":
        if remove_non200:
            # Update global counter
            update_filter_counter()
            return
        message = "~"+message

    # Update global counter
    update_counter()

    # print\write the message
    if file:
        with file_lock:
            file_object.write(message+"\n")
    else:
        print(message)


def brute_map(target_url, words_queue, extensions=None, file=False, remove_non200=False, status_code_name=False):
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

        # Iterate over our list of urls
        for subdir in subdir_list:
            # Create full url
            full_url = f"{target_url}{urllib.parse.quote(subdir)}"

            try:
                response = urllib.request.urlopen(full_url)
                # Check if the response have data
                if len(response.read()):
                    inform_new_url_available(response.code,
                                             full_url,
                                             file=file,
                                             status_code_name=status_code_name,
                                             remove_non200=remove_non200)

            except urllib.request.URLError as e:
                if hasattr(e, 'code') and e.code != 404:
                    inform_new_url_available(e.code,
                                             full_url,
                                             file=file,
                                             status_code_name=status_code_name,
                                             remove_non200=remove_non200)

    # Update number of thread finished counter before died
    with number_of_threads_counter_lock:
        global number_of_threads_finish_counter
        global number_of_threads
        global file_object
        number_of_threads_finish_counter += 1
        # Check if he is the last thread
        if number_of_threads == number_of_threads_finish_counter:
            if file_object:
                file_object.close()
            print(f"\nFinish! {counter} match, {filtered_counter} filtered")


def main(args):
    # Declare global variables
    global number_of_threads
    global file_object

    # Create the word queue from the file
    print("Loads a list of words from the file... ", end="")
    word_queue = create_word_queue(args.wordfile)

    # Open file if toFile option is on
    if args.file:
        file_object = open(args.file, 'w')

    # Create the threads
    print("done")
    print("Begins to create threads...")
    print("Results:\n")
    number_of_threads = args.thread
    for i in range(number_of_threads):
        t = threading.Thread(target=brute_map, args=(args.url,
                                                     word_queue,
                                                     args.extension,
                                                     args.file,
                                                     args.remove,
                                                     args.status))
        t.start()


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()
    main(args)
