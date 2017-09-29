#!/usr/bin/python

import sys, os, copy

"""
GROUPS

Defines constants for CONF (the name of the conference), and for the names of each group.
All other groups will be named by joining the name with CONF: <CONF>/<NAME>

Example:

    CONF = 'my.conference/2017'
    PROGRAM_CHAIRS = 'Program_Chairs'

    --> my.conference/2017/Program_Chairs

"""

CONF = "ICLR.cc/2018/Conference"
ADMIN = CONF + '/Admin'
PROGRAM_CHAIRS = CONF + '/Program_Chairs'

AUTHORS = CONF + '/Authors'

AREA_CHAIRS = CONF + '/Area_Chairs'
AREA_CHAIRS_INVITED = AREA_CHAIRS + '/Invited'
AREA_CHAIRS_DECLINED = AREA_CHAIRS + '/Declined'
AREA_CHAIRS_EMAILED = AREA_CHAIRS + '/Emailed'

REVIEWERS = CONF + '/Reviewers'
REVIEWERS_INVITED = REVIEWERS + '/Invited'
REVIEWERS_DECLINED = REVIEWERS + '/Declined'
REVIEWERS_EMAILED = REVIEWERS + '/Emailed'

REVIEWERS_PLUS = REVIEWERS + '_and_Higher'
AREA_CHAIRS_PLUS = AREA_CHAIRS + '_and_Higher'

DUE_TIMESTAMP = 1509138000000 # 17:00:00 EST on October 27, 2017
WEBPATH = os.path.join(os.path.dirname(__file__), '../webfield/conferenceWebfield_tabs.js')

"""
INVITATIONS

Defines constants for various invitations.
The full name of an invitation will be generated by joining the name with CONF by "/-/": <CONF>/-/<INVITATION_NAME>

Example:

    CONF = 'my.conference/2017'
    SUBMISSION = 'Submission'

    --> my.conference/2017/-/Submission

PARAMETERS

Dictionaries that represent argument combinations defining Group and Invitation permissions.

Example:

    restricted = {
        'readers': [CONF],
        'writers': [CONF],
        'signatories': [CONF],
    }

    The "restricted" configuration above will only allow the CONF group to read, write, and sign
    for the newly created Group that uses it.
"""

group_params = {
    'readers': [CONF, PROGRAM_CHAIRS],
    'writers': [CONF],
    'signatories': [CONF],
    'signatures': [CONF]
}

public_group_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'signatories': [CONF],
    'signatures': [CONF]
}

program_chairs_params = {
    'readers': [CONF, PROGRAM_CHAIRS],
    'writers': [CONF],
    'signatories': [CONF, PROGRAM_CHAIRS],
    'signatures': [CONF]
}

area_chairs_params = {
    'readers': [CONF, PROGRAM_CHAIRS, AREA_CHAIRS],
    'writers': [CONF],
    'signatories': [CONF],
    'signatures': [CONF],
    'web': os.path.join(os.path.dirname(__file__), '../webfield/areachairWebfield.html'),
}

reviewer_group_params = {
    'readers': [CONF, AREA_CHAIRS, PROGRAM_CHAIRS],
    'writers': [CONF],
    'signatories': [CONF],
    'signatures': [CONF]
}


"""
/-/Submission

This is the invitation that users submit to. These are un-blinded notes. The process
function generates a /-/Blind_Submission note.

"""
SUBMISSION = CONF + '/-/Submission'

submission_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': ['~'],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/submissionProcess.js'),
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [CONF, PROGRAM_CHAIRS, '{content.authorids}', '{signatures}']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values': []
        },
        'content':{
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names. Please provide real names; identities will be anonymized.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile. Please provide real emails; identities will be anonymized.',
                'order': 3,
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 7,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 8,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf',
                'order': 9,
                'value-regex': 'upload',
                'required':True
            }
        }
    }
}


"""
/-/Blind_Submission

This is the invitation for the blinded version of the submissions.
Each of these notes have an "original" field which points to the non-anonymous
version of the note. They are generated by the /-/Submission process function.

"""
BLIND_SUBMISSION = CONF + '/-/Blind_Submission'

blind_submission_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [CONF],
    'signatures': [CONF],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': [CONF]
        },
        'writers': {
            'values': [CONF]
        },
        'content': {
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 1,
                'values-regex': '.*',
                'required': False
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 2,
                'values-regex': '.*',
                'required': False
            }
        }
    }
}


"""
/-/Public_Comment

This is the invitation for non-anonymous comments made by the public.
Users sign using their tilde (~) IDs.
"""
PUBLIC_COMMENT = CONF + '/-/Public_Comment'

public_comment_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [],
    'noninvitees': [REVIEWERS, AREA_CHAIRS, AUTHORS, PROGRAM_CHAIRS],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/commentProcess.js'),
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'value-dropdown': ['everyone', REVIEWERS_PLUS, AREA_CHAIRS_PLUS, PROGRAM_CHAIRS]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*|\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '~.*|\\(anonymous\\)'
        },
        'content':{
            'title': {
                'order': 0,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your comment.',
                'required': True
            },
            'comment': {
                'order': 1,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Your comment or reply.',
                'required': True
            }
        }
    }
}


"""
/-/Paper[0-9]+/Official_Comment

This is the invitation for comments by users in official ICLR reviewing
roles (reviewers, area chairs, or program chairs).

"""

official_comment_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/commentProcess.js'),
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'value-dropdown': ['everyone', REVIEWERS_PLUS, AREA_CHAIRS_PLUS, PROGRAM_CHAIRS]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': ''
        },
        'writers': {
            'values-regex': ''
        },
        'content':{
            'title': {
                'order': 0,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your comment.',
                'required': True
            },
            'comment': {
                'order': 1,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Your comment or reply.',
                'required': True
            }
        }
    }
}

"""
/-/Paper[0-9]+/Official_Review

This is the invitation for official reviews left by invited ICLR 2018 reviewers.
It gets posted with toggle-invitations.py, which also assigns it an ID based on paper number.
"""

official_review_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/officialReviewProcess.js'),
    'duedate': 1511845199000, # 23:59:59 EST on November 27, 2017
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [AREA_CHAIRS_PLUS]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': ''
        },
        'writers': {
            'values-regex': ''
        },
        'content':{
            'title': {
                'order': 1,
                'value-regex': '.{0,500}',
                'description': 'Brief summary of your review.',
                'required': True
            },
            'review': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,200000}',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
                'required': True
            },
            'rating': {
                'order': 3,
                'value-dropdown': [
                    '10: Top 5% of accepted papers, seminal paper',
                    '9: Top 15% of accepted papers, strong accept',
                    '8: Top 50% of accepted papers, clear accept',
                    '7: Good paper, accept',
                    '6: Marginally above acceptance threshold',
                    '5: Marginally below acceptance threshold',
                    '4: Ok but not good enough - rejection',
                    '3: Clear rejection',
                    '2: Strong rejection',
                    '1: Trivial or wrong'
                ],
                'required': True
            },
            'confidence': {
                'order': 4,
                'value-radio': [
                    '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
                    '4: The reviewer is confident but not absolutely certain that the evaluation is correct',
                    '3: The reviewer is fairly confident that the evaluation is correct',
                    '2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper',
                    '1: The reviewer\'s evaluation is an educated guess'
                ],
                'required': True
            }
        }
    }
}

"""
/-/Paper[0-9]+/Meta_Review

This is the invitation for meta reviews left by invited ICLR 2018 area chairs.
It gets posted with toggle-invitations.py, which also assigns it an ID based on paper number.
"""

meta_review_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [],
    'signatures': [CONF],
    'process': os.path.join(os.path.dirname(__file__), '../process/metaReviewProcess.js'),
    'duedate': 1517270399000, # 23:59:59 EST on January 1, 2018
    'reply': {
        'forum': None,
        'replyto': None,
        'writers': {
            'values-regex': CONF + '.*'
        },
        'signatures': {
            'values-regex': CONF + '.*'
        },
        'readers': {
            'values': [AREA_CHAIRS_PLUS],
            'description': 'The users who will be allowed to read the above content.'
        },
        'content': {
            'title': {
                'order': 1,
                'value-regex': '.{1,500}',
                'description': 'Brief summary of your review.',
                'required': True
            },
            'metareview': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,5000}',
                'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
                'required': True
            },
            'recommendation': {
                'order': 3,
                'value-dropdown': [
                    'Accept (Oral)',
                    'Accept (Poster)',
                    'Reject',
                    'Invite to Workshop Track'
                ],
                'required': True
            },
            'confidence': {
                'order': 4,
                'value-radio': [
                    '5: The area chair is absolutely certain',
                    '4: The area chair is confident but not absolutely certain',
                    '3: The area chair is somewhat confident',
                    '2: The area chair is not sure',
                    '1: The area chair\'s evaluation is an educated guess'
                ],
                'required': True
            }
        }
    }
};

"""
/-/Paper[0-9]+/Withdraw_Paper

This is the invitation for paper withdrawals.
"""

withdraw_paper_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [],
    'signatures': [CONF],
    'reply': {
        'referent': None, # replaced in invitations.py
        'forum': None, # replaced in invitations.py
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values-regex': '~.*'
        },
        'content':{
            'withdrawal': {
                'description': 'Confirm your withdrawal',
                'order': 1,
                'value-radio': ['Confirmed'],
                'required':True
            }
        }
    }
}

"""
/-/Paper[0-9]+/Add_Revision

This is the invitation for paper revisions
"""

add_revision_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [], # set during submission process function; replaced in invitations.py
    'signatures': [CONF],
    'reply': {
        'forum': None,
        'referent': None,
        'signatures': submission_params['reply']['signatures'],
        'writers': submission_params['reply']['writers'],
        'readers': submission_params['reply']['readers'],
        'content': submission_params['reply']['content']
    }
}


"""
/-/Add_Bid

This is the invitation to bid on papers.

There is a special interface to view bids, defined by the webfield.

"""
ADD_BID = CONF + '/-/Add_Bid'

add_bid_params = {
    'readers': [CONF, PROGRAM_CHAIRS, AREA_CHAIRS, REVIEWERS],
    'writers': [CONF],
    'invitees': [],
    'signatures': [CONF],
    'duedate': 1511845199000, # 23:59:59 EST on November 27, 2017
    'web': os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/bidWebfield.html')),
    'taskCompletionCount': 50,
    'multiReply': False,
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': BLIND_SUBMISSION,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [CONF, '{signatures}']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'content': {
            'tag': {
                'description': 'Bid description',
                'order': 1,
                'value-dropdown': ['I want to review',
                    'I can review',
                    'I can probably review but am not an expert',
                    'I cannot review',
                    'No bid'],
                'required':True
            }
        }
    }
}


"""
/-/Paper_Metadata

This is the invitation to post paper metadata, used in paper-reviewer matching.

"""
METADATA = CONF + '/-/Paper_Metadata'

metadata_params = {
    'readers': [CONF],
    'writers': [CONF],
    'invitees': [CONF],
    'signatures': [CONF],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [CONF]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': CONF
        },
        'writers': {
            'values-regex': CONF
        },
        'content': {}
    }
}



"""
/-/Paper_Assignments

This is the invitation to post assignment notes, used in the paper-reviewer
matching system.

"""
ASSIGNMENTS = CONF + '/-/Paper_Assignments'

assignments_params = {
    'writers': [CONF],
    'readers': [CONF],
    'invitees': [CONF],
    'signatures': [CONF],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [CONF]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': CONF
        },
        'writers': {
            'values-regex': CONF
        }
    }
}


"""
/-/Recruit_Area_Chairs

This is the invitation to recruit area chairs.
"""
RECRUIT_AREA_CHAIRS = CONF + '/-/Recruit_Area_Chairs'

recruit_area_chairs_params = {
    'readers': [CONF],
    'writers': [CONF],
    'invitees': [AREA_CHAIRS_INVITED],
    'signatures': [CONF],
    'process': os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/recruitAreachairsProcess.js')),
    'web': os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/recruitAreachairsWebfield.html')),
    'reply': {
        'content': {
            'username': {
                'description': 'OpenReview username (e.g. ~Alan_Turing1)',
                'order': 1,
                'value-regex': '~.*'
            },
            'key': {
                'description': 'Email key hash',
                'order': 2,
                'value-regex': '.{0,100}'
            },
            'response': {
                'description': 'Invitation response',
                'order': 3,
                'value-radio': ['Yes', 'No']
            }
        },
        'readers': {
            'values': [CONF]
        },
        'signatures': {
            'values-regex': '\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '\\(anonymous\\)'
        }
    }
}



"""
/-/Recruit_Reviewers

This is the invitation to recruit reviewers.
"""
RECRUIT_REVIEWERS = CONF + '/-/Recruit_Reviewers'

recruit_reviewers_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': [REVIEWERS_INVITED],
    'signatures': [CONF],
    'process': os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/recruitReviewersProcess.js')),
    'web': os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/recruitReviewersWebfield.html')),
    'reply': {
        'content': {
            'username': {
                'description': 'OpenReview username or email address (e.g. ~Alan_Turing1)',
                'order': 1,
                'value-regex': '.*'
            },
            'key': {
                'description': 'Email key hash',
                'order': 2,
                'value-regex': '.{0,100}'
            },
            'response': {
                'description': 'Invitation response',
                'order': 3,
                'value-radio': ['Yes', 'No']
            }
        },
        'readers': {
            'values': [CONF]
        },
        'signatures': {
            'values-regex': '\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '\\(anonymous\\)'
        }
    }
}

