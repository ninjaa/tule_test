# ## The problem: CSV normalization

# Please write a tool that reads a CSV formatted file on `stdin` and
# emits a normalized CSV formatted file on `stdout`. Normalized, in this
# case, means:

# * The entire CSV is in the UTF-8 character set.
# * DONE The Timestamp column should be formatted in ISO-8601 format.
# * DONE The Timestamp column should be assumed to be in US/Pacific time;
#   please convert it to US/Eastern.
# * DONE All ZIP codes should be formatted as 5 digits. If there are less
#   than 5 digits, assume 0 as the prefix.
# * DONE All name columns should be converted to uppercase. There will be
#   non-English names.
# * The Address column should be passed through as is, except for
#   Unicode validation. Please note there are commas in the Address
#   field; your CSV parsing will need to take that into account. Commas
#   will only be present inside a quoted string.
# * DONE The columns `FooDuration` and `BarDuration` are in HH:MM:SS.MS
#   format (where MS is milliseconds); please convert them to a floating
#   point seconds format.
# * DONE The column "TotalDuration" is filled with garbage data. For each
#   row, please replace the value of TotalDuration with the sum of
#   FooDuration and BarDuration.
# * OK The column "Notes" is free form text input by end-users; please do
#   not perform any transformations on this column. If there are invalid
#   UTF-8 characters, please replace them with the Unicode Replacement
#   Character.

# You can assume that the input document is in UTF-8 and that any times
# that are missing timezone information are in US/Pacific. If a
# character is invalid, please replace it with the Unicode Replacement
# Character. If that replacement makes data invalid (for example,
# because it turns a date field into something unparseable), print a
# warning to `stderr` and drop the row from your output.


import codecs
import csv
from datetime import datetime
import pytz
import sys
import time

# UTF8reader = codecs.getreader('utf-8')
# reader = csv.DictReader(sys.stdin.replace(bytes([0xff]), '\uFFFD'))
# reader = csv.DictReader(sys.stdin.buffer.readlines().decode('utf-8', 'replace'))


def get_fractional_sec(time_str):
    time_str, float_ = time_str.split('.')
    h, m, s = time_str.split(':')
    return float(int(h) * 3600 + int(m) * 60 + int(s)) + float("0." + float_)


if __name__ == "__main__":

    raw_input = sys.stdin.buffer.readlines()
    for idx, line in enumerate(raw_input):
        raw_input[idx] = line.decode('utf-8', 'replace')

    # print(raw_input)

    reader = csv.DictReader(raw_input)

    # collected_output = []

    for idx, row in enumerate(reader):
        if idx == 0:
            writer = csv.DictWriter(sys.stdout, row.keys())
            writer.writeheader()
        try:
            try: # first try strptime with TZ, then without
                new_timestamp = datetime.strptime(row['Timestamp'], "%m/%d/%y %I:%M:%S %p %Z")
            except ValueError:
                new_timestamp = datetime.strptime(row['Timestamp'], "%m/%d/%y %I:%M:%S %p")
            if new_timestamp.tzinfo == None:
                new_timestamp = pytz.timezone('America/Los_Angeles').localize(new_timestamp)
                # print(new_timestamp.isoformat())
            new_timestamp = new_timestamp.astimezone(tz=pytz.timezone('America/New_York'))
            row['Timestamp'] = new_timestamp.isoformat()
            row['ZIP'] = row['ZIP'].zfill(5)
            row['FullName'] = row['FullName'].upper()
            new_foo_duration = get_fractional_sec(row['FooDuration'])
            row['FooDuration'] = new_foo_duration
            new_bar_duration = get_fractional_sec(row['BarDuration'])
            row['BarDuration'] = new_bar_duration
            new_total_duration = new_foo_duration + new_bar_duration
            row['TotalDuration'] = new_total_duration
            # collected_output.append(row)
            writer.writerow(row)
        except BaseException as err:
            print("Exception in row {}, row skipped: {}".format(idx + 1, err), file=sys.stderr) # skip a row in which we found an exception
            continue
