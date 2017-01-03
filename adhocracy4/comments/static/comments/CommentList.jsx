var Comment = require('./Comment')

var React = require('react')

var CommentList = React.createClass({
  render: function () {
    return (
      <div>
        {
          this.props.comments.map((comment, index) => {
            return <Comment
              key={comment.id}
              user_name={comment.user_name}
              child_comments={comment.child_comments}
              created={comment.created}
              modified={comment.modified}
              authorIsModerator={comment.is_moderator}
              id={comment.id}
              content_type={comment.content_type}
              is_deleted={comment.is_deleted}
              index={index}
              parentIndex={this.props.parentIndex}
              handleCommentDelete={this.props.handleCommentDelete}
              handleCommentSubmit={this.props.handleCommentSubmit}
              handleCommentModify={this.props.handleCommentModify}
              positiveRatings={comment.ratings.positive_ratings}
              negativeRatings={comment.ratings.negative_ratings}
              userRating={comment.ratings.current_user_rating_value}
              userRatingId={comment.ratings.current_user_rating_id}
              isReadOnly={this.props.isReadOnly}
            >{comment.comment}</Comment>
          })
        }
      </div>
    )
  }
})

module.exports = CommentList
