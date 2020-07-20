
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import shodan
import time
import concurrent.futures

import sslyze
import sslyze.errors

import src.ipe_tools.ipe_common as ipe_tools

class IpeDiscover(ipe_tools.IpeTools):
    """
    This class realize method to check
    - check SSL/TLS settings using SSlyze library
      documentation: https://nabla-c0d3.github.io/sslyze/documentation/index.html
    - brute force hidden web directory using wfuzz
      documentation: https://github.com/xmendez/wfuzz
    """

    def __init__(self):
        ipe_tools.IpeTools.__init__()
        pass

    def check_ssl_tls(self, tls_servers, ports, num_thread=4):
        """
        Check SSL/TLS settings using sslyze library
        :param:     tls_servers - list of ip, to check SSL/TLS settings
        :param:     ports - list of ports
        :param:     num_thread - how many thread run in parallel mode
        :return:
        """
        # with open(fin.name, "r") as fid:
        #     tls_servers = fid.readlines()
        #
        # tls_servers = self.ipv4_sorted(tls_servers)
        #
        # if fout is None:
        #     fout = fin.name
        #
        # self.check_fout_name(fout)

        tls_to_check = []

        for host in tls_servers:

            for port in ports:
                tls_to_check.append("{}:{}".format(host, port))

        tls_result_ret = {}

        # with open(self.fout, "w") as fid:

        with concurrent.futures.ProcessPoolExecutor(num_thread) as executor:
            future_tls = {executor.submit(self._tls_server_check, tls_server) : tls_server for tls_server in tls_to_check}

            for future in concurrent.futures.as_completed(future_tls):

                result_tls_checking = future.result()

                if result_tls_checking["status"] == "error":
                    # click.secho("\n{:<20} -> ".format(result_tls_checking["result"]["host"]), nl=False)
                    # click.secho("{}".format(result_tls_checking["result"]["msg"]), fg="yellow")
                    # fid.write("ip:{:<20} => error:{}\n".format(result_tls_checking["result"]["host"],
                    #                                            result_tls_checking["result"]["msg"]))

                    tls_result_ret.update({result_tls_checking["result"]["host"] :
                                               {'status' : 'error',
                                                'msg'    : result_tls_checking["result"]["msg"]}})


                elif result_tls_checking["status"] == "ok":

                    # click.secho("\nResult of checking for: ")
                    # click.secho("{:<3} {}".format(" ", result_tls_checking["result"]["host"]), fg="cyan")

                    # for item in result_tls_checking["result"]["msg"].keys():

                        # fid.write("ip:{:<20} => {} : {}\n".format(result_tls_checking["result"]["host"],
                        #                                         item,
                        #                                         result_tls_checking["result"]["msg"][item]))

                        # color_msg = self._select_color_msg(item, result_tls_checking["result"]["msg"][item])

                        # click.secho("{:<5} {:<33}: ".format(" ", item), nl=False)
                        # click.secho("{}".format(result_tls_checking["result"]["msg"][item]), fg=color_msg)


                    tls_result_ret.update({result_tls_checking["result"]["host"] :
                                               {'status' : result_tls_checking["status"],
                                                'msg'    : result_tls_checking["result"]["msg"]}})


        # click.secho("\nResult check TLS server settings:")
        # click.secho(self.fout, fg="green")

        return tls_result_ret

    @staticmethod
    def _tls_server_check(tls_server):
        """
        Check TLS/SSL server settings using SSlyze library
        documentation: https://nabla-c0d3.github.io/sslyze/documentation/index.html
        :param tls_server:  'ip_address:port'
        :return:            dictionary: msg = {'type'   : "tlscheck",
                                               'status' : "error",
                                               'result' : {'host': "host:port",
                                                            'mag': e.error_message
                                                          },
                                               }
                            or
                            dictionary: msg = {'type'   : "tlscheck",
                                               'status' : "ok",
                                               'result': {'host': "host:port",
                                                          'msg': { "issue": result,
                                                                   "issue": result,
                                                                   ....
                                                                 }
                                                          },
                                               }
        """

        host = tls_server.split(':')[0]
        port = tls_server.split(':')[1]

        server_location = sslyze.ServerNetworkLocationViaDirectConnection.with_ip_address_lookup(host, port)

        try:
            # click.secho("\nTry to connect to ", nl=False)
            # click.secho("{}:{}".format(host, port), fg="green")
            server_info = sslyze.ServerConnectivityTester().perform(server_location)

        except sslyze.errors.ConnectionToServerFailed as e:

            msg = {'type': "tlscheck",
                   'status': "error",
                   'result': {'host': "{}:{}".format(host, port),
                              'msg': e.error_message},
                   }

            return msg

        else:

            tls_result = {}

            scanner = sslyze.Scanner()

            request_for_check = sslyze.ServerScanRequest(server_info=server_info,
                                                         scan_commands={sslyze.ScanCommand.HEARTBLEED,
                                                                        sslyze.ScanCommand.TLS_COMPRESSION,
                                                                        sslyze.ScanCommand.ROBOT,
                                                                        sslyze.ScanCommand.TLS_1_3_EARLY_DATA,
                                                                        sslyze.ScanCommand.TLS_FALLBACK_SCSV,
                                                                        sslyze.ScanCommand.OPENSSL_CCS_INJECTION,
                                                                        sslyze.ScanCommand.SESSION_RENEGOTIATION,
                                                                        sslyze.ScanCommand.SSL_2_0_CIPHER_SUITES,
                                                                        sslyze.ScanCommand.SSL_3_0_CIPHER_SUITES,
                                                                        sslyze.ScanCommand.TLS_1_0_CIPHER_SUITES,
                                                                        sslyze.ScanCommand.TLS_1_1_CIPHER_SUITES,
                                                                        sslyze.ScanCommand.TLS_1_2_CIPHER_SUITES,
                                                                        sslyze.ScanCommand.TLS_1_3_CIPHER_SUITES,
                                                                        sslyze.ScanCommand.CERTIFICATE_INFO}
                                                         )

            scanner.queue_scan(request_for_check)

            for scan_result in scanner.get_results():

                try:
                    res_ssl_v2 = scan_result.scan_commands_results[sslyze.ScanCommand.SSL_2_0_CIPHER_SUITES]

                except KeyError:
                    tls_result.update({"SSL v2": "don't know"})

                else:
                    tls_result.update({"SSL v2": res_ssl_v2.is_tls_protocol_version_supported})

                try:
                    res_ssl_v3 = scan_result.scan_commands_results[sslyze.ScanCommand.SSL_3_0_CIPHER_SUITES]
                except KeyError:
                    tls_result.update({"SSL v3": "don't know"})
                else:
                    tls_result.update({"SSL v3": res_ssl_v3.is_tls_protocol_version_supported})

                try:
                    res_tls_v10 = scan_result.scan_commands_results[sslyze.ScanCommand.TLS_1_0_CIPHER_SUITES]
                except KeyError:
                    tls_result.update({"TLS v1.0": "don't know"})
                else:
                    tls_result.update({"TLS v1.0": res_tls_v10.is_tls_protocol_version_supported})

                try:
                    res_tls_v11 = scan_result.scan_commands_results[sslyze.ScanCommand.TLS_1_1_CIPHER_SUITES]
                except KeyError:
                    tls_result.update({"TLS v1.1": "don't know"})
                else:
                    tls_result.update({"TLS v1.1": res_tls_v11.is_tls_protocol_version_supported})

                try:
                    res_tls_v12 = scan_result.scan_commands_results[sslyze.ScanCommand.TLS_1_2_CIPHER_SUITES]
                except KeyError:
                    tls_result.update({"TLS v1.2": "don't know"})
                else:
                    tls_result.update({"TLS v1.2": res_tls_v12.is_tls_protocol_version_supported})

                try:
                    res_tls_v13 = scan_result.scan_commands_results[sslyze.ScanCommand.TLS_1_3_CIPHER_SUITES]
                except KeyError:
                    tls_result.update({"TLS v1.3": "don't know"})
                else:
                    tls_result.update({"TLS v1.3": res_tls_v13.is_tls_protocol_version_supported})

                try:
                    res_cert_info = scan_result.scan_commands_results[sslyze.ScanCommand.CERTIFICATE_INFO]
                except KeyError:
                    tls_result.update({"cert info": "don't know"})
                else:
                    # print(res_cert_info)
                    for item in res_cert_info.certificate_deployments[0].received_certificate_chain:
                        # print(res_cert_info.certificate_deployments[0].received_certificate_chain)
                        print(item.not_valid_after)
                        print("*****")
                try:
                    res_robot = scan_result.scan_commands_results[sslyze.ScanCommand.ROBOT]

                except KeyError:
                    tls_result.update({"Robot vuln": "don't know"})
                    pass
                else:
                    tls_result.update({"Robot vuln": res_robot.robot_result.value})

                try:
                    res_heartbleed = scan_result.scan_commands_results[sslyze.ScanCommand.HEARTBLEED]
                except KeyError:
                    tls_result.update({"Heartbleed": "don't know"})
                else:
                    tls_result.update({"Heartbleed": res_heartbleed.is_vulnerable_to_heartbleed})

                try:
                    res_crime = scan_result.scan_commands_results[sslyze.ScanCommand.TLS_COMPRESSION]
                except KeyError:
                    tls_result.update({"Crime": "don't know"})
                else:
                    tls_result.update({"Crime": res_crime.supports_compression})

                try:
                    res_tls_v13_early_data = scan_result.scan_commands_results[
                        sslyze.ScanCommand.TLS_1_3_EARLY_DATA]
                except KeyError:
                    tls_result.update({"TLS v1.3 early data": "don't know"})
                else:
                    tls_result.update({"TLS v1.3 early data": res_tls_v13_early_data.supports_early_data})

                try:
                    res_downgrade = scan_result.scan_commands_results[sslyze.ScanCommand.TLS_FALLBACK_SCSV]
                except KeyError:
                    tls_result.update({"Downgrade prevention": "don't know"})
                else:
                    tls_result.update({"Downgrade prevention": res_downgrade.supports_fallback_scsv})

                try:
                    res_openssl_inj = scan_result.scan_commands_results[sslyze.ScanCommand.OPENSSL_CCS_INJECTION]
                except KeyError:
                    tls_result.update({"OpenSSL CCS Injection": "don't know"})
                else:
                    tls_result.update({"OpenSSL CCS Injection": res_openssl_inj.is_vulnerable_to_ccs_injection})

                try:
                    res_insecure_reneg = scan_result.scan_commands_results[sslyze.ScanCommand.SESSION_RENEGOTIATION]
                except KeyError:
                    tls_result.update({"Secure Renegotiation Server side": "don't know"})
                else:
                    tls_result.update(
                        {"Secure Renegotiation Server side": res_insecure_reneg.supports_secure_renegotiation})

            msg = {'type': "tlscheck",
                   'status': "ok",
                   'result': {'host': "{}:{}".format(host, port),
                              'msg': tls_result},
                   }

            return msg

    def discover_hidden_web_path(self):
        pass