import datetime
import os
import sys
import time

import yaml
from colorama import Back
from colorama import Fore
from colorama import Style


def generate_path(s):
    if s[-1] == "/" or s[-1] == "\\":
        sp = s[0:-1]
    else:
        sp = s[:]
    return sp.replace("/", "-").replace(":", "-").replace("\\", "-")


def delta(freq):
    if freq == "hourly":
        return datetime.timedelta(hours=1)
    elif freq == "semidaily":
        return datetime.timedelta(hours=12)
    elif freq == "daily":
        return datetime.timedelta(days=1)


def waitstatus_to_exitcode(status):
    if os.WIFSIGNALED(status):
        returncode = -os.WTERMSIG(status)
    elif os.WIFEXITED(status):
        returncode = os.WEXITSTATUS(status)
    elif os.WIFSTOPPED(status):
        returncode = -os.WSTOPSIG(status)
    else:
        raise Exception("... put your favorite error message here ...")
    return returncode


def main():

    d = yaml.safe_load(open(sys.argv[1]).read())
    config = d["config"]
    print(config)
    backup_data = d["data"]

    for backup_item in backup_data:
        backup_item["next_run"] = []
        for freq in backup_item["frequency"]:
            backup_item["next_run"].append(datetime.datetime.now())

    while True:
        for backup_item in backup_data:
            norm_loc = generate_path(backup_item["location"])
            for i, (freq, nxt) in enumerate(
                zip(backup_item["frequency"], backup_item["next_run"]),
            ):
                if datetime.datetime.now() >= nxt:
                    dest_path = os.path.join(config["backup_location"], norm_loc, freq)
                    os.makedirs(dest_path, exist_ok=True)
                    cmd = f"rsync -avrP {backup_item['location']}/* {dest_path}/"
                    print(Back.WHITE + Fore.BLACK + f"->{cmd}", end="")
                    print(Style.RESET_ALL)
                    status = os.system(cmd)
                    if waitstatus_to_exitcode(status) == 0:
                        print(Fore.GREEN + "->done (successfully)", end="")
                        print(Style.RESET_ALL)
                        backup_item["next_run"][i] = datetime.datetime.now() + delta(
                            freq,
                        )
                    else:
                        print(
                            Fore.RED
                            + "->problem (see above), will try again in 10 minutes",
                            end="",
                        )
                        print(Style.RESET_ALL)
                        backup_item["next_run"][
                            i
                        ] = datetime.datetime.now() + datetime.timedelta(minutes=10)

        time.sleep(300)
    return 0


if __name__ == "__main__":
    sys.exit(main())
