
def execute_instruction(instruction, pc, registers, memory):

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
        raise ValueError("Unknown instruction: " + operation)

    return pc + 1


instruction_cycles = {
    "LOADI": 1,
    "ADD": 1,
    "SUB": 1,
    "BEQ": 1,
    "BNE": 1,
    "LOAD": 3,
    "STORE": 3
}


def run_program(program):

    registers = {
        "R1": 0,
        "R2": 0,
        "R3": 0
    }

    memory = {}

    pc = 0
    cycles = 0
    instructions_executed = 0

    while pc < len(program):

        instruction = program[pc]

        pc = execute_instruction(
            instruction, pc, registers, memory
        )

        cycles += instruction_cycles[instruction[0]]
        instructions_executed += 1

    cpi = cycles / instructions_executed
    ipc = instructions_executed / cycles

    return instructions_executed, cycles, cpi, ipc


# Workload 1: Compute-heavy
compute_program = [
    ("LOADI", "R1", 10),
    ("LOADI", "R2", 20),
    ("ADD", "R3", "R1", "R2"),
    ("ADD", "R3", "R3", "R1"),
    ("SUB", "R2", "R3", "R1")
]


# Workload 2: Memory-heavy
memory_program = [
    ("LOADI", "R1", 10),
    ("STORE", "R1", 100),
    ("LOAD", "R2", 100),
    ("STORE", "R2", 200),
    ("LOAD", "R3", 200)
]


# Run both workloads
compute_results = run_program(compute_program)
memory_results = run_program(memory_program)


# Display comparison
print("ATLAS WORKLOAD COMPARISON")
print("=========================")

print("\nCOMPUTE-HEAVY WORKLOAD")
print("Instructions:", compute_results[0])
print("Clock Cycles:", compute_results[1])
print("CPI:", round(compute_results[2], 2))
print("IPC:", round(compute_results[3], 2))

print("\nMEMORY-HEAVY WORKLOAD")
print("Instructions:", memory_results[0])
print("Clock Cycles:", memory_results[1])
print("CPI:", round(memory_results[2], 2))
print("IPC:", round(memory_results[3], 2))
