import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from bson import ObjectId

console = Console()

app = typer.Typer()

@app.command(short_help='Add an item')
def add(task: str, category: str):
    count = Todo.collection.count_documents({})
    todo = Todo(task, category)
    todo.position = count if count else 0
    todo.save()
    typer.echo(f"adding {task}, {category}")
    show()

@app.command(short_help='Delete an item')
def delete(position: int):
    todo = Todo.collection.find({"position": position - 1})[0]
    if todo:
        Todo.collection.delete_one({"_id": ObjectId(todo['_id'])})
        typer.echo(f"deleting {position}")
    else: 
        typer.echo(f"todo at {position} not found")
    show()

@app.command(short_help='Update an item')
def update(position: int, task: str = None, category: str = None):
    todo = Todo.collection.find({"position": position - 1})[0]

    if todo:
        task = task if task is not None else todo['task']
        category = category if category is not None else todo['category']
   
        Todo.collection.update_one({"_id": ObjectId(todo['_id'])}, {
            '$set': {
                "task": task,
                "category": category
            }
        })
        typer.echo(f"updating {position}")
    else: 
        typer.echo(f"todo at {position} not found")
    show()

@app.command(short_help='Complete an item')
def complete(position: int):
    todo = Todo.collection.find({"position": position - 1})[0]

    if todo:   
        Todo.collection.update_one({"_id": ObjectId(todo['_id'])}, {
            '$set': {"status": 2}
        })
        typer.echo(f"Complete {position}")
    else: 
        typer.echo(f"todo at {position} not found")
    show()

@app.command(short_help='List all item')
def show():
    todos = Todo.collection.find()
    
    console.print("[bold magenta]Todos[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column('#', style="dim", width=6)
    table.add_column('Todo', width=20)
    table.add_column('Category', width=12, justify="right")
    table.add_column('Done', width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'Youtube': 'red', 'Sports': 'yellow', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for index, todo in enumerate(todos, start=1):
        category = todo['category']
        category_color = get_category_color(category)
        is_done_str = 'Complete' if todo['status'] == 2 else 'Not yet'
        is_done_color = 'green' if todo['status'] == 2 else 'red'
        table.add_row(str(index), todo['task'], f'[{category_color}]{category}[/{category_color}]', f'[{is_done_color}]{is_done_str}[/{is_done_color}]')

    console.print(table)

if __name__ == "__main__":
    app()