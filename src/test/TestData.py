def roundData_startGroup():
    return {
            'roundId' : '000001',
            'QUEUED' : [
                {'groupId': 'group001',
                'roomId' : 'abcroomd',
                'judgesIds': ['aaa', 'bbb'],
                'competitorIds': ['c1', 'c2','c3'],
                'judgeingresult': {
                    
                }}
                ],
            'ASSIGNED': [
                ],
            'STARTED' : [],
            'COMPLETED': []
            }


def roundData_startCompetition():
    return {
            'roundId' : '000001',
            'QUEUED' : [],
            'ASSIGNED': [
                {'groupId': 'group001',
                'roomId' : 'abcroomd',
                'judgesIds': ['aaa', 'bbb'],
                'competitorIds': ['c1', 'c2','c3'],
                'judgeingresult': {
                    
                }}
                ],
            'STARTED' : [],
            'COMPLETED': []
            }

def roundData_collectResult():
    return {
            'roundId' : '000001',
            'QUEUED' : [],
            'ASSIGNED': [],
            'STARTED' : [
                {'groupId': 'group001',
                'roomId' : 'abcroomd',
                'judgesIds': ['aaa', 'bbb'],
                'competitorIds': ['c1', 'c2','c3'],
                'judgeingresult': {}
                }
                ],
            'COMPLETED': []
            }
def groupData():
    return {
                'groupId': 'group001',
                'roomId' : 'abcroomd',
                'judgesIds': ['aaa', 'bbb'],
                'competitorIds': ['c1', 'c2','c3'],
                'judgeingresult': {}
            }
