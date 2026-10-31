
# PROJECT ATLAS
# Sprint 14: Workload-Based Architecture Experiments
# Five-stage pipeline: IF, ID, EX, MEM, WB
# Compare execution with and without ALU-result forwarding.

pipeline_stages = ["IF", "ID", "EX", "MEM", "WB"]


# --------------------------------------------------
# 1. DEFINE WORKLOADS
# --------------------------------------------------

workloads = {

    "Independent": [
        ("ADD", "R1", "R2", "R3"),
        ("SUB", "R4", "R5", "R6"),
        ("ADD", "R7", "R8", "R9"),
        ("SUB", "R10", "R11", "R12"),
        ("ADD", "R13", "R14", "R15")
    ],

    "Dependency-heavy": [
        ("ADD", "R1", "R2", "R3"),
        ("ADD", "R4", "R1", "R5"),
        ("SUB", "R6", "R4", "R7"),
        ("ADD", "R8", "R6", "R9"),
        ("SUB", "R10", "R8", "R11")
    ],

    "Mixed": [
        ("ADD", "R1", "R2", "R3"),
        ("SUB", "R4", "R5", "R6"),
        ("ADD", "R7", "R1", "R4"),
        ("SUB", "R8", "R7", "R9"),
        ("ADD", "R10", "R11", "R12")
    ]
}


# --------------------------------------------------
# 2. INSTRUCTION INFORMATION
# --------------------------------------------------

def get_destination(instruction):

    operation = instruction[0]

    if operation in ("ADD", "SUB"):
        return instruction[1]

    return None


def get_sources(instruction):

    operation = instruction[0]

    if operation in ("ADD", "SUB"):
        return [instruction[2], instruction[3]]

    return []


# --------------------------------------------------
# 3. PIPELINE SIMULATOR
# --------------------------------------------------

def simulate_pipeline(program, forwarding_enabled):

    stages = {
        "IF": 0,
        "ID": None,
        "EX": None,
        "MEM": None,
        "WB": None
    }

    next_instruction = 1
    cycle = 0
    total_stalls = 0

    history = {
        index: []
        for index in range(len(program))
    }

    while any(value is not None for value in stages.values()):

        cycle += 1

        # Detect RAW hazards for the instruction in ID.
        stalled = False

        consumer_index = stages["ID"]

        if consumer_index is not None:

            consumer_sources = get_sources(
                program[consumer_index]
            )

            # Check producers currently in EX and MEM.
            producers = [
                stages["EX"],
                stages["MEM"]
            ]

            for producer_index in producers:

                if producer_index is None:
                    continue

                producer = program[producer_index]

                destination = get_destination(producer)

                if (
                    destination is not None
                    and destination in consumer_sources
                ):

                    if not forwarding_enabled:
                        stalled = True
                        break

        if stalled:
            total_stalls += 1

        # Record current pipeline state.
        for stage_name in pipeline_stages:

            instruction_index = stages[stage_name]

            if instruction_index is not None:

                label = stage_name

                if stage_name == "ID" and stalled:
                    label = "ID*"

                history[instruction_index].append(
                    (cycle, label)
                )

        # Advance pipeline stages.
        next_stages = {
            "IF": None,
            "ID": None,
            "EX": None,
            "MEM": stages["EX"],
            "WB": stages["MEM"]
        }

        if stalled:

            # Hold Fetch and Decode.
            next_stages["IF"] = stages["IF"]
            next_stages["ID"] = stages["ID"]

            # EX receives a bubble.

        else:

            next_stages["EX"] = stages["ID"]
            next_stages["ID"] = stages["IF"]

            # Fetch next instruction.
            if next_instruction < len(program):

                next_stages["IF"] = next_instruction
                next_instruction += 1

        stages = next_stages

    total_instructions = len(program)

    return {
        "instructions": total_instructions,
        "cycles": cycle,
        "stalls": total_stalls,
        "cpi": cycle / total_instructions,
        "ipc": total_instructions / cycle,
        "history": history
    }


# --------------------------------------------------
# 4. RUN ALL WORKLOAD EXPERIMENTS
# --------------------------------------------------

