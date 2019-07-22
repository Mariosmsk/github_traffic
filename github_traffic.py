# (C) 2018 by Marios S. Kyriakou, University of Cyprus, KIOS Research and Innovation Center of Excellence (KIOS CoE)
# Get traffic of your repo
# This code run one time of day or every 14 days to get the traffic results
# Include all history data of your traffic.

import github
import pathlib
from datetime import date

repo = 'repo'
org = 'organization/user'
token = 'token'
filename = 'traffic.csv'
total_filename = 'totals.csv'

gh = github.GitHub(username=None, password=None, access_token=token)
views_14_days = gh.repos(org, repo).traffic.views.get()

file = pathlib.Path(filename)
if file.exists():
    fread = open(filename, 'r')
    before_data = fread.read()
    check = before_data[:]
    before_data = before_data.split('\n')
    fread.close()

f = open(filename, 'w')
f.write('#Date, Visitors, Views')
f.write('\n')

ftotal = open(total_filename, 'w')
unique_visits = []
views_counts = []

if 'before_data' in globals():
    for data in before_data:
        if '#' in data or data == '':
            continue
        if str(date.today()) in data:
            continue
        line = data.split(', ')
        unique_visits.append(int(line[1]))
        views_counts.append(int(line[2]))
        f.write(line[0] + ', ' + line[1] + ', ' + line[2])
        f.write('\n')

for view_per_day in views_14_days['views']:

    if 'before_data' in globals():
        if view_per_day['timestamp'] in check:
            continue
        if str(date.today()) in view_per_day['timestamp']:
            continue
    unique_visits.append(view_per_day['uniques'])
    views_counts.append(view_per_day['count'])

    f.write(str(view_per_day['timestamp']) + ', ' + str(view_per_day['uniques']) + ', ' + str(
        view_per_day['count']))
    f.write('\n')

ftotal.write('Total visitors: ' + str(sum(unique_visits)))
ftotal.write('\n')
ftotal.write('Total views: ' + str(sum(views_counts)))
ftotal.close()
f.close()