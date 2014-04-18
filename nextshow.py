"""
nextshow.py - Is there a show this week?
Author: Delwin
Licensed under the Eiffel Forum License 2

More info:
 * Jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/

This module was created for #linuxlugcast, which
hosts a show on the first and third friday of the month.
"""

import datetime, re

def weekcheck(jenni, t, generic):
    noshow = True
    #t is the date to check, either today's date or a user defined date
    #jenni.reply("debug, t is " + t.ctime())

    #today is the integer corresponding to the day of the week.
    #Monday = 0, Friday = 4, Sunday = 6
    today = t.weekday()
    #jenni.reply("debug, day of the week is " + str(today))

    #use timedelta to find out the date of the Friday in the week being checked
    daydelta = 4 - today
    frcheck = t + datetime.timedelta(days=daydelta)
    #jenni.reply("debug, that friday's date is " + frcheck.ctime())

    #get the date string for the showdate. we'll rewrite this later if we have to
    #look into future weeks
    showdate = frcheck.strftime("%A, %B %d, %Y")
    showmessage = "Something went wrong"

    #look for first week
    if frcheck.day >= 1 and frcheck.day <= 7:
        #if it's Saturday or Sunday, go ahead and look for the next show date
        if today == 5 or today == 6:
            noshow = True
        #if it's Friday, the show is today
        elif today == 4:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (first week) is TODAY, " + showdate
            return showmessage
            #return jenni.reply("The next show (first week) is TODAY, " + showdate)
        #if it's Monday to Thursday, let them know the show is coming this week
        else:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (first week) is this week, " + showdate
            return showmessage
            #return jenni.reply("The next show (first week) is this week, " + showdate)

    #look for third week
    elif frcheck.day >= 15 and frcheck.day <= 21:
        if today == 5 or today == 6:
            noshow = True
        elif today == 4:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (third week) is TODAY, " + showdate
            return showmessage
            #return jenni.reply("The next show (third week) is TODAY, " + showdate)
        else:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (third week) is this week, " + showdate
            return showmessage
            #return jenni.reply("The next show (third week) is this week, " + showdate)

    #if noshow, look for next date of show
    if noshow:
        while noshow:
            #add 1 week timedelta to frcheck until the friday falls in proper date range
            frcheck = frcheck + datetime.timedelta(weeks=1)
            showdate = frcheck.strftime("%A, %B %d, %Y")
            if frcheck.day >= 1 and frcheck.day <= 7:
                if generic:
                    showmessage = "The next show is on " + showdate
                else:
                    showmessage = "The next show date (first week) is " + showdate
                return showmessage
                #return jenni.reply("The next show date (first week) is " + showdate)
            elif frcheck.day >= 15 and frcheck.day <= 21:
                if generic:
                    showmessage = "The next show is on " + showdate
                else:
                    showmessage = "The next show date (third week) is " + showdate
                return showmessage
                #return jenni.reply("The next show date (third week) is " + showdate)

    return showmessage

def nextshow(jenni, input):
    """When is the next show?"""
    #if there's no argument given, check this week. if there is an argument,
    #see if it's a valid date string and calculate at that date
    check = input.group(2)

    if not check:
        t = datetime.date.today()
        generic = False
    else:
        generic = True
        gooddate = re.search('\/', check)
        if not gooddate:
            return jenni.reply("Please enter '.ns YYYY/MM/DD' to check against a specific date.")
        if gooddate:
            parts = check.split("/")
            y, m, d = 0, 0, 0
            if len(parts) == 3:
                y, m, d = parts
                try:
                    y = int(y)
                    m = int(m)
                    d = int(d)
                except:
                    return jenni.reply("One of your date fields is mangled.")
                try:
                    t = datetime.date(y, m, d)
                except:
                    return jenni.reply("Something was off about the date you entered. I expect it in YYYY/MM/DD format.")
            else:
                return jenni.reply("Please enter the date in YYYY/MM/DD format.")


    #jenni.reply("Checking date now.")
    showmessage = weekcheck(jenni, t, generic)
    return jenni.reply(showmessage)

nextshow.commands = ['nextshow', 'ns']
nextshow.example = '.ns YYYY/MM/DD, or simply .ns to see if there is a show on this week'

if __name__ == "__main__":
    print __doc__.strip()
