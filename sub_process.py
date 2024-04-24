import subprocess

# Define the command to run
command = "ls l"

# Execute the command
try:
    result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print("Command output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("An error occurred while trying to execute the command.")
    print("Error code:", e.returncode)
    print("Error message:", e.stderr)
