import pandas as pd
import os

# Define the directory where the CSVs are stored (assuming they are in the root of the repository)
directory = './dework/m3/'

# Ensure the CSV directory exists
if not os.path.exists(directory):
    os.makedirs(directory)

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# List to store tasks details
tasks = []

# Loop through each CSV
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        try:
            # Read the CSV
            df = pd.read_csv(os.path.join(directory, filename))

            # Extract the required details
            for index, row in df.iterrows():
                task_name = row.get('Name', None)
                amount = row.get('Reward', None)
                date_posted = row.get('Due Date', None)

                if task_name and amount and date_posted:
                    tasks.append({
                        'name': task_name,
                        'amount': amount,
                        'date_posted': date_posted
                    })
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Filter out tasks without both a reward and a due date
filtered_tasks = [task for task in tasks if task['amount'] and task['date_posted']]

# Extract the numeric part of the reward for sorting
for task in filtered_tasks:
    task['amount_numeric'] = float(task['amount'].split()[0])

# Sort tasks
sorted_tasks = sorted(filtered_tasks, key=lambda x: (x['amount_numeric'], x['date_posted']), reverse=True)

# Extract the top 3 tasks
top_3_tasks = sorted_tasks[:3]

# Format the tasks
formatted_tasks = [f"{task['amount']} | {task['name']} | Date Posted: {task['date_posted']}" for task in top_3_tasks]

# Directory to save the text files (assuming they should be in the root of the repository)
output_directory = './automation/top_tasks/'

# Generate the text files
for index, task in enumerate(formatted_tasks, 1):
    with open(os.path.join(output_directory, f"task{index}.txt"), "w") as file:
        file.write(task)

print("Text files updated successfully!")
