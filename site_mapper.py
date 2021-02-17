import threading
import queue
import argparse

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
                    action='store',type=str,
                    help='The wordlist address', required=False, default="all.txt")


def main(args):
    pass

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
