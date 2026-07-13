from json_struct import JSonClass


def main():
    while True:
        action = input("input action\n").strip().lower()
        if action == "new" or action == "new habbit":
            task = input("input habits\n")
            print(new_habbit(task))
        elif action == "delete" or action == "delete habbit":
            task = input("input habits\n")
            print(delete_habbit(task))
        elif action == "current habits":
            print(f"{"\n".join(habits)}")
        elif action == "exit": break
        else: print("incorrect input")
           
def new_habbit(habit: str) -> str:
    global habits
    if habit in habits:
        return f"habit \' {habit}\' is exist"
    habits.append(habit)
    return f"habbit wrote. currrent habits:\n {"\n".join(habits)}"

def delete_habbit(habit: str) -> str:
    obj = JSonClass()

if __name__ == "__main__":
    main()
