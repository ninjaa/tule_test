# Tule Interview Test
This is Aditya Advani's response to the 'CSV Normalization' challenge provided him.


## Prerequisites

- Python 3.6
- pip package for pytz


## Steps to run

You can test the code by running the following commands. Please note that 'python3.6' is the name for the Python 3.6 binary on my Ubuntu 14.04 machine, on your distro the command name may be different.

Try the following on the command line:

```
$> cat sample.csv | python3.6 tule_test.py > output/output.csv
```

```
$> cat sample-with-broken-utf8.csv | python3.6 tule_test.py > output/output-with-broken-utf8-input.csv
```

And to trigger an exception, I created a sample file with a broken timestamp (14 is not a valid PM hour value):

```
$> cat sample-with-broken-timestamp.csv | python3.6 tule_test.py > output/output-with-broken-timestamp-input.csv
Exception time data '10/5/12 14:31:11 PM' does not match format '%m/%d/%y %I:%M:%S %p'
```

The output subdirectory is in gitignore so you can keep dumping files into it and then truncating it to test.

