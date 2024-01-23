## CS6250 Computer Networks

### Spring 2024

- Student resources: https://gatech.instructure.com/courses/245818
- How to write a research paper - https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/
- How to read a paper - https://people.cs.umass.edu/~phillipa/CSE390/paper-reading.pdf
- ATNDP = Application, Transport, Network, Data link, Physical
- The transport layer is responsible for the end-to-end communication between end hosts. In this layer, there are two transport protocols:
  - Transmission Control Protocol (TCP)
  - User Datagram Protocol (UDP)
  - TCP offers connection oriented services; guaranteed delivery of application layer messages; flow control (Throttle);
  - UDP is stateless; connection less; best-effort to layers above; no reliability;
  - in transport layer; we call the packets as `segments`;
  - Network layer
    - packet is addressed as `datagram` in the network layer;
    - responsible for moving from one to another host;
    - n/w layer must use IP Protocol (Schema)
    - IP proto defines the fields in the datagram and how the source/destination hosts and the intermediate routers use these fields so that the datagrams that a source Internet host sends reach their destination. It is the routing protocols that determine the routes that the datagrams can take between sources and destinations.
  - Data Link layer
    - packets are called as `Frames`
    - Ethernet and wifi are here
    - Host A> B : Network layer(A) > Data link layer (A) >> Data link layer (B) > Network layer (B)
  - Physical layer:
    - This is hardware
    - Transfer bits w/in the frame btwn two nodes connected physically
  - ATNDP - Application>Transport(TCP,UDP;Segment)>Network(IP address;datagram)>Data Link(Ethernet, wifi;frame)>Physical (Cable,wire)
- Layer Encapsulation:
  - each layer adding its header info -- encapsulation
- End nodes/hosts impl. all 5 layers, intermediate devices do not impl. all 5, routes are level3 and switches are level2
- End to End principle
  - Don't have the appl. logic in the core of the n/w or in the intermediate nodes/devices
  - The end-to-end (e2e) principle is a design choice that characterized and shaped the current architecture of the Internet. The e2e principle suggests that specific application-level functions usually cannot, and preferably should not, be built into the lower levels of the system at the core of the network.
- Firewalls - Violate the E2E principle - bc they block traffic.
- NAT: N/W Address Translation - Home router keeping tabs on the devices using a 10.0.0.0 something; then they update destination IP google.com>router>laptop1
- Hourglass shape of internet architecture
- Evolutionary Architecture model, or EvoArch

  - This model proves that the waist is slim, as new nodes are introduced at layers above and below, death of nodes will happen
  - Redesigning the existing Internet architecture is difficult bc of its established applications and protocols.

- Interconnecting hosts and n/w:

  - Repeaters and Hubs: They operate on the physical layer (L1) as they receive and forward digital signals to connect different Ethernet segments. They provide connectivity between hosts that are directly connected (in the same network). The advantage is that they are simple and inexpensive devices, and they can be arranged in a hierarchy. Unfortunately, hosts that are connected through these devices belong to the same collision domain, meaning that they compete for access to the same link.
  - Bridges and Layer-2 Switches: These devices can enable communication between hosts that are not directly connected. They operate on the data link layer (L2) based on MAC addresses. They receive packets and forward them to the appropriate destination. A limitation is the finite bandwidth of the outputs. If the arrival rate of the traffic is higher than the capacity of the outputs, then packets are temporarily stored in buffers. But if the buffer space gets full, then this can lead to packet drops.
  - Routers and Layer-3 Switches: These are devices that operate on the network layer (L3). We will talk more about these devices and the routing protocols in the upcoming lectures.

- Learning bridges:
  - Bridge connects n/w
  - Device with multile i/p and o/p; transfers `frames` (Data link layer) from one i/p to one/many o/p
  - doesnot need to forward all the frames that it receives
  - Learns, populates and maintains a FORWARDING TABLE at PORT LEVEL
    if a frame says A to B, no need to send it to port 2 because A,B are on the port1 side
  ```
  A---B---C
        | (Port1)
        BRIDGE
        | (Port2)
        X--Y--V
  ```
  - Learns about HOST|PORT mapping, bc it knows what frame came in what port
- Looping problem and spanning tree

  - If there is anyone closer than me, I am not going to route traffic
  - Iterative approach
    ========== 11:45 PM

- DNS is in the application layer

---

## Lesson 2

