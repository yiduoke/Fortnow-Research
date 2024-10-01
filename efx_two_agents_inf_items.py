import random
from tabulate import tabulate

def get_descending_utility_lists(item_utilities):
    """
    Given a dictionary of item utilities, return two lists of items sorted in descending
    order of utility for Agent 1 and Agent 2.

    Args:
    - item_utilities (dict): A dictionary where keys are item ids and values are 
      2-tuples representing (utility_for_agent_1, utility_for_agent_2).

    Returns:
    - list: Items sorted in descending order of utility for Agent 1.
    - list: Items sorted in descending order of utility for Agent 2.
    """
    # Sort items based on the utility for Agent 1 (first value in the tuple)
    agent1_sorted_items = sorted(item_utilities.keys(), key=lambda x: item_utilities[x][0], reverse=True)

    # Sort items based on the utility for Agent 2 (second value in the tuple)
    agent2_sorted_items = sorted(item_utilities.keys(), key=lambda x: item_utilities[x][1], reverse=True)

    return agent1_sorted_items, agent2_sorted_items

def generate_item_utilities(n_items):
    """
    Generate a dictionary of n_items where each key is an item ID and 
    the value is a tuple (utility_for_agent_1, utility_for_agent_2).
    """
    item_utilities = {}
    for i in range(n_items):
        utility_agent1 = random.randint(1, 100)
        utility_agent2 = random.randint(1, 100)
        item_utilities[i] = (utility_agent1, utility_agent2)
    return item_utilities

class Agent:
    def __init__(self, name):
        self.name = name
        self.items = set()
        self.total_utility = 0

    def add_item(self, item_id, utility):
        self.items.add(item_id)
        self.total_utility += utility

def efx_condition(agent1, agent2, utilities_agent1, utilities_agent2):
    """
    Checks the EFX condition between two agents.
    """
    # Agent 1 does not envy Agent 2 up to any item
    agent1_no_envy = True
    for item in agent2.items:
        u1_S2_minus_j = agent2.total_utility - utilities_agent1[item]
        if agent1.total_utility < u1_S2_minus_j:
            agent1_no_envy = False
            break

    # Agent 2 does not envy Agent 1 up to any item
    agent2_no_envy = True
    for item in agent1.items:
        u2_S1_minus_j = agent1.total_utility - utilities_agent2[item]
        if agent2.total_utility < u2_S1_minus_j:
            agent2_no_envy = False
            break

    return agent1_no_envy and agent2_no_envy

def efx_allocation(n_iterations):
    # Initialize agents
    agent1 = Agent('Agent 1')
    agent2 = Agent('Agent 2')

    # Generate the item utilities for both agents
    item_utilities = generate_item_utilities(n_iterations)

    # Get the items in descending order of utility for both agents
    agent1_items, agent2_items = get_descending_utility_lists(item_utilities)

    # Dictionaries to store utilities of items for both agents
    utilities_agent1 = {item: item_utilities[item][0] for item in item_utilities}
    utilities_agent2 = {item: item_utilities[item][1] for item in item_utilities}

    # Set to track allocated items
    allocated_items = set()

    # List to hold deferred items
    deferred_items = []

    # Utility table for displaying at the end
    utility_table = []

    for iteration in range(n_iterations):
        print(f"Iteration {iteration}")

        # Items output by the Turing machines
        item1 = agent1_items[iteration]
        item2 = agent2_items[iteration]

        # Add to utility table
        utility_table.append({
            'Iteration': iteration,
            'Item_ID_TM1': item1,
            'U_Agent1_Item1': utilities_agent1[item1],
            'U_Agent2_Item1': utilities_agent2[item1],
            'Item_ID_TM2': item2,
            'U_Agent1_Item2': utilities_agent1[item2],
            'U_Agent2_Item2': utilities_agent2[item2],
        })

        # Try to allocate item1
        if item1 not in allocated_items:
            # Temporarily add item1 to Agent 1
            agent1_temp = Agent(agent1.name)
            agent1_temp.items = agent1.items.copy()
            agent1_temp.total_utility = agent1.total_utility
            agent1_temp.add_item(item1, utilities_agent1[item1])

            # Check EFX condition
            if efx_condition(agent1_temp, agent2, utilities_agent1, utilities_agent2):
                # Allocate item1 to Agent 1
                agent1.add_item(item1, utilities_agent1[item1])
                allocated_items.add(item1)
                print(f"Allocated {item1} to {agent1.name}")
            else:
                deferred_items.append(item1)
                print(f"Deferred {item1}")

        # Try to allocate item2
        if item2 not in allocated_items:
            # Temporarily add item2 to Agent 2
            agent2_temp = Agent(agent2.name)
            agent2_temp.items = agent2.items.copy()
            agent2_temp.total_utility = agent2.total_utility
            agent2_temp.add_item(item2, utilities_agent2[item2])

            # Check EFX condition
            if efx_condition(agent1, agent2_temp, utilities_agent1, utilities_agent2):
                # Allocate item2 to Agent 2
                agent2.add_item(item2, utilities_agent2[item2])
                allocated_items.add(item2)
                print(f"Allocated {item2} to {agent2.name}")
            else:
                deferred_items.append(item2)
                print(f"Deferred {item2}")

        # Output current allocation for both agents
        print(f"{agent1.name} Items: {agent1.items}, Total Utility: {agent1.total_utility}")
        print(f"{agent2.name} Items: {agent2.items}, Total Utility: {agent2.total_utility}")
        print("-" * 50)

    # Print the utility table at the end
    print("\nUtility Table:")
    headers = ['Iteration', 'Item_ID_TM1', 'U_Agent1_Item1', 'U_Agent2_Item1',
               'Item_ID_TM2', 'U_Agent1_Item2', 'U_Agent2_Item2']
    table = [[row[h] for h in headers] for row in utility_table]
    print(tabulate(table, headers=headers, tablefmt='pretty'))

# Run the allocation simulation
efx_allocation(15)
