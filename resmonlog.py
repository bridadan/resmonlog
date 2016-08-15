#!/usr/bin/env python

"""A simple python script template.
"""

import os
import sys
import argparse
import psutil
import time
import json

def key_func(key):
  if key == 'datetime_string':
    return -2
  elif key == 'timestamp':
    return -1
  else:
    return key


def stdout_log(data):
  print(json.dumps(data))


def json_log(logfile, data):
  logfile.write(json.dumps(data))
  logfile.flush()

def csv_get_sorted_keys(keys):
  return sorted(keys, key=key_func)


def csv_write_headers(logfile, data):
  keys = csv_get_sorted_keys(data.keys())
  logfile.write(','.join(keys) + '\r\n')
  logfile.flush()


def csv_log(logfile, data):
  keys = csv_get_sorted_keys(data.keys())
  values = [str(data[k]) for k in keys]
  logfile.write(','.join(values) + '\r\n')
  logfile.flush()


def main(arguments):
  parser = argparse.ArgumentParser(description=__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-j', '--json-file', dest='json_file', help="JSON formatted log file", type=argparse.FileType('w'))
  parser.add_argument('-c', '--csv-file', dest='csv_file', help="CSV formatted log file", type=argparse.FileType('w'))
  parser.add_argument('-p', '--period', help="Period in seconds for logging data (Default: 30)", type=float, default=30)

  args = parser.parse_args(arguments)

  wrote_headers = False

  try:

    while(True):
      start_time = time.time()
      local_time = time.localtime(start_time)
      datetime_string = time.strftime("%Y-%m-%d %H:%M:%S")
      data = {
        'timestamp': start_time,
        'datetime_string': datetime_string
      }

      per_cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
      data.update({'cpu_%d' % x: per_cpu_percentages[x] for x in range(0, len(per_cpu_percentages))})

      cpu_times_stats = psutil.cpu_times(percpu=False)
      data.update({'cpu_time_%s' % k: v for k, v in cpu_times_stats._asdict().iteritems()})

      virtual_memory_stats = psutil.virtual_memory()
      data.update({'virtual_mem_%s' % k: v for k, v in virtual_memory_stats._asdict().iteritems()})

      swap_memory_stats = psutil.swap_memory()
      data.update({'swap_mem_%s' % k: v for k, v in swap_memory_stats._asdict().iteritems()})

      disk_usage_stats = psutil.disk_usage('/')
      data.update({'disk_%s' % k: v for k, v in disk_usage_stats._asdict().iteritems()})

      if not wrote_headers:
        if args.csv_file:
          csv_write_headers(args.csv_file, data)
      
        wrote_headers = True

      stdout_log(data)

      if args.json_file:
        json_log(args.json_file, data)

      if args.csv_file:
        csv_log(args.csv_file, data)
      
      end_time = time.time()
      diff_time = end_time - start_time
      delay = args.period - diff_time

      time.sleep(args.period - diff_time)
              

  except KeyboardInterrupt, e:
    print "\n[CTRL+c] exit"
  except Exception,e:
    import traceback
    traceback.print_exc(file=sys.stdout)
    print "[ERROR] %s" % str(e)
    sys.exit(1)

  

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
