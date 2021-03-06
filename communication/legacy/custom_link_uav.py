#
# This file is part of DroneBridgeLib: https://github.com/seeul8er/DroneBridge
#
#   Copyright 2018 Wolfgang Christl
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import time

from legacy.DroneBridge_Protocol import DBProtocol, DBDir


def main():
    """
    Example of how to use the DroneBridgeLib python lib to send & receive your custom data.
     -- Run using root privileges! --
     -- set interface_drone_comm to your wifi adapter! --

    Run on UAV using the DroneBridgeLib image. If used with EZ-WBC image you need to install some extra packages for
    python3. If not executed on DroneBridgeLib/WBC rpi-image the wifi adapters must be in monitor mode and patched with
    patches provided by EZ-WBC project.
    :return:
    """
    udp_port_rx = 5010  # relict - set to some free port - not used
    ip_rx = "192.168.2.2"  # relict - set to something - not used
    udp_port_smartphone = udp_port_rx  # not used - choose any

    comm_direction = DBDir.DB_TO_GND  # On UAV we want to send stuff to ground station (do not change)
    interface_drone_comm = "000ee8dcaa2c"  # Interface name of your wifi adapter (with DroneBridgeLib & WBC it is the MAC)
    mode = "m"  # not used - tell him to use long range link and not wifi - wifi will be implemented in a later stage
    communication_id = 201  # Must be same on ground and UAV - identifies a link - choose a number between 0-255

    # Channel/packet identifier - must be the same on ground & UAV - ports 1-7 are already assigned
    # - choose number from 8-255 in byte/hex format
    dronebridge_port = b'\x08'
    tag = 'MY_CUST_LINK: '  # Gets written in front of every message produced by DBProtocol class

    db_protocol = DBProtocol(udp_port_rx, ip_rx, udp_port_smartphone, comm_direction, interface_drone_comm, mode,
                             communication_id, dronebridge_port, tag=tag)
    db_lr_socket = db_protocol.getcommsocket()  # get the configured long range socket

    while True:
        # receive a packet, parse it, get payload (pure bytes)
        my_payload = db_protocol.parse_packet(bytearray(db_lr_socket.recv(2048)))
        # alternative: my_payload = db_protocol.receive_from_db(custom_timeout=2)
        print("Got: " + str(my_payload) + " from the ground station!")

        # Send something back to your custom port:
        my_new_payload = b'\x01\x01\x05\x07\x07\x08\x03\x02\x01\x01\x01\x01\x05\x01\x02\x08'
        db_protocol.sendto_groundstation(my_new_payload, dronebridge_port)
        print("Sent: " + str(my_new_payload) + " back the ground station!")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
