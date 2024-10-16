# Write a function that receives as a parameters a list of musical notes (strings), a list of moves (integers) and a
# start position (integer). The function will return the song composed by going through the musical notes beginning
# with the start position and following the moves given as parameter.
# Example : compose(["do", "re", "mi", "fa",  "sol"], [1, -3, 4, 2], 2) will return ["mi", "fa", "do", "sol", "re"]

def compose(notes: list, moves: list, start_position: int):
    current_note = start_position
    song = [notes[current_note]]
    for i in moves:
        current_note = (current_note + i) % len(notes)
        song.append(notes[current_note])
    return song


print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
