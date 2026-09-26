from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)

@router.get('/', response_model=list[schemas.Post])
def get_posts(db: Annotated[Session, Depends(get_db)],
              user: Annotated[models.User, Depends(oauth2.get_current_user)],
              limit: int = 10, 
              skip: int = 0,
              search: str | None = ""
              ):
    
    posts = (db.query(
                    models.Post,
                    func.count(models.Vote.post_id).label("votes")
                ).filter(
                    models.Post.title.icontains(search)
                ).join(
                    target=models.Vote, 
                    onclause=models.Post.id == models.Vote.post_id, 
                    isouter=True
                ).group_by(
                    models.Post.id
                ).order_by(
                    models.Post.id
                ).limit(limit).offset(skip).all())
    
    result = []
    
    for post, vote in posts:
        result.append(
            schemas.Post(
                id=post.id,
                title=post.title,
                content=post.content,
                published=post.published,
                created_at=post.created_at,
                user_id=post.user_id,
                user=post.user,
                votes=vote
            )
        )
    
    return result

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, 
                db: Annotated[Session, Depends(get_db)],
                user: Annotated[models.User, Depends(oauth2.get_current_user)]
               ):
    
    new_post = models.Post(user_id = user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    result_post = schemas.Post(
            id=new_post.id,
            title=new_post.title,
            content=new_post.content,
            published=new_post.published,
            created_at=new_post.created_at,
            user_id=new_post.user_id,
            user=schemas.UserResponse(id=user.id, email=user.email, created_at=user.created_at),
            votes=0
        )
    
    return result_post

@router.get('/{id}', response_model=schemas.Post)
def get_post_by_id(id: int, 
                   db: Annotated[Session, Depends(get_db)],
                   user: Annotated[models.User, Depends(oauth2.get_current_user)]
                  ):
    # post = db.query(models.Post).filter(models.Post.id==id).first()
    
    post = (db.query(
                        models.Post,
                        func.count(models.Vote.post_id).label("votes")
                    ).filter(
                        models.Post.id==id
                    ).join(
                        target=models.Vote, 
                        onclause=models.Post.id == models.Vote.post_id, 
                        isouter=True
                    ).group_by(
                        models.Post.id
                    )).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} was not found")
    
    print(f"\n\npost: {post}\t post_type: {type(post)}")
    
    post = schemas.Post(
        id=post[0].id,
        title=post[0].title,
        content=post[0].content,
        published=post[0].published,
        created_at=post[0].created_at,
        user_id=post[0].user_id,
        user=post[0].user,
        votes=post[1]
    )
    
    return post

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, 
                post: schemas.PostCreate, 
                db: Annotated[Session, Depends(get_db)],
                user: Annotated[models.User, Depends(oauth2.get_current_user)]
               ):
    
    post_query = db.query(models.Post).filter(
                        and_(models.Post.id == id, 
                             models.Post.user_id == user.id)
                        )
    
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} was not found")

    post_query.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    db.refresh(updated_post)
    
    votes = (db.query(
                        func.count(models.Vote.post_id).label("votes")
                    ).filter(
                        models.Vote.post_id == id
                    )
    ).scalar()

    return schemas.Post(
        id=updated_post.id,
        title=updated_post.title,
        content=updated_post.content,
        published=updated_post.published,
        created_at=updated_post.created_at,
        user_id=updated_post.user_id,
        user=schemas.UserResponse(id=user.id, email=user.email, created_at=user.created_at),
        votes=int(votes)
    )

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Annotated[Session, Depends(get_db)], 
                user: Annotated[models.User, Depends(oauth2.get_current_user)]
               ):
    post_query = db.query(models.Post).filter(
                        and_(models.Post.id == id,
                             models.Post.user_id == user.id)
                        )
    deleted_post = post_query.first()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} was not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)