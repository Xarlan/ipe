
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

# This file contain class and method to
# - reconnaissance ip:port via masscan
# - reconnaissance ip:port via Shodan

import shodan
import time
import xml.etree.ElementTree as ET

import src.ipe_tools.ipe_common as ipe_tools

class IpeReconIpPort(ipe_tools.IpeTools):
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


    def import_masscan_xml(self, xml):
        """
        Import xml file from 'masscan' tool to IPE database
        :param xml:         xml file
        # :param fout:        name of output file
        # :param tout:        format of output: sort by ip-address or port
        :return:
        """

        try:
            masscan_tree = ET.parse(xml.name)

        except ET.ParseError:
            pass
            # click.secho("Wrong format of xml", fg='yellow')
            # exit(0)

        else:
            root_masscan = masscan_tree.getroot()
            if root_masscan.attrib['scanner'] != 'masscan':
                pass
                # click.secho("This xml isn't output of masscan tool", fg='yellow')
                # exit(0)

                                # dictionary, where will be stored result
            output_ip = {}      # sorted by IP:port
            output_port = {}    # sorted by tcp/udp_port: ip

            for tag_host in root_masscan:

                if len(tag_host.findall(".//")) == 4:

                    ip_addr = ""
                    port = ""
                    tcp_udp = ""

                    for item in tag_host.findall(".//"):

                        if item.tag == 'address':
                            ip_addr = item.attrib['addr']

                        elif item.tag == 'port':
                            port = item.attrib['portid']
                            tcp_udp = item.attrib['protocol']

                    if ip_addr in output_ip:
                        output_ip[ip_addr].append("{}/{}".format(tcp_udp, port))
                    else:
                        output_ip.update({ip_addr: ["{}/{}".format(tcp_udp, port)]})

                    key_port = "{}/{}".format(tcp_udp, port)

                    if key_port in output_port:
                        output_port[key_port].append(ip_addr)
                    else:
                        output_port.update({key_port: [ip_addr]})

            return output_ip, output_port

            # if fout is None:
            #     fout = xml.name.split('.')[0]

            # fout_ip = self.check_fout_name(fout + "_ip")
            # fout_port = self.check_fout_name(fout + "_port")

            # if tout == 'all' or tout == 'ip':

                # fid = open(fout_ip, 'w')

                # for ipv4 in sorted(output_ip.keys(), key=lambda ipv4: (int(ipv4.split(".")[0], 10),
                #                                                          int(ipv4.split(".")[1], 10),
                #                                                          int(ipv4.split(".")[2], 10),
                #                                                          int(ipv4.split(".")[3], 10))):


                    # for detail in output_ip[ipv4]:
                    #     fid.write('ip:{:<15} => {}\n'.format(ipv4, detail))

                # fid.close()

                # click.secho("\nResult stored (sorting by ip):")
                # click.secho(fout_ip, fg='green')

            # if humanr:
            #     fid_human = open(fout_ip + "_human", "w")
            #     for ipv4 in sorted(output_ip.keys(), key=lambda ipv4: (int(ipv4.split(".")[0], 10),
            #                                                              int(ipv4.split(".")[1], 10),
            #                                                              int(ipv4.split(".")[2], 10),
            #                                                              int(ipv4.split(".")[3], 10))):
            #
            #         fid_human.write("ip:{:<15} =>\n".format(ipv4))
            #
            #         for detail in output_ip[ipv4]:
            #             fid_human.write("{:<21} {}\n".format(" ", detail))
            #
            #     fid_human.close()
            #
            #     click.secho("\nResult stored (sorting by ip & human readble):")
            #     click.secho(fout_ip + "_human", fg='green')

            # if tout == 'all' or tout == 'port':
            #
            #     fid = open(fout_port, 'w')
            #
            #     for index in sorted(output_port.keys()):
            #         fid.write("{}\n".format(index))
            #
            #         for detail in output_port[index]:
            #             fid.write("{:>13}{}\n".format("ip:", detail))
            #
            #     fid.close()
            #
            #     click.secho("\nResult stored (sorting by port):")
            #     click.secho(fout_port, fg='green')
