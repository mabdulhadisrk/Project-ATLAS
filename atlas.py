
registers = {
    "R1": 0,
    "R2": 0,
    "R3": 0
}

memory = {}

program = [
    ("LOADI", "R1", 10),
    ("STORE", "R1", 100),
    ("LOAD", "R2", 100),
    ("ADD", "R3", "R1", "R2")
]


def execute_instruction(instruction, pc):

    operation = instruction[0]

    if operation == "LOADI":
        destination = instruction[1]
        value = instruction[2]
        registers[destination] = value

    elif operation == "ADD":
        destination = instruction[1]
        source1 = instruction[2]
        source2 = instruction[3]
        registers[destination] = registers[source1] + registers[source2]

    elif operation == "SUB":
        destination = instruction[1]
        source1 = instruction[2]
        source2 = instruction[3]
        registers[destination] = registers[source1] - registers[source2]

    elif operation == "STORE":
        source = instruction[1]
        address = instruction[2]
        memory[address] = registers[source]

    elif operation == "LOAD":
        destination = instruction[1]
        address = instruction[2]
        registers[destination] = memory[address]

    elif operation == "BEQ":
        source1 = instruction[1]
        source2 = instruction[2]
        target = instruction[3]

        if registers[source1] == registers[source2]:
            return target

    elif operation == "BNE":
        source1 = instruction[1]
        source2 = instruction[2]
        target = instruction[3]

        if registers[source1] != registers[source2]:
            return target

    else:
        print("Unknown instruction:", operation)

    return pc + 1


# Assumed cycle costs for each instruction
instruction_cycles = {
    "LOADI": 1,
    "ADD": 1,
    "SUB": 1,
    "BEQ": 1,
    "BNE": 1,
    "LOAD": 3,
    "STORE": 3
}


# Execute program and track cycles
pc = 0
cycles = 0

while pc < len(program):
    instruction = program[pc]

    pc = execute_instruction(instruction, pc)

    cycles += instruction_cycles[instruction[0]]


# Display results
print("Total Clock Cycles:", cycles)

print("Final Register State:")

for register, value in registers.items():
    print(register, "=", value)

print("Final Memory State:", memory)
