# Media Router

Media Router provides on-demand or streaming media contents routing servcie to end users.

  - Collect status reports from edges. Which may include workload (cpu usage, memory useage, network bandwidth usage, etc), contents (segments cached) and healthy status.
  - Store data collected.
  - Accep request from client, response appropriate edge address.

## Status Report Example
    {
        'id1234': {
            'name': 'name1',
            'status': 'OK',
            'workload': {
                'bandwidth': 80,
                'cpu': 70,
                'memory': 50
            }
            'contents': (
                'contentId1',
                'contentId2',
            )
            health: {
                'failRate': 0
            }
        }
    }