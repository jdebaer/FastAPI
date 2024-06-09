from fastapi import FastAPI
from models import Todo

# PUT implies putting a resource - completely replacing whatever is available at the given URL with a different thing. By definition, a PUT is idempotent. 
# Do it as many times as you like, and the result is the same. x=5 is idempotent. You can PUT a resource whether it previously exists, or not (eg, to Create, 
# or to Update)!
# POST updates a resource, adds a subsidiary resource, or causes a change. A POST is not idempotent, in the way that x++ is not idempotent.
# By this argument, PUT is for creating when you know the URL of the thing you will create. POST can be used to create when you know the URL of 
# the "factory" or manager for the category of things you want to create.
#
#So:
#POST /expense-report
#or:
#PUT  /expense-report/10929

todos = [] 									# Using a non-persisted list since we're focusing on the API alone here.

app = FastAPI()

# Landing 'page'.
@app.get('/')									# The method below this decorator handles everything for '/'.
async def root():								# Call this method anything you want.
    return {'message': 'Welcome to the todo web app!'}				# Let's just return some JSON.

# Get all todos.
@app.get('/todos')
async def get_todos():
    # This wraps the list in an outer JSON object.
    #return {'todos': todos}
    # This return the list itself.    
    return todos

# Create a todo.
@app.post('/todos')
async def create_todo(new_todo: Todo):
    
    # Simulating DB constraint that each ID has to be unique.
    for todo in todos:                                                          # It's a list of Todo objects.
        if todo.id == new_todo.id:
            return {'message': 'Todo with this ID already exists - not created.'}

    todos.append(new_todo)
    return {'message': 'Todo has been added.'}

# Get a single todo.
@app.get('/todos/{todo_id}')
async def get_todo(todo_id: int):
    for todo in todos:								# It's a list of Todo objects.
        if todo.id == todo_id:
            # return {'todo': todo}
            return todo
    return {'message': 'Todo was not found.'}

# Delete a single todo - start with copy from get single.
@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id: int):
    for todo in todos:                                                          # It's a list of Todo objects.
        if todo.id == todo_id:
            todos.remove(todo)
            return {'message': 'Todo was removed.'}
    return {'message':'Todo was not found.'}

# Update a single todo - remember that PUT has to be idempotent. Start with copy from get single.
# PUT should replace the whole object, with PATCH you modify parts of the object.
@app.put('/todos/{todo_id}')
async def update_todo(todo_id: int, todo_new: Todo):				# The Todo item has to be in the body.

    if todo_id != todo_new.id:
        return {'message': 'ID of new Todo has to match ID used for retrieval.'}

    for todo in todos:                                                          # It's a list of Todo objects.
        if todo.id == todo_id:							# We use todo_id to match, but not for the update itself.
            todo.id = todo_new.id						# Id of the replacing object that we're passing in.
            todo.item = todo_new.item						# Item of the replacing object that we're passing in.
            #return {'todo', todo} 
            return todo
    return {'message':'Todo to update was not found.'}
