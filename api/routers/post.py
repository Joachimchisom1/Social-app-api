from fastapi import APIRouter, HTTPException
from api.models.post import (
    UserPost,
    UserPostIn,
    Comment,
    CommentIn,
    UserPostWithComment,
)

router = APIRouter()
post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


# CREATE POST
@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


# GET ALL POSTS
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


# CREATE Comment
@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
    # check if post exist
    post= find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    data = comment.dict()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment

# GET COMMENT ON POST @
@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_all_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values()
        if comment["post_id"] == post_id
    ]
    
@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comment(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "post": post,
        "comments": await get_all_comments_on_post(post_id)
    }