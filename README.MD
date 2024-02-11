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

As a packet travels from the sending host to the destination host, each `intermediate router along the packet's path is responsible for forwarding that packet to the next router`. When a packet arrives at a router, the router consults its forwarding table to determine the outgoing link over which it should forward the packet. In this context, "`forwarding`" refers to transferring a packet from an incoming link to an outgoing link within a `single` router. We will talk about forwarding in an upcoming lesson.

On the other hand, "`routing`" refers to how routers work (_muliple routers_)together using routing protocols to determine the good paths (or good routes as we call them) over which the packets travel from the source to the destination node. When we have routers that belong to the `same administrative domain`, we refer to the routing as `intradomain` routing. But when routers belong to `different administrative domains`, we refer to `interdomain` routing. This lecture focuses on intradomain routing algorithms or `Interior Gateway Protocols (IGPs)`.

The two major classes of algorithms that we have are `link-state and distance-vector` algorithms. We use a graph to understand these algorithms. Routers are represented as nodes and links between routers as an edge. Each edge has an associated cost.

- Link state
- Distance vector

### Link State routing

O(n2)

- In link-state algorithms, the link costs and the network topology are known to all nodes
- We have the graph below and we consider our source node to be u. Our goal is to compute the least-cost paths from u to all nodes v in the network
- We start with the initialization step, where we set all the currently known least-cost paths from u to it’s directly attached neighbors v, x and w. For the rest of the nodes in the network we set the cost to infinity, because they are not immediate neighbors to source node u. We also initialize the set N' to include only the source node u. The first row in our table represents the initialization step.

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
- In some cases there are `multiple` egress points that the routers can choose from.
- These egress points (routers) can be `equally good` in the sense that they offer similarly good external paths to the final destination.
- hot potato routing is a technique/practice of choosing a path `within the network`, by choosing the `closest egress point` based on intradomain path cost (Interior Gateway Protocol/IGP cost).
- Hot potato routing also effectively reduces the network’s resource consumption by getting the traffic out as soon as possible.

---

### Lesson 4 - AS Relationship and interdomain routing

AS - Autonomous Systems

- how does data travel between networks?

  > We know that the Internet is an ecosystem that consists of thousands of independently operated networks. Each network operates in its own interest, and they have independent economic and traffic engineering objectives. And yet they must interconnect to provide global connectivity. In this lesson, we learn about the BGP protocol that provides the glue for this connectivity. We will also learn about the different interconnections types based on business relationships between networks. Finally, we will learn about increasingly popular infrastructures called Internet Exchange Points, which primarily provide interconnection services so that the participant networks can directly exchange traffic.

- Internet is an ecosystem with independently operated networks
- Networks have individual economic and traffic engineering goals
- Interconnection is essential for global connectivity
- BGP protocol facilitates connectivity in the Internet
- Different interconnection types based on business relationships
- Internet Exchange Points (IXPs) are popular infrastructures for direct traffic exchange between participant networks

### References and readings

Interdomain Internet Routing
https://web.mit.edu/6.829/www/currentsemester/papers/AS-bgp-notes.pdfLinks to an external site.

BGP routing policies in ISP networks
https://www.cs.princeton.edu/~jrex/papers/policies.pdfLinks to an external site.

On the importance of Internet eXchange Points for today’s Internet ecosystem
https://cryptome.wikileaks.org/2013/07/ixp-importance.pdfLinks to an external site.

Peering at Peerings: On the Role of IXP Route Servers
https://people.csail.mit.edu/richterp/imc238-richterA.pdfLinks to an external site.

Book References
Kurose-Ross

6th Edition: Section 1.3.3 (A Network of Networks), Section 4.6.3 (Inter-AS Routing: BGP)

7th Edition: Section 1.3.3 (A Network of Networks), Section 5.4.1 (The Role of BGP)

Optional Readings
Investigating Interdomain Routing Policies in the Wild
https://people.cs.umass.edu/~phillipa/papers/AnwarIMC15.pdfLinks to an external site.

BGP Communities: Even more Worms in the Routing Can
https://people.mpi-inf.mpg.de/~fstreibelt/preprint/communities-imc2018.pdfLinks to an external site.

