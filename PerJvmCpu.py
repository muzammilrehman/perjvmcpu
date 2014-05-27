#!/usr/bin/env python2.6
"""
Per JVM cpu collector.
Version 0.1
"""

import collections
import logging
import psutil

_DEFAULT_QUIT_TIME = 600
_DEFAULT_INTERVAL = 60
_DEFAULT_ERROR_SLEEP = 7200
_DEFAULT_PATTERN = '-Dprogram.name='


class NoJavaPid(Exception):

    """

    Exception raised when no java pids are found

    """
    pass


class PerJvmCpu(object):

    def __init__(self, exclude_list=None, name_pattern=None,
                 dryrun=False, logger=None, interval=1):
        self.dryrun = dryrun
        self.log = logger
        self.exclude_patterns = exclude_list or []
        self.name_pattern = name_pattern
        self.interval = interval
        self.name_pattern = self.name_pattern or _DEFAULT_PATTERN
        if not self.log:
            self.log = logging

    def get_pid_details(self):
        """
        After getting the java pid's need to get the process name
        and instance for container style graphing
        """
        self.java_pidlist = []
        self.java_piddict = collections.defaultdict(list)
        try:
            processlist = psutil.process_iter()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as ex:
            self.log.error(
                "[get_pid_details] Failed to extract pid list {0}".format(ex))
            raise
        for process in processlist:
            if process.name == 'java':
                self.java_pidlist.append(process.pid)
        if self.java_pidlist:
            self.log.info("List of java process {0}".format(self.java_pidlist))
            for pid in self.java_pidlist:
                options = None
                name = None
                try:
                    options = psutil.Process(pid).cmdline
                except (psutil.NoSuchProcess, psutil.AccessDenied) as ex:
                    self.log.error(
                        "[get_pid_details] Skipping pid {0}. Caused by {1}".format(pid, ex))
                exclusion = set(self.exclude_patterns) & set(options)
                if exclusion:
                    self.log.info("[get_pid_details] Skipping pid {0} "
                                  "part of exclusion list match {1}".format(pid, list(exclusion)))
                    continue
                if options:
                    for option in options:
                        if option.startswith(self.name_pattern):
                            if '=' in option:
                                name = option.split('=')[-1]
                if name:
                    self.log.info(
                        "[get_pid_details] Processing PID={0}, name={1}".format(pid, name))
                    self.java_piddict[pid] = name
                else:
                    self.log.error(
                        "[get_pid_details] Name could not "
                        "determined for {0} options {1}".format(pid, options))
        else:
            raise NoJavaPid
        return self.java_piddict

    def cpu_stats(self, pid):
        """
        After we have process name and instance id get the cpu details
        """
        cpu_data = None
        try:
            ps = psutil.Process(pid)
            cpu_data = ps.get_cpu_percent(
                self.interval) / float(psutil.NUM_CPUS)
        except (psutil.AccessDenied, psutil.NoSuchProcess) as ex:
            self.log.error(
                "[cpu_stats] Could not calculate cpu usage for {0}. Caused by {1}".format(pid, ex))
        return cpu_data


if __name__ == "__main__":
    ob = PerJvmCpu(name_pattern="-Dprogram.name=", interval=10)
    for pid in ob.get_pid_details():
        print ob.cpu_stats(pid)

