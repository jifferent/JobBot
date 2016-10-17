#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import ujson
import sys
import traceback
import random
import datetime

GROUP_ID = ""

MSG_HELP = """List of commands:


!help - 显示帮助信息

!jobs - 显示所有的职位Posting, 包括职位ID和职位Title。不包括Detail

!display <职位ID> - 显示一个职位的ID, Title, Detail, 还有发布者

!push title - <职位Title> detail: <职位Detail> - 发布新的职位。详细使用说明请打!push, 还是不懂的话请联系群主(⊙ˍ⊙)

!my - 显示自己的发布的所有职位

!delete <职位ID>: 删除一条自己发布过的职位"""

MSG_TITLE_AND_LIST = """{}

{}"""

MSG_DISPLAY_NO_JOBID = """Please format you posting to: !display <job ID>

Example 1:
!display 1111 - This will display the information for job 1111"""

MSG_DISPLAY = """Job ID: {}
Posted by: {}

{}
{}"""

MSG_NO_SUCH_JOB = """No such job ID"""

MSG_PUSH_NO_TITLE = """Your message does not contain title. We can't process your request."""

MSG_PUSH_NO_DETAIL = """Your message does not contain detail. We can't process your request."""

MSG_PUSH_SUCCESS = """You job posting has been recorded. Job ID: {}"""

MSG_PUSH_ERROR = """Please format you posting to: !push title: <Job Posting Title> detail: <Job Posting Detail>

Example 1:
!push title: 数据分析实习生 contant: 要求会VBA, 熟悉EXCEL指令, 本科文凭, blah blah blah"""

MSG_MY_ERROR = """Sorry, I can't process this request"""

MSG_DELETE_ERROR = """Please format you posting to: !delete <id>

Example 1:
!delete 1111 - If job 1111 belongs to you, then job 1111 will be removed"""

MSG_DELETE_SUCCESS = """Job removed: {}"""

MSG_JOB_NOT_BELONGTO_SENDER = """You did not post this job"""


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
                print "No such command: {}".format(command.encode('utf-8'))
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

    def respond_to_user(self, msg, note):
        if self.is_to_group(msg):
            self.send_msg_by_uid(note, GROUP_ID)
        elif self.is_to_self(msg):
            self.send_msg_by_uid(note, msg['user']['id'])

    def is_job_belongsto_sender(self, job, msg):
        return job['user']['id'] != msg['user']['id']

    def make_note_from_job_list(self, jobs, note_title='Jobs:'):
        return MSG_TITLE_AND_LIST.format(
            note_title,
            '\n'.join(
                ['{} | {}'.format(job['id'].encode('utf-8'), job['title'].encode('utf-8'))
                for job in jobs]
            )
        )

    def replyto_help(self, msg):
        """
        Author: Zhu BroBro
        Bot reply to user with '!help'
        """
        self.respond_to_user(msg, MSG_HELP)

    def get_all_jobs(self):
        with open(os.path.join(self.temp_pwd, 'jobs.json'), 'r') as data_file:    
            jobs = json.loads(data_file).get("jobs", [])
        return jobs

    def replyto_jobs(self, msg):
        jobs = [self.id_job_map[id] for id in self.id_job_map]
        note = self.make_note_from_job_list(jobs, "Here are the jobs that you have posted:")
        self.respond_to_user(msg, note)

    def replyto_display(self, msg):
        job_id = self.arg(msg, 2)
        if job_id is None:
            self.respond_to_user(msg, MSG_DISPLAY_NO_JOBID)
            return
        if job_id not in self.id_job_map:
            self.respond_to_user(msg, MSG_NO_SUCH_JOB)
            return
        job = self.id_job_map[job_id]
        if not self.is_job_belongsto_sender(job, msg):
            self.respond_to_user(msg, MSG_JOB_NOT_BELONGTO_SENDER)
            return
        note = MSG_DISPLAY.format(
            job_id,
            job['user']['name'].encode('utf-8'),
            job['title'].encode('utf-8'),
            job['detail'].encode('utf-8')
        )
        self.respond_to_user(msg, note)

    def replyto_push(self, msg):
        try:
            msg_pure = msg["content"]["data"].split("!push")[1].strip()
            if not msg_pure.startswith('title:'):
                self.respond_to_user(msg, MSG_PUSH_NO_TITLE)
                return
            if 'detail:' not in msg_pure:
                self.respond_to_user(msg, MSG_PUSH_NO_DETAIL)
                return
            job = {}
            job["title"] = ''.join(msg_pure.split('title:')[1]).split('detail:')[0].strip()
            job["detail"] = ''.join(msg_pure.split('detail:')[1]).strip()
            job["user"] = msg["user"]
            job["datetime"] = datetime.datetime.now()
            while(True):
                job["id"] = self.random_number_string()
                if job['id'] not in self.id_job_map:
                    break
            note = MSG_PUSH_SUCCESS.format(job['id'].encode('utf-8'))
            with open(os.path.join(self.temp_pwd, 'jobs.json'), 'a') as data_file:
                data_file.write(ujson.dumps(job) + '\n')
            self.id_job_map[job["id"]] = job
            self.respond_to_user(msg, note)
        except:
            traceback.print_exc()
            self.respond_to_user(msg, MSG_PUSH_ERROR)

    def replyto_my(self, msg):
        try:
            user_jobs = []
            for _, job in self.id_job_map.iteritems():
                if job['user']['id'] == msg['user']['id']:
                    user_jobs.append(job)
            note = self.make_note_from_job_list(user_jobs, "Here are the jobs that you have posted:")
            self.respond_to_user(msg, note)
        except:
            traceback.print_exc()
            self.respond_to_user(msg, MSG_MY_ERROR)

    def replyto_delete(self, msg):
        try:
            job_id = msg['content']['data'].split('!delete')[1].strip()
            if job_id not in self.id_job_map:
                self.respond_to_user(msg, MSG_NO_SUCH_JOB)
                return
            if not self.is_job_belongsto_sender(self.id_job_map[job_id], msg):
                self.respond_to_user(msg, MSG_JOB_NOT_BELONGTO_SENDER)
                return
            self.id_job_map.pop(job_id, None)
            file_data = {}
            with open(os.path.join(self.temp_pwd, 'jobs.json'), 'r') as data_file:
                for line in data_file:
                    entry = ujson.loads(line.strip())
                    file_data[entry['id']] = entry
            file_data.pop(job_id, None)
            with open(os.path.join(self.temp_pwd, 'jobs.json'), 'w') as data_file:
                for entry in file_data:
                    data_file.write(ujson.dumps(entry) + '\n')
            note = MSG_DELETE_SUCCESS.format(job_id.encode('utf-8'))
            self.respond_to_user(msg, note)
        except:
            traceback.print_exc()
            self.respond_to_user(msg, MSG_DELETE_ERROR)


def main():
    bot = JobBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