On the scalability of BGP: the roles of topology growth and update rate-limiting
https://www.cc.gatech.edu/home/dovrolis/Papers/bgp-scale-conext08.pdfLinks to an external site.

O Peer, Where Art Thou? Uncovering Remote Peering Interconnections at IXPs
https://www.inspire.edu.gr/wp-content/pdfs/uncovering_remote_peering_interconnections_v1.pdfLinks to an external site.

Detecting BGP Configuration Faults with Static Analysis
https://www.usenix.org/legacy/events/nsdi05/tech/feamster/feamster.pdfLinks to an external site.

### Autonomous Systems and Internet Interconnection

The Internet as a an Ecosystem:

Today's Internet is a complex ecosystem built of a network of networks. The basis of this ecosystem includes `Internet Service Providers (ISPs)`, `Internet Exchange Points (IXPs)`, and `Content Delivery Networks (CDNs)`

**Border Gateway Protocol - BGP**

3 Types of **ISP**:

- Tier 3 - Access ISPs - Connect to Tier 2 ISPs
- Tier 2 - Regional USPs - Connect to Tier 1 ISPs
- Tier 1 - Large Global scale ISPs - `Backbone n/w` over which the smaller n/w can connect (ATT, Sprint)

**IXPs**
Second, IXPs are interconnection infrastructures that provide the physical infrastructure where multiple networks (e.g., ISPs and CDNs) can interconnect and exchange traffic locally. As of 2019, there are approximately 500 IXPs around the world.

Third, CDNs are networks that content providers create with the goal of having greater control of how the content is delivered to the end-users while reducing connectivity costs. Examples of CDNs are Google and Netflix. These networks have multiple data centers, and each one of them may be housing hundreds of servers that are distributed across the world.

**Competition and Cooperation Among Networks:**

This ecosystem we described forms a hierarchical structure since smaller networks (e.g., access ISPs) connect to larger networks (e.g., Tier-2 ISPs). In other words, an access ISP receives Internet connectivity, becoming the customer of a larger ISP. In this case, the larger ISP becomes the provider of the smaller ISP. This leads to competition at every level of the hierarchy. For example, Tier-1 ISPs compete with each other, and the same is true for regional ISPs that compete with each other. But, at the same time, competing ISPs need to cooperate in providing global connectivity to their respective customer networks. As a result, ISPs deploy multiple interconnection strategies depending on the number of customers in their network and the geographical location of these networks.

More interconnection options in the Internet ecosystem: To complete the picture of today's Internet interconnection ecosystem, we note that ISPs may also connect through `Points of Presence (PoPs), multi-homing, and peering`. PoPs are one (or more) routers in a provider's network, which a customer network can use to connect to that provider. Also, an ISP may choose to multi-home by connecting to one or more provider networks. Finally, two ISPs may choose to connect through a settlement-free agreement where neither network pays the other to directly send traffic to one another.

The Internet topology: hierarchical versus flat: As we said, this ecosystem we just described forms a hierarchical structure, especially in the earlier days of the Internet. But, it's important to note that as the Internet has been evolving, the dominant presence of IXPs and CDNs has caused the structure to begin morphing from hierarchical to flat.

**Autonomous Systems:** `Each of the networks we discussed above (e.g., ISPs and CDNs) may operate as an Autonomous System (AS).`

> An AS is a group of routers (including the links among them) that operate under the same administrative authority. An ISP, for example, may operate as a single AS, or it may operate through multiple ASes. Each AS implements its own policies, makes its own traffic engineering decisions and interconnection strategies, and determines how the traffic leaves and enters its network.

Protocols for routing traffic between and within ASes: The border routers of the ASes use the `Border Gateway Protocol (BGP) to exchange routing information with one another`.

In contrast, the `Interior Gateway Protocols (IGPs)` operate `within` an AS, and they are focused on "optimizing a path metric" within that network.

Example IGPs include Open Shortest Paths First (OSPF), Intermediate System - Intermediate System (IS-IS), Routing Information Protocol (RIP), and E-IGRP. In this lesson, we will focus on BGP.

