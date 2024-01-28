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
- > TCP offers `IN-ORDER` delivery of the app. layer data w/o any loss or corruption
- > To have a reliable communication, the sender should be able to know which segments were received by the remote host and which were lost. Now, how can we achieve this? One way to do this is by having the receiver send acknowledgments indicating that it has successfully received the specific segment. If the sender does not receive an acknowledgment within a given period of time, the sender can assume the packet is lost and resend it. This method of using acknowledgments and timeouts is also known as **Automatic Repeat Request or ARQ**.

- > The simplest way would be for the sender to `send a packet and wait` for its acknowledgment from the receiver. This is known as Stop and Wait ARQ. Note that the algorithm typically needs to figure out the waiting time after which it resends the packet, and this estimation can be tricky. A small timeout value can lead to unnecessary retransmissions, but a large timeout value can lead to unnecessary delays. Typically the timeout value is a function of the estimated round trip time (RTT) of the connection.
- Send and wait has significant low perf. so introduce `windowing`; Send N packets in one shot w/o waiting for acks. Here, N is the `window size`
  - need to id packets in the window - incrementally
  - buffer the packets at src and client side; Sender needs to buffer packets that were `transmitted but not acked` and recv. may buffer packets for difference in rate of receive and consume. (I/O to disk)
- > One way is for the receiver to send an ACK for the most recently received in-order packet. The sender would then send all packets from the most recently received in-order packet, even if some of them had been sent before. The receiver can simply discard any out-of-order received packets. This is called `Go-back-N`. In the figure below, packet 7 is lost in the network so the receiver will discard any subsequent packets. The sender will send all the packets starting from 7 again.
- `selective ACKing` -
  - > The sender retransmits only those packets that it suspects were received in error. Then, the receiver would acknowledge a correctly received packet even if it is not in order. The out-of-order packets are buffered until any missing packets have been received, at which point the batch of the packets can be delivered to the application layer.
- `Fast retransmit` - Duplicate ACKs as a means to detect packet loss.
  - > A duplicate ACK is an additional acknowledgment of a segment for which the sender has already received acknowledgment earlier. When the sender receives 3 duplicate ACKs for a packet, it considers the packet to be lost and will retransmit it instead of waiting for the timeout. This is known as fast retransmit. For example, in the figure below, once the sender receives 3 duplicate ACKs, it will retransmit packet 7 without waiting for a timeout.

---

### Transmission Control

- mechanisms provided in the trans. layer to `control the transmission rate`
- Where should the transmission control fn reside int he n/w stack? UDP does this.
- Trans. Control is a fundamental fn. for most apps. hence impl. in transport layer is easy

### Flow control

> Flow control: Controlling the Transmission Rate to Protect the Receiver buffer

- protect reveiver budder from overflowing

> TCP uses a buffer at the receiver end to buffer packets that have not been transmitted to the application. The receiver might be involved with multiple processes and does not read the data instantly. This can cause the accumulation of a massive amount of data and overflow the receive buffer.

- TCP offeres rate control also known as `Flow control`
- Sender - maintains a receive window `rwnd`: how much the recv. can handle
- Recv. allocates `RcvBuffer`

We will illustrate its working using an example. Consider two hosts, A and B, communicating with each other over a TCP connection. Host A wants to send a file to Host B. Host B allocates a receive buffer of size RcvBuffer to this connection. The receiving host maintains two variables:

LastByteRead: the number of the last bytes in the data stream read from the buffer by the application process in B `(target)`

LastByteRcvd: the number of the last bytes in the data stream that has arrived from the network and has been placed in the receive buffer at B `Target`

Thus, to not overflow the buffer, TCP needs to make sure that

`LastByteRcvd - LastByteRead <= RcvBuffer`

The extra space that the receive buffer has is specified using a parameter termed as receive window.

`rwnd = RcvBuffer - [LastByteRcvd - LastByteRead]`

LBRead (2) LBRecv (10) => it has read 2. 8 pending
RcvBuffer = 10; so in this case, LBRv - LBRd = 10-2 = 8; 8 fits in the buffer..

Now, the extra space.. that is 10 - [ 8 - 2 ]=> 10 -6 => can accomodate 4 more.. to fill the buffer..
OK

- Spare room is `Receive Window` which the dest. tells to source
- Recevie buffer = Spare room + TCP buffer

- The sender also keeps track of two variables, `LastByteSent and LastByteAcked.`
  UnACKed Data Sent = LastByteSent - LastByteAcked

To not overflow the receiver’s buffer, the sender must ensure that the maximum number of unacknowledged bytes it sends is no more than the rwnd. Thus we need

LastByteSent – LastByteAcked <= rwnd

> Caveat: However, there is one scenario where this scheme has a problem. Consider a scenario where the receiver had informed the sender that rwnd = 0, and thus the sender stops sending data. Also, assume that B has nothing to send to A. Now, as the application processes the data at the receiver, the receiver buffer is cleared. Still, the sender may never know that new buffer space is available and will be blocked from sending data even when the receiver buffer is empty.

> TCP resolves this problem by making the sender continue sending segments of size 1 byte even after rwnd = 0. When the receiver acknowledges these segments, it will specify the rwnd value, and the sender will know as soon as the receiver has some room in the buffer.

### Congession Control

- Congestion control: Controlling the transmission rate to protect the network from congestion

The second and significant reason for transmission control is to avoid congestion in the network.

Let us look at an example to understand this. Consider a set of senders and receivers sharing a single link with capacity
. Assume other links have a capacity greater than
. How fast should each sender transmit data? We do not want the combined transmission rate to be higher than the link's capacity as it can cause issues in the network such as long queues, packet drops, etc. Thus, we want a mechanism to control the transmission rate at the sender to avoid congestion in the network. This is known as congestion control.

It is important to note that networks are quite dynamic, with users joining and leaving the network, initiating data transmission, and terminating existing flows. Thus the mechanisms for congestion control need to be dynamic enough to adapt to these changing network conditions.

#### Goals of n/w congresion control:

Let us consider some of the desirable properties of a good congestion control algorithm:

Efficiency. We should get high throughput, or utilization of the network should be high.

Fairness. Each user should have their fair share of the network bandwidth. The notion of fairness is dependent on the network policy. For this context, we will assume that every flow under the same bottleneck link should get equal bandwidth.

Low delay. In theory, it is possible to design protocols with consistently high throughput assuming infinite buffer. Essentially, we could keep sending the packets to the network, and they will get stored in the buffer and eventually get delivered. However, it will lead to long queues in the network leading to delays. Thus, applications sensitive to network delays such as video conferencing will suffer. Therefore, we want the network delays to be minor.

Fast convergence. The idea here is that a flow should converge to its fair allocation fast. Fast convergence is crucial since a typical network’s workload is composed of many short flows and few long flows. If the convergence to fair share is not fast enough, the network will still be unfair for these short flows.

- Flavors of congession control - 2x:

  - E2E - No n/w assistance; hosts infer congestion from n/w behavior and tune transmission rate
  - N/w assisted -> n/w layer provides feedback to the sender abt congestion in the n/w

- TCP uses the `end to end` approach
- Congrestion control is a primitive provided in the `TRANSPORT` layer; but routers operate in the `N/W` layer; Therefore this features resides in the end-node w/ no support from the n/w

### How TCP infers n/w congestion from n/w behavior

> Packet delay and Packet loss

There are mainly two signals of congestion.

First is the packet delay. As the network becomes congested, the queues in the router buffers build-up, leading to increased packet delays. Thus, an increase in the round trip time, which can be estimated based on ACKs, can indicate congestion in the network. However, it turns out that packet delays in a network tend to be variable, making delay-based congestion inference quite tricky.

Another signal for congestion is packet loss. As the network gets congested, routers start dropping packets. Note that packets can also be lost due to other reasons such as routing errors, hardware failure, time-to-live (TTL) expiry, error in the links, or flow control problems, although it is rare.

The earliest implementation of TCP used packet loss as a signal for congestion. This is mainly because TCP already detected and handled packet losses to provide reliability.

### TCP Sender limit the sending rate

TCP congestion control was introduced so that each source can do the following:

- First, determine the network's available capacity.
- Then, choose how many packets to send without adding to the network's congestion level.

ACKs is used as the probing mechanism. if the recv. received a packet sent earlier, then more are sent

`Congestion window` similar to the receive window used for flow control = Max no. of packets a sending host can hold in transit (`Sent but not yet acked`)

`Probe-and-adapt approach`; Start with something, increase to achieve available thruput, then adjust/decrease based on congestion

`LastByteSent – LastByteAcked <= min{cwnd, rwnd}`

### AIMD

Additive Increase and Multiplicative Decrease

Incrementally add +1 to `cwnd` congestion window
and reduce the `cwnd` /2 once a congestion is detected.

- Saw tooth pattern over time

> TCP does not wait for ACKs of all the packets from the previous RTT. Instead, it increases the congestion window size as soon as each ACK arrives. In bytes

> The value of cwnd cannot be reduced further than a value of 1 packet.

- `Max. Segment Size MSS`

TCP Reno:

- Triple ACKs (`mild congestion`) and timeout (`Severe`): loss events as a signal for congestion

### Slow Start

> In contrast, when we have a new connection that starts from a cold start, the sending host can take much longer to increase the congestion window by using AIMD. So for a new connection, we need a mechanism that can rapidly increase the congestion window from a cold start.

> TCP Reno has a slow start phase where the congestion window is increased exponentially instead of linearly, as in the case of AIMD. Once the congestion window becomes more than a threshold, often called the slow start threshold, it starts using AIMD.

> we note that there is one more scenario where slow start kicks in: when a connection dies while waiting for a timeout to occur.

> The source will have a fair idea about the congestion window from the last time it had a packet loss. It will now use this information as the “target” value to avoid packet loss in the future. This target value is stored in a temporary variable, CongestionThreshold.

### TCP Fairness

> AIMD leads to fairness in bandwidth sharing.
> Increase and decrease as the utilized bandwidth sum grows

- Other alternatives
  - AIAD, MIAD - not aggressive reduction..
  - MIMD is too aggressive.

`RTT` - Round trip time may affect the congestion window > unfair
N apps using `ONE` TCP connection sharing a link of rate R; new app having parallel TCP connections > unfair

- TCP CUBIC: Use a cubic function for the growth rate. Increase slowly over time when approaching the Window maximum `Wmax` (this is where the multiplicative decrease happened dur to n/w congestion) instead of linear.

> Growth window is a fn. of tow consecutive congestion events. First congestion event, TCP undergoes a fast recovery; so all connections/flows will have the same reduced window size.. vs their individual RTT

> TCP throughput is very sensitive to loss
