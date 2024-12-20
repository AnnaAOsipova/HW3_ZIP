import yaml
from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestNegative:
    def test_nstep1(self):
        assert checkout_negative("cd {}; 7z t arxbad.{}".format(data["folder_out"],
                                                                data["type"]), "ERROR:"), "test2 FAIL"