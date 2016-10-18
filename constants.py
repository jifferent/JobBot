#!/usr/bin/env python
# coding: utf-8


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