### AS Business Relationships

In this topic, we will talk about the prevalent forms of business relationships between ASes:

> Provider-Customer relationship (or transit): This relationship is based on a financial settlement that determines how much the customer will pay the provider. The provider forwards the customer's traffic to destinations found in the provider's routing table (including the opposite direction of the traffic).

Peering relationship: In a peering relationship, two ASes share access to a subset of each other's routing tables. The routes shared between two peers are often restricted to the respective customers of each one. The agreement holds as long as the traffic exchanged between the two peers is not highly asymmetric. Peering relationships are formed between Tier-1 ISPs but also between smaller ISPs. In the case of Tier-1 ISPs, the two peers need to be of similar size and handle proportional amounts of traffic. Otherwise, the larger ISP would lack the incentive to enter a peering relationship with a smaller size ISP. When two small ISPs peer, they both save the money they would otherwise pay to their providers by directly forwarding traffic between themselves instead of through their providers. This arrangement is primarily beneficial when a significant amount of traffic is destined for each other (or each other's customers).
AS Business relationships diagram

How do providers charge customers?

While peering allows networks to have their traffic forwarded without cost, provider ASes have a financial incentive to forward as much of their customers' traffic as possible. One major factor determining a provider's revenue is the data rate of an interconnection. A provider usually charges in one of two ways:

Based on a fixed price, given that the bandwidth used is within a predefined range.
Based on the bandwidth used. The bandwidth usage is calculated based on periodic measurements, e.g., five-minute intervals. The provider then charges by taking the 95th percentile of the distribution of the measurements.
We might observe complex routing policies. In some cases, the driving force behind these policies is to increase traffic from a customer to its provider so that the provider gains more revenue.

### BGP Routing policies, importing and exporting routes:

In the previous topic, we talked about AS business relationships. AS business relationships drive an AS's routing policies and influence which routes an AS needs to import or export. This topic will talk about why it matters which routes an AS imports/exports.

Transit and Peering.png

Exporting Routes
Deciding which routes to export is an important decision with business and financial implications. Advertising a route for a destination to a neighboring AS means that this route may be selected by that AS, and traffic will start to flow through. Therefore, deciding which routes to advertise is a policy decision, which is implemented through route filters. Route filters are rules that determine which routes an AS's router should advertise to the routers of neighboring ASes.

Let's look at the different types of routes an AS (let's call it X) decides whether to export.

### EXPORT RULES:

**Routes learned from customers:** These are the routes X receives as advertisements from its customers. Since provider X is getting paid to provide reachability to a customer AS, it makes sense that X wants to advertise these customer routes to as many neighboring ASes as possible. This will likely cause more traffic toward the customer (through X) and, hence, more revenue for X.

**Routes learned from providers:** These are the routes X receives as advertisements from its providers. Advertising these routes does not make sense since X has no financial incentive to carry traffic for its provider's routes. Therefore, these routes are withheld from X's peers and X's other providers, but they are advertised to X's customers.

**Routes learned from peers:** These are routes that X receives as advertisements from its peers. As we saw earlier, it does not make sense for X to advertise to provider A the routes it receives from provider B. Because in that case, providers A and B will use X to reach the advertised destinations without X making revenue. The same is true for the routes that X learns from peers.

> Customer > Provider > Peer for EXPORT

### Importing Routes

Like exporting, ASes are selective about which routes to import. These decisions are primarily based on which neighboring AS advertises them and the type of business relationship established. An AS receives route advertisements from its customers, providers, and peers.

When an AS receives multiple route advertisements towards the same destination from multiple ASes, it needs to rank the routes before selecting which one to import. In order of preference, the imported routes are the customer routes, then the peer routes, and finally, the provider routes. The reasoning behind this ranking is as follows:

An AS wants to ensure that routes toward its customers do not traverse other ASes, unnecessarily generating costs.

An AS uses routes learned from peers since these are usually "free" (under the peering agreement).

An AS resorts to importing routes learned from providers only when necessary for connectivity since these will add to costs.

> Customer > Peer > Provider for IMPORT

### BGP and Design Goals

- Scalability
- Express routing policies
- Allow cooperation among ASes
- Security

In the previous pages, we talked about importing and exporting routes. In the following topics, we will learn how the default routing protocol, called Border Gateway Protocol, or BGP, is used to implement routing policies.

Let’s first start with the design goals of the BGP protocol.

Scalability: As the size of the Internet grows, the same is true for the number of ASes, the number of prefixes in the routing tables, the network churn, and the BGP traffic exchanged between routers. One of the design goals of BGP is to manage the complications of this growth while achieving convergence in reasonable timescales and providing loop-free paths.

Express routing policies: BGP has defined route attributes that allow ASes to implement policies (which routes to import and export) through route filtering and route ranking. Each ASes routing decisions can be kept confidential, and each AS can implement them independently.

Allow cooperation among ASes: Each AS can still make local decisions (which routes to import and export) while keeping these decisions confidential from other ASes.

Security: Originally, the design goals for BGP did not include security. However, the increase in size and complexity of the Internet demands security measures to be implemented. We need protection and early detection for malicious attacks, misconfiguration, and faults. These vulnerabilities still cause routing disruptions and connectivity issues for individual hosts, networks, and even entire countries. There have been several efforts to enhance BGP security ranging from protocols (e.g., S-BGP), additional infrastructure (e.g., registries to maintain up-to-date information about which ASes own which prefixes ASes), public keys for ASes, etc. Also, there has been extensive research to develop machine learning-based approaches and systems. But these solutions have not been widely deployed or adopted for multiple reasons that include difficulties in transitioning to new protocols and a lack of incentives.

### BGP Protocol basics

> A BGP session between a pair of routers in two different ASes is called an external BGP (eBGP) session, and a BGP session between routers that belong to the same AS is called an internal BGP (iBGP) session.

> autonomous system number (ASN).

In this topic, we will review some of the basic ideas of the BGP protocol.

A pair of routers, known as BGP peers, exchange routing information over a semi-permanent TCP port connection called a BGP session. In order to begin a BGP session, a router will send an OPEN message to another router. Then the sending and receiving routers will send each other announcements from their routing tables. The time it takes to exchange routes varies from a few seconds to several minutes, depending on the number of routes exchanged.

A BGP session between a pair of routers in two different ASes is called an external BGP (eBGP) session, and a BGP session between routers that belong to the same AS is called an internal BGP (iBGP) session.

In the following diagram, we can see three different ASes along with iBGP (e.g., between 3c and 3a) and eBGP (e.g., between 3a and 1c ) sessions between their border routers.

BGP messages: After BGP peers establish a session, they can exchange BGP messages to provide reachability information and enforce routing policies. We have two types of BGP messages:

1. The `UPDATE` messages contain information about the routes that have changed since the previous update. There are two kinds of updates:

   - `Announcements` are messages that advertise new routes and updates to existing routes. They include several standardized attributes.
   - `Withdrawals` messages inform that receive that a previously announced route is no longer available. The removal could be due to some failure or a change in the routing policy.

2. The `KEEPALIVE` messages are exchanged between peers to keep a current session going.

**BGP Prefix Reachability:** In the BGP protocol, destinations are represented by IP prefixes. Each prefix represents a subnet or a collection of subnets that an AS can reach. Gateway routers running eBGP advertise the IP prefixes they can reach according to the AS's specific export policy to routers in neighboring ASes. Then, using separate iBGP sessions, the gateway routers disseminate these routes for external destinations to other internal routers according to the AS's import policy. Internal routers run iBGP to propagate the external routes to other internal iBGP speaking routers.

**Path Attributes and BGP Routes:** In addition to the reachable IP prefix field, advertised BGP routes consist of several BGP attributes. Two notable attributes are AS-PATH and NEXT-HOP.

- ASPATH: Each AS is identified by its autonomous system number (ASN). As an announcement passes through various ASes, their identifiers are included in the ASPATH attribute. `This attribute prevents loops and is used to choose between multiple routes to the same destination, the route with the shortest path.`
- NEXT HOP: This attribute refers to the next-hop router's IP address (interface) along the path towards the destination. `Internal routers use the field to store the IP address of the border router`. Internal BGP routers will forward all traffic bound for external destinations through the border router. Suppose there is more than one such router on the network, and each advertises a path to the same external destination. In that case, NEXT HOP allows the internal router to store in the forwarding table the best path according to the AS routing policy.

### iBGP and eBGP

> IGP-like protocols are used to establish paths between the internal routers of an AS based on specific costs within the AS. In contrast, iBGP is only used to disseminate external routes within the AS.

In the previous topic, we saw that we have two flavors of BGP: eBGP (for sessions are between border routers of neighboring ASes) and iBGP (for sessions between internal routers of the same AS).

Both protocols are used to disseminate routes for external destinations.

The eBGP speaking routers learn routes to external prefixes and disseminate them to all routers within the AS. This dissemination is happening with iBGP sessions. For example, as the figure below shows, the border routers of AS1, AS2, and AS3 establish eBGP sessions to learn external routes. Inside AS2, these routes are disseminated using iBGP sessions.

The dissemination of routes within the AS is done by establishing `a full mesh of iBGP sessions between the internal routers`. Each eBGP speaking router has an iBGP session with every other BGP router in the AS to send updates about the routes it learns (over eBGP).

Finally, we note that iBGP is not another IGP-like protocol (e.g., RIP or OSPF). IGP-like protocols are used to `establish paths between the internal routers of an AS based on specific costs within the AS`. In contrast, iBGP is only used to disseminate external routes within the AS.

- Both iBGP and eBGP take care of dissemination of "External" routes.
- eBGP is between two border routes that belong to different ASes.
- iBGP is between routes that belong to same AS

### BGP Decision Process: Selecting Routes at a Router

As we already discussed in earlier topics, ASes are operated and managed by different administrative authorities. Therefore, they can operate with different business goals and network conditions (e.g., traffic volumes). Of course, all these factors can affect the BGP policies for each AS independently.

Still, routers follow the same process to select routes. So let's zoom into what is happening as the routers exchange BGP messages to select routes.

BGP Decision Process: Selecting Routes at a Router-1

Conceptually, we can consider the model of a router as in the figure above (Reference: https://www.cc.gatech.edu/home/dovrolis/Papers/bgp-scale-conext08.pdfLinks to an external site.). A router receives incoming BGP messages and processes them. When a router receives advertisements, it first applies the import policies to exclude routes from further consideration. Then the router implements the decision process to select the best routes that reflect the policy in place. Next, the newly selected routes are installed in the forwarding table. Finally, the router decides which neighbors to export the route to by applying the export policy.

The Router's Decision Process
Let's take a look at the router's decision process. Suppose that a router receives multiple route advertisements to the same destination. How does the router choose which route to import? In a nutshell, the decision process is how the router compares routes. It goes through the list of attributes in the route advertisements. In the simplest scenario, where there is no policy in place (meaning it does not matter which route will be imported), the router uses the attribute of the path length to select the route with the fewest number of hops. This simple scenario rarely occurs in practice.

A router compares a pair of routes by going through the list of attributes, as shown in the figure below. For each attribute, it selects the route with the attribute value that will help apply the policy. If for a specific attribute, the values are the same, then it goes to the next attribute.

Influencing The Route Decision Using the LocalPref

```txt
LocalPref - outbound traffic (high preferred)
MED - Inbound traffic (Low preferred)
```

Let's focus on two attributes, `LocalPref and MED (Multi-Exit Discriminator)`, and let's see how we can use them to influence the decision process.

The LocalPref attribute is used to prefer routes learned through a specific AS over other ASes. For example, suppose AS B learns of a route to the same destination x via A and C. If B prefers to route its traffic through A, due to peering or business, it can assign a higher LocalPref value to routes it learns from A. And therefore, by using LocalPref, AS B can control where the traffic exits the AS. In other words, it will influence which `routers will be selected as exit points` for the traffic that leaves the AS (`outbound` traffic).

As we saw earlier in this lesson, an AS ranks the routes it learns by preferring first the routes learned from its customers, then the routes learned from its peers, and finally, the routes learned from its providers. An operator can assign a non-overlapping range of values to the LocalPref attribute according to the type of relationship. So assigning different LocalPref ranges will influence which routes are imported. The following image shows a scheme that can be used to reflect the business relationships:

Influencing the Route Decision Using the MED Attribute

The MED (Multi-Exit Discriminator) value is used by ASes connected by multiple links to designate which links are preferred for `inbound` traffic. For example, the network operator of AS B will assign different MED values to its routes advertised to AS A through R1 and different MED values to its routes advertised through R2. As a result of different MED values for the same routes, AS A will be influenced to choose R1 to forward traffic to AS B, if R1 has a lower MED value, and if all other attributes are equal.

We have seen in the previous topics that an AS does not have an economic incentive to export routes that it learns from providers or peers to other providers or peers. An AS can reflect this by tagging routes with a MED value to "staple" the type of business relationship. Also, an AS filters routes with specific MED values before exporting them to other ASes. Finally, we note that influencing the route exports will also affect how the traffic enters an AS (the routers that are entry points for the traffic that enters the AS).

So, where/how are the attributes controlled? The attributes are set either (a) locally by the AS (e.g., LocalPref), (b) by the neighboring AS (e.g., MED), (c) or by the protocol (e.g., if a route is learned through eBGP or iBGP).

- ASes operated by different authorities with diverse business goals and network conditions.
- BGP Decision Process at a router involves import policies, route selection, forwarding table installation, and export policies.
- Decision process considers attributes; path length often crucial if no policy in place.
- LocalPref attribute used to prefer routes from a specific AS, influencing outbound traffic and exit points.
- Routes ranked by preference: customers, peers, providers; LocalPref ranges reflect business relationships.
- MED (Multi-Exit Discriminator) influences inbound traffic preference for ASes with multiple links.
- ASes use MED values to designate preferred links, affecting route choice for inbound traffic.
- ASes tag routes with specific MED values to indicate business relationships, affecting route exports.
- Attributes controlled locally (e.g., LocalPref), by neighboring AS (e.g., MED), or by the protocol (e.g., eBGP/iBGP).

### Challenges with BGP: Scalability and Misconfigurations

Unfortunately, the BGP protocol in practice can suffer from two significant limitations: misconfigurations and faults. A possible misconfiguration or an error can result in an excessively large number of updates, resulting in route instability, router processor and memory overloading, outages, and router failures. One way that ASes can help reduce the risk that these events will happen is by `limiting the routing table size and limiting the number of route changes`.

An AS can limit the routing table size using **filtering**. For example, long, specific prefixes can be filtered to encourage route aggregation. In addition, routers can limit the number of prefixes advertised from a single source on a per-session basis. Some small ASes also have the option to configure **default routes** into their forwarding tables. ASes can likewise protect other ASes by using route aggregation and exporting less specific prefixes where possible.

Also, an AS can limit the number of routing changes, explicitly limiting the propagation of unstable routes by using a mechanism known as **flap damping**. To apply this technique, an AS will track the number of updates to a specific prefix over a certain amount of time. If the tracked value reaches a configurable value, the AS can suppress that route until a later time. Because this can affect reachability, an AS can be strategic about how it uses this technique for certain prefixes. For example, more specific prefixes could be more aggressively suppressed (lower thresholds), while routes to known destinations that require high availability could be allowed higher thresholds.

### Peering at IXPs

n the previous topics, we talked about ASes’ business relationships. ASes can either peer with one another directly or peer at Internet Exchange Points (IXPs), which are infrastructures that facilitate peering and provide more services.

What are IXPs?

IXPs are physical infrastructures that provide the means for ASes to interconnect and directly exchange traffic with one another. The ASes that interconnect at an IXP are called participant ASes. The physical infrastructure of an IXP is usually a network of switches located either in the same physical location or distributed over a region or even at a global scale. Typically, the infrastructure has a fully redundant switching fabric that provides fault tolerance. The equipment is usually located in facilities such as data centers, which provide reliability, sufficient power, and physical security.

For example, in the figure below we see an IXP infrastructure (2012), called DE-CIX that is located in Frankfurt, Germany. The figure shows the core of the infrastructure (noted as 3 and 6) and additional sites (1-4 and 7) that are located at different colocation facilities in the area.

ASes Peering at IXPs-1

Why have IXPs become increasingly popular, and why are they important to study?

Some of the most important reasons include:

IXPs are interconnection hubs handling large traffic volumes: A 2012 study by Ager et al. analyzed a large European IXP and showed the presence of more than 50,000 actively used peering links! For some large IXPs (mostly located in Europe), the daily traffic volume is comparable to that of global Tier 1 ISPs.

An important role in mitigating DDoS attacks: As IXPs have become increasingly popular interconnection hubs, they can observe the traffic to/from an increasing number of participant ASes. In this role, IXPs can play the role of a “shield” to mitigate DDoS attacks and stop the DDoS traffic before it hits a participant AS. As a result, there are many DDoS events that IXPs have mitigated. For example, back in March 2013, a massive DDoS attack took place that involved Spamhaus, Stophaus, and CloudFare. Lesson 9 Internet Security will look into specific techniques that IXPs use to mitigate DDoS based on BGP blackholing.  
“Real-world” infrastructures with a plethora of research opportunities: IXPs play an important role in today’s Internet infrastructure. Studying this peering ecosystem, the end-to-end flow of network traffic, and the traffic that traverses these facilities can help us understand how the Internet landscape is changing. IXPs also provide an excellent “research playground” for multiple applications. Such as security applications. For example, BGP blackholing for DDoS mitigation or applications for Software Defined Networking.
IXPs are active marketplaces and technology innovation hubs: IXPs are active marketplaces, especially in North America and Europe. They provide an expanding list of services that go beyond interconnection. Most notably are DDoS mitigation and SDN-based services. As a result, IXPs have been evolving from interconnection hubs to technology innovation hubs.

What are the steps for an AS to peer at an IXP?

Each participating network must have a public Autonomous System Number (ASN). Each participant brings a router to the IXP facility (or one of its locations if the IXP has an infrastructure distributed across multiple data centers) and connects one of its ports to the IXP switch. The router of each participant must be able to run BGP since the exchange of routes across the IXP is via BGP only. In addition, each participant must agree to the IXP’s General Terms and Conditions (GTC).

Two networks may publicly peer at IXP by using the IXP infrastructure to establish a connection for exchanging traffic according to their own requirements and business relationships. But, first, each network incurs a one-time cost to establish a circuit from the premises to the IXP. Then, there is a monthly charge for using a chosen IXP port, where higher port speeds are more expensive. The entity that owns and operates the IXP might also charge an annual membership fee. In particular, exchanging traffic over an established public peering link at an IXP is in principle “settlement-free” (i.e., involves no form of payment between the two parties) as IXPs typically do not charge for exchanged traffic volume. Moreover, IXPs usually do not interfere with the bilateral relationships between the IXP’s participants unless they violate the GTC. For example, the two parties of an existing IXP peering link are free to use that link in ways that involve paid peering. Other networks may even offer transit across an IXP’s switching fabric. Depending on the IXP, the time it takes to establish a public peering link can range from a few days to a couple of weeks.

Why do networks choose to peer at IXPs?

They are keeping local traffic local. In other words, the traffic exchanged between two networks do not need to travel unnecessarily through other networks if both networks are participants in the same IXP facility.  
Lower costs. Typically peering at an IXP is offered at a lower cost than relying on third parties to transfer the traffic, which is charged based on volume.
Network performance is improved due to reduced delay.
Incentives. Critical players in today’s Internet ecosystem often “incentivize” other networks to connect at IXPs. For example, a prominent content provider may require another network to be present at a specific IXP or IXPS in order to peer with them.

What services are offered at IXPs?

Public peering: The most well-known use of IXPs is public peering service, in which two networks use the IXP’s network infrastructure to establish a connection to exchange traffic based on their bilateral relations and traffic requirements. The costs required to set up this connection are a one-time cost for establishing the connection, the monthly charge for using the chosen IXP port (those with higher speeds are more expensive), and perhaps an annual fee of membership in the entity owning and operating the IXP. However, the IXPs do not usually charge based on the amount of exchanged volume. They also do not usually interfere with bilateral relations between the participants unless there is a violation of the GTC. Even with the set-up costs, IXPs are generally cheaper than other conventional methods of exchanging traffic (such as relying on third parties which charge based on the volume of exchanged traffic). IXP participants also often experience better network performance and Quality-of-Service (QoS) because of reduced delays and routing efficiencies. In addition, many companies that are significant players in the Internet space (such as Google) incentivize other networks to connect at IXPs by making it a requirement to peering with them.

Private peering: Most operational IXPs also provide a private peering service (Private Interconnects, or PIs) that allows direct traffic exchange between the two parties, and doesn’t use the IXP’s public peering infrastructure. This is commonly used when the participants want a well-provisioned, dedicated link capable of handling high-volume, bidirectional, and relatively stable traffic.

Route servers and Service level agreements: Many IXPs also include service level agreements (SLAs) and free use of the IXP’s route servers for participants. This allows participants to arrange instant peering with many co-located participant networks using essentially a single agreement/BGP session.

Remote peering through resellers: Another popular service is IXP reseller/partner programs. Third parties resell IXP ports wherever they have infrastructure connected to the IXP. These third parties can offer the IXP’s service remotely, which will enable networks that have little traffic also to use the IXP. This also enables remote peering, where networks in distant geographic areas can use the IXP.

Mobile peering: Some IXPs also provide support for mobile peering, which is a scalable solution for the interconnection of mobile GPRS/3G networks.

DDoS blackholing: A few IXPs support customer-triggered blackholing, which allows users to alleviate the effects of DDoS attacks against their network.
Free value-added services: In the interest of ‘good of the Internet’, a few IXPs such as Scandinavian IXP Netnod offer free value-added services like Internet Routing Registry (IRR), consumer broadband speed tests9, DNS root name servers, country-code top-level domain (ccTLD) nameservers, as well as distribution of the official local time through NTP.

### Peering at IXPs: How Does a Route Server Work?

Generally, two ASes exchange traffic through the switching fabric utilize a two-way BGP session, called a `bilateral BGP` session. However, since many ASes are peering at an IXP, we have another challenge to accommodate a rising number of BGP sessions. As a result, this option does not scale with many participants. To mitigate this, some IXPs operate a route server, which helps to make peering more manageable. In summary, a Route Server (RS) does the following:

It `collects and shares routing information` from its peers or participants of the IXP that connect to the RS.
It executes its `own BGP decision process and re-advertises` the resulting information (e.g., best route selection) to all RS's peer routers.

The figure below shows a `multi-lateral BGP` peering session, an RS that facilitates and manages how multiple ASes can "talk" on the control plane simultaneously.

How does a route server (RS) maintain multi-lateral peering sessions?

Let's look at a modern route server architecture in the figure below to understand how it works. A typical routing daemon maintains a `Routing Information Base (RIB)`, which contains **all BGP paths that it receives from its peers - the Master RIB.** In addition, the route server also maintains AS-specific RIBs to keep track of the individual BGP sessions they maintain with each participant AS.

Route servers maintain two types of route filters.

`Import filters `are applied to ensure that each member AS only advertises routes that it should advertise. And `export filters` are typically triggered by the IXP members themselves to restrict the set of other IXP member ASes that receive their routes. Let's look at an example where AS X and AS Z exchange routes through a multi-lateral peering session that the route server holds. The steps are as follows:

In the first step, AS X advertises a prefix p1 to the RS, which is added to the route server's RIB specific to AS X.
The route server uses the peer-specific import filter to check whether AS X is allowed to advertise p1. If it passes the filter, the prefix p1 is added to the Master RIB.
The route server applies the peer-specific export filter to check if AS X allows AS Z to receive p1, and if true, it adds that route to the AS Z-specific RIB.
Lastly, the route server advertises p1 to AS Z with AS X as the next hop.
BIRD Route Server
