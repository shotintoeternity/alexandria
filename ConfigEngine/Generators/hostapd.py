from ConfigEngine.Generators import engine
from ConfigEngine import toBool,writeLines

@engine.assertConfig("service.dnsmasq",(
        "enable",
        "interface",
        "channel",
        "ssid",
        "wpa",
        "psk"
        ))
@engine.generator("hostapd configuration")
def hostapd(io):
    io.write("# This file is auto generated by a script\n")

    # get the hostapd settings.
    network = engine.getSection("service.hostapd")
     
    # the first thing we write to the hostapd config is the details on interface and specific
    # details. 
    if toBool(network["enable"]) == False:
       return
    writeLines(io, [
        "interface={0}".format(network['interface']),
        "hw_mode=g",
        "channel={0}".format(network['channel']),
        "ssid={0}".format(network["ssid"]),
        ])
    if (toBool(network['no_broadcast'])):
        writeLines(["ignore_broadcast_ssid=2"],io)
    if( toBool( network["wpa"]) ):
        # Enable WPA encryption
        writeLines(io, [
            "auth_algs=1",
            "wpa=2",
            "wpa_key_mgmt=WPA-PSK",
            "wpa_pairwise=CCMP",
            "rsn_pairwise=CCMP",
            "wpa_passphrase={0}".format(network["psk"])
            ])
    # end hostapd configuration generator
