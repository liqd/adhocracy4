var Comment = require('./Comment')

var React = require('react')

var CommentList = (props) => {
  return (
    <div>
      {
        props.comments.map((comment, index) => {
          return <Comment
            key={comment.id}
            user_name={comment.user_name}
            child_comments={comment.child_comments}
            created={comment.created}
            modified={comment.modified}
            authorIsModerator={comment.is_moderator}
            id={comment.id}
            content_type={comment.content_type}
            object_pk={comment.object_pk}
            is_deleted={comment.is_deleted}
            index={index}
            parentIndex={props.parentIndex}
            handleCommentDelete={props.handleCommentDelete}
            handleCommentSubmit={props.handleCommentSubmit}
            handleCommentModify={props.handleCommentModify}
            positiveRatings={comment.ratings.positive_ratings}
            negativeRatings={comment.ratings.negative_ratings}
            userRating={comment.ratings.current_user_rating_value}
            userRatingId={comment.ratings.current_user_rating_id}
            isReadOnly={props.isReadOnly}
            replyError={comment.replyError}
            errorMessage={comment.errorMessage}
            handleReplyErrorClick={props.handleReplyErrorClick}
            editError={comment.editError}
            handleEditErrorClick={props.handleEditErrorClick}
          >{comment.comment}
          </Comment>
        })
      }
    </div>
  )
}

module.exports = CommentList
