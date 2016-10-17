#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import ujson
import sys
import traceback
import random

GROUP_ID = ""

class JobBot(WXBot):
    

    def __init__(self):
        WXBot.__init__(self)
        self.callback = {
            '!help': self.replyto_help,
            '!jobs': self.replyto_jobs,
            '!display': self.replyto_display,
            '!my': self.replyto_my,
            '!delete': self.replyto_delete,
            '!push': self.replyto_push,
        }
        self.id_job_map = {}
        with open(os.path.join(self.temp_pwd, 'jobs.json'), 'r') as data_file:
            for line in data_file:
                entry = ujson.loads(line.strip())
                self.id_job_map[entry['id']] = entry

    def handle_msg_all(self, msg):
        try:
            print "Start handling all msg"
            command = self.arg(msg, 1)
            if command in self.callback:
                self.callback[command](msg)
            else:
                print "No such command: {}".format(command)
        except:
            traceback.print_exc()
            print "Error happen in user to group"


    def is_command(self, msg, command):
        return msg['content']['data'].startswith(command)

    def arg(self, msg, num):
        """
        Get <num>th argument of <msg>

        Example: self.arg("!job d2e198a", 2) returns d2e198a
        Example: self.arg("!job", 2) returns None
        Example: self.arg("!job d2e198a wahahahaha", 1) returns !job
        """
        commands = msg['content']['data'].strip().split()
        return commands[num - 1] if len(commands) > num - 1 else None

    def random_number_string(self, length=4):
        return ''.join(random.choice('0123456789') for _ in range(length))

    def is_to_self(self, msg):
        return msg['msg_type_id'] == 4

    def is_to_group(self, msg):
        return msg['msg_type_id'] == 3

    def is_from_bot(self, msg):
        pass

    def is_from_others(self, msg):
        pass

    def replyto_help(self, msg):
        """
        Author: Zhu BroBro
        Bot reply to user with '!help'
        """
        # Display menu
        note = ""
        # Get jobs
        jobs = self.get_all_jobs()
        if len(jobs) == 0:
            note = "There is no job for now"
        else:
            for job in jobs:
                note += "ID: {}, Title: {}".format(job['id'], job['title'])

        user_id = self.get_user_id("朱brobro")
        self.send_msg_by_uid(note, user_id)
        # self.send_msg_by_uid(note, GROUP_ID)

    def get_all_jobs(self):
        with open(os.path.join(self.temp_pwd, 'jobs.json'), 'r') as data_file:    
            jobs = json.loads(data_file).get("jobs", [])
        return jobs

    def replyto_jobs(self, msg):
        pass

    def replyto_job_id(self, msg):
        pass

    def replyto_display(self, msg):
        pass

    def replyto_push(self, msg):
        try:
            msg_pure = msg["content"]["data"].split("!push")[1].strip()
            if not msg_pure.startswith('title:'):
                print 'There is no title'
                return
            if 'content:' not in msg_pure:
                print 'There is no content'
                return
            job = {}
            job["title"] = ''.join(msg_pure.split('title:')[1]).split('content:')[0].strip()
            job["content"] = ''.join(msg_pure.split('content:')[1]).strip()
            job["user"] = msg["user"]
            while(True):
                job["id"] = self.random_number_string()
                if job['id'] not in self.id_job_map:
                    break
            note = "You job posting has been recorded. Job ID: {}".format(job['id'])
            with open(os.path.join(self.temp_pwd, 'jobs.json'), 'a') as data_file:
                data_file.write(ujson.dumps(job) + '\n')
            self.id_job_map[job["id"]] = job
            if self.is_to_group(msg):
                self.send_msg_by_uid(note, GROUP_ID)
            elif self.is_to_self(msg):
                self.send_msg_by_uid(note, msg['user']['id'])
        except:
            traceback.print_exc()
            note =\
            """
            Please format you posting to: !push title: <Job Posting Title> content: <Job Posting Content>

            Example 1:
            !push title: 数据分析实习生 contant: 要求会VBA, 熟悉EXCEL指令, 本科文凭, blah blah blah
            """
            self.send_msg_by_uid(note, GROUP_ID)

    def replyto_my(self, msg):
        pass

    def replyto_delete(self, msg):
        pass

def main():
    bot = JobBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
