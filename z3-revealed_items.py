from z3 import *
import random

# Simulated parameters
num_items = 10  # Number of items to allocate
random.seed(42)  # Seed for reproducibility

# List of items
items = [f"item_{i}" for i in range(num_items)]

# Random utility functions for agents A1 and A2
u_A1 = {item: random.randint(1, 20) for item in items}  # Random utilities for A1
u_A2 = {item: random.randint(1, 20) for item in items}  # Random utilities for A2

# Print utilities for debugging
print("Agent A1's utilities:", u_A1)
print("Agent A2's utilities:", u_A2)

# Simulate Turing machine outputs
tm_A = sorted(items, key=lambda item: u_A1[item], reverse=True)  # TM A: decreasing utility for A1
tm_B = sorted(items, key=lambda item: u_A2[item], reverse=True)  # TM B: decreasing utility for A2

# Merge outputs from TM A and TM B, maintaining order
revealed_items = []
seen_items = set()
for i in range(max(len(tm_A), len(tm_B))):
    if i < len(tm_A) and tm_A[i] not in seen_items:
        revealed_items.append(tm_A[i])
        seen_items.add(tm_A[i])
    if i < len(tm_B) and tm_B[i] not in seen_items:
        revealed_items.append(tm_B[i])
        seen_items.add(tm_B[i])

print("\nRevealed Item Order:", revealed_items)

# Z3 variables for allocation
x = {item: Int(f"x_{item}") for item in items}  # 0 for A1, 1 for A2

# Initialize Z3 solver
solver = Solver()

# Fixed assignment constraint: Every item must be assigned to one agent
for item in items:
    solver.add(Or(x[item] == 0, x[item] == 1))

# Compute utilities for each agent
U_A1 = Sum([If(x[item] == 0, u_A1[item], 0) for item in items])
U_A2 = Sum([If(x[item] == 1, u_A2[item], 0) for item in items])

# Add global EFX constraints
for item in items:
    solver.add(Or(
        U_A1 >= U_A2,  # No envy for A1
        U_A1 >= U_A2 - If(x[item] == 1, u_A2[item], 0)  # Removing item resolves envy
    ))
    solver.add(Or(
        U_A2 >= U_A1,  # No envy for A2
        U_A2 >= U_A1 - If(x[item] == 0, u_A1[item], 0)  # Removing item resolves envy
    ))

# Solve for global allocation
if solver.check() == sat:
    model = solver.model()
    allocation = {item: model[x[item]].as_long() for item in items}
    print("\nGlobal EFX Allocation Found:")
    print("Allocation:", allocation)
    
    # Verify EFX for partial allocations
    print("\nVerifying Partial Allocations:")
    assigned_A1 = []
    assigned_A2 = []
    for step, item in enumerate(revealed_items):
        # Update partial allocations
        if allocation[item] == 0:
            assigned_A1.append(item)
        else:
            assigned_A2.append(item)

        # Compute partial utilities
        partial_U_A1 = sum(u_A1[i] for i in assigned_A1)
        partial_U_A2 = sum(u_A2[i] for i in assigned_A2)

        # Check EFX for partial allocations
        partial_EFX = True
        for i in assigned_A1:
            partial_U_A1_without_i = partial_U_A1 - u_A1[i]
            if partial_U_A2 > partial_U_A1_without_i:
                partial_EFX = False
                break
        for j in assigned_A2:
            partial_U_A2_without_j = partial_U_A2 - u_A2[j]
            if partial_U_A1 > partial_U_A2_without_j:
                partial_EFX = False
                break
        
        # Print result for this step
        print(f"Step {step + 1}:")
        print(f"  Items so far: {revealed_items[:step + 1]}")
        print(f"  Partial Allocation - A1: {assigned_A1}, A2: {assigned_A2}")
        print(f"  Partial Utilities - U_A1: {partial_U_A1}, U_A2: {partial_U_A2}")
        print(f"  EFX Satisfied: {'Yes' if partial_EFX else 'No'}\n")

        if not partial_EFX:
            print("Partial allocation violated EFX at step", step + 1)
            break
else:
    print("No global EFX allocation found.")
