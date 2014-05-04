import collections

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

    leaderboard = []
    heatmap = {}

    call_details = {}
    for call in calls:

        num = call.number
        time = int(call.seconds)
        who = call.who

        if num in call_details:
            details = call_details[num]
            total_seconds = int(details["total_seconds"])
            total_seconds += time
            call_details[num]["total_seconds"] = total_seconds

            if len(who.strip()) != 0:
                heatmap[who] = total_seconds

        else:
            this_call_detail = {}
            this_call_detail["total_seconds"] = time
            this_call_detail["who"] = who
            call_details[num] = this_call_detail

            if len(who.strip()) != 0:
                heatmap[who] = time

    reverse_heatmap = {v:k for k,v in heatmap.items()}

    ordered_reverse_heatmap = collections.OrderedDict(sorted(
        reverse_heatmap.items()))

    print collections.OrderedDict(reversed(ordered_reverse_heatmap.items()))

    #print ordered_reverse_heatmap

if __name__ == "__main__":
    calls = parse("./calls.tsv")
    spit(calls)

