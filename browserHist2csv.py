#!/usr/bin/python
# Browsing History to csv
# by:maTWed
# updated: 4/5/2022
# Created for internal use do to all the browsing history investigation
# Instructions: Copy Chrome & Firefox browsing DB to the directory of this script
# Or use 'get_browsing_history.sh' to collect the history and place them in this script's directory.

# TODO: Creat a function that connects to the smb share and copies the
#       browsing files to local machine then gathers the data.

import os, time, datetime, operator, string, sqlite3, csv, argparse


def firefox_history():

    if not os.path.exists(fox_db):
        print("[-] Firefox DB not found!")
    else:
        db = sqlite3.connect(fox_db)
        cursor = db.cursor()
        cursor.execute("SELECT * from moz_places")
        url_data = (cursor.fetchall())

        db = sqlite3.connect(fox_db)
        cursor = db.cursor()
        cursor.execute("SELECT * from moz_historyvisits")
        browsing_data = (cursor.fetchall())

        for record in browsing_data:
            url_reference = record[2]
            for saved_url in url_data:
                if saved_url[0] == url_reference:
                    visit_url = saved_url[1]

            visit_time = str(datetime.datetime(1970,1,1)
                            + datetime.timedelta(microseconds=record[3], hours=-4))
            visit_time = visit_time[:-7]

            visit_line = visit_time + "," + "Website visited (Firefox)" + "," \
                + "," + visit_url + "," + username + "," + visit_time + "," \
                + "Firefox history" + "," + "\places.sqlite" + "\n"
            timeline_csv.write(visit_line)
        print("[+] FIREFOX HISTORY ADDED TO THE TIMELINE. \n")


def chrome_history():

    if not os.path.exists(chrome_db):
        print("[-] Chrome DB not found!")
    else:
        db = sqlite3.connect(chrome_db)
        cursor = db.cursor()
        cursor.execute("SELECT * from urls")
        browsing_data = (cursor.fetchall())
        for record in browsing_data:
            visit_time = str(datetime.datetime(1601,1,1) \
                            + datetime.timedelta(microseconds=record[5]))
            if visit_time[:4] == "1601":
                pass
            else:
                visit_time = str(datetime.datetime.strptime(
                    visit_time, "%Y-%m-%d %H:%M:%S.%f"))
                visit_time = visit_time[:-7]
                visit_title = record[2]
                visit_title = visit_title.replace(",", "")
                visit_url = record[1]
                visit_line = visit_time + "," + "Website visited (Chrome)" + "," \
                        + visit_title + "," + visit_url + "," + username + "," \
                        + visit_time + "," + "Google Chrome history" + "," \
                        + "History" + "\n"
                timeline_csv.write(visit_line)
        print("[+] CHROME HISTORY ADDED TO THE TIMELINE.\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Open Firefox & Chrome browsing history databases and create a csv with the data')
    parser.add_argument('-u', '--username', type=str, metavar='', help='Username of the data owner')
    args = parser.parse_args()

    # Variables
    username = args.username
    dir = os.getcwd()
    chrome_db = dir + r"/History"
    fox_db = dir + r"/places.sqlite"

    timeline_csv = open("timeline.csv", "a")
    
    # Function Calls
    firefox_history()
    chrome_history()

    timeline_csv.close()

    # creating the csv & adding column headers
    with open("timeline.csv") as f:
        timeline_csv = csv.reader(f, delimiter=",")
        sorted_timeline = sorted(timeline_csv, key=operator.itemgetter(0),
                                 reverse=True)

    with open("timeline.csv", "w") as f:
        fileWriter = csv.writer(f, delimiter=",")
        header_row = "Artefact Timestamp", "Action", "Filename", "Full Path", \
            "User", "File Accessed", "Source", "Source File"
        fileWriter.writerow(header_row)
        for row in sorted_timeline:
            fileWriter.writerow(row)
