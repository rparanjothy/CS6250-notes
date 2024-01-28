class Switch:
    def __init__(self, name):
        self.name = str(name)
        self.ports = {}
        self.root_bridge = None
        self.root_distance = float('inf')

    def add_port(self, port_name, connected_switch):
        self.ports[port_name] = {'connected_switch': connected_switch, 'cost': 1}

    def update_root_bridge(self, new_root_bridge, new_distance):
        if new_distance < self.root_distance:
            self.root_bridge = new_root_bridge
            self.root_distance = new_distance
            print(f"{self.name} updated root bridge to {new_root_bridge.name} with distance {new_distance}")
    
    def __repr__(self) -> str:
        return str([self.name,self.root_bridge,self.root_distance])
        # self.name

def simulate_stp(network_topology):
    switches = {name: Switch(name) for name in network_topology.keys()}

    for switch_name, destinations in network_topology.items():
        switch = switches[switch_name]
        for port_name, destination in enumerate(destinations):
            switch.add_port(f'Port_{port_name}', switches[destination])

    for switch in switches.values():
        print(f"{switch.name} connected to {', '.join(port['connected_switch'].name for port in switch.ports.values())}")

    # Simulate STP
    for _ in range(1):  # Simulate three rounds of STP (you may need more in real scenarios)
        for switch in switches.values():
            for port_name, port in switch.ports.items():
                destination_switch = port['connected_switch']
                if destination_switch.root_bridge is None or switch.root_bridge is None:
                    destination_switch.update_root_bridge(switch, switch.root_distance + port['cost'])
                    print(destination_switch)
                elif switch.root_bridge.name != destination_switch.root_bridge.name:
                    if switch.root_distance + port['cost'] < destination_switch.root_distance:
                        destination_switch.update_root_bridge(switch, switch.root_distance + port['cost'])

if __name__ == "__main__":
    network_topology_with_loops = { 
        1 : [2, 5],
         2 : [1, 3, 6],
         3 : [2, 7, 4],
         4 : [3, 8],
         5 : [1, 6, 9],
         6 : [2, 5, 7, 10],
         7 : [3, 6, 11, 8],
         8 : [4, 7, 12],
         9 : [5, 10],
         10: [6, 9, 11, 13],
         11: [7, 10, 12, 13],
         12: [8, 11],
         13: [10, 11] }
    simulate_stp(network_topology_with_loops)
