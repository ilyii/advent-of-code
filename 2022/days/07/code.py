
with open("input.txt") as file:
    folder_sizes = {}
    folder_path = []

    for line in file.readlines():
        cmd = line.split()
        if cmd[0] == "$":
            if cmd[1] == "cd":
                if cmd[2] == "..":
                    folder_path = folder_path[:-1]
                elif cmd[2] == "/":
                    folder_path = ["/"]
                else:
                    folder_path.append(cmd[2])
        else:
            if cmd[0] != "dir":
                current_path = ""
                for folder in folder_path:
                    if current_path != "/" and folder != "/":
                        current_path += "/"
                    current_path += folder
                    folder_sizes[current_path] = folder_sizes.get(current_path, 0) + int(cmd[0])

# Part 1
print(sum(value for name, value in folder_sizes.items() if value < 100000))

# Part 2
needed_space = 30000000 - (70000000 - folder_sizes.get("/"))
print(min(value for name, value in folder_sizes.items() if value >= needed_space))

