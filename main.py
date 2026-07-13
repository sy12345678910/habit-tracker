from json_struct import JSonClass


def main():
    print("Welcome to Habit Tracker!")
    print("Available actions: 'new', 'delete', 'current habits', 'exit'")
    
    while True:
        action = input("\ninput action:\n").strip().lower()
        
        if action in ["new", "new habit"]:
            user_input = input("input habit name and target date (YYYY-MM-DD) by comma:\n")
            if "," in user_input:
                task = user_input.split(",")
                new_habit(task)
            else:
                print("Format error! Please enter name and date separated by comma.")
                
        elif action in ["delete", "delete habit"]:
            habit_id = input("input habit ID to delete:\n").strip()
            if habit_id.isdigit():
                delete_habit(int(habit_id))
                print('habit deleted')
            else:
                print("Please enter a valid numeric ID.")
                
        elif action == "current habits":
            habits_list = read_file()
            if not habits_list:
                print("Your habit list is empty!")
            else:
                print("\nYour habits:")
                for h in habits_list:
                    print(f"[{h['id']}] {h['title']} — Until: {h['complete']} (Created: {h['create_at']})")
                    
        elif action == "exit": 
            print("Goodbye!")
            break
        else: 
            print("incorrect input")
           
def new_habit(habit_and_time: list):
    obj = JSonClass()
    struct = obj.build_struct(habit_and_time[0].strip(), habit_and_time[1].strip(), is_deleting=False)
    if struct:
        obj.operation(struct, is_delete=False)
        print("Habit created successfully!")
    else:
        print("Error: Invalid date format. Use YYYY-MM-DD.")

def delete_habit(habit_id: int):
    obj = JSonClass()
    struct = {"id": habit_id}
    obj.operation(struct, is_delete=True)
    
def read_file():
    obj = JSonClass()
    return obj.read()  

if __name__ == "__main__":
    main()
