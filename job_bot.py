#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json

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

    def handle_msg_all(self, msg):
        try:
            print "Start handling all msg"
            command = self.arg(msg, 1)
            print "commands is " + commands
            if command in self.callback:
                self.callback[command](msg)
        except:
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
        commands = msg.strip().split()
        return commands[1] if len(commands) > 1 else None

    def check_job_id(self, job_id, all_jobs):
        for job in all_jobs:
            if job_id == job["id"]:
                return True
        return False
        
    def is_to_self(self, msg):
        pass

    def is_to_group(self, msg):
        pass

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
        jobs = get_all_jobs()
        if len(jobs) == 0:
            note = "There is no job for now"
        else:
            for job in jobs:
                note += "ID: {}, Title: {}".format(job['id'], job['title'])

        user_id = self.get_user_id("朱brobro")
        self.send_msg_by_uid(note, user_id)
        # self.send_msg_by_uid(note, GROUP_ID)

    def get_all_jobs():
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
        title = "title:"
        content = "content:"
        note = ""
        try:
            pure_msg = msg["content"]["data"].split("!push", '')[1]
            title_msg = pure_msg.split(title, 1)[1].split(content, 1)[0]
            content_msg = pure_msg.split(contect, 1)[1]
            note = "You job posting has been record"
            # Save to tile
            with open(os.path.join(self.temp_pwd, 'jobs.json'), 'a') as data_file:    
                jobs = json.loads(data_file)
            all_jobs = jobs.get("jobs", [])
            job = {}
            while(True):
                job["id"] = random.randrange(1, 1000)
                if check_job_id(job["id"], all_jobs) is False:
                    break
            job["title"] = title_msg
            job["content"] = content_msg
            job["user"] = meg["user"]
            all_jobs.append(job)
            data_file.write(json.dumps({"jobs":all_jobs }))
        except:
            note = "Please format you posting to: !push title: CS jobs content: This is a job"
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
