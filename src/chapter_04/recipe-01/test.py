### ############################################################################
### # File: test.py                                                            #
### # Project: recipe-01                                                       #
### # Created Date: 2024/04/12 14:13:29                                        #
### # Author: realjf                                                           #
### # -----                                                                    #
### # Last Modified: 2024/04/12 14:13:31                                       #
### # Modified By: realjf                                                      #
### # -----                                                                    #
### #                                                                          #
### ############################################################################
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--executable', help='full path to executable')
parser.add_argument('--short', default=False, action='store_true', help='run a shorter test')
args = parser.parse_args()

def execute_cpp_code(integers):
  result = subprocess.check_output([args.executable]+integers)
  return int(result)

if args.short:
  result = execute_cpp_code([str(i) for i in range(1, 101)])
  assert result == 5050, 'summing up to 100 failed'
else:
  result = execute_cpp_code([str(i) for i in range(1, 1001)])
  assert result == 500500, 'summing up to 1000 failed'
