import platform

from ptcs_bridge.bridge2 import Bridge2
from ptcs_bridge.master_controller_client import MasterControllerClient
from ptcs_bridge.train_client import TrainClient
from ptcs_bridge.train_simulator import TrainSimulator
from ptcs_bridge.wire_pole_client import WirePoleClient

if platform.system() == "Windows":
    ADDRESS_T0 = "e0:5a:1b:e2:7a:f2"
    ADDRESS_T1 = "94:b5:55:84:15:42"
    ADDRESS_T2 = "e0:5a:1b:e2:7b:1e"
    ADDRESS_T3 = "1c:9d:c2:66:84:32"
    ADDRESS_T4 = "24:4c:ab:f5:c6:3e"
    ADDRESS_WIRE_POLE = "24:62:AB:E3:67:9A"
    ADDRESS_MASTER_CONTROLLER = "9c:9c:1f:cf:ea:de"
elif platform.system() == "Darwin":
    ADDRESS_T0 = "00B55AE6-34AA-23C2-8C7B-8C11E6998E12"
    ADDRESS_T1 = "F2158243-18BB-D34C-88BC-F8F193CAD15E"
    ADDRESS_T2 = "EB57E065-90A0-B6D0-98BA-81096FA5765E"
    ADDRESS_T3 = "4AA3AAE5-A039-8484-013C-32AD94F50BE0"
    ADDRESS_T4 = "FC44FB3F-CF7D-084C-EA29-7AFD10C47A57"
    ADDRESS_WIRE_POLE = ""
    ADDRESS_MASTER_CONTROLLER = ""
else:
    raise Exception(f"{platform.system()} not supported")


def create_bridge() -> Bridge2:
    bridge = Bridge2()
    bridge.add_train(TrainSimulator("t0"))
    # bridge.add_train(TrainClient("t0", ADDRESS_T0))
    # bridge.add_train(TrainSimulator("t1"))
    bridge.add_train(TrainClient("t1", ADDRESS_T1))
    # bridge.add_train(TrainSimulator("t2"))
    bridge.add_train(TrainClient("t2", ADDRESS_T2))
    # bridge.add_train(TrainSimulator("t3"))
    bridge.add_train(TrainClient("t3", ADDRESS_T3))
    bridge.add_train(TrainSimulator("t4"))
    # bridge.add_train(TrainClient("t4", ADDRESS_T4))
    bridge.add_obstacle(WirePoleClient("obstacle_0", ADDRESS_WIRE_POLE))
    bridge.add_controller(MasterControllerClient("t3", ADDRESS_MASTER_CONTROLLER))
    return bridge
