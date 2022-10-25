import requests, time
from datetime import datetime


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    NORMAL = "\033[0;37;40m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

today = datetime.now()

channel_id = #SET THIS TO THE CHANNEL ID

header = {
    "authorization": "Discord key"
}


def send_message():
    a = input("What is your message? (cancel)\n")
    if a == "cancel":
        return

    requests.post(
        fr"https://discord.com/api/v9/channels/{channel_id}/messages",
        data={"content": a},
        headers=header,
    )


def check_messages(last):

    r = list(
        reversed(
            requests.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=header,
            ).json()
        )
    )

    for x in range(last, 0, -1):
        value = r[-x]
        dayyy = "Today"
        if (
            int(value["timestamp"].replace(".", "T").split("T")[0].split("-")[2])
            != today.day
        ):
            dayyy = value["timestamp"].replace(".", "T").split("T")[0]
        z = ""
        if len(value["attachments"]) > 0 and value["content"] == "":
            value["content"] = f'{value["attachments"][0]["url"]}\n'
        elif len(value["attachments"]) > 0:
            z += f'{value["attachments"][0]["url"]}\n'
        if "referenced_message" in value.keys():
            z += (
                "Replying to"
                + f' {value["referenced_message"]["author"]["username"]} - '
                + value["referenced_message"]["content"]
                + "\n"
            )
        elif len(value["mentions"]) > 0:
            for _ in value["mentions"]:
                z += f"@{_['username']} "
            z+='\n'
        timee = value["timestamp"].replace(".", "T").split("T")[1].split(":")

        if int(timee[0]) - 4 > 12:
            print(
                "\033[1;31;40m" + value["author"]["username"] + "\033[0;37;40m",
                f" - {dayyy} at {int(timee[0])-16}:{timee[1]} PM",
                "\n" + color.BOLD + value["content"] + color.NORMAL,
                "\n" + z,
            )
        else:
            print(
                "\033[1;31;40m" + value["author"]["username"] + "\033[0;37;40m",
                f" - {dayyy} at {int(timee[0])-4}:{timee[1]} AM",
                "\n" + color.BOLD + value["content"] + color.NORMAL,
                "\n" + z,
            )
    return list(reversed(r))


choice = input("send or check? (s/c)")
if choice == "s":
    send_message()
else:
    temp = check_messages(int(input("How many messages? (max is 50)")))
# MAIN
while True:
    choice = input("Check or send? (c/s)")
    if "s" in choice:
        send_message()
    else:
        if (
            temp
            != requests.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=header,
            ).json()
        ):
            temp = check_messages(int(input("How many? ")))
        else:
            print("nothing new")
