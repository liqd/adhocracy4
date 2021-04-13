import React from 'react'

import Comment from './comment'

export default function (props) {
  return (
    <div>
      {
        props.comments.map((comment, index) => {
          return (
            <Comment
              comment_categories={comment.comment_categories}
              key={comment.id}
              user_name={comment.user_name}
              user_pk={comment.user_pk}
              user_profile_url={comment.user_profile_url}
              user_image={comment.user_image}
              child_comments={comment.child_comments}
              created={comment.created}
              modified={comment.modified}
              authorIsModerator={comment.is_moderator}
              id={comment.id}
              content_type={comment.content_type}
              object_pk={comment.object_pk}
              is_deleted={comment.is_deleted}
              is_moderator_marked={comment.is_moderator_marked}
              index={index}
              parentIndex={props.parentIndex}
              onCommentDelete={props.onCommentDelete}
              onCommentSubmit={props.onCommentSubmit}
              onCommentModify={props.onCommentModify}
              positiveRatings={comment.ratings.positive_ratings}
              negativeRatings={comment.ratings.negative_ratings}
              userRating={comment.ratings.current_user_rating_value}
              userRatingId={comment.ratings.current_user_rating_id}
              isReadOnly={props.isReadOnly}
              isContextMember={props.isContextMember}
              replyError={comment.replyError}
              errorMessage={comment.errorMessage}
              onReplyErrorClick={props.onReplyErrorClick}
              editError={comment.editError}
              commentCategoryChoices={props.commentCategoryChoices}
              onEditErrorClick={props.onEditErrorClick}
              displayNotification={comment.displayNotification}
              anchoredCommentId={props.anchoredCommentId}
              anchoredCommentParentId={props.anchoredCommentParentId}
            >{comment.comment}
            </Comment>
          )
        })
      }
    </div>
  )
}
