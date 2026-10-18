#!/bin/bash
set -o pipefail

/usr/bin/journalctl -u ssh.service --since today --no-pager -o short-iso | /usr/bin/grep -E 'Failed password|Accepted password' > /home/socadmin/soc-dashboard/ssh-events.log.tmp
result=$?

if [ "$result" -eq 0 ] || [ "$result" -eq 1 ]; then
    /usr/bin/mv /home/socadmin/soc-dashboard/ssh-events.log.tmp /home/socadmin/soc-dashboard/ssh-events.log
else
    /usr/bin/rm -f /home/socadmin/soc-dashboard/ssh-events.log.tmp
    exit "$result"
fi
