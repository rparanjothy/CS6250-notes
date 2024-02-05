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

- Triple ACKs (`mild congestion`)

  > The first is the triple duplicate ACKs, which is considered mild congestion. In this case, the congestion window is reduced to half the original.

- Timeout (`Severe`): GOES BACK TO INITIAL loss events as a signal for congestion
  > The second kind of congestion detection is timeout, i.e., when no ACK is received within a specified amount of time. It is considered a more severe form of congestion, and the congestion window is reset to the initial window size.

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

> TCP CUBIC as one such example for high bandwidth-delay product networks.

> DCTCP and TIMELY are two popular examples of TCP designed for DC environments. DCTCP is based on a hybrid approach of using both implicit feedback, e.g., packet loss, and explicit feedback from the network using ECN for congestion control. TIMELY uses the gradient of RTT to adjust its window.

QUIZ:

> No error checking,error correction, or acknowledgment is done by UDP. UDP is only concerned with speed. So when, the data sent over the Internet is affected by collisions, and errors will be present.

> TCP Cubic - increase the Congestion window ultimately

---

### Lesson 3 Intradomain Routing

- What it takes for 2 hosts to exchange data.
  > In this lecture, we will learn about the protocols that enable data to travel over a "good" path from the source to the destination within a single administrative domain. First, we'll learn about two types of intradomain routing algorithms: the link-state and distance-vector algorithms. Next, we'll look at example protocols such as OSPF (Open Shortest Path First) and RIP (Routing Information Protocol). We will also look at challenges that intradomain routing protocols face, such as convergence delay. Finally, we will look at how routing protocols are used for purposes beyond determining a "good" path. For example, we can use routing for traffic engineering purposes to steer traffic through the network, avoiding congested links.

### Important Readings

Experience in Black-box OSPF Measurements
http://conferences.sigcomm.org/imc/2001/imw2001-papers/82.pdfLinks to an external site.

Book References
If you have access to the Kurose-Ross book and the Peterson book, you can find the list of chapters discussed in this lecture. As mentioned in the course schedule, purchasing the books is not required.

Kurose-Ross (6e)
4.5.1:The Link-State (LS) Routing Algorithm
4.5.2: The Distance- Vector (DV) Routing Algorithm
4.6.1: Intra-AS Routing in the Internet: RIP
4.6.2: Intra-AS Routing in the Internet: OSPF
Kurose-Ross (7e)
5.2.1The Link-State (LS) Routing Algorithm
5.2.2: The Distance- Vector (DV) Routing Algorithm
5.3: Intra-AS Routing in the Internet: OSPF
Kurose-Ross (8e)
5.2.1: The Link-State (LS) Routing Algorithm
5.2.2: The Distance- Vector (DV) Routing Algorithm
5.3: Intra-AS Routing in the Internet: OSPF
Optional Readings
Hot Potatoes Heat Up BGP Routing
https://www.cs.princeton.edu/~jrex/papers/hotpotato.pdfLinks to an external site.

Traffic Engineering With Traditional IP Routing Protocols
https://www.cs.princeton.edu/~jrex/teaching/spring2005/reading/fortz02.pdfLinks to an external site.

Dynamics of Hot-Potato Routing in IP Networks
https://www.cs.princeton.edu/~jrex/papers/sigmetrics04.pdfLinks to an external site.

OSPF Monitoring: Architecture, Design and Deployment Experience
https://www.cs.princeton.edu/~jrex/teaching/spring2005/reading/shaikh04.pdfLinks to an external site.

### Routing algos

Each of the two hosts knows the default router (or first-hop router). A host will first send a packet to the default router, but what happens after that? In this lecture, we will see the algorithms that we need so that when a packet leaves the default router of the sending host, it will travel over a path towards the default router of the destination host.

As a packet travels from the sending host to the destination host, each `intermediate router along the packet's path is responsible for forwarding that packet to the next router`. When a packet arrives at a router, the router consults its forwarding table to determine the outgoing link over which it should forward the packet. In this context, "`forwarding`" refers to transferring a packet from an incoming link to an outgoing link within a single router. We will talk about forwarding in an upcoming lesson.

On the other hand, "`routing`" refers to how routers work (_muliple routers_)together using routing protocols to determine the good paths (or good routes as we call them) over which the packets travel from the source to the destination node. When we have routers that belong to the `same administrative domain`, we refer to the routing as `intradomain` routing. But when routers belong to `different administrative domains`, we refer to `interdomain` routing. This lecture focuses on intradomain routing algorithms or `Interior Gateway Protocols (IGPs)`.

The two major classes of algorithms that we have are `link-state and distance-vector` algorithms. We use a graph to understand these algorithms. Routers are represented as nodes and links between routers as an edge. Each edge has an associated cost.

- Link state
- Distance vector

### Link State routing

O(n2)

---

Feb 4 2024

### Distance Vector Routing

- Iterative (loop until no updates)
- Async (Nodes does not need to be synchronized)
- distributed (direct nodes send information to each other, then resend their results back after their compute; so calculations are not happening in a centralized manner.)

> The DV algorithm is based on the Bellman Ford Algorithm. Each node maintains its own distance vector, with the costs to reach every other node in the network. Then, from time to time, each node sends its own distance vector to its neighbor nodes. The neighbor nodes in turn, receive that distance vector and they use it to update their own distance vectors. In other words, the neighboring nodes exchange their distance vectors to update their own view of the network.

> How is the vector update is happening? Each node x updates its own distance vector using the Bellman Ford equation: Dx(y) = minv{c(x,v) + Dv(y)} for each destination node y in the network. A node x, computes the least cost to reach destination node y, by considering the options that it has to reach y through each of its neighbor v. So node x considers the cost to reach neighbor v, and then it adds the least cost from that neighbor v to the final destination y. It calculates that quantity over all neighbors v and it takes the minimum

