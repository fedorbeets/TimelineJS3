# Convert google doc spreadsheet format for timelinejs to json file
# useful if you want to experiment using google doc but eventually
# host everything yourself privately.

# Example: go to google docs spreadsheet and do File -> Download As -> CSV (Comma Separated Values)
# save as timeline.csv, run this, you get a timeline.json out
#
# Or look at your google doc ID long string like for example 1xTn9OSdmnxbBtQcKxZYV-xXkKoOpPSu6AUT0LXXszHo
# wget -qO timeline.csv 'https://docs.google.com/spreadsheets/d/1xTn9OSdmnxbBtQcKxZYV-xXkKoOpPSu6AUT0LXXszHo/pub?output=csv'

import csv
import json

csvfile = open('timeline.csv', 'rb')
outfile = open('timeline.json', 'w')
reader = csv.DictReader(csvfile)

data = {}
events = []
eras = []
data['events'] = events
data['eras'] = eras

MONTHS = 12  # amount of max months in a year
DAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def check_event(event):
    assert int(event['start_date']['year'])  # check every event has start year
    if int(event['start_date']['year']) > 6000:
        print("Warning: An event has year > 6000" + event['end_date']['year'])
    if int(event['start_date']['year']) < -6000:
        print("Warning: An event has year < -6000" + event['end_date']['year'])
    # unlike spec says, headline IS required, else JSON cannot load
    assert 'text' in event, "Event has no headline: " + event['start_date']['year']
    assert 'headline' in event['text'], "Event has no headline" + event['start_date']['year']
    if 'month' in event['start_date']:
        check_month(int(event['start_date']['month']))
    if 'day' in event['start_date']:
        assert 'month' in event['start_date'], "event with start_day but no start_month"
        check_day(int(event['start_date']['month']), int(event['start_date']['day']))
    if 'end_date' in event:
        if int(event['end_date']['year']) > 6000:
            print("Warning: An event has year > 6000" + event['end_date']['year'])
        if int(event['end_date']['year']) < -6000:
            print("Warning: An event has year < -6000: " + event['end_date']['year'])
        if 'month' in event['end_date']:
            check_month(int(event['end_date']['month']))
        if 'day' in event['end_date']:
            assert 'month' in event['end_date'], "event with end_day but no end_month"
            check_day(int(event['end_date']['month']), int(event['end_date']['day']))


def check_month(month):
    assert month < 13, "event with month > 12: " + str(month)
    assert month > 0, "event with month < 1: " + str(month)


def check_day(month, day):
    assert day > 0
    assert day <= DAYS[month-1], "event with day not in month: " + str(month) + " " + str(day)


# Didn't support 'End Time': '', 'Time': ''
keymap = {'Media': 'media|url','Media Caption': 'media|caption', 'Media Thumbnail': 'media|thumbnail',
          'Month': 'start_date|month', 'Day': 'start_date|day', 'Year': 'start_date|year',
          'End Month': 'end_date|month', 'End Day': 'end_date|day', 'End Year': 'end_date|year',
          'Headline': 'text|headline', 'Text': 'text|text',
          'Group': 'group', 'Display Date': 'display_date'}

for row in reader:
    event = {}
    for a in keymap:
        if row[a]:
            if '|' in keymap[a]:
                (x,y)=keymap[a].split("|")
                if not x in event: event[x]={}
                event[x][y] = row[a]
            else:
                event[keymap[a]] = row[a]
    if 'group' in event:
        event['group'] = event['group'].lower()  # TimeLineJS3 capitalises group name anyway
    if row['Background']:
        event['background'] = {}
        if row['Background'].startswith("#"):
            event['background']['color']=row['Background']
        else:
            event['background']['url']=row['Background']
    if row['Type'] == 'title':
        data['title'] = event
    elif row['Type'] == 'era':
        eras.append(event)
        assert event['start_date']['year']  # check that era has a start/end year
        assert event['end_date']['year']
    else:
        check_event(event)
        events.append(event)

json.dump(data, outfile, sort_keys=True, indent=4)

