
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
    branch_instructions = 0
    branches_taken = 0

    while pc < len(program):

        instruction = program[pc]
        operation = instruction[0]

        next_pc = execute_instruction(
            instruction, pc, registers, memory
        )

        cycles += instruction_cycles[operation]
        instructions_executed += 1

        if operation in ("BEQ", "BNE"):
            branch_instructions += 1

            if next_pc != pc + 1:
                branches_taken += 1

        pc = next_pc

    cpi = cycles / instructions_executed
    ipc = instructions_executed / cycles

    return {
        "instructions": instructions_executed,
        "cycles": cycles,
        "cpi": cpi,
        "ipc": ipc,
        "branches": branch_instructions,
        "taken": branches_taken
    }


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


# Workload 3: Branch-heavy
branch_program = [
    ("LOADI", "R1", 10),
    ("LOADI", "R2", 20),
    ("BEQ", "R1", "R2", 5),
    ("ADD", "R3", "R1", "R2"),
    ("BNE", "R1", "R2", 6),
    ("LOADI", "R3", 100),
    ("ADD", "R3", "R3", "R1")
]


workloads = {
    "COMPUTE-HEAVY": compute_program,
    "MEMORY-HEAVY": memory_program,
    "BRANCH-HEAVY": branch_program
}


print("ATLAS WORKLOAD COMPARISON")
print("=========================")

for name, program in workloads.items():

    result = run_program(program)

    print("\n" + name)
    print("Instructions:", result["instructions"])
    print("Clock Cycles:", result["cycles"])
    print("CPI:", round(result["cpi"], 2))
    print("IPC:", round(result["ipc"], 2))
    print("Branch Instructions:", result["branches"])
    print("Branches Taken:", result["taken"])
