#!/usr/bin/env python
# coding: utf-8

from job_bot import JobBot
from constants import *


class JobBotTester:
    def initialize(self):
        self.bot = JobBot()
        self.msg_

    def test_replyto_help(self):
        assert self.bot.replyto_help()

    def test_replyto_jobs(self):
        pass

    def test_replyto_display(self):
        pass

    def test_replyto_push(self):
        pass

    def test_replyto_my(self):
        pass

    def test_replyto_delete(self):
        pass

    def finish(self):
        pass

if __name__ == '__main__':
    tester = JobBotTester()
    tester.test_replyto_help()
    tester.test_replyto_jobs()
    tester.test_replyto_display()
    tester.test_replyto_push()
    tester.test_replyto_my()
    tester.test_replyto_delete()

