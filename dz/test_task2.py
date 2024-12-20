import yaml
from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestNegative:
    def test_nstep1(self,make_bad_arx, log_stat):
        assert checkout_negative("cd {}; 7z e arxbad.{} -o{} -y".format(data["folder_out"], data["type"],
                                                         data["folder_ext"]), "ERROR:"), "test2 FAIL"


    def test_nstep2(self, make_bad_arx, log_stat):
        assert checkout_negative("cd {}; 7z t arxbad.{}".format(data["folder_out"], data["type"]),
                                 "ERROR:"), "test2 FAIL"
