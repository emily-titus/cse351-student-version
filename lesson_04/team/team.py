""" 
Course: CSE 351
Team  : Week 04
File  : team.py
Author: <Emily>

See instructions in canvas for this team activity.

"""

import random
import threading

# Include CSE 351 common Python files. 
from cse351 import *

# Constants
MAX_QUEUE_SIZE = 10
PRIME_COUNT = 1000
FILENAME = 'primes.txt'
PRODUCERS = 3
CONSUMERS = 5

# ---------------------------------------------------------------------------
def is_prime(n: int):
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# ---------------------------------------------------------------------------
class Queue351():
    """ This is the queue object to use for this class. Do not modify!! """

    def __init__(self):
        self.__items = []
   
    def put(self, item):
        assert len(self.__items) <= 10
        self.__items.append(item)

    def get(self):
        return self.__items.pop(0)

    def get_size(self):
        """ Return the size of the queue like queue.Queue does -> Approx size """
        extra = 1 if random.randint(1, 50) == 1 else 0
        if extra > 0:
            extra *= -1 if random.randint(1, 2) == 1 else 1
        return len(self.__items) + extra

# ---------------------------------------------------------------------------
def producer(que:Queue351, space_in_queue:threading.Semaphore, stuff_in_queue, barrier:threading.Barrier):
    for i in range(PRIME_COUNT):
        number = random.randint(1, 1_000_000_000_000)
        # TODO - place on queue for workers
        space_in_queue.acquire()
        que.put(number)
        stuff_in_queue.release()

    # TODO - select one producer to send the "All Done" message
    if barrier.wait() == 0:
        space_in_queue.acquire()
        que.put(None)
        stuff_in_queue.release()

# ---------------------------------------------------------------------------
def consumer(que, space_in_queue, stuff_in_queue, FILENAME):
    # TODO - get values from the queue and check if they are prime
    # TODO - if prime, write to the file
    # TODO - if "All Done" message, exit the loop
    ...
    with open(FILENAME, 'a') as f:
        while True:
            stuff_in_queue.acquire()
            value = que.get()
            stuff_in_queue.release()

            if value is None:
                space_in_queue.acquire()
                que.put(None)
                stuff_in_queue.release()
                break

            if is_prime(value):
                f.write(f'{value}\n')
    

            

# ---------------------------------------------------------------------------
def main():

    random.seed(102030)

    que = Queue351()


    # TODO - create semaphores for the queue (see Queue351 class)
    space_in_queue = threading.Semaphore(MAX_QUEUE_SIZE)
    stuff_in_queue = threading.Semaphore(0)

    # TODO - create barrier
    barrier = threading.Barrier(PRODUCERS)

    # TODO - create producers threads (see PRODUCERS value)
    producers = [threading.Thread(target=producer, args=(que, space_in_queue, stuff_in_queue, barrier)) for _ in range(PRODUCERS)]

    # TODO - create consumers threads (see CONSUMERS value)
    consumers = [threading.Thread(target=consumer, args=(que, space_in_queue, stuff_in_queue)) for _ in range(CONSUMERS)]

    for t in producers + consumers:
        t.start()
    for t in producers + consumers:
        t.join()

    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            primes = len(f.readlines())
    else:
        primes = 0
    print(f"Found {primes} primes.  Should be {108}.")



if __name__ == '__main__':
    main()
