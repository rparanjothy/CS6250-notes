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

- Logical connection btwn 2 m/c in different n/w and diff location happens thru the `TRANSPORT` layer
