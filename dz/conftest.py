import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    return checkout("mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")

@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"]), "")
@pytest.fixture()
def make_files():
    list_off_files = [ ]
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"]), ""):
            list_off_files.append(filename)
    return list_off_files

@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/arxbad -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
    checkout("truncate -s 1 {}/arxbad.{}".format(data["folder_out"], data["type"]), "Everything is Ok")
    yield "arxbad"
    checkout("rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")

@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                            data["count"], data["bs"], stat), "")

@pytest.fixture()
def log_stat(make_files):
    count_files = len(make_files)
    size_files = data["bs"]
    stat_file_path = 'stat.txt'
    #yield

    #with open('/proc/loadavg', 'r') as loadavg_file:
       # loadavg_stats = loadavg_file.read().strip()
    current_time = datetime.now().strftime("%H-%M-%S-%f")
    log_entry = f'{current_time=}, {count_files=}, {size_files=}, {loadavg_stats=}\n'

    with open(stat_file_path, 'a') as stat_file:
        stat_file.write(log_entry)