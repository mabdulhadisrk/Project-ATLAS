
# Project ATLAS
# Day 1 - Task 3

registers = {
    "R1": 0,
    "R2": 0,
    "R3": 0
}

program = [
    ("LOAD", "R1", 15),
    ("LOAD", "R2", 25),
    ("ADD", "R3", "R1", "R2"),
    ("LOAD", "R1", 100),
    ("ADD", "R2", "R3", "R1")
]


def execute_instruction(instruction):

    operation = instruction[0]

    if operation == "LOAD":
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


pc = 0

while pc < len(program):

    instruction = program[pc]

    execute_instruction(instruction)

    pc += 1


print("Final Register State:")

for register, value in registers.items():
    print(register, "=", value)
