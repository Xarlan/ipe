

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import ipaddress

class IpeTools(object):

    def __init__(self):
        pass

    def write_to_db(self):
        """
        Write data to database
        :return:
        """
        pass

    def read_from_db(self):
        """
        Read data from database
        :return:
        """
        pass

    @staticmethod
    def ipv4_sorted(unsorted_ip_list):
        """
        Sort input ip list by order
        :param unsorted_ip_list:    unsorted ip list
        :return:                    sorted ip list
        """
        if isinstance(unsorted_ip_list, list):
            raw_ip = []
            ipv4_hosts = []

            for item in unsorted_ip_list:
                try:
                    ipaddress.ip_address(item.split('\n')[0])

                except ValueError:
                    pass
                    # click.secho("It seems this is not an ipv4 address: ", nl=False)
                    # click.secho("{}".format(item), fg="yellow")

                else:
                    raw_ip.append(item.split('\n')[0])



            for ipv4 in sorted(raw_ip, key=lambda ipv4: (int(ipv4.split(".")[0], 10),
                                                          int(ipv4.split(".")[1], 10),
                                                          int(ipv4.split(".")[2], 10),
                                                          int(ipv4.split(".")[3], 10))):
                ipv4_hosts.append(ipv4)

            return ipv4_hosts

        else:
            pass
            # click.secho("This is not list of ipv4 address", fg="yellow")
            # exit(1)