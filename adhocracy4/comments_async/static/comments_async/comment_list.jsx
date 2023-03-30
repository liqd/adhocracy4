import React from 'react'

import Comment from './comment'

const CommentList = (props) => {
  return (
    <div>
      {
        props.comments.map((comment, index) => {
          return (
            <Comment
              comment_categories={comment.comment_categories}
              onRenderFinished={props.onRenderFinished}
              key={comment.id}
              user_name={comment.user_name}
              user_pk={comment.user_pk}
              user_profile_url={comment.user_profile_url}
              user_image={comment.user_image ? comment.user_image : comment.user_image_fallback}
              child_comments={comment.child_comments}
              created={comment.created}
              modified={comment.modified}
              authorIsModerator={comment.author_is_moderator}
              id={comment.id}
              content_type={comment.content_type}
              object_pk={comment.object_pk}
              is_deleted={comment.is_deleted}
              is_removed={comment.is_removed}
              is_censored={comment.is_censored}
              is_blocked={comment.is_blocked}
              is_moderator_marked={comment.is_moderator_marked}
              is_users_own_comment={comment.user_info.is_users_own_comment}
              authenticated_user_pk={comment.user_info.authenticated_user_pk}
              comment_content_type={comment.comment_content_type}
              has_viewing_permission={comment.user_info.has_viewing_permission}
              has_rating_permission={comment.user_info.has_rating_permission}
              has_changing_permission={comment.user_info.has_changing_permission}
              has_deleting_permission={comment.user_info.has_deleting_permission}
              has_moderating_permission={comment.user_info.has_moderating_permission}
              has_comment_commenting_permission={comment.user_info.has_comment_commenting_permission}
              index={index}
              parentIndex={props.parentIndex}
              onCommentDelete={props.onCommentDelete}
              onCommentSubmit={props.onCommentSubmit}
              onCommentModify={props.onCommentModify}
              positiveRatings={comment.ratings.positive_ratings}
              negativeRatings={comment.ratings.negative_ratings}
              userRating={comment.ratings.current_user_rating_value}
              userRatingId={comment.ratings.current_user_rating_id}
              replyError={comment.replyError}
              errorMessage={comment.errorMessage}
              onReplyErrorClick={props.onReplyErrorClick}
              editError={comment.editError}
              commentCategoryChoices={props.commentCategoryChoices}
              onEditErrorClick={props.onEditErrorClick}
              displayNotification={comment.displayNotification}
              anchoredCommentId={props.anchoredCommentId}
              anchoredCommentParentId={props.anchoredCommentParentId}
              hasCommentingPermission={props.hasCommentingPermission}
              wouldHaveCommentingPermission={props.wouldHaveCommentingPermission}
              projectIsPublic={props.projectIsPublic}
              moderatorFeedback={comment.moderator_feedback ? comment.moderator_feedback : null}
              useTermsOfUse={props.useTermsOfUse}
              agreedTermsOfUse={props.agreedTermsOfUse}
              orgTermsUrl={props.orgTermsUrl}
            >{comment.comment}
            </Comment>
          )
        })
      }
    </div>
  )
}

export default CommentList
