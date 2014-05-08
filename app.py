import collections

from redis import Redis
from datetime import datetime

class call_record:

    def __init__(self, when, number, who, seconds, direction):
        self.when = when
        self.number = number
        self.who = who
        self.seconds = seconds
        self.direction = direction

def parse(file_name):

    lines = []
    with open(file_name) as f:
        lines = f.readlines()

    lines = lines[1:]

    calls = []
    for line in lines:

        line_parts = line.split("\t")
        when = line_parts[0]
        number = line_parts[1]
        who = line_parts[2]
        seconds = line_parts[3]
        direction = line_parts[4]

        call = call_record(when, number, who, seconds, direction)
        calls.append(call)

    return calls

def process(r, calls):

    LEADERBOARD = "leaderboard"
    FREQUENCY = "call_frequency"

    if not r.exists(LEADERBOARD) and not r.exists(FREQUENCY):
        for call in calls:

            number = call.number
            who = call.who.strip()
            seconds = int(call.seconds)
            when = datetime.strptime(call.when, "%B %d, %Y at %I:%M%p")

            if len(who) == 0:
                continue

            frequency_key=when.strftime("%d%m%Y") + "#" + number

            r.zincrby(LEADERBOARD, who, seconds)
            r.hincrby(FREQUENCY, frequency_key)

    leaderboard_list = r.zrevrangebyscore(LEADERBOARD, "+inf", "-inf", 
            withscores=True)

    call_frequency_list = r.hgetall(FREQUENCY)

    print call_frequency_list

def clear_redis(r):
    r.flushall()


if __name__ == "__main__":
    r = Redis()

    calls = parse("./calls.tsv")

    clear_redis(r)
    process(r, calls)