_Kurose-Ross Edition 6, Section 4.5.2_

- Each node maintains a cross-tab of distances, for distances that it cant mesasure, it will initialize with `INFINITY` in the first iteration.
- As nodes communicate, this cross-tab is updated.
- This is repeated until every node has no updates to make and waits for next changes. `The nodes enter a waiting mode, until there is a change in the link costs. `

### Link Cost Changes and Failures in DV - Count to Infinity Problem

> In contrast to the previous scenario, this link cost change took a long time to propagate among the nodes of the network. This is known as the `count-to-infinity` problem.

- It might not be instantaneous all the time, there are cases when the cost goes up from X-Y, it might be bouncing between Y and Z and takes time to break the loop until the weight is significantly high for a propagation to happen.

`Bad news travels slow: increase in weights/cost`
`Good news travels fast: decrease in weights/cost`

### Poison Reverse

- solution to the `count-to-infinity` problem

A solution to the previous problem is the following idea, called poison reverse: since z reaches x through y, z will advertise to y that the distance to x is infinity (Dz(x)=infinity). However z knows that this is not true and Dz(x)=5. z tells this lie to y, as long as it knows that it can reach to x via y. Since y assumes that z has no path to x except via y, it will never send packets to x via z.

So z poisons the path from z to y.

Things change when the cost from x to y changes to 60. y will update its table and send packet to x directly with cost Dy(x)=60. It will inform z about its new cost to x, after this update is received. Then z will immediately shift its route to x to be via the direct (z,x) link at cost 50. Since there is a new path to x, z will inform y that Dz(x)=50.

When y receives this update from z, y will update Dy(x)=51=c(y,z)+Dz(x).

Since z is now on least cost path of y to reach x, y poisons the reverse path from z to x. Y tells z that Dy(x)=inf, even though y knows that Dy(x)=51.

This technique will solve the problem with 2 nodes, **however poisoned reverse will not solve a general count to infinity problem involving 3 or more nodes that are not directly connected.**

### Distance Vector Routing Protocol Example: RIP

- Routing Information Protocol (RIP) is based on the Distance Vector protocol
- `HOP COUNT` as a metric
- Intradomain routing algo
- Routing updates are exchanged between neighbors periodically vs Distance vectors in DV protocol
- _RIP advertisements_
- Routing tables Dest. subnet, next router, hops
- `AS` Autonomous System
- Some of the challenges with RIP include updating routes, reducing convergence time, and avoiding loops/count-to-infinity problems.

### Linkstate Routing Protocol Example: OSPF

- Open Shortest Path First

Open Shortest Path First (OSPF) is a routing protocol that uses a link-state routing algorithm to find the best path between the source and the destination router. OSPF was introduced as an advancement of the RIP Protocol, operating in upper-tier ISPs. It is a link-state protocol that uses flooding of link-state information and a Dijkstra least-cost path algorithm. Advances include authentication of messages exchanged between routers, the option to use multiple same-cost paths, and support for hierarchy within a single routing domain.

As we have seen already, a link-state routing algorithm is a dynamic routing algorithm in which each router shares knowledge of its neighbors with every other router in the network. The network topology built as a result can be viewed as a directed graph with preset weights for each edge assigned by the administrator.

Hierarchy: An OSPF autonomous system can be configured hierarchically into areas. Each area runs its own OSPF link-state routing algorithm, with each router in an area broadcasting its link-state to all other routers in that area. Within each area, one or more area border routers are responsible for routing packets outside the area.

Exactly one OSPF area in the AS1 is configured to be the backbone area. The primary role of the backbone area is to route traffic between the other areas in the AS. The backbone always contains all area border routers in the AS and may contain non-border routers as well.

For packet routing between two different areas, it is required that the packet be sent through an area border router, through the backbone, and then to the area border router within the destination area before finally reaching the destination.

Operation: First, a graph (topological map) of the entire AS is constructed. Then, considering itself as the root node, each router computes the shortest path tree to all subnets by running Dijkstra's algorithm locally. The link costs have been pre-configured by a network administrator. The administrator has a variety of choices while configuring the link costs. For instance, he may choose to set them to be inversely proportional to link capacity or set them all to one. Given a set of link weights, OSPF provides the mechanisms for determining the least-cost path routing.

Whenever there is a change in a link's state, the router broadcasts routing information to all other routers in the AS, not just to its neighboring routers. It also periodically broadcasts a link's state even if its state hasn't changed.

Link State Advertisements: Every router within a domain that operates on OSPF uses Link State Advertisements (LSAs). LSA communicates the router's local routing topology to all other local routers in the same OSPF area. In practice, LSA is used for building a database (called the link state database) containing all the link states. LSAs are typically flooded to every router in the domain. This helps form a consistent network topology view. Any change in the topology requires corresponding changes in LSAs.

The refresh rate for LSAs: OSPF typically has a refresh rate for LSAs, which has a default period of 30 minutes. If a link comes alive before this refresh period is reached, the routers connected to that link ensure LSA flooding. Since the flooding process can happen multiple times, every router receives multiple copies of refreshes or changes - and stores the first received LSA change as new and the subsequent ones as duplicates.

`Forwarding Information Base (FIB)`

### Hot Potato

- networks exit (egress points)
- hot potato routing is a technique/practice of choosing a path `within the network`, by choosing the `closest egress point` based on intradomain path cost (Interior Gateway Protocol/IGP cost).
- Hot potato routing also effectively reduces the network’s resource consumption by getting the traffic out as soon as possible.
