import random
from tabulate import tabulate

def get_descending_utility_lists(item_utilities):
  """
  Given a dictionary of item utilities, return two lists of items sorted in descending
  order of utility for Agent 1 and Agent 2.
  """
  agent1_sorted_items = sorted(item_utilities.keys(), key=lambda x: item_utilities[x][0], reverse=True)
  agent2_sorted_items = sorted(item_utilities.keys(), key=lambda x: item_utilities[x][1], reverse=True)
  return agent1_sorted_items, agent2_sorted_items

def generate_item_utilities(n_items):
  """
  Generate a dictionary of n_items where each key is an item ID and 
  the value is a tuple (utility_for_agent_1, utility_for_agent_2).
  """
  item_utilities = {}
  for i in range(n_items):
      utility_agent1 = random.randint(1, n_items * 4)
      utility_agent2 = random.randint(1, n_items * 4)
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

def efx_condition(agent1, agent2, item_utilities):
  """
  Checks the EFX condition between two agents, reduced to considering the least favorite item.
  If Agent 1 doesn't envy Agent 2 up to removing Agent 1's least favorite item in Agent 2's allocation
  and vice versa, then EFX holds.
  """
  # Agent 1's envy check: calculate Agent 1's utility for Agent 2's bundle
  if agent2.items:
    total_agent1_view_of_agent2 = sum(item_utilities[item][0] for item in agent2.items)
    least_favorite_item_for_agent1 = min(agent2.items, key=lambda item: item_utilities[item][0])
    u1_S2_minus_least = total_agent1_view_of_agent2 - item_utilities[least_favorite_item_for_agent1][0]
    
    if agent1.total_utility < u1_S2_minus_least:
      return False

  # Agent 2's envy check: calculate Agent 2's utility for Agent 1's bundle
  if agent1.items:
    total_agent2_view_of_agent1 = sum(item_utilities[item][1] for item in agent1.items)
    least_favorite_item_for_agent2 = min(agent1.items, key=lambda item: item_utilities[item][1])
    u2_S1_minus_least = total_agent2_view_of_agent1 - item_utilities[least_favorite_item_for_agent2][1]

    if agent2.total_utility < u2_S1_minus_least:
      return False

  return True


def efx_allocation(n_iterations):
  # Initialize agents
  agent1 = Agent('Agent 1')
  agent2 = Agent('Agent 2')

  # Generate the item utilities for both agents
  item_utilities = generate_item_utilities(n_iterations)

  # Get the items in descending order of utility for both agents
  agent1_items, agent2_items = get_descending_utility_lists(item_utilities)

  # Set to track allocated items
  allocated_items = set()

  # List to hold deferred items
  deferred_items = []

  # Utility table for displaying at the end
  utility_table = []

  num_deferred = 0
  for iteration in range(n_iterations):
    print(f"Iteration {iteration}")

    # Items output by the Turing machines
    item1 = agent1_items[iteration]
    item2 = agent2_items[iteration]

    print(f"TM1 released {item1}")
    print(f"TM2 released {item2}")

    # Add to utility table
    utility_table.append({
        'Iteration': iteration,
        'Item_ID_TM1': item1,
        'U_Agent1_Item1': item_utilities[item1][0],
        'U_Agent2_Item1': item_utilities[item1][1],
        'Item_ID_TM2': item2,
        'U_Agent1_Item2': item_utilities[item2][0],
        'U_Agent2_Item2': item_utilities[item2][1],
    })

    # Try to allocate item1
    if item1 not in allocated_items:
        agent1_temp = Agent(agent1.name)
        agent1_temp.items = agent1.items.copy()
        agent1_temp.total_utility = agent1.total_utility
        agent1_temp.add_item(item1, item_utilities[item1][0])

        # Check EFX condition
        if efx_condition(agent1_temp, agent2, item_utilities):
            agent1.add_item(item1, item_utilities[item1][0])
            allocated_items.add(item1)
            print(f"Allocated {item1} to {agent1.name}")
        else:
            deferred_items.append(item1)
            print(f"Deferred {item1}")
            num_deferred += 1

    # Try to allocate item2
    if item2 not in allocated_items:
        agent2_temp = Agent(agent2.name)
        agent2_temp.items = agent2.items.copy()
        agent2_temp.total_utility = agent2.total_utility
        agent2_temp.add_item(item2, item_utilities[item2][1])

        # Check EFX condition
        if efx_condition(agent1, agent2_temp, item_utilities):
            agent2.add_item(item2, item_utilities[item2][1])
            allocated_items.add(item2)
            print(f"Allocated {item2} to {agent2.name}")
        else:
            deferred_items.append(item2)
            print(f"Deferred {item2}")
            num_deferred += 1

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

  print(f"\nNumber of times we deferred: {num_deferred}")
  
  # Check that the final allocation is EFX
  assert efx_condition(agent1, agent2, item_utilities)

  # Check that there are no unallocated items
  assert len(allocated_items) == n_iterations

# Run the allocation simulation
efx_allocation(10)


# 1st iteration: both agents receive same item (i.e. their most liked item is the
# same item)

# some later iteration: the agent that didn't receive the first item gets 0-value
# item and the other agent gets a non-zero item