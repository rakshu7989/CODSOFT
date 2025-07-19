import json
import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional
import argparse

class Task:
    
    def __init__(self, task_id: int, title: str, description: str = "", 
                 priority: str = "medium", due_date: Optional[str] = None):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.due_date = due_date
        self.completed = False
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.completed_date = None
        
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_date': self.created_date,
            'completed_date': self.completed_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            data['id'], 
            data['title'], 
            data.get('description', ''),
            data.get('priority', 'medium'),
            data.get('due_date')
        )
        task.completed = data.get('completed', False)
        task.created_date = data.get('created_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        task.completed_date = data.get('completed_date')
        return task
    
    def is_overdue(self) -> bool:
        if not self.due_date or self.completed:
            return False
        try:
            due = datetime.strptime(self.due_date, '%Y-%m-%d').date()
            return due < date.today()
        except ValueError:
            return False

class TodoApp:
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        print("\n" + "=" * 60)
        print(f"📝 {title.upper()}")
        print("=" * 60)
    
    def print_separator(self):
        print("-" * 60)
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
            except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                print(f"⚠️  Error loading tasks: {e}")
                self.tasks = []
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")
    
    def add_task(self):
        self.print_header("Add New Task")
        
        title = input("📌 Task title: ").strip()
        if not title:
            print("❌ Task title cannot be empty!")
            return
        
        description = input("📄 Description (optional): ").strip()
        
        print("\n🎯 Priority levels:")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        
        priority_choice = input("Select priority (1-3, default: 2): ").strip()
        priority_map = {'1': 'low', '2': 'medium', '3': 'high'}
        priority = priority_map.get(priority_choice, 'medium')
        
        due_date = input("📅 Due date (YYYY-MM-DD, optional): ").strip()
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                print("❌ Invalid date format! Task will be created without due date.")
                due_date = None
        else:
            due_date = None
        
        task = Task(self.next_id, title, description, priority, due_date)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        
        print(f"\n✅ Task '{title}' added successfully!")
        input("\nPress Enter to continue...")
    
    def list_tasks(self, filter_type: str = "all"):
        if filter_type == "all":
            filtered_tasks = self.tasks
            title = "All Tasks"
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
            title = "Pending Tasks"
        elif filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
            title = "Completed Tasks"
        elif filter_type == "overdue":
            filtered_tasks = [task for task in self.tasks if task.is_overdue()]
            title = "Overdue Tasks"
        else:
            filtered_tasks = self.tasks
            title = "All Tasks"
        
        self.print_header(title)
        
        if not filtered_tasks:
            print("📭 No tasks found!")
            return
        
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        filtered_tasks.sort(key=lambda x: (
            x.completed,
            priority_order.get(x.priority, 3),
            x.due_date or '9999-12-31'
        ))
        
        for task in filtered_tasks:
            self.print_task(task)
        
        print(f"\n📊 Total: {len(filtered_tasks)} task(s)")
    
    def print_task(self, task: Task):
        status = "✅" if task.completed else "⏳"
        priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        priority_icon = priority_icons.get(task.priority, '⚪')
        
        print(f"\n{status} [{task.id}] {priority_icon} {task.title}")
        
        if task.description:
            print(f"    📄 {task.description}")
        
        if task.due_date:
            due_status = " (OVERDUE!)" if task.is_overdue() else ""
            print(f"    📅 Due: {task.due_date}{due_status}")
        
        print(f"    📝 Created: {task.created_date}")
        
        if task.completed and task.completed_date:
            print(f"    ✅ Completed: {task.completed_date}")
        
        self.print_separator()
    
    def update_task(self):
        self.print_header("Update Task")
        
        if not self.tasks:
            print("📭 No tasks available to update!")
            return
        
        self.list_tasks("all")
        
        try:
            task_id = int(input("\n🔢 Enter task ID to update: "))
            task = self.find_task_by_id(task_id)
            
            if not task:
                print("❌ Task not found!")
                return
            
            print(f"\n📝 Updating task: {task.title}")
            print("(Press Enter to keep current value)")
            
            new_title = input(f"📌 Title [{task.title}]: ").strip()
            if new_title:
                task.title = new_title
            
            new_description = input(f"📄 Description [{task.description}]: ").strip()
            if new_description or new_description == "":
                task.description = new_description
            
            print("\n🎯 Priority levels:")
            print("1. Low")
            print("2. Medium") 
            print("3. High")
            
            priority_choice = input(f"Priority [{task.priority}] (1-3): ").strip()
            if priority_choice:
                priority_map = {'1': 'low', '2': 'medium', '3': 'high'}
                task.priority = priority_map.get(priority_choice, task.priority)
            
            new_due_date = input(f"📅 Due date [{task.due_date or 'None'}] (YYYY-MM-DD): ").strip()
            if new_due_date:
                try:
                    datetime.strptime(new_due_date, '%Y-%m-%d')
                    task.due_date = new_due_date
                except ValueError:
                    print("❌ Invalid date format! Due date not changed.")
            elif new_due_date == "":
                task.due_date = None
            
            self.save_tasks()
            print(f"\n✅ Task '{task.title}' updated successfully!")
            
        except ValueError:
            print("❌ Invalid task ID!")
        except KeyboardInterrupt:
            print("\n❌ Update cancelled!")
        
        input("\nPress Enter to continue...")
    
    def toggle_task_completion(self):
        self.print_header("Toggle Task Completion")
        
        if not self.tasks:
            print("📭 No tasks available!")
            return
        
        self.list_tasks("all")
        
        try:
            task_id = int(input("\n🔢 Enter task ID to toggle: "))
            task = self.find_task_by_id(task_id)
            
            if not task:
                print("❌ Task not found!")
                return
            
            task.completed = not task.completed
            if task.completed:
                task.completed_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"✅ Task '{task.title}' marked as completed!")
            else:
                task.completed_date = None
                print(f"⏳ Task '{task.title}' marked as pending!")
            
            self.save_tasks()
            
        except ValueError:
            print("❌ Invalid task ID!")
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
        
        input("\nPress Enter to continue...")
    
    def delete_task(self):
        self.print_header("Delete Task")
        
        if not self.tasks:
            print("📭 No tasks available to delete!")
            return
        
        self.list_tasks("all")
        
        try:
            task_id = int(input("\n🔢 Enter task ID to delete: "))
            task = self.find_task_by_id(task_id)
            
            if not task:
                print("❌ Task not found!")
                return
            
            confirm = input(f"⚠️  Are you sure you want to delete '{task.title}'? (y/N): ").strip().lower()
            
            if confirm == 'y' or confirm == 'yes':
                self.tasks.remove(task)
                self.save_tasks()
                print(f"🗑️  Task '{task.title}' deleted successfully!")
            else:
                print("❌ Deletion cancelled!")
                
        except ValueError:
            print("❌ Invalid task ID!")
        except KeyboardInterrupt:
            print("\n❌ Deletion cancelled!")
        
        input("\nPress Enter to continue...")
    
    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def search_tasks(self):
        self.print_header("Search Tasks")
        
        if not self.tasks:
            print("📭 No tasks available to search!")
            return
        
        query = input("🔍 Enter search term: ").strip().lower()
        
        if not query:
            print("❌ Search term cannot be empty!")
            return
        
        matching_tasks = [
            task for task in self.tasks 
            if query in task.title.lower() or query in task.description.lower()
        ]
        
        if matching_tasks:
            print(f"\n🔍 Found {len(matching_tasks)} matching task(s):")
            for task in matching_tasks:
                self.print_task(task)
        else:
            print(f"❌ No tasks found matching '{query}'")
        
        input("\nPress Enter to continue...")
    
    def show_statistics(self):
        self.print_header("Task Statistics")
        
        if not self.tasks:
            print("📭 No tasks available for statistics!")
            return
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        pending_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(1 for task in self.tasks if task.is_overdue())
        
        high_priority = sum(1 for task in self.tasks if task.priority == 'high' and not task.completed)
        medium_priority = sum(1 for task in self.tasks if task.priority == 'medium' and not task.completed)
        low_priority = sum(1 for task in self.tasks if task.priority == 'low' and not task.completed)
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        print(f"📊 Total Tasks: {total_tasks}")
        print(f"✅ Completed: {completed_tasks}")
        print(f"⏳ Pending: {pending_tasks}")
        print(f"⚠️  Overdue: {overdue_tasks}")
        print(f"📈 Completion Rate: {completion_rate:.1f}%")
        
        print(f"\n🎯 Pending Tasks by Priority:")
        print(f"🔴 High: {high_priority}")
        print(f"🟡 Medium: {medium_priority}")
        print(f"🟢 Low: {low_priority}")
        
        if self.tasks:
            oldest_task = min(self.tasks, key=lambda x: x.created_date)
            newest_task = max(self.tasks, key=lambda x: x.created_date)
            
            print(f"\n📅 Task Timeline:")
            print(f"Oldest task: {oldest_task.title} ({oldest_task.created_date})")
            print(f"Newest task: {newest_task.title} ({newest_task.created_date})")
        
        input("\nPress Enter to continue...")
    
    def clear_completed_tasks(self):
        self.print_header("Clear Completed Tasks")
        
        completed_tasks = [task for task in self.tasks if task.completed]
        
        if not completed_tasks:
            print("📭 No completed tasks to clear!")
            return
        
        print(f"Found {len(completed_tasks)} completed task(s):")
        for task in completed_tasks:
            print(f"  ✅ {task.title}")
        
        confirm = input(f"\n⚠️  Are you sure you want to delete all {len(completed_tasks)} completed task(s)? (y/N): ").strip().lower()
        
        if confirm == 'y' or confirm == 'yes':
            self.tasks = [task for task in self.tasks if not task.completed]
            self.save_tasks()
            print(f"🗑️  {len(completed_tasks)} completed task(s) cleared successfully!")
        else:
            print("❌ Operation cancelled!")
        
        input("\nPress Enter to continue...")
    
    def export_tasks(self):
        self.print_header("Export Tasks")
        
        if not self.tasks:
            print("📭 No tasks to export!")
            return
        
        filename = f"todo_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("📝 TO-DO LIST EXPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Tasks: {len(self.tasks)}\n\n")
                
                for task in self.tasks:
                    status = "COMPLETED" if task.completed else "PENDING"
                    f.write(f"[{task.id}] {task.title}\n")
                    f.write(f"Status: {status}\n")
                    f.write(f"Priority: {task.priority.upper()}\n")
                    
                    if task.description:
                        f.write(f"Description: {task.description}\n")
                    
                    if task.due_date:
                        f.write(f"Due Date: {task.due_date}\n")
                    
                    f.write(f"Created: {task.created_date}\n")
                    
                    if task.completed_date:
                        f.write(f"Completed: {task.completed_date}\n")
                    
                    f.write("-" * 30 + "\n\n")
            
            print(f"✅ Tasks exported successfully to '{filename}'!")
            
        except Exception as e:
            print(f"❌ Error exporting tasks: {e}")
        
        input("\nPress Enter to continue...")
    
    def show_menu(self):
        self.print_header("To-Do List Manager")
        print("1. 📝 Add Task")
        print("2. 📋 List All Tasks")
        print("3. ⏳ List Pending Tasks")
        print("4. ✅ List Completed Tasks")
        print("5. ⚠️  List Overdue Tasks")
        print("6. ✏️  Update Task")
        print("7. 🔄 Toggle Task Completion")
        print("8. 🗑️  Delete Task")
        print("9. 🔍 Search Tasks")
        print("10. 📊 Show Statistics")
        print("11. 🧹 Clear Completed Tasks")
        print("12. 📤 Export Tasks")
        print("0. 🚪 Exit")
        print("=" * 60)
    
    def run(self):
        while True:
            try:
                self.clear_screen()
                self.show_menu()
                
                choice = input("👉 Select an option (0-12): ").strip()
                
                if choice == '1':
                    self.add_task()
                elif choice == '2':
                    self.list_tasks("all")
                    input("\nPress Enter to continue...")
                elif choice == '3':
                    self.list_tasks("pending")
                    input("\nPress Enter to continue...")
                elif choice == '4':
                    self.list_tasks("completed")
                    input("\nPress Enter to continue...")
                elif choice == '5':
                    self.list_tasks("overdue")
                    input("\nPress Enter to continue...")
                elif choice == '6':
                    self.update_task()
                elif choice == '7':
                    self.toggle_task_completion()
                elif choice == '8':
                    self.delete_task()
                elif choice == '9':
                    self.search_tasks()
                elif choice == '10':
                    self.show_statistics()
                elif choice == '11':
                    self.clear_completed_tasks()
                elif choice == '12':
                    self.export_tasks()
                elif choice == '0':
                    print("\n👋 Thank you for using To-Do List Manager!")
                    print("Your tasks have been saved automatically.")
                    sys.exit(0)
                else:
                    print("❌ Invalid option! Please try again.")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("\nPress Enter to continue...")



def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='📝 Command-Line To-Do List Manager')
    parser.add_argument('--file', '-f', default='tasks.json', 
                       help='JSON file to store tasks (default: tasks.json)')
    parser.add_argument('--add', '-a', help='Quickly add a task')
    parser.add_argument('--list', '-l', action='store_true', help='List all tasks')
    parser.add_argument('--pending', '-p', action='store_true', help='List pending tasks')
    parser.add_argument('--completed', '-c', action='store_true', help='List completed tasks')
    parser.add_argument('--stats', '-s', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    app = TodoApp(args.file)
    
    # Handle command line operations
    if args.add:
        task = Task(app.next_id, args.add)
        app.tasks.append(task)
        app.next_id += 1
        app.save_tasks()
        print(f"✅ Task '{args.add}' added successfully!")
        return
    
    if args.list:
        app.list_tasks("all")
        return
    
    if args.pending:
        app.list_tasks("pending")
        return
    
    if args.completed:
        app.list_tasks("completed")
        return
    
    if args.stats:
        app.show_statistics()
        return
    
    # Run interactive mode
    app.run()

if __name__ == "__main__":
    main()