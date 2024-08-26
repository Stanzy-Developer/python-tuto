from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Create a pydantic model called Post 
# it acts as a data model for the blog post entity.
class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


my_list = [
     {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
]

@app.get("/posts/")
def read_posts():
  return my_list

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
   post_dict = post.dict()
   post_dict["id"] = randrange(1, 100)
   my_list.append(post_dict)
   return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
   post = my_list[-1]
   return {"post_details": post}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
   post = find_post(id)
   if not post:
      raise HTTPException(status_code=status.HTTP_404_N0T_FOUND, detail=f"Post with ID {id} not found")
   return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_202_NO_CONTENT)
def delete_post(id: int):
   idx = find_index_post(id)
   if idx is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Post with ID: {id} does not exist")
   my_list.pop(idx)
   return {"message": f"Post with ID: {id} successfully deleted"}

@app.put("posts/{id}")
def update_post(id: int, post: Post):
   idx = find_index_post(id)
   if idx is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Post with ID {id} dose not exist")
   post_dict = post.dict()
   post_dict["id"] = id
   my_list[idx] = post_dict
   return{"message": f"Post with ID {id} successfully updated"}

def find_post(id):
   for p in my_list:
      if p["id"] == id:
       return p
      
def find_index_post(id):
   for i, p in enumerate(my_list):
      if p["id"] == id:
         return i
