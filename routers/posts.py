from fastapi import FastAPI,status, HTTPException, Response,Depends, APIRouter
from fastapi.params import Body
from Schema.model import Posts
from Schema.schema import CreatePost, UpdatePosts, RespondPosts,ResponseOut
from typing import List, Optional
from concel_data.oauth import get_current_user
from concel_data.database import get_db
from Schema import model
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts",tags=['Posts'])

# @router.get("/", response_model=List[RespondPosts] )
@router.get("/",response_model=List[ResponseOut] )
async def posts(db:Session = Depends(get_db),current_user:int =Depends(get_current_user),limit:int=10, skip: int =0, search:Optional[str] = ""):

#     cur.execute(""" SELECT * FROM posts """)
#     my_posts = cur.fetchmany(size=2)

    # posts = db.query(model.Posts).filter(model.Posts.title.contains(search)).limit(limit=limit).offset(skip).all()
    results = db.query(model.Posts,func.count(model.Vote.post_id).label("likes")).join(model.Vote, model.Vote.post_id == model.Posts.id, isouter=True).group_by(model.Posts.id).filter(func.lower(model.Posts.title).contains(search.lower())).limit(limit=limit).offset(skip).all()
    # results = []
    # for post, likes in query_result:
    #     # FastAPI can automatically handle the Post object, so we convert it to a dictionary
    #     # and then add our custom 'likes' field.
    #     post_dict = post.__dict__
    #     post_dict['likes'] = likes
    #     results.append(post_dict)
    
    return results


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=RespondPosts)
async def create_post(payload: CreatePost, db:Session = Depends(get_db), current_user:int =Depends(get_current_user)):
    # cur.execute("""INSERT INTO posts (title,content,publish) values (%s , %s, %s ) RETURNING * """,(payload.title,payload.content, payload.publish))
    # new_post = cur.fetchone()
    # conn.commit()
    # new_post = model.Posts(title =payload.title, content = payload.content, publish = payload.publish)
    # or just do the following 
    new_post = model.Posts(owner_id = current_user.id ,**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=ResponseOut)
async def get_posts(id:int, db:Session = Depends(get_db)): 
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),) )
    # pos = cur.fetchone()
    pos = db.query(model.Posts,func.count(model.Vote.post_id).label("likes")).join(model.Vote, model.Vote.post_id == model.Posts.id, isouter=True).group_by(model.Posts.id).filter(model.Posts.id ==id).first()
    # pos = db.query(model.Posts).filter(model.Posts.id ==id).first()
    if not pos:
        return{"detalis":"No data found ", "status": status.HTTP_404_NOT_FOUND}
    return pos

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session = Depends(get_db),current_user:int =Depends(get_current_user)):
    # cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # index_post = cur.fetchone()
    # conn.commit()
    index_post = db.query(model.Posts).filter(model.Posts.id ==id)
    post_to_delete = index_post.first()
    if post_to_delete is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="The post with was not found please trry again later")
    if post_to_delete.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorized to perform requested action")
    index_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", response_model=RespondPosts)
async def update_post(id : int , paylod: UpdatePosts, db: Session = Depends(get_db) , current_user:int = Depends(get_current_user)):
    post_query = db.query(model.Posts).filter(model.Posts.id == id)
    post = post_query.first()
    if post is None or post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"The post id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail= "You need to be the owner of the post")
    post_query.update(paylod.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post

@router.get("/get/user", status_code=status.HTTP_200_OK, response_model=List[ResponseOut])
async def get_post_of_user(db:Session = Depends(get_db), current_user:int = Depends(get_current_user)):
    if current_user:
        user_post =db.query(model.Posts,func.count(model.Vote.post_id).label("likes")).join(model.Vote, model.Vote.post_id == model.Posts.id, isouter=True).group_by(model.Posts.id).filter(model.Posts.owner_id == current_user.id and model.Posts.publish == 'false').all()
        # user_post = db.query(model.Posts).filter(model.Posts.owner_id == current_user.id and model.Posts.publish == 'false').all()
        if user_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found ")
        return user_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not Found")
    
# @app.patch("/posts/{id}")
# async def update_post(payload, id:int):
#     set_cause = []
#     set_param = []
#     if id:
#         if payload.title is not None:
#             set_cause.append("title = %s")
#             set_param.append(payload.title)
#         if payload.content is not None:
#             set_cause.append("content = %s")
#             set_param.append(payload.content)
#         if payload.publish is not None:
#             set_cause.append("publish =%s")
#             set_param.append(payload.publish)
#         if not set_cause:
#             raise HTTPException(status_code=400, detail="No fields to update provided.")
#         sql_query = f"UPDATE posts SET {', '.join(set_cause)} WHERE id = %s RETURNING *"
#         set_param.append(id)

#         cur.execute(sql_query, tuple(set_param))
#         updated_post = cur.fetchone()
#         conn.commit()
#         if not updated_post:
#             raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found.")

#         return {"message": "Post updated successfully", "post": updated_post}   
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id : {id} was not found")