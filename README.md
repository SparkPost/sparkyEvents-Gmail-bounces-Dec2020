<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?plan=free-0817?src=Social%20Media&sfdcid=70160000000pqBb&pc=GitHubSignUp&utm_source=github&utm_medium=social-media&utm_campaign=github&utm_content=sign-up) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# sparkyEvents-Gmail-bounces-Dec2020
[![Build Status](https://travis-ci.org/tuck1s/sparkyEvents.svg?branch=master)](https://travis-ci.org/tuck1s/sparkyEvents)

Specific version of this tool, specifically to retrieve Gmail Hard Bounces class 10 ONLY, for a specific time-range.

## Gmail December 2020 hard bounces

Run the tool with the following advised time ranges:

```
./sparkyEvents.py outfile.csv 2020-12-14T22:00:00Z 2020-12-16T00:00:00Z
```

## Easy installation

Firstly ensure you have `python3`, `pip` and `git`.

Next, get the project. Install `pipenv` (`--user` option recommended, [see this article](https://stackoverflow.com/questions/42988977/what-is-the-purpose-pip-install-user)) and use this to install the project dependencies.
```
git clone https://github.com/tuck1s/sparkyEvents.git
cd sparkyEvents
pip install --user pipenv
pipenv install
pipenv shell
```
_Note: In the above commands, you may need to run `pip3` instead of `pip`._

You can now type `./sparkyEvents.py -h` and see usage info:

```
 ./sparkyEvents.py -h
usage: sparkyEvents.py [-h] outfile.csv from_time to_time

Simple command-line tool to retrieve SparkPost message events into a .CSV
file.

positional arguments:
  outfile.csv  output filename (CSV format), must be writeable.
  from_time    Datetime in format of YYYY-MM-DDTHH:MM:ssZ, inclusive.
  to_time      Datetime in format of YYYY-MM-DDTHH:MM:ssZ, exclusive.

optional arguments:
  -h, --help   show this help message and exit

SparkPost API key, host, record event type(s) and properties are specified in sparkpost.ini.
```

## Pre-requisites
Set up the `sparkpost.ini` file based on the enclosed `sparkpost.ini.example`.

Replace `<YOUR API KEY>` with your specific, private API key.

## See Also
[SparkPost Developer Hub](https://developers.sparkpost.com/)

[SparkPost Event Types](https://developers.sparkpost.com/api/events/#header-event-types)

[SparkPost Event Properties](https://www.sparkpost.com/docs/tech-resources/webhook-event-reference/)