results = {}

for workload_name, program in workloads.items():

    without_forwarding = simulate_pipeline(
        program,
        False
    )

    with_forwarding = simulate_pipeline(
        program,
        True
    )

    results[workload_name] = {
        "without": without_forwarding,
        "with": with_forwarding
    }


# --------------------------------------------------
# 5. DISPLAY WORKLOADS
# --------------------------------------------------

print("PROJECT ATLAS")
print("WORKLOAD EXPERIMENTS")
print("====================")

for workload_name, program in workloads.items():

    print(f"\n{workload_name.upper()} WORKLOAD")

    for index, instruction in enumerate(program):
        print(f"I{index + 1}: {instruction}")


# --------------------------------------------------
# 6. PERFORMANCE COMPARISON
# --------------------------------------------------

print("\n\nPERFORMANCE COMPARISON")
print("======================")

print(
    f"{'Workload':<20}"
    f"{'No Fwd Cycles':<16}"
    f"{'Fwd Cycles':<14}"
    f"{'No Fwd Stalls':<16}"
    f"{'Fwd Stalls':<13}"
)

for workload_name, result in results.items():

    without = result["without"]
    with_fwd = result["with"]

    print(
        f"{workload_name:<20}"
        f"{without['cycles']:<16}"
        f"{with_fwd['cycles']:<14}"
        f"{without['stalls']:<16}"
        f"{with_fwd['stalls']:<13}"
    )


# --------------------------------------------------
# 7. DETAILED METRICS
# --------------------------------------------------

print("\n\nDETAILED PERFORMANCE METRICS")
print("============================")

for workload_name, result in results.items():

    without = result["without"]
    with_fwd = result["with"]

    cycles_saved = without["cycles"] - with_fwd["cycles"]

    improvement = (
        cycles_saved / without["cycles"]
    ) * 100

    print(f"\n{workload_name.upper()}")

    print(
        "Without forwarding: "
        f"Cycles={without['cycles']}, "
        f"Stalls={without['stalls']}, "
        f"CPI={without['cpi']:.2f}, "
        f"IPC={without['ipc']:.3f}"
    )

    print(
        "With forwarding:    "
        f"Cycles={with_fwd['cycles']}, "
        f"Stalls={with_fwd['stalls']}, "
        f"CPI={with_fwd['cpi']:.2f}, "
        f"IPC={with_fwd['ipc']:.3f}"
    )

    print("Cycles saved:", cycles_saved)
    print("Cycle reduction:", round(improvement, 2), "%")


# --------------------------------------------------
# 8. DISPLAY ONE DETAILED PIPELINE SCHEDULE
# --------------------------------------------------

selected_workload = "Dependency-heavy"

print("\n\nDETAILED PIPELINE SCHEDULE")
print("==========================")
print("Workload:", selected_workload)

program = workloads[selected_workload]

for configuration, forwarding in [
    ("WITHOUT FORWARDING", False),
    ("WITH FORWARDING", True)
]:

    schedule = simulate_pipeline(program, forwarding)

    print(f"\n{configuration}")
    print("-" * len(configuration))

    print(f"{'Instruction':<16}", end="")

    for current_cycle in range(1, schedule["cycles"] + 1):
        print(f"{current_cycle:^9}", end="")

    print()

    for index in range(len(program)):

        row = [""] * schedule["cycles"]

        for current_cycle, label in schedule["history"][index]:
            row[current_cycle - 1] = label

        print(f"I{index + 1:<15}", end="")

        for stage in row:
            print(f"{stage:^9}", end="")

        print()


# --------------------------------------------------
# 9. MODEL ASSUMPTIONS
# --------------------------------------------------

print("\n\nSIMULATION ASSUMPTIONS")
print("======================")

print("Pipeline stages: IF, ID, EX, MEM, WB")
print("Instruction types: ADD and SUB")
print("Forwarding: ALU-result forwarding")
print("Memory operations: Not yet modelled")
print("Branch instructions: Not yet modelled")
print("Register writes: Visible to ID during WB cycle")
print("Pipeline model: Simplified cycle-by-cycle model")