Lesson 2 Readings and Additional Resources
Important Readings
CUBIC: A New TCP-Friendly High-Speed TCP Variant
https://www.cs.princeton.edu/courses/archive/fall16/cos561/papers/Cubic08.pdfLinks to an external site.

Book References
Kurose-Ross (Edition 6): Sections 3.1.1, 3.2, 3.3, 3.4, 3.5.5, 3.6

Peterson Section 6.3

Optional Readings
Congestion Avoidance and Control
https://ee.lbl.gov/papers/congavoid.pdfLinks to an external site.

A Protocol for Packet Network Intercommunication
https://www.cs.princeton.edu/courses/archive/fall06/cos561/papers/cerf74.pdfLinks to an external site.

End-to-End Internet Packet Dynamics
https://people.eecs.berkeley.edu/~sylvia/cs268-2019/papers//pktdynamics.pdfLinks to an external site.

Data Center TCP (DCTCP)
https://people.csail.mit.edu/alizadeh/papers/dctcp-sigcomm10.pdfLinks to an external site.
(Links to an external site.)

TIMELY: RTT-based Congestion Control for the Datacenter
https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p537.pdfLinks to an external site.

Design, implementation and evaluation of congestion control for multipath TCP
https://www.usenix.org/legacy/events/nsdi11/tech/full_papers/Wischik.pdfLinks to an external site.

Sizing Router Buffers
https://web.archive.org/web/20210120232627/http://yuba.stanford.edu/techreports/TR04-HPNG-060800.pdfLinks to an external site.

---

- Logical connection btwn 2 m/c in different n/w and diff location happens thru the `TRANSPORT` layer
- Focus on TCP
- Algos for reliability, flow control and congestion control
- latency vs sustained thruput

- Transport layer and the reln Transport and Network Layer:

  - Provides E2E connection for machines across n/w
  - Message from the `application layer` + Transport layer header => `Segment`
  - O/P of transport layer is a **SEGMENT**
  - N/W layer then encapsulates its headers to the segment and then send it to receiving hosts like routes, bridges and switches

- Multiplexing
  - Several applications to use the n/w simultaneously.
  - `PORTS` - additional identifiers used by the `TRANSPORT` layer to find what application in the host should it route the packet!
  - Each application will bind to a port by opening `Sockets` and listening for data from remote apps.
  - The transport layer can do multiplexing by using ports.
  - 2 modes - Connectionless and Connection-Oriented

---

### Connection Oriented and Connectionless Multiplexing and Demultiplexing

- `Happens in the transport layer`
- > Transport layer segment > Network layer datagram
- Incoming trans. layer segment will have info on what socket it needs to be sent, which the receiving host identifies
- > The job of delivering the data included in the transport-layer segment to the appropriate socket, as defined in the segment fields, is called demultiplexing
- > Similarly, the sending host will need to gather data from different sockets and encapsulate each data chunk with header information (that will later be used in demultiplexing) to create segments, and then forward the segments to the network layer. We refer to this job as multiplexing.

- Connectionless multiplexing/Demultiplexing

  - Identifier of UDP socket - Tuple of dest. IP and dest. PORT only!
  - fire and forget

- Connection oriented multiplexing/Demultiplexing
  - TCP - 4 tuple ource IP, source port, destination IP, and destination port.
  - 3-way handshake
  - Client exposes IP/port, Server establishes connection to clients IP/PORT via socket.

### More on UDP

> UDP is an unreliable protocol that lacks the mechanisms that TCP has. It is a connectionless protocol that does not require the establishment of a connection (e.g., the three-way handshake) before sending packets.

- No congestion control or similar mechanisms
- No connection management overhead
- higher packet loss
- DNS is app. layer proto that used UDP
- 64 bit header
- Error checking
  > 1 bit error is detected, 2 bit will go undetected; sum is always one after one-complement

### TCP 3 way h/s

- Special `segment` w/no app data is sent with SYN bit set to 1
- Server acks and sends a special `connection-granted` segment called `SYNACK` segment
- Client receives `SYNACK` segment, allocates resources and then sends an ack, with SYN bit set to 0
- **Connection teardown:**
  - Client sends a `FIN` bit set to 1
  - Server acks and closes the connetion
  - Server sends a segment with FIN set to 1.. indicatin the connection is closed;
  - client sends ACK back to server .. also waits and retires in case of segment lost.

### Reliable Transmission

- Network layer > `PACKETS`
- Network layer is not reliable; missing packets and out of order packets
- Reliability is an important `PRIMITIVE`; which TCP Developers decided to implement in the `TRANSPORT` layer
