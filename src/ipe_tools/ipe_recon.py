
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import shodan
import time

import src.ipe_tools.ipe_common as ipe_tools

class IpeRecon(ipe_tools.IpeTools):
    """
    This class describe the functionality:
    - scan ip address using masscan
    - import external xml file, generated masscan to ipe database
    - scan ip address using Shoda
    """

    def __init__(self):
        ipe_tools.IpeTools.__init__()
        pass

    def scan_masscan(self):
        """
        Make scan/recon ip address using masscan tool
        :return:  [tmp] need check
        """
        pass

    def scan_shodan(self, raw_list_ip=None, api_key=None):
        """
        Make scan/recon ip address using Shodan
        :param api_key:         Shodan API-KEY
        :param raw_list_ip:     list of raw ip address
        :return:
        """
        output_ip = {'No info' : []}
        output_port = {}

        api_shodan = shodan.Shodan(api_key)


        # if fout is None:
        #     fout = fin.name

        # fout_ip = self.check_fout_name(fout)  + "_ip"
        # fout_port = self.check_fout_name(fout)  + "_port"

        # fid = open(fin.name, "r")
        # ipv4_hosts = fid.readlines()
        # fid.close()

        ipv4_hosts = self.ipv4_sorted(raw_list_ip)

        # fid_ip = open(fout_ip, "w")
        # fid_port = open(fout_port, "w")

        # with click.progressbar(ipv4_hosts, label="Completed") as hosts:

        # for host in hosts:
        for host in ipv4_hosts:

            try:
                info = api_shodan.host(host)

            except shodan.exception.APIError as e:

                if e.value == "Invalid API key":
                    pass
                    # click.secho("Invalid API key: ", nl=False)
                    # click.secho("{}".format(api_key), fg="yellow")

                    # fid_ip.close()
                    # fid_port.close()

                    # exit(0)

                # click.secho("\nip:{:<15} : {}".format(host, e.value))
                # sys.stdout.write("\rip:{:<15} : {}".format(host, e.value))

                output_ip['No info'].append(host)

                # if tout == 'all' or tout == 'ip':
                #     fid_ip.write("ip:{:<15} => {}\n".format(host, "no info"))

            else:

                # click.secho("\nip:", nl=False)
                # click.secho("{}".format(host), fg="cyan")

                for index in info['data']:
                    # click.secho("{:>21}/{}".format(index['transport'], index['port']))

                    # if tout == 'all' or tout == 'ip':
                    #     fid_ip.write("ip:{:<15} => {}/{}\n".format(host, index['port'], index['transport']))

                    port_key = "{}/{}".format(index['port'], index['transport'])

                    # if port_key in output_port:
                    #     output_port[port_key].append(host)
                    # else:
                    #     output_port.update({port_key: [host]})

                    if host in output_ip:
                        output_ip[host].append(port_key)
                    else:
                        output_ip.update({host : [port_key]})

            # This delay need for correct work with Shodan.
            # If send request more faster then 2 second
            # Shodan.io can't answer
            time.sleep(2)

        # click.secho("\nResult search engine 'Shodan' (sorted by ip):")
        # click.secho(fout_ip, fg="green")

        # for index in sorted(output_port.keys()):
        #
        #     click.secho('{}'.format(index))
        #     fid_port.write('{}\n'.format(index))
        #
        #     for ip in output_port[index]:
        #         print('{:>12} {}'.format(' ', ip))
        #         fid_port.write('{:>12} {}\n'.format(' ', ip))

        # fid_ip.close()
        # fid_port.close()

        # click.secho("\nResult search engine 'Shodan' (sorted by port):")
        # click.secho(fout_port, fg="green")

        return output_ip

