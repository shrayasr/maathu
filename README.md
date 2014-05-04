# maathu
> Means "to talk" in Kannada

## Motivation
I had this idea a while back to run some analytics on the people i speak to via phone on a daily basis.  This is that.

## Steps

### Capturing that information

I was wondering how do I capture this information and along came IFTTT with a 
superb [announcement](http://blog.ifttt.com/post/83729472199/the-power-of-ifttt-now-on-android) which allowed me to do one thing - Put the information after a call into a Google spreadsheet, YAY!

I could capture the following sets of information which is all i needed: 

* When the call was placed/recieved?
* Which number was it?
* If there is a name associated to it, that name
* Total duration I spoke for
* If it was an Incoming/Outgoing call

### Analyzing the information

#### The "GO" route

The first thing that came to my mind was [textql](https://github.com/dinedal/textql) by Paul Bergeron. I jumped on this, ran the installation procedure and things didn't work. No point bothering since i'm not too much of a GO guy yet. Though I really love the language. Wanted to get something done so moved on to something I know.

#### Python

Started off writing something in Python. The first step was to fetch the information from Google Drive. I remember [Aravind](https://github.com/arg0s) talking about a way to fetch content from a spreadsheet in JSON format via a simple URL call. But then I quickly realized that for this, the spreadsheet had to be public. I didn't want that. Moving on.

On the pretext of getting things done, I decided i'll just download the spreadsheet in CSV format and get going. Got the spreadsheet via the drive "export" command in CSV format and got cracking. 

Created a simple `record` class to hold each record. Wrote a simple parser on top of the CSV file to throw stuff in but I quickly hit a roadblock. The first column - `when` had a comma in it. BOOM. CSV wont work. I went back to Google drive and exported it as a Tab seperated file now. Things were working

Now for the analytics. 

##### Leaderboard - Pure Python

The first task I gave myself was to get some kind of a leaderboard representing in a descending order, the list of people I spoke to most. I wanted Name -> Total No. of seconds i've spoken to them (outgoing and incoming) 

Sat down to do this with plain Python and it didn't get me anywhere. This was the approach I followed: 

* Fetch required information from the `record`
* Create a dictionary of `Who` -> `Total_seconds_spoken`
* Reverse that dictionary so that I get `Total_seconds_spoken` -> `Who`
* Sort that dictionary using Python `OrderedDict`
* Reverse Sort them to get it in descending order

[commit](https://github.com/shrayas/maathu/commit/82d77421c0bcd1c5e4efb3592a1f850ad265ea5d)

As yu can clearly see, this was utter and pure **BS** 

Learning: There are some things that are meant for doing somethings. This would have been **SO** easy with SQL. I believe the query would be this: 

```sql
select name, sum(seconds) from calls group by number order by seconds desc
```

or at least something to that kind. Basically what i'm trying to get at here is that that would have been the right way to do it.

##### Leaderboard - Redis

Enter Redis. I had been to the Redis [miniconf](https://funnel.hasgeek.com/redis-miniconf-2014/) organized by [hasgeek](https://github.com/hasgeek) just a few weeks ago and I wanted to try out Redis. This seemed like a good opportunity to try it out.

I remembered something about "Sorted Sets" in redis and I went over to redis.io to check it out. 

Sorted Sets allows to assign a score to a key within a set. This seemed perfect. The score could be the no. of seconds and the key could be the person I spoke to. The `zincrby` command was what I had to use to keep incrementing this score everytime a new `record` was processed. Thats it, i was done!

[commit](https://github.com/shrayas/maathu/commit/89fb063ffa3be117a4a63444ae23468db05492aa)

To get the leaderboard I just had to reverse sort it and `zrevrangebyscore` did the job for me. 

As @vk said: _"30 odd lines, reduced to about 3"_. Thats the power of application. Applying the right things to the right places. I don't know if this is the **right** implementation for Redis but it really did solve my problem.

##### Call Frequency - Redis

The next metric I wanted to add was: Given the date and a number, can I find out how many times i've spoken to them. 

I think there is no _native_ way of storing dates in redis, I had to fit it into the key somehow. So I parsed out the `when` from the `record` and used a custom key to store this information within another sorted set. In retrospect a sorted set really isn't required here. Since there isn't anything to sort by. Should use a hash instead. The complexity jumps down to O(1).

Stored the key as `DDMMYYYY#PHONE_NUMBER` with the score being the no. of times i've called in that day. the `zincrby` in python has a default increment value of 1 which solved the problem for me. 

[commit](https://github.com/shrayas/maathu/commit/400cbf6edb4319c55f6dec2e16758af3c871f968)

---

These are the metrics that are currently in the system: 

* Leaderboard - Who is the most called person in my list?
* Call frequency - How many times did i call someone on a day?

This README looks to capture my thoughts as I add more metrics(?). Please do correct me if i'm doing something wrong. I'm still learning.

Thanks for reading!
