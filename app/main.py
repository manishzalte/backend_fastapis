from fastapi import FastAPI,status, HTTPException, Response,Depends
from fastapi.params import Body
from Schema.model import Posts,User, UpdatePost
from random import randrange
from concel_data.database import connect_to_db
import time

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1","id":1},{"title":"favorite foods", "content": "I Like Pizza","id":2}]
# while True:
#     cursor =connect_to_db()
#     if cursor:
#         break
#     else:
#         print("Failed to connect trying again ")
#         time.sleep(2)
cur ,conn = connect_to_db()
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 
    return None

def find_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i 
    return None

@app.get("/posts")
async def posts():
    return {"Message":my_posts}

@app.post("/user")
async def greet_user(names:User):
    return {f"Hi {names.name.capitalize()} how are you ?"}

@app.post('/create/posts', status_code=status.HTTP_201_CREATED)
async def create_post(payload:Posts):
    cur.execute("""INSERT INTO posts (title,content,publish) values (%s , %s, %s ) RETURNING * """,(payload.title,payload.content, payload.publish))
    new_post = cur.fetchone()
    conn.commit()
    return{"message": "Sucessfully recived the data!","details":new_post}

@app.get("/posts/{id}")
async def get_posts(id:int):
    is_Posts = find_post(id)
    cur.execute(""" Select * FROM posts WHERE id = %s RETURNING * """,(str(id),) )
    pos = cur.fetchone()
    if not pos:
        return{"detalis":"No data found ", "status": status.HTTP_404_NOT_FOUND}
    return {"details": pos}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    index_post = cur.fetchone()
    conn.commit()
    if not index_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id : {id} was not found please try again")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.patch("/posts/{id}")
async def update_post(payload: UpdatePost, id:int):
    if id:
        posts = find_post(id)
        if posts:
            if payload.title:
                posts['title'] = payload.title
            elif payload.content:
                posts['content'] = payload.content
            return {"message":f"{id = } updated successfuly "}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id : {id} was not found")               
