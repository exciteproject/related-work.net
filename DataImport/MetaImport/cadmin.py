#
# Celery Job Scheduler
#
# Remarks:
# * Meta information is downloaded in chunks of delta=1 moths
# * The arxiv meta repository starts with introduction of the new arxiv-id format in 2007.
#   However, older articles are contained in the 2007-05 month.
# * Arguments are parsed from the commandline. Only '--from' and '--to' are really important.
#

import argparse, os, json
from datetime import date, datetime, timedelta
import capp as app

#
# MAIN PRORGRAM
#

# Read command line arguments
arg_parser = argparse.ArgumentParser(description = 'Download metadata from Arxiv')
arg_parser.add_argument('--from', default = '2005-01-01', dest='from_date',
                        help='enter from date in iso format,e.g. 2011-01-01')
arg_parser.add_argument('--to', default = '2016-11-25', dest='to_date',
                        help='enter end  date in iso format,e.g. 2011-01-05')
arg_parser.add_argument('--step', dest='delta', default = '1', type = int,
                        help = 'number of months to querry at a time')

args = arg_parser.parse_args()

# Set global variables
# Arxiv oa server:

# Get records in time range in chunks of .. months
from_date    = datetime.strptime(args.from_date, "%Y-%m-%d")
until_date   = datetime.strptime(args.to_date,   "%Y-%m-%d")
delta_months = args.delta
                     
def loop_months(start_date, end_date, month_step=1):
    if month_step == 0: return

    current_date = start_date
    while True:
        if month_step > 0 and current_date >= end_date: break
        if month_step < 0 and current_date <= end_date: break

        carry, new_month = divmod(current_date.month - 1 + month_step, 12)
        new_month += 1
        next_date = current_date.replace(year=current_date.year + carry, month=new_month)

        if month_step > 0 and next_date > end_date: next_date = end_date
        if month_step < 0 and next_date < end_date: next_date = end_date

        if month_step > 0:
            yield current_date, next_date
        if month_step < 0:
            yield next_date, current_date

        current_date = next_date

def main():
    for (c_date,n_date) in loop_months(from_date, until_date, delta_months):
        print('Schedule fetch %s -- %s' % (c_date.strftime('%Y-%m-%d'), n_date.strftime('%Y-%m-%d')))
        app.fetch_arxiv_meta.apply_async(
            args=(c_date.strftime('%Y-%m-%d'), n_date.strftime('%Y-%m-%d'))
        )

if __name__ == '__main__':
    main()
