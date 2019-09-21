"""
Whatsapp analyzer.

Usage:
  main.py test
  main.py analyze <filename>   [--daily] [--limit=<row> |--listall]

Options:
  -h --help     Show this screen.
  --listall     Always show all records.
  --limit=<row> Limits number of records [default: 20].
  --daily       Shows details on a daily level
"""
from unittest import TestCase, TestSuite, TextTestRunner
from datetime import datetime
from unittest import TestCase
import emoji
from operator import attrgetter
import pandas as pd
import dateutil
import re
from docopt import docopt
c_dt_format = '%d/%m/%Y, %H:%M'
def main(args):
    if args["test"]:
        testing()
    elif args["analyze"]:
        if args["--limit"] is not None:
            analyze(args["<filename>"], args["--daily"],args["--limit"])
        elif args["--listall"]:
            analyze(args["<filename>"], args["--daily"],-1)
        else:
            analyze(args["<filename>"], args["--daily"])

def testing():
    ## do testing
    run(MessageTest('parsemessage'))
    run(MessageTest('wordcount'))
    run(MessageTest('emojicount'))
    run(MessageTest('append'))
    print('--------------------------------------')

def analyze(filename, daily, rows=20):
    ## open wa file
    print(f'Maximum {rows} per report are shown.')
    if daily:
        print(f'Daily reports are included')
    else:
        print(f'Daily reports are excluded')

    inp = open(filename, 'r')
    lines = inp.readlines()

    pattern = re.compile("Messages to this chat and calls are now secured with end-to-end encryption")
    messages = []
    for line in lines:
        if line != '\n' and line!='' and not pattern.search(line):
            if Message.isValid(line):
                m = Message.parse(line)
                messages.append(m)
            else:
                m.append(line)

    data = pd.DataFrame.from_records([s.to_dict() for s in messages])

    if rows == -1:
        rows = 999

    with pd.option_context('display.max_rows', int(rows)):
        print('--------------------------------------')
        print('How it all started and ended...')
        print('--------------------------------------')
        print(data)
        print('')
        print('--------------------------------------')
        print(f'The longest message is {data["wordcount"].max()} words long')
        print('--------------------------------------')
        print('')
        if daily:
            print('--------------------------------------')
            print('Messages per day')
            print('--------------------------------------')
            ##tpd = data.groupby('date')['content'].count()
            print(data.groupby('date')['content'].count())
            print('')
            print('--------------------------------------')
            print('Messages per day and person')
            print('--------------------------------------')
            print(data.groupby(['date','sender'])['content'].count())
            print('')

        print('')
        print('--------------------------------------')
        print('Messages per month')
        print('--------------------------------------')

        #data['date'] = pd.to_datetime(data['date'])

        data.date = pd.to_datetime(data.date)
        dg = data.groupby([pd.Grouper(key='date', freq='1M')]).agg({'content':'count', 'wordcount':'sum', 'emoji_count':'sum'})
        dg.index = dg.index.strftime('%Y %B')
        print(dg)
        print('')
        print('--------------------------------------')
        print('Messages per year')
        print('--------------------------------------')

        #data['date'] = pd.to_datetime(data['date'])
        dg = data.groupby([pd.Grouper(key='date', freq='1Y')]).agg({'content':'count', 'wordcount':'sum', 'emoji_count':'sum'})
        dg.index = dg.index.strftime('%Y')
        print(dg)
        print('')
        print('--------------------------------------')
        print('Messages total')
        print('--------------------------------------')
        dg = data.agg({'content':'count', 'wordcount':'sum', 'emoji_count':'sum'})
        print(dg)

        print('')
        print('--------------------------------------')
        print('Messages total per person')
        print('--------------------------------------')
        #data['date'] = pd.to_datetime(data['date'])
        print(data.groupby('sender').agg({'content':'count', 'wordcount':'sum', 'emoji_count':'sum'}))
        print('')
        print('--------------------------------------')
        print('Media per person ')
        print('--------------------------------------')
        print(data[data['media']==True].groupby('sender').agg({'media':'count'}))

class Message:
    def __init__(self, datetime, sender, content):
        self.datetime = datetime
        self.sender = sender
        self.content = content
        self.media = False
        if self.content == '<Media omitted>':
            self.media = True

    def append(self, s):
        self.content += " " + s

    @property
    def wordcount(self):
        return len(self.content.split())

    @property
    def emoji_count(self):
        return len(''.join(c for c in self.content if c in emoji.UNICODE_EMOJI))

    def to_dict(self):
        return {
            'datetime': self.datetime,
            'date': self.datetime.date(),
            'sender': self.sender,
            'content': self.content,
            'wordcount': self.wordcount,
            'emoji_count': self.emoji_count,
            'media':self.media,
        }
    @classmethod
    def parse(cls, s):
        # date, remainder = s.split(',',1)
        datetime_object, remainder = [x.strip() for x in s.split('-',1)]
        datetime_object = datetime.strptime(datetime_object, c_dt_format)
        sender, remainder = [x.strip() for x in remainder.split(':',1)]
        return cls(datetime_object, sender, remainder)

    @classmethod
    def isValid(cls, s):
        try:
            t = Message.parse(s)
            return True
        except:
            return False

    def __repr__(self):
        return f"{self.datetime.strftime(c_dt_format)} - {self.sender}: {self.content}"

def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

class MessageTest(TestCase):
    def parsemessage(self):
        t1 = "21/09/2019, 07:41 - Peter Pan: Python has a different way of representing syntax and default values for function arguments. Default values indicate that."
        m1 = Message.parse(t1)
        t2 = "07/09/2019, 20:48 - Carl Todd: Yes, I did 😴."
        m2 = Message.parse(t2)
        self.assertEqual(t1, m1.__repr__())
        self.assertEqual(t2, m2.__repr__())

    def wordcount(self):
        t1 = "21/09/2019, 07:41 - Peter Pan: Python has a different way of representing syntax and default values for function arguments. Default values indicate that."
        m1 = Message.parse(t1)
        self.assertEqual(m1.wordcount, 18)

    def emojicount(self):
        t2 = "07/09/2019, 20:48 - Carl Todd: Yes😴, I did 😴."
        m2 = Message.parse(t2)
        self.assertEqual(m2.emoji_count, 2)

    def append(self):
        t1 = "21/09/2019, 07:41 - Peter Pan: Python has a different way of representing syntax and default values for function arguments. Default values indicate that."
        m1 = Message.parse(t1)
        wordcount = m1.wordcount
        m1.append('Helloo')
        self.assertEqual(m1.wordcount, wordcount + 1)

if __name__ == '__main__':
    # print(docopt(__doc__))
    main(docopt(__doc__))
