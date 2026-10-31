
# PROJECT ATLAS
# Memory Instructions

registers = {
    "R1": 0,
    "R2": 0,
    "R3": 0
}

memory = {}

program = [
    ("LOADI", "R1", 15),
    ("LOADI", "R2", 25),
    ("ADD", "R3", "R1", "R2"),
    ("STORE", "R3", 100),
    ("LOAD", "R1", 100)
]


def execute_instruction(instruction):

    operation = instruction[0]

    if operation == "LOADI":
        destination = instruction[1]
        value = instruction[2]
        registers[destination] = value

    elif operation == "ADD":
        destination = instruction[1]
        source1 = instruction[2]
        source2 = instruction[3]

        registers[destination] = (
            registers[source1] + registers[source2]
        )

    elif operation == "SUB":
        destination = instruction[1]
        source1 = instruction[2]
        source2 = instruction[3]

        registers[destination] = (
            registers[source1] - registers[source2]
        )

    elif operation == "STORE":
        source = instruction[1]
        address = instruction[2]
        memory[address] = registers[source]

    elif operation == "LOAD":
        destination = instruction[1]
        address = instruction[2]
        registers[destination] = memory[address]

    else:
        print("Unknown instruction:", operation)


pc = 0

while pc < len(program):
    instruction = program[pc]
    execute_instruction(instruction)
    pc += 1


print("Final Register State:")

for register, value in registers.items():
    print(register, "=", value)

print("Final Memory State:", memory)
