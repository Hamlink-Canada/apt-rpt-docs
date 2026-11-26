"""Run the three prebuilt :review images against an ephemeral, isolated Kafka broker.

Requires Docker and local images built as documented in each service README.
No host ports, external services, persisted credentials, or registry writes are used.
"""

import secrets
import subprocess
import tempfile
import time
from pathlib import Path


def docker(*args, check=True):
    return subprocess.run(
        ["docker", *args], check=check, capture_output=True, text=True
    )


def main():
    suffix = secrets.token_hex(4)
    network = f"rpt-integration-{suffix}"
    names = []
    password = secrets.token_urlsafe(24)
    with tempfile.TemporaryDirectory(prefix="rpt-integration-") as temporary:
        directory = Path(temporary)
        credentials = directory / "credentials.csv"
        credentials.write_text(f"node_id,password\n1234,{password}\n2345,{password}\n")
        # Docker's non-root runtime user must traverse the bind-mounted directory.
        credentials.chmod(0o644)
        config = directory / "client.properties"
        config.write_text("default.api.timeout.ms=5000\nrequest.timeout.ms=3000\n")
        docker("network", "create", "--internal", network)
        try:
            broker = f"rpt-broker-{suffix}"
            names.append(broker)
            args = [
                "run",
                "-d",
                "--name",
                broker,
                "--network",
                network,
                "--network-alias",
                "broker",
                "--mount",
                f"type=bind,src={config},dst=/tmp/client.properties,readonly",
            ]
            for key, value in {
                "KAFKA_NODE_ID": "1",
                "KAFKA_PROCESS_ROLES": "broker,controller",
                "KAFKA_LISTENERS": "PLAINTEXT://:9092,CONTROLLER://:9093",
                "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://broker:9092",
                "KAFKA_CONTROLLER_LISTENER_NAMES": "CONTROLLER",
                "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": "PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT",
                "KAFKA_CONTROLLER_QUORUM_VOTERS": "1@broker:9093",
                "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": "1",
                "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR": "1",
                "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR": "1",
            }.items():
                args += ["-e", f"{key}={value}"]
            docker(*args, "apache/kafka:4.1.2")
            for attempt in range(12):
                result = docker(
                    "exec",
                    broker,
                    "/opt/kafka/bin/kafka-topics.sh",
                    "--bootstrap-server",
                    "broker:9092",
                    "--command-config",
                    "/tmp/client.properties",
                    "--create",
                    "--if-not-exists",
                    "--topic",
                    "rpt.registrations",
                    "--partitions",
                    "2",
                    "--replication-factor",
                    "1",
                    check=False,
                )
                if result.returncode == 0:
                    break
                time.sleep(0.5)
            else:
                raise RuntimeError(
                    "Kafka did not become ready: " + result.stderr[-1000:]
                )
            print("Kafka ready with a two-partition registration topic", flush=True)
            for role, image in [
                ("dns", "rpt-dnsserver"),
                ("http", "rpt-http-register"),
                ("iax", "rpt-iax-register"),
            ]:
                name = f"rpt-{role}-{suffix}"
                names.append(name)
                args = [
                    "run",
                    "-d",
                    "--name",
                    name,
                    "--network",
                    network,
                    "--network-alias",
                    role,
                    "-e",
                    "RPT_KAFKA__BOOTSTRAP=broker:9092",
                ]
                if role != "dns":
                    args += [
                        "--mount",
                        f"type=bind,src={credentials},dst=/run/secrets/credentials.csv,readonly",
                    ]
                docker(*args, image + ":review")
            http = f"rpt-http-{suffix}"
            code = """import json,time,urllib.request,urllib.error
password=PASSWORD
body={"port":4570,"data":{"nodes":{"1234":{"node":"1234","passwd":password,"remote":0}}}}
for attempt in range(30):
 try:
  request=urllib.request.Request("http://127.0.0.1:5000/",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
  result=json.load(urllib.request.urlopen(request,timeout=10))
  assert "successfully registered" in str(result["data"]),result
  break
 except urllib.error.URLError:
  time.sleep(.2)
else: raise AssertionError("HTTP registration failed")
print("HTTP registration published and acknowledged")
""".replace("PASSWORD", repr(password))
            print(docker("exec", http, "python", "-c", code).stdout.strip(), flush=True)
            iax = f"rpt-iax-{suffix}"
            code = """import socket,struct,time,hashlib
password=PASSWORD
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
 sock.settimeout(10)
 def ie(kind,value): return bytes([kind,len(value)])+value
 initial=struct.pack("!HHIBBBB",0x8001,0,0,0,0,6,13)+ie(6,b"2345")
 sock.sendto(initial,("127.0.0.1",4569))
 challenge_packet=sock.recv(4096)
 assert challenge_packet[11]==14
 payload=challenge_packet[12:]; fields={}
 while payload:
  kind,size=payload[:2];fields[kind]=payload[2:2+size];payload=payload[2+size:]
 dest=struct.unpack("!H",challenge_packet[:2])[0]&0x7fff
 proof=hashlib.md5(fields[15]+password.encode()).hexdigest().encode()
 request=struct.pack("!HHIBBBB",0x8001,dest,1,1,1,6,13)+ie(6,b"2345")+ie(16,proof)
 sock.sendto(request,("127.0.0.1",4569))
 response=sock.recv(4096)
 assert response[11]==15
print("IAX registration published and acknowledged")
""".replace("PASSWORD", repr(password))
            print(docker("exec", iax, "python", "-c", code).stdout.strip(), flush=True)
            dns = f"rpt-dns-{suffix}"
            code = """from dnslib import DNSRecord
import socket,time
for node in [1234,2345]:
 for attempt in range(50):
  with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
   sock.settimeout(1)
   sock.sendto(DNSRecord.question(f"{node}.nodes.example.org","A").pack(),("127.0.0.1",5054))
   try: reply=DNSRecord.parse(sock.recv(4096))
   except TimeoutError: continue
  if reply.rr:
   assert str(reply.rr[0].rdata)=="127.0.0.1"
   assert 0<reply.rr[0].ttl<=60
   break
  time.sleep(.2)
 else: raise AssertionError(f"DNS did not consume registration {node}")
print("DNS consumed both nested updates and answered with bounded TTLs")
"""
            print(docker("exec", dns, "python", "-c", code).stdout.strip(), flush=True)
            print("Local registration → Kafka → DNS integration passed", flush=True)
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stderr[-1500:]) from error
        finally:
            for name in reversed(names):
                docker("rm", "-f", name, check=False)
            docker("network", "rm", network, check=False)


if __name__ == "__main__":
    main()
