data = open("input.txt").read()
for i, c in enumerate(data):
    i += 3
    chars = set({data[i], data[i - 1], data[i - 2], data[i - 3]})
    #print(data[i], data[i - 1], data[i - 2], data[i - 3])
    if len(chars) == 4:
        start_packet_position = i+1
        print(start_packet_position)
        break

for i, c in enumerate(data):
    i += 13
    chars = set(data[i-z] for z in range(14))
    if len(chars) == 14:
        start_message_position = i + 1
        print(start_message_position)
        break
