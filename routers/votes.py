from fastapi import FastAPI,status, HTTPException, Response,Depends, APIRouter
from fastapi.params import Body
from Schema.schema import Vote
from typing import List, Optional
import time
from concel_data.oauth import get_current_user
from concel_data.database import get_db
from Schema import model
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes",tags=['Likes'])

@router.post("/", status_code = status.HTTP_201_CREATED,)
async def vote(vote: Vote,db: Session= Depends(get_db), current_user: Session = Depends(get_current_user)):
    posts = db.query(model.Posts).filter(model.Posts.id == vote.post_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {vote.post_id} doesn't exists ")

    vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id, model.Vote.user_id== current_user.id)
    found_vote = vote_query.first()
    if vote.dir ==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User id : {current_user.id} has already voted on post {vote.post_id}')
        new_vote = model.Vote(post_id =vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted"}
