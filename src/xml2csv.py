import pandas as pd
import re
from bs4 import BeautifulSoup
import html

"""
Extract Post Data
"""
def handle_none(result): return int(
    result.group(1)) if result is not None else None


def handle_none2(result): return int(result) if result is not None else None


def clean(text):
    if text is None:
        return ''
    for trash in ['&lt;', 'p&gt;', '&gt;', '&#xA;', '&quot;']:
        text = text.replace(trash, '')
    return text


def process_line_post(line):
    date_match = re.search(' CreationDate="(.*?)" ', line)
    if date_match is not None:
        DateTime = re.search(' CreationDate="(.*?)" ', line).group(1)
    else:
        DateTime = None

    body_match = re.search(' Body="(.*?)" ', line)
    if body_match is not None:
        body = clean(body_match.group(1))
        body_length = len(re.findall(r'\w+', body))
        if body_length == 0:
            math_ratio = 0
        else:
            math_ratio = len(
                ''.join(re.findall('\$(.*?)\$', body))) / body_length
    else:
        body = None
        body_length = None
        math_ratio = None
    
    Tags_match = re.search(' Tags="(.*?)" ', line)
    if Tags_match is not None:
        Tags = Tags_match.group(1)
        decoded_tags = html.unescape(Tags)
        tags = re.findall('<(.*?)>', decoded_tags)
    else:
        tags = None

    return dict(
        CreationDate=DateTime,
        Id=handle_none(re.search(r' Id="(\d+)" ', line)),
        PostTypeId=handle_none(re.search(' PostTypeId="(\d+)" ', line)),
        Tags = tags,
        Score=handle_none(re.search(' Score="(\d+)" ', line)),
        OwnerUserId=handle_none(re.search(' OwnerUserId="(\d+)" ', line)),
        ParentId=handle_none(re.search(' ParentId="(\d+)" ', line)),
        AnswerCount=handle_none(re.search(' AnswerCount="(\d+)" ', line)),
        CommentCount=handle_none(re.search(' CommentCount="(\d+)" ', line)),
        FavoriteCount=handle_none(re.search(' FavoriteCount="(\d+)" ', line)),
        AcceptedAnswerId=handle_none(
            re.search(' AcceptedAnswerId="(\d+)" ', line)),
        PostLength=body_length,
        MathRatio=math_ratio,
    )

"""
Extract User Data
"""


def extract_user_data(row):
    return dict(
        Id=handle_none2(row.get('id')),
        Reputation=handle_none2(row.get('reputation')),
        CreationDate=row.get('creationdate'),
        DisplayName=row.get('displayname'),
        Views=handle_none2(row.get('views')),
        UpVotes=handle_none2(row.get('upvotes')),
        DownVotes=handle_none2(row.get('downvotes')),
        AccountId=handle_none2(row.get('accountid'))
    )


"""
Extract Badge Data
"""


def extract_badge_data(row):
    return dict(
        Id=int(row.get('id')),
        UserId=int(row.get('userid')),
        Name=row.get('name'),
        Date=row.get('date'),
        Class=int(row.get('class').pop()),
    )


"""
Extract Votes Data
"""


def process_line_votes(line):
    date_match = re.search(' CreationDate="(.*?)" ', line)
    if date_match is not None:
        DateTime = re.search(' CreationDate="(.*?)" ', line).group(1)
    else:
        DateTime = None
    return dict(
        CreationDate=DateTime,
        Id=handle_none(re.search(r' Id="(\d+)" ', line)),
        PostId=handle_none(re.search(' PostId="(\d+)" ', line)),
        VoteTypeId=handle_none(re.search(' VoteTypeId="(\d+)" ', line)),
    )

"""
Extract comment data
"""

def extract_comments_data(row):
    return dict(
        Id=handle_none2(row.get('id')),
        PostId=handle_none2(row.get('postid')),
        CreationDate=row.get('creationdate'),
        Score=row.get('score'),
        Text=row.get('text'),
        UserId=row.get('userid')
    )

"""
Extract tag data
"""

def extract_tags_data(row):
    return dict(
        Id=handle_none2(row.get('id')),
        ExcerptPostId=handle_none2(row.get('excerptpostid')),
        TagName=row.get('tagname'),
        WikiPostId=handle_none2(row.get('wikipostid')),
        Count=handle_none2(row.get('count'))
    )
