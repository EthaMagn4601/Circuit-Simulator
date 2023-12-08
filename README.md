# Circuit-Simulator

A FEW IMPORTANT STIPULATIONS SHOULD BE MADE CLEAR OF THE CIRCUIT SIMULATOR BEFORE USAGE:

1. DEFINING THE NETLIST SHOULD BE OF THE FORM (component_name, node_a, node_b, component_value), where the component's name should be "V", "R", or "I", node_a = any value, node_b = any value, and component_value = any value respective to the component's base respective units
(i.e. don't use 12A expecting 12000 ohms a component named "R3", things will not look right at all).

2. WHEN DEFINING THE NETLIST VALUES MAKE SURE THAT THE GROUND NODE IS ZERO PLEASE, THINGS ARE MORE PRONE TO BREAKING IF YOU DO NOT MAKE SURE THAT NODE ZERO IS THE GROUND NODE.

3. ALSO PLEASE MAKE SURE THAT THE NODES ARE IN ASCENDING ORDER, I.E. IF THE HIGHEST NODE VALUE IS 4 AND THE LOWEST IS 0, MAKE SURE THERE ARE AT LEAST 4 COMPONENTS THAT CONNECT TO NODE 1, 2, 3, and 4 THAT COMPLETE A LOOP TO NODE ZERO.