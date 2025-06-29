# Resource Allocation Using Genetic Algorithm
# Problem Scenario
# A company must allocate limited resources to projects. Each project has a different potential benefit, cost and time requirement.

import random


# Choice: These control the genetic algorithm (GA) and problem constraints, reusable across scenarios
POP_SIZE = 100          # Number of solutions to try in each generation - big enough to explore options
GENERATIONS = 200       # How many rounds to improve solutions - balances time and quality
ELITE_SIZE = 2          # Top solutions kept unchanged - keeps the best ideas
TOURNAMENT_SIZE = 5     # Solutions compared in selection - fair competition size
MUTATION_RATE = 0.15     # Chance of random change - adds variety without chaos
MAX_HOURS_PER_EMPLOYEE = 40  # Max hours per employee - matches real-world work limits

# Data class holding project and employee info
class Data:
    # PROJECTS_10: List of 10 projects, each with [name, required skills, hours needed, priority]
    # - name (str): Project ID (e.g., "P1") - just a label to know which project
    # - required skills (list): Skills needed (e.g., ["Python", "Database"]) - who can work on it
    # - hours needed (int): Hours to complete (e.g., 16) - how long it takes
    # - priority (int): Importance (1-3) - higher means bigger reward when done
    PROJECTS_10 = [
        ["P1", ["Python", "Database"], 16, 2],       # P1: Needs Python & Database skills, 16 hours, priority 2
        ["P2", ["Java", "Networking"], 8, 1],        # P2: Needs Java & Networking, 8 hours, priority 1
        ["P3", ["Python", "Machine Learning"], 20, 3], # P3: Needs Python & ML, 20 hours, priority 3 (high reward)
        ["P4", ["Database", "Java"], 8, 1],          # P4: Needs Database & Java, 8 hours, priority 1
        ["P5", ["Networking", "Machine Learning"], 16, 2], # P5: Needs Networking & ML, 16 hours, priority 2
        ["P6", ["AI", "Cloud"], 16, 2],              # P6: Needs AI & Cloud, 16 hours, priority 2
        ["P7", ["Cybersecurity", "Networking"], 16, 1], # P7: Needs Cybersecurity & Networking, 16 hours, priority 1
        ["P8", ["Python", "AI"], 20, 2],             # P8: Needs Python & AI, 20 hours, priority 2
        ["P9", ["Data Science", "Machine Learning"], 20, 3], # P9: Needs Data Science & ML, 20 hours, priority 3
        ["P10", ["Java", "Database"], 16, 1]         # P10: Needs Java & Database, 16 hours, priority 1
    ]
    
    # PROJECTS_15: Extends PROJECTS_10 with 5 more projects
    # Same format: [name, required skills, hours needed, priority]
    PROJECTS_15 = PROJECTS_10 + [
        ["P11", ["Python", "Cloud"], 20, 2],         # P11: Needs Python & Cloud, 20 hours, priority 2
        ["P12", ["Java", "Cybersecurity"], 16, 2],   # P12: Needs Java & Cybersecurity, 16 hours, priority 2
        ["P13", ["Networking", "Data Science"], 16, 2], # P13: Needs Networking & Data Science, 16 hours, priority 2
        ["P14", ["AI", "Database"], 20, 2],          # P14: Needs AI & Database, 20 hours, priority 2
        ["P15", ["Machine Learning", "Cloud"], 24, 3] # P15: Needs ML & Cloud, 24 hours, priority 3 (high reward)
    ]
    # EMPLOYEES_10: List of 10 employees, each with [ID, name, skills, available hours]
    # - ID (str): Employee ID (e.g., "E1") - a unique tag
    # - name (str): Employee name (e.g., "Alice") - who they are
    # - skills (list): Skills they have (e.g., ["AI", "Cloud"]) - what they can do
    # - available hours (int): Max hours they can work per week (e.g., 40) - their time limit
    EMPLOYEES_10 = [
        ["E1", "Alice", ["AI", "Cloud"], 40],           # E1: Alice, has AI & Cloud skills, can work 40 hours
        ["E2", "Bob", ["Java", "Networking"], 20],      # E2: Bob, has Java & Networking, can work 20 hours
        ["E3", "Charlie", ["Python", "Machine Learning"], 20], # E3: Charlie, has Python & ML, can work 20 hours
        ["E4", "David", ["Database", "Java"], 40],      # E4: David, has Database & Java, can work 40 hours
        ["E5", "Eve", ["Networking", "Machine Learning"], 40], # E5: Eve, has Networking & ML, can work 40 hours
        ["E6", "Frank", ["Python", "Java"], 40],        # E6: Frank, has Python & Java, can work 40 hours
        ["E7", "Grace", ["Database", "Networking"], 40], # E7: Grace, has Database & Networking, can work 40 hours
        ["E8", "Heidi", ["Machine Learning", "Python"], 20], # E8: Heidi, has ML & Python, can work 20 hours
        ["E9", "Ivan", ["Java", "Database"], 20],       # E9: Ivan, has Java & Database, can work 20 hours
        ["E10", "Judy", ["Networking", "Python"], 40]   # E10: Judy, has Networking & Python, can work 40 hours
    ]
    
    # MORE_EMPLOYEES: Adds 5 more employees to extend to 15
    # Same format: [ID, name, skills, available hours]
    MORE_EMPLOYEES = [
        ["E11", "Kevin", ["AI", "Cloud"], 20],          # E11: Kevin, has AI & Cloud skills, can work 20 hours
        ["E12", "Laura", ["Cybersecurity", "Networking"], 20], # E12: Laura, has Cybersecurity & Networking, can work 20 hours
        ["E13", "Mike", ["Python", "AI"], 20],          # E13: Mike, has Python & AI, can work 20 hours
        ["E14", "Nina", ["Data Science", "Machine Learning"], 20], # E14: Nina, has Data Science & ML, can work 20 hours
        ["E15", "Oscar", ["Java", "Database"], 20]      # E15: Oscar, has Java & Database, can work 20 hours
    ]
    
    # EMPLOYEES_15: Combines EMPLOYEES_10 and MORE_EMPLOYEES for a total of 15 employees
    EMPLOYEES_15 = EMPLOYEES_10 + MORE_EMPLOYEES


# Function: Makes a lookup table to find employees by skill
# Purpose: Helps us quickly see which employees have a certain skill - like a phonebook!
def create_skill_mapping(employees):
    # Create an empty dictionary to store skills and the employees who have them
    # Think of it as a blank list where we’ll write "Python: [Alice, Bob]" etc.
    skill_to_employees = {}
    
    # Loop through all employees, numbering them with emp_idx (e.g., 0, 1, 2...)
    # 'enumerate' gives us both the number (emp_idx) and the employee info (emp)
    for emp_idx, emp in enumerate(employees):
        # emp[2] is the list of skills for this employee (e.g., ["Python", "Database"])
        # Loop through each skill this employee has
        for skill in emp[2]:
            # Add the employee’s number (emp_idx) to the list for this skill
            # 'setdefault' means: if the skill isn’t in the dictionary yet, start an empty list
            # Then append the employee’s number to that list
            skill_to_employees.setdefault(skill, []).append(emp_idx)
    
    # Return the finished dictionary - now we can look up any skill and see who has it!
    return skill_to_employees


# Function: Creates starting solutions (population) by randomly assigning employees to projects
# Purpose: Makes a bunch of random team plans - like drafting different lineups for a game!
def generate_population(projects, employees, skill_to_employees):
    # Start with an empty list to hold all our team plans (called the population)
    population = []
    
    # Loop POP_SIZE times (e.g., 100) to make that many different plans
    # '_' means we don’t need the loop number, just want to repeat 100 times
    for _ in range(POP_SIZE):
        # Make a blank plan: a list of empty teams, one for each project (e.g., 10 projects = 10 empty lists)
        allocation = [[] for _ in projects]
        
        # Make a set of all employee numbers (e.g., 0 to 9) who haven’t been assigned yet
        # A set is like a checklist we can cross off as they get assigned to projects
        # Set is also being used to avoid duplicates unlike a 'list'
        unassigned_employees = set(range(len(employees)))
        
        # Step 1: Try to give every employee a project
        # Loop through each employee by their number (e.g., 0 for Alice, 1 for Bob...)
        for emp_idx in range(len(employees)):
            # Start with an empty list of projects this employee can do
            valid_projects = []
            
            # Get this employee’s skills as a set (e.g., {"Python", "Database"}) for fast checking compared to a list
            emp_skills = set(employees[emp_idx][2])
            
            # Check every project to see if this employee’s skills match
            for proj_idx, proj in enumerate(projects):
                # proj[1] is the project’s required skills (e.g., ["Python", "Database"])
                # '&' checks if any skills overlap (like a Venn diagram!)
                if emp_skills & set(proj[1]):
                    # If there’s a match, add the project number to the list
                    # Example: Charlie’s valid_projects might be [0, 8] (P1, P9)
                    valid_projects.append(proj_idx)
            
            # If we found any matching projects for this employee
            if valid_projects:
                # Pick one project randomly - like flipping a coin to choose!
                # Flip a coin with random.choice—say it picks 0 (P1)
                chosen_proj = random.choice(valid_projects)
                # Add the employee’s number to that project’s team
                # Add Charlie (2) to P1’s team: allocation[0] = [2]
                allocation[chosen_proj].append(emp_idx)
                # Cross this employee off our unassigned list
                # Cross Charlie off: unassigned_employees loses 2 (e.g., {0, 1, 3, 4, ...})
                unassigned_employees.discard(emp_idx)
        
        # Step 2: Fill any empty projects
        # Loop through each project again to check if it has a team
        for proj_idx, proj in enumerate(projects):
            # Get the skills this project needs as a set
            required_skills = set(proj[1])
            
            # Make a list of employees whose skills match (even if already assigned)
            valid_employees = [i for i in range(len(employees)) 
                             if set(employees[i][2]) & required_skills]
            
            # If there are matching employees and the project’s team is still empty
            if valid_employees and not allocation[proj_idx]:
                # Pick a random number between 1 and 3 for how many employees to assign
                # But don’t pick more than we have available
                k = min(len(valid_employees), random.randint(1, 3))
                # Randomly choose that many employees from the valid list
                allocation[proj_idx] = random.sample(valid_employees, k)
        
        # Add this finished plan (allocation) to our population
        population.append(allocation)
    
    # Return the full population - 100 different ways to assign the team!
    return population


# Function: Scores how good a solution is (higher is better)
# Purpose: Gives a grade to our team plan - like judging a group project!
def fitness(allocation, projects, employees):
    # Start with a score of 0 - we’ll add points for good stuff and subtract for bad
    total_benefit = 0
    
    # Make a dictionary of each employee’s available hours (e.g., {0: 40, 1: 20...})
    # emp[3] is their max hours; this tracks how much they have left
    employee_hours = {i: emp[3] for i, emp in enumerate(employees)}
    
    # Dictionary to store each project’s score (e.g., {"P1": 20})
    project_scores = {}
    
    # Set to track which employees get used - like a roll call
    used_employees = set()
    
    # Set to track which projects get done - keeps count of finished ones
    assigned_projects = set()
    
    # Loop through each project and its assigned team in our plan
    for project_idx, assigned_employees in enumerate(allocation):
        # Get the project details (e.g., ["P1", ["Python", "Database"], 16, 2])
        project = projects[project_idx]
        
        # Project’s required skills as a set (e.g., {"Python", "Database"})
        required_skills = set(project[1])
        
        # How many hours this project needs
        required_hours = project[2]
        
        # Project’s priority (1-3) - higher means more points
        project_priority = project[3]
        
        # Flag to check if this team works - starts as True (good)
        valid_assignment = True
        
        # Check each employee assigned to this project
        for emp_idx in assigned_employees:
            # Get this employee’s skills as a set (e.g., {"Python", "Java"})
            emp_skills = set(employees[emp_idx][2])
            
            # If no skills match (no overlap), this team can’t do it
            if not (emp_skills & required_skills):
                valid_assignment = False
                break  # Stop checking - team’s no good
            
            # Add this employee to the used list
            used_employees.add(emp_idx)
        
        # If we have a team and their skills match
        if assigned_employees and valid_assignment:
            # Check if every employee has enough hours left
            if all(employee_hours.get(emp_idx, 0) >= required_hours for emp_idx in assigned_employees):
                # Base score is 20 points for finishing a project
                base_score = 20
                
                # Penalty for big teams - smaller is better (e.g., 1/2 if 2 people)
                employee_penalty = 1 / len(assigned_employees)
                
                # Calculate score: base * priority * penalty (e.g., 20 * 2 * 0.5 = 20)
                project_score = base_score * project_priority * employee_penalty
                
                # Add this project’s score to the total
                total_benefit += project_score
                
                # Save the score for this project (e.g., "P1": 20)
                project_scores[project[0]] = project_score
                
                # Mark this project as done
                assigned_projects.add(project_idx)
                
                # Subtract the hours each employee worked
                for emp_idx in assigned_employees:
                    employee_hours[emp_idx] -= required_hours
            else:
                # If anyone’s out of hours, cancel this team and score it 0
                allocation[project_idx] = []
                project_scores[project[0]] = 0
        else:
            # If no team or skills don’t match, score is 0
            project_scores[project[0]] = 0
    
    # Penalty: Count employees who didn’t work and subtract 100 points each
    unassigned_employee_count = len(employees) - len(used_employees)
    total_benefit -= unassigned_employee_count * 100
    
    # Penalty: Check for overwork (hours < 0) and subtract 50 points per extra hour
    over_allocation_penalty = 0
    for emp_idx, hours in employee_hours.items():
        if hours < 0:
            over_allocation_penalty += abs(hours) * 50
    total_benefit -= over_allocation_penalty
    
    # Penalty: Count unassigned projects and subtract 50 points each
    unassigned_project_count = len(projects) - len(assigned_projects)
    total_benefit -= unassigned_project_count * 50
    
    # Calculate total hours used (original hours minus what’s left)
    # If an employee wasn’t used, their hours stay the same, so difference is 0
    hours_used = sum(employees[i][3] - employee_hours.get(i, employees[i][3]) for i in range(len(employees)))
    
    # Return four things: total score, project scores, projects done, and hours used
    return total_benefit, project_scores, len(assigned_projects), hours_used


# Function: Picks top solutions for next round
# Purpose: Chooses the best team plans to keep - like picking winners for the next game!
def selection(population, projects, employees):
    # Sort all 100 plans by their score (fitness) from best to worst
    # 'lambda x: fitness(x, projects, employees)[0]' grabs the score (first item) from fitness
    # 'reverse=True' means highest score first, like ranking top to bottom
    population.sort(key=lambda x: fitness(x, projects, employees)[0], reverse=True)
    
    # Keep the top few plans (e.g., 2) as 'elite' - these are our superstars!
    # ELITE_SIZE is how many we save (set to 2 in your code)
    elite = population[:ELITE_SIZE]
    
    # Start our final list with these elite plans
    # 'copy()' makes sure we don’t mess with the original elite
    selected = elite.copy()
    
    # Figure out how many more plans we need
    # POP_SIZE is 100 (total plans), we want half (50), minus the elite (e.g., 50 - 2 = 48)
    num_to_select = (POP_SIZE // 2) - ELITE_SIZE
    
    # Loop to pick the rest of our winners
    # Repeat 'num_to_select' times (e.g., 48 times)
    for _ in range(num_to_select):
        # Pick a small random group (e.g., 5 plans) for a mini-competition
        # TOURNAMENT_SIZE is 5 - like a quick playoff!
        tournament = random.sample(population, TOURNAMENT_SIZE)
        
        # Find the best plan in this group by checking their fitness scores
        # 'max' picks the highest score; 'lambda' gets the score from fitness again
        best_in_tournament = max(tournament, key=lambda x: fitness(x, projects, employees)[0])
        
        # Add this winner to our selected list
        selected.append(best_in_tournament)
    
    # Return our final list of 50 plans (2 elite + 48 winners) to move forward
    return selected


# Function: Mixes two solutions to make new ones
# Purpose: Combines two team plans to create fresh ones - like parents making kids with mixed traits!
def crossover(parent1, parent2):
    # Pick a random spot to split the plans (e.g., between 1 and 9 if 10 projects)
    # 'random.randint(1, len(parent1) - 1)' chooses a number from 1 to one less than the total projects
    # This is our crossover point - where we’ll swap parts
    point = random.randint(1, len(parent1) - 1)
    
    # Make child 1: Take the start of parent1 up to the split, then add the end of parent2
    # 'parent1[:point]' grabs the first part (e.g., projects 0 to 3)
    # 'parent2[point:]' grabs the rest (e.g., projects 4 to 9)
    # '+' sticks them together into a new plan
    child1 = parent1[:point] + parent2[point:]
    
    # Make child 2: Take the start of parent2 up to the split, then add the end of parent1
    # Same idea, just flipped - mixing the other way around
    child2 = parent2[:point] + parent1[point:]
    
    # Return both new plans (kids) - two fresh team combos to try out!
    return child1, child2


# Function: Randomly changes a solution to add variety
# Purpose: Shakes up a team plan a little - like swapping players to try something new!
def mutate(allocation, mutation_rate, projects, employees, skill_to_employees):
    # Roll a dice (0 to 1) and see if it’s less than mutation_rate (e.g., 0.1 or 10% chance)
    # 'random.random()' gives a number between 0 and 1 - it’s our chance to mutate!
    if random.random() < mutation_rate:
        # Pick a random project to change (e.g., 0 to 9 if 10 projects)
        # 'random.randint(0, len(projects) - 1)' chooses one project’s number
        idx = random.randint(0, len(projects) - 1)
        
        # Get the skills this project needs as a set (e.g., {"Python", "Database"})
        # projects[idx][1] is the skill list for that project
        required_skills = set(projects[idx][1])
        
        # Make a list of employees who have matching skills
        # Check each employee’s skills (employees[i][2]) against the project’s needs
        # 'set() & set()' finds overlaps - if any skill matches, they’re in!
        valid_employees = [i for i in range(len(employees)) 
                         if set(employees[i][2]) & required_skills]
        
        # If we found any employees who can do this project
        if valid_employees:
            # Decide how many to assign: pick a random number (1 to 3), but not more than we have
            # 'min()' ensures we don’t pick more people than available
            k = min(len(valid_employees), random.randint(1, 3))
            
            # Randomly pick that many employees from the valid list
            # 'random.sample' grabs k people without repeats - like drawing names from a hat
            allocation[idx] = random.sample(valid_employees, k)
    
    # Return the plan - it might be changed (mutated) or the same if no mutation happened
    return allocation


# Function: Runs the full genetic algorithm
# Purpose: Evolves team plans to find the best one - like training a team to win the championship!
def genetic_algorithm(mutation_rate, generations, elite_size, tournament_size, projects, employees, skill_to_employees):
    # Use POP_SIZE (e.g., 100) from outside - it’s how many plans we start with
    global POP_SIZE
    
    # Create 100 random team plans to kick things off
    # 'generate_population' makes our starting lineup
    population = generate_population(projects, employees, skill_to_employees)
    
    # Loop 'generations' times (e.g., 200) - each loop is like a training round
    # '_' means we don’t need the loop number, just repeat the process
    for _ in range(generations):
        # Pick the best 50 plans from the 100
        # 'selection' keeps the elite and winners from tournaments
        selected = selection(population, projects, employees)
        
        # Start an empty list for new plans (kids) we’ll make
        offspring = []
        
        # Pair up the 50 selected plans to mix them
        # Step by 2 (e.g., 0, 2, 4...) to grab pairs like parent1 and parent2
        for i in range(0, len(selected), 2):
            # Check if there’s a pair (e.g., if 49 plans, skip the last solo one)
            if i + 1 < len(selected):
                # Mix two plans to make two new ones
                # 'crossover' swaps parts of the parents to create child1 and child2
                child1, child2 = crossover(selected[i], selected[i + 1])
                
                # Tweak each new plan a little with a chance to change
                # 'mutate' might swap a team randomly based on mutation_rate (e.g., 0.1)
                offspring.append(mutate(child1, mutation_rate, projects, employees, skill_to_employees))
                offspring.append(mutate(child2, mutation_rate, projects, employees, skill_to_employees))
        
        # Combine the 50 selected plans with the new kids to make a new 100
        # This is our updated population for the next round
        population = selected + offspring
    
    # After all rounds, find the best plan by its score
    # 'max' picks the highest fitness score; 'lambda' grabs the score from fitness
    best_solution = max(population, key=lambda x: fitness(x, projects, employees)[0])
    
    # Return the winning plan and its full fitness details (score, projects done, etc.)
    return best_solution, fitness(best_solution, projects, employees)


# Function: Displays the best solution in a nice format
# Purpose: Shows our winning team plan - like a scorecard for who did what and how we scored!
def print_result(scenario, best_allocation, best_fitness, project_scores, projects, employees):
    # Print two big lines (100 dashes) to separate this from other stuff - like a fancy border
    print("-" * 100)
    print("-" * 100)
    
    # Print the scenario name (e.g., "Scenario 1") with a new line before it
    print(f"\n{scenario}:")
    
    # Show the total score (best_fitness) - our final grade!
    print("Maximized Benefit:", best_fitness)
    
    # Make a dictionary to track hours worked per employee, starting all at 0
    # emp[1] is the name (e.g., "Alice"), so { "Alice": 0, "Bob": 0, ... }
    employee_work_hours = {emp[1]: 0 for emp in employees}
    
    # Calculate hours worked by each employee
    # Loop through each project and its team in the best plan
    for project_idx, assigned_employees in enumerate(best_allocation):
        # Get how many hours this project takes (e.g., 16)
        required_hours = projects[project_idx][2]
        
        # Add those hours to each employee on the team
        for emp_idx in assigned_employees:
            # emp_idx is their number; employees[emp_idx][1] is their name
            employee_work_hours[employees[emp_idx][1]] += required_hours
    
    # Print a header for project details
    print("\nProject Allocations:")
    print("-" * 75)  # A line to make it look neat
    # Set up columns with widths: Project (10), Employees (30), Hours (15), Score (10)
    print("{:<10} {:<30} {:<15} {:<10}".format("Project", "Assigned Employees", "Hours", "Score"))
    print("-" * 75)  # Another line for style
    
    # Show each project’s details
    for project_idx, assigned_employees in enumerate(best_allocation):
        # Get the project’s name (e.g., "P1")
        project_name = projects[project_idx][0]
        
        # Get the hours it needs
        required_hours = projects[project_idx][2]
        
        # List the names of employees assigned (e.g., ["Alice", "Bob"])
        employee_names = [employees[emp_idx][1] for emp_idx in assigned_employees]
        
        # Get this project’s score, 0 if it wasn’t done
        project_score = project_scores.get(project_name, 0)
        
        # Print the row: name, team (joined with commas), hours, score (2 decimals)
        print("{:<10} {:<30} {:<15} {:<10.2f}".format(project_name, ', '.join(employee_names), required_hours, project_score))
    
    print("-" * 75)  # Close the project section
    
    # Print a header for employee hours
    print("\nEmployee Work Hours (Max 40/week):")
    print("-" * 60)  # Smaller line for this section
    # Set up columns: Employee (10), Hours Worked (15), Skills (15)
    print("{:<10} {:<15} {:<15}".format("Employee", "Hours Worked", "Skills"))
    print("-" * 60)
    
    # Show each employee’s hours and skills
    for emp in employees:
        # emp[1] is name (e.g., "Alice")
        name = emp[1]
        
        # Get their total hours from our dictionary
        hours = employee_work_hours[name]
        
        # Join their skills into a string (e.g., "Python, Database")
        skills = ', '.join(emp[2])
        
        # Print the row: name, hours, skills
        print("{:<10} {:<15} {:<15}".format(name, hours, skills))
    
    print("-" * 60)  # End the employee section

# Function: Runs the algorithm multiple times and shows average results
# Purpose: Tests our team plan over 3 games to see how it performs on average - like a season recap!
# Key Metrics Recap (what we’re measuring):
# - Total Benefit: Average score across runs - how good we usually do
# - Projects Done: How many projects we finish (max 10 or 15) - our completion rate
# - Hours Used: Total hours worked - how busy our team gets
# - Efficiency (%): Hours used / total hours (e.g., 10 employees * 40 = 400) - how much we use our time
# - Spread: Biggest score minus smallest - how steady our results are
def summarize_scenario(scenario_name, params, projects, employees, skill_map, runs=3):
    # Print a header with the scenario name (e.g., "Scenario 1 Summary") and triple equals for emphasis
    print(f"\n=== {scenario_name} ===")
    
    # Show the settings we used (e.g., "GEN=200, ELITE=2, TOURN=5, MUT=0.1")
    print(f"Parameters: {params}")
    
    # Draw a line (80 dashes) to make it look clean
    print("-" * 80)
    
    # Set up a table header with columns: Run, Total Benefit, Projects Done, Hours Used, Efficiency
    # Each number (e.g., :<20) sets the width to keep it neat
    print("{:<20} {:<15} {:<15} {:<15} {:<15}".format("Run", "Total Benefit", "Projects Done", "Hours Used", "Efficiency (%)"))
    
    # Another line to separate header from data
    print("-" * 80)
    
    # Empty list to store results from each run
    results = []
    
    # Calculate total hours available (e.g., 10 employees * 40 hours = 400)
    # MAX_HOURS_PER_EMPLOYEE is 40 from your constants
    total_hours_available = len(employees) * MAX_HOURS_PER_EMPLOYEE
    
    # Run the algorithm 3 times (or however many 'runs' says)
    for i in range(runs):
        # Split the params string (e.g., "GEN=200, ELITE=2...") and grab the numbers
        # Turn "GEN=200" into 200 (as int), "MUT=0.1" into 0.1 (as float)
        param_values = [float(x.split('=')[1]) if '=' in x else x for x in params.split(', ')]
        
        # Assign the values: mutation_rate is 4th, generations 1st (int), elite_size 2nd (int), tournament_size 3rd (int)
        mutation_rate, generations, elite_size, tournament_size = param_values[3], int(param_values[0]), int(param_values[1]), int(param_values[2])
        
        # Run the genetic algorithm with these settings to get the best plan and its stats
        # Returns best_allocation and a tuple (benefit, proj_scores, projects_done, hours_used)
        best_allocation, (benefit, proj_scores, projects_done, hours_used) = genetic_algorithm(
            mutation_rate, generations, elite_size, tournament_size, projects, employees, skill_map
        )
        
        # Calculate efficiency: hours used divided by total hours, times 100 for percentage
        # If no hours available (unlikely), set to 0 to avoid errors
        efficiency = (hours_used / total_hours_available) * 100 if total_hours_available > 0 else 0
        
        # Save this run’s stats (benefit, projects done, hours, efficiency) as a tuple
        results.append((benefit, projects_done, hours_used, efficiency))
        
        # Print this run’s row: Run 1, score, projects, hours, efficiency (2 decimals for neatness)
        print("{:<20} {:<15.2f} {:<15} {:<15} {:<15.2f}".format(f"Run {i+1}", benefit, projects_done, hours_used, efficiency))
    
    # Get just the benefit scores from all runs (e.g., [350, 340, 360])
    benefits = [r[0] for r in results]
    
    # Calculate average score: add them up and divide by how many runs
    avg_benefit = sum(benefits) / runs
    
    # Calculate spread: highest score minus lowest to show consistency
    spread_benefit = max(benefits) - min(benefits)
    
    # Draw a line to separate data from summary
    print("-" * 80)
    
    # Print the average and spread with 2 decimals - our season stats!
    print(f"Average Benefit: {avg_benefit:.2f}, Spread: {spread_benefit:.2f}")
    
    # Smaller line to finish it off
    print("-" * 40)
    
    # Return all the results in case we need them later
    return results

# Function: Runs the whole program with different scenarios
# Purpose: Tests our team plans in different setups - like running experiments to find the best strategy!
def main():
    # --- Setup Data ---
    # Grab our project and employee lists from the Data class - like gathering our tools
    projects_10 = Data.PROJECTS_10    # 10 projects to assign
    employees_10 = Data.EMPLOYEES_10  # 10 employees to work
    projects_15 = Data.PROJECTS_15    # 15 projects for bigger tests
    employees_15 = Data.EMPLOYEES_15  # 15 employees for extra help
    
    # Make skill maps - quick lookups of who has what skills (e.g., "Python": [0, 2])
    skill_map_10 = create_skill_mapping(employees_10)  # For 10 employees
    skill_map_15 = create_skill_mapping(employees_15)  # For 15 employees
    
    # --- For each scenario: Show one detailed run, then a summary of 3 runs ---
    # Each test gets a close-up (print_result) and a big-picture view (summarize_scenario)
    
    # Scenario 1: 10 Projects + 10 Employees
    # Set our recipe: how many rounds, top picks, competition size, and change chance
    params = "GEN=200, ELITE=2, TOURN=5, MUT=0.1"  # String for display
    mutation_rate, generations, elite_size, tournament_size = 0.15, 200, 2, 5  # Actual values
    
    # Run the algorithm to find the best plan and its stats
    best_allocation_1, (best_fitness_1, project_scores_1, proj_done_1, hours_1) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_10, employees_10, skill_map_10
    )
    # Show the detailed result - who worked where, hours, score
    print_result("SCENARIO 1: 10 PROJECTS + 10 EMPLOYEES", best_allocation_1, best_fitness_1, project_scores_1, projects_10, employees_10)
    # Show the summary - average over 3 runs to check consistency
    summarize_scenario("Scenario 1 Summary", params, projects_10, employees_10, skill_map_10)
    
    # Scenario 2: 15 Projects + 10 Employees (Baseline)
    # Same settings as Scenario 1 - this is our starting point for tweaks
    best_allocation_2, (best_fitness_2, project_scores_2, proj_done_2, hours_2) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_15, employees_10, skill_map_10
    )
    print_result("Scenario 2: 15 PROJECTS + 10 EMPLOYEES", best_allocation_2, best_fitness_2, project_scores_2, projects_15, employees_10)
    summarize_scenario("Scenario 2 Summary", params, projects_15, employees_10, skill_map_10)
    
    # Scenario 3: 10 Projects + 15 Employees
    # Still same settings - testing more people than projects
    best_allocation_3, (best_fitness_3, project_scores_3, proj_done_3, hours_3) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_10, employees_15, skill_map_15
    )
    print_result("Scenario 3: 10 PROJECTS + 15 EMPLOYEES", best_allocation_3, best_fitness_3, project_scores_3, projects_10, employees_15)
    summarize_scenario("Scenario 3 Summary", params, projects_10, employees_15, skill_map_15)
    
    # Variation 1: Higher Generations (500)
    # Tweak: More rounds (500 vs. 200) to train longer
    params_v1 = "GEN=500, ELITE=2, TOURN=5, MUT=0.1"
    mutation_rate, generations, elite_size, tournament_size = 0.15, 500, 2, 5
    best_allocation_v1, (best_fitness_v1, project_scores_v1, proj_done_v1, hours_v1) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_15, employees_10, skill_map_10
    )
    print_result("VARIATION 1: 15 PROJECTS + 10 EMPLOYEES, MORE GENERATIONS", best_allocation_v1, best_fitness_v1, project_scores_v1, projects_15, employees_10)
    summarize_scenario("Variation 1 Summary", params_v1, projects_15, employees_10, skill_map_10)
    
    # Variation 2: Higher Elitism (5)
    # Tweak: Keep more top plans (5 vs. 2) to favor the best
    params_v2 = "GEN=200, ELITE=5, TOURN=5, MUT=0.1"
    mutation_rate, generations, elite_size, tournament_size = 0.15, 200, 5, 5
    best_allocation_v2, (best_fitness_v2, project_scores_v2, proj_done_v2, hours_v2) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_15, employees_10, skill_map_10
    )
    print_result("VARIATION 2: 15 PROJECTS + 10 EMPLOYEES, MORE ELITISM", best_allocation_v2, best_fitness_v2, project_scores_v2, projects_15, employees_10)
    summarize_scenario("Variation 2 Summary", params_v2, projects_15, employees_10, skill_map_10)
    
    # Variation 3: Higher Tournament Size (10)
    # Tweak: Bigger competitions (10 vs. 5) to pick stronger winners
    params_v3 = "GEN=200, ELITE=2, TOURN=10, MUT=0.1"
    mutation_rate, generations, elite_size, tournament_size = 0.15, 200, 2, 10
    best_allocation_v3, (best_fitness_v3, project_scores_v3, proj_done_v3, hours_v3) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_15, employees_10, skill_map_10
    )
    print_result("VARIATION 3: 15 PROJECTS + 10 EMPLOYEES, BIGGER TOURNAMENT", best_allocation_v3, best_fitness_v3, project_scores_v3, projects_15, employees_10)
    summarize_scenario("Variation 3 Summary", params_v3, projects_15, employees_10, skill_map_10)
    
    # Variation 4: Higher Mutation Rate (0.3)
    # Tweak: More random changes (0.3 vs. 0.1) to shake things up
    params_v4 = "GEN=200, ELITE=2, TOURN=5, MUT=0.3"
    mutation_rate, generations, elite_size, tournament_size = 0.3, 200, 2, 5
    best_allocation_v4, (best_fitness_v4, project_scores_v4, proj_done_v4, hours_v4) = genetic_algorithm(
        mutation_rate, generations, elite_size, tournament_size, projects_15, employees_10, skill_map_10
    )
    print_result("VARIATION 4: 15 PROJECT + 10 EMPLOYEES, MORE MUTATION", best_allocation_v4, best_fitness_v4, project_scores_v4, projects_15, employees_10)
    summarize_scenario("Variation 4 Summary", params_v4, projects_15, employees_10, skill_map_10)

# Run the main function when we start the program
# This line checks if we’re running this file directly - standard Python trick!
if __name__ == "__main__":
    main()
