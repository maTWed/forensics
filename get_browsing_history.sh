#!/bin/bash
# Get Browsing history data using smb
# by: maTWed

if [ $# -eq 0 ]; then
    echo "[!] This script needs arguments!"
    echo "[!] ./getHistory.sh username ip "
    echo "[!] OR ..."
    echo "[!] ./getHistory.sh username ip <dir name in Profiles>"
elif [ $# -eq 2 ]; then
    usr=$1
    ip=$2

    # Change the localuser to correct user name
    mkdir -p /home/<localuser>/$usr

    # Change localuser to correct user name
    # Change username after -U and add the authentication password to a hidden folder called .pw
    # chmod 600 .pw
    # Change domain & username for authentication to the remote system
    smbclient //$ip/C$ -c 'get users\'$usr'\appdata\local\google\chrome\User Data\Default\History /home/<localuser>/'$usr'/History' -W domain -U username$(cat .pw) -p 445

    # We are listing the contents in the profiles directory so we can add the correct dir name as
    # the next argument which would give us the places.sqlite db
    # add correct domain name & username
    smbclient //$ip/C$ -c 'dir users\'$usr'\appdata\roaming\mozilla\firefox\profiles\' -W domain -U username%$(cat .pw) -p 445
elif [ $# -eq 3 ]; then
    usr=$1
    ip=$2
    dir=$3

    # Change localuser to correct user name
    # Change domain & username
    smbclient //$ip/C$ -c 'get users\'$usr'\appdata\roaming\mozilla\firefox\profiles\'$dir'\places.sqlite /home/<localuser>/'$usr'/places.sqlite' -W domain -U username%$(cat .pw) -p 445
fi
