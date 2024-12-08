#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "ksingh631"
Semester: "Fall 2024, OPS445NCC"

The python code in this file is original work written by
"student name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human readable format")
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    ...
    # percent to graph function
    input_length = int(length * percent) #no of characters' length
    blank_length = length - input_length #no of blanks
    return '#' * input_length + ' ' * blank_length #bar graph string

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    ...
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if 'MemTotal' in line:
                return int(line.split()[1]) #getting the total memory value
    return 0

def get_avail_mem() -> int:
    "return total memory that is currently in use"
    ...
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if 'MemAvailable' in line:
                return int(line.split()[1]) #getting the available memory value
    return 0

#Assignment 2 - 1st milestone done. ----------


def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...
    result = os.popen(f'pidof {app_name}').read().strip()
    if result:
        return result.split()
    return []

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...
    with open(f'/proc/{proc_id}/status', 'r') as f:
        for line in f:
            if 'VmRSS' in line:
                return int(line.split()[1])
    return 0

#2ndstoner done

#Final part

def bytes_to_human_r(kilobytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kilobytes
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    total_memory = get_sys_mem()
    
    if not args.program:
        used_memory = total_memory - get_avail_mem()        #Used memory
        percent_used = used_memory / total_memory           #Used memory in percentage
        graph = percent_to_graph(percent_used, args.length) #graphical
        
        #Human readable with -H
        if args.human_readable:
            used_memory_str = bytes_to_human_r(used_memory)
            total_memory_str = bytes_to_human_r(total_memory)

            #output prints
            #numericals
            print(f"Memory         [{graph}| {int(percent_used * 100)}%] {used_memory_str}/{total_memory_str}")
        else:
            #human readable/bytes, etc
            print(f"Memory         [{graph}| {int(percent_used * 100)}%] {used_memory}/{total_memory}")
    
    else:
        pids = pids_of_prog(args.program)
        #print alternative result
        if not pids:
            print(f"{args.program} not found.")
            
        else:
            total_program_memory = 0
            for pid in pids:
                #numerical
                rss_memory = rss_mem_of_pid(pid)
                percent_used = rss_memory / total_memory
                graph = percent_to_graph(percent_used, args.length)

                #human readable
                if args.human_readable:
                    rss_memory_str = bytes_to_human_r(rss_memory)
                    total_memory_str = bytes_to_human_r(total_memory)

                    #prints
                    print(f"{pid:<15} [{graph}| {int(percent_used * 100)}%] {rss_memory_str}/{total_memory_str}")
                else:
                    print(f"{pid:<15} [{graph}| {int(percent_used * 100)}%] {rss_memory}/{total_memory}")
                total_program_memory += rss_memory
            

#OPS445 Assignment 2 done. By ksingh631: Thanks!