import numpy as np
import sympy as sp

comp_names, comp_nd1, comp_nd2, comp_values = [], [], [], []
solved_voltages = []
file_name = 'Circuit_Simulator_Current_Supply'
np.set_printoptions(suppress=True)

# IMPORTANT STIPULATION FOR MAKING THE NETLIST: MAKE SURE THAT THE GROUND NODE IS ZERO PLEASE, THINGS ARE MORE PRONE
# TO BREAKING IF YOU DO NOT MAKE SURE THAT NODE ZERO IS THE GROUND NODE

# ALSO PLEASE MAKE SURE THAT THE NODES ARE IN ASCENDING ORDER, I.E. IF THE HIGHEST NODE VALUE IS 4 AND THE LOWEST IS
# 0, MAKE SURE THERE ARE AT LEAST 4 COMPONENTS THAT CONNECT TO NODE 1, 2, 3, and 4 THAT COMPLETE A LOOP TO NODE ZERO.

# Function that reads the number of lines within the netlist for list size in other functions
def netlist_numlines():
    f = open(file_name)
    lines = f.readlines()
    total_lines = len(lines)
    f.close()
    # Return statement returns the value of listed variable as though the function is equal to those variables
    return total_lines, lines

# Function that will read the values of the netlist and will execute if statements based off data received from reading
# the .txt file
def netlist_reading():
    total_lines, lines = netlist_numlines()
    # For loop that tests if the component is a resistor, voltage source, or current source, and does a process
    # accordingly
    for i in range(0, total_lines):
        if 'V' in lines[i]:
            voltage_data = lines[i].split()
            comp_names.append(voltage_data[0])
            comp_nd1.append(voltage_data[1])
            comp_nd2.append(voltage_data[2])
            comp_values.append(voltage_data[3])
        elif 'R' in lines[i]:
            resistor_data = lines[i].split()
            comp_names.append(resistor_data[0])
            comp_nd1.append(resistor_data[1])
            comp_nd2.append(resistor_data[2])
            comp_values.append(resistor_data[3])
        elif 'I' in lines[i]:
            current_data = lines[i].split()
            comp_names.append(current_data[0])
            comp_nd1.append(current_data[1])
            comp_nd2.append(current_data[2])
            comp_values.append(current_data[3])
        elif lines[i] == '\n':
            count = 0
        elif lines[i] == '==============================================\n':
            return
        else:
            return print('Make sure your components are correctly typed in the netlist')
def simultaneous_equations_setup():
    if max(comp_nd1) > max(comp_nd2):
        max_value = int(max(comp_nd1))
    else:
        max_value = int(max(comp_nd2))
    if min(comp_nd1) > min(comp_nd2):
        min_value = int(min(comp_nd2))
    else:
        min_value = int(min(comp_nd1))
    # for loop that makes the last known voltage source in the
    for i in range(0, np.size(comp_names)):
        if comp_nd1[i] > comp_nd2[i]:
            temp_var = comp_nd2[i]
            comp_nd2[i] = comp_nd1[i]
            comp_nd1[i] = temp_var
    currentsupp_case_statement = 0
    voltsupp_case_statement = 0
    for i in range(0, 1000):
        print(i)
        if 'V'+str(i) in comp_names:
            nd = comp_names.index('V'+str(i))
            voltsupp_nodes = [comp_nd1[nd], comp_nd2[nd]]
            voltsupp_voltage = comp_values[nd]
            voltsupp_active_node = max(voltsupp_nodes)
            comp_names.pop(nd), comp_nd2.pop(nd), comp_nd1.pop(nd), comp_values.pop(nd)
            solved_voltages.append(int(voltsupp_voltage))
            voltsupp_case_statement = 1
            break
        elif 'I'+str(i) in comp_names:
            nd = comp_names.index('I' + str(i))
            currentsupp_nodes = [comp_nd1[nd], comp_nd2[nd]]
            currentsupp_current = int(comp_values[nd])
            currentsupp_active_node = max(currentsupp_nodes)
            comp_names.pop(nd), comp_nd2.pop(nd), comp_nd1.pop(nd), comp_values.pop(nd)
            # solved_currents.append(int(currentsupp_current))
            currentsupp_case_statement = 1
            break
    if voltsupp_case_statement == 1:
        equation_matrix = np.zeros([max_value - min_value - 1, max_value - min_value])
        print(equation_matrix)
        for i in range(0, np.size(comp_names)):
            if comp_nd1[i] == str(min_value):
                equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] + \
                    1 / int(comp_values[i])
            elif comp_nd1[i] == str(voltsupp_active_node):
                equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] + \
                    1 / int(comp_values[i])
                equation_matrix[int(comp_nd2[i]) - min_value - 2][len(equation_matrix)] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 2][len(equation_matrix)] + \
                    1 * int(voltsupp_voltage) / int(comp_values[i])
            else:
                equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] + \
                    1 / int(comp_values[i])
                equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 2] = \
                    equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 2] + \
                    1 / int(comp_values[i])
                equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 3] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 3] - \
                    1 / int(comp_values[i])
                equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 1] = \
                    equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 1] - \
                    1 / int(comp_values[i])
    elif currentsupp_case_statement == 1:
        equation_matrix = np.zeros([max_value - min_value, max_value - min_value + 1])
        for i in range(0, np.size(comp_names)):
            if comp_nd1[i] == str(min_value):
                equation_matrix[int(comp_nd2[i]) - min_value - 1][int(comp_nd2[i]) - min_value - 1] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 1][int(comp_nd2[i]) - min_value - 1] + \
                    1 / int(comp_values[i])
            elif comp_nd1[i] == str(currentsupp_active_node):
                equation_matrix[int(comp_nd2[i]) - min_value - 1][int(comp_nd2[i]) - min_value - 1] = \
                    equation_matrix[int(comp_nd2[i]) - min_value - 1][int(comp_nd2[i]) - min_value - 1] + \
                    1 / int(comp_values[i])
                print(int(comp_nd2[i]) - min_value - 2)
                print(equation_matrix[int(comp_nd2[i]) - min_value - 2][len(equation_matrix)])
                if (int(comp_nd2[i]) - min_value - 2) == min_value and
                    equation_matrix[int(comp_nd2[i]) - min_value - 2][len(equation_matrix)] = \
                    -1 * currentsupp_current
            # else:
            #     # equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] = \
            #     #     equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 2] + \
            #     #     1 / int(comp_values[i])
            #     # equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 2] = \
            #     #     equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 2] + \
            #     #     1 / int(comp_values[i])
            #     # equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 3] = \
            #     #     equation_matrix[int(comp_nd2[i]) - min_value - 2][int(comp_nd2[i]) - min_value - 3] - \
            #     #     1 / int(comp_values[i])
            #     # equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 1] = \
            #     #     equation_matrix[int(comp_nd1[i]) - min_value - 2][int(comp_nd1[i]) - min_value - 1] - \
            #     #     1 / int(comp_values[i])
        print(equation_matrix)
        return print('This has a current supply')
    if len(equation_matrix) == 1:
        m = sp.Matrix(equation_matrix).rref()[0]
        solved_voltages.append(m)
        print(m[1])
    else:
        m = sp.Matrix(equation_matrix).rref()[0]
        print(m)
        for i in range(0, len(equation_matrix)):
            solved_voltages.append(m[len(equation_matrix)+i*len(equation_matrix[0])])
            print(m[len(equation_matrix)+i*len(equation_matrix[0])])
    return voltsupp_active_node, voltsupp_voltage

def netlistdata_writing():
    voltsupp_active_node, voltsupp_voltage = simultaneous_equations_setup()
    if max(comp_nd1) > max(comp_nd2):
        max_value = int(max(comp_nd1))
    else:
        max_value = int(max(comp_nd2))
    if min(comp_nd1) > min(comp_nd2):
        min_value = int(min(comp_nd2))
    else:
        min_value = int(min(comp_nd1))
    f = open(file_name, 'r')
    lines = f.readlines()
    total_lines = len(lines)
    f.close()
    f = open(file_name, 'w')
    case_statement = 0
    for i in range(0, total_lines):
        if lines[i] == '==============================================\n':
            # f = open('Circuit_Simulator.txt', 'w')
            for i_ in range(0, i):
                f.write(lines[i_])
            case_statement = 1
            break
    if case_statement == 0:
        for i_ in range(0, total_lines):
            f.write(lines[i_])
        f.write('\n')
    f.close()
    f = open(file_name,'a')
    branch_lines = '=============================================='+ '\n' + '               branch quantities' +\
        '\n' + '=============================================='
    f.write(branch_lines)
    comp_power = 0
    comp_voltage = 0
    comp_current = 0
    for i in range(0, np.size(comp_names)):
        if comp_nd1[i] == str(min_value):
            comp_voltage = solved_voltages[int(comp_nd2[i])-1]
            comp_current = comp_voltage / int(comp_values[i])
            comp_power = comp_voltage * comp_current
            f.write('\n'+f'p({comp_names[i]}) =     {comp_power:.5f} W'+'\n'+f'v({comp_names[i]}) =     {comp_voltage:.5f} V'
                    +'\n'+f'i({comp_names[i]}) =     {comp_current:.5f} A'+'\n'+
                    '----------------------------------------------')
        elif comp_nd1[i] == str(voltsupp_active_node):
            comp_voltage = int(voltsupp_voltage) - solved_voltages[(int(comp_nd2[i]) - 1)]
            comp_current = comp_voltage / int(comp_values[i])
            comp_power = comp_voltage * comp_current
            f.write(
                '\n' + f'p({comp_names[i]}) =     {comp_power:.5f} W' + '\n' + f'v({comp_names[i]}) =     {comp_voltage:.5f} V'
                + '\n' + f'i({comp_names[i]}) =     {comp_current:.5f} A' + '\n' +
                '----------------------------------------------')
        else:
            comp_voltage = solved_voltages[(int(comp_nd1[i])) - 1] - solved_voltages[(int(comp_nd2[i])) - 1]
            comp_current = comp_voltage / int(comp_values[i])
            comp_power = comp_voltage * comp_current
            f.write(
                '\n' + f'p({comp_names[i]}) =     {comp_power:.5f} W' + '\n' + f'v({comp_names[i]}) =     {comp_voltage:.5f} V'
                + '\n' + f'i({comp_names[i]}) =     {comp_current:.5f} A' + '\n' +
                '----------------------------------------------')
def main():
    netlist_reading()
    # The below function should only be called when testing for the actual function, it serves no purpose when
    # called here and breaks things otherwise

    simultaneous_equations_setup()

    # netlistdata_writing()
    print(comp_names, comp_nd1, comp_nd2, comp_values)
main()