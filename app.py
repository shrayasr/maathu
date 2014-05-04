import collections
from redis import Redis

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

def spit(calls):

    r = Redis()
    LEADERBOARD = "leaderboard"

    if not r.exists(LEADERBOARD):
        for call in calls:

            number = call.number
            who = call.who
            seconds = int(call.seconds)

            r.zincrby(LEADERBOARD, number, seconds)

    print r.zrevrangebyscore(LEADERBOARD, "+inf", "-inf", withscores=True)

if __name__ == "__main__":
    calls = parse("./calls.tsv")
    spit(calls)

