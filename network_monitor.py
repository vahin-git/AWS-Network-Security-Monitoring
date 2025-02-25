import pyshark
import logging
import yagmail

# Email Configuration
SENDER_EMAIL = #enter your email 
APP_PASSWORD = #enter your app password
RECEIVER_EMAIL = #enter receiver email

# Set up email sender
yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)

# Configure logging
logging.basicConfig(filename="network_alerts.log", level=logging.INFO, format="%(asctime)s - %(message)s", force=True)

interface = "ens5"
print(f"Monitoring network traffic on {interface}...\n")

capture = pyshark.LiveCapture(interface=interface)

for packet in capture.sniff_continuously(packet_count=20):
    try:
        if "TCP" in packet:
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
            log_message = f"📡 Packet: {src_ip}:{src_port} → {dst_ip}:{dst_port}"
            print(log_message)
            logging.info(log_message)

            # Detect SSH brute-force attack
            if dst_port == "22":
                alert_message = "🚨 Warning: Multiple SSH connection attempts detected!"
                print(alert_message)
                logging.warning(alert_message)

                # Send an email alert
                yag.send(to=RECEIVER_EMAIL, subject="🚨 Security Alert: SSH Attack Detected", contents=alert_message)

    except AttributeError:
        continue  # Ignore packets without TCP headers

