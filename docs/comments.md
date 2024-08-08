# Comments
Work in progress documentation of the comment code structure

## React

### Class Diagram
The below diagram describes the dependencies between the main comment components
and the props they require to work.

```mermaid
classDiagram
    direction LR
    CommentBox --|> CommentList : Render Comments
    CommentBox --|> CommentForm : New Comment
    CommentList --|> "0 to n" Comment : Comments / Child Comments
    Comment --|> CommentForm : Edit Comment
    Comment --|> CommentList : Render Child Comments
    Comment --|> CommentForm : New Child Comment
    class CommentBox{
       Required Props
       -----------------------------------
       anchoredCommentId
       id
       noControlBar
       subjectId
       subjectType
       useModeratorMarked
       withCategories
    }
    class CommentList{
        Required Props
        ----------------------------------
        agreedTermsOfUse
        anchoredCommentId
        anchoredCommentParentId
        commentCategoryChoices
        comments
        hasCommentingPermission
        orgTermsUrl
        parentIndex
        projectIsPublic
        setCommentEditError
        setCommentError
        useTermsOfUse
        withCategories
        wouldHaveCommentingPermission
        hideNotification()
        onCommentDelete()
        onCommentModify()
        onCommentSubmit()
        onEditErrorClick()
        onRenderFinished()
        onReplyErrorClick()
    }
    class CommentForm{
        Required Props
        ----------------------------------
        agreedTermsOfUse
        autoFocus [new child comment]
        comment [when editing]
        commentCategoryChoices [new comment / when editing comment]
        commentId
        commentLength [when editing]
        comment_categories [when editing comment]
        editing [when editing]
        error
        errorMessage
        hasCommentingPermission
        index
        orgTermsUrl
        parentIndex [when editing / new child comment]
        projectIsPublic [new comment / new child comment]
        rows [new comment / when editing comment]
        showCancel [when editing]
        showCommentError
        subjectId
        subjectType
        useTermsOfUse
        withCategories [new comment]
        wouldHaveCommentingPermission
        handleCancel() [when editing]
        handleErrorClick()
        onCommentSubmit()
        setCommentError() [new comment]
    }
    class Comment{
        Required Props
        ----------------------------------
        agreedTermsOfUse
        aiReport
        anchoredCommentId
        anchoredCommentParentId
        authenticated_user_pk
        child_comments
        children
        commentCategoryChoices
        comment_categories
        comment_categories
        comment_content_type
        content_type
        created
        displayNotification
        editError
        errorMessage
        hasCommentingPermission
        has_changing_permission
        has_comment_commenting_permission
        has_deleting_permission
        has_deleting_permission
        has_rating_permission
        id
        index
        is_blocked
        is_censored
        is_deleted
        is_moderator_marked
        is_removed
        is_users_own_comment
        moderatorFeedback
        modified
        negativeRatings
        object_pk
        orgTermsUrl
        parentindex
        positiveRatings
        projectIsPublic
        replyError
        useTermsOfUse
        userRating
        userRatingId
        user_image
        user_name
        user_profile_url
        withCategories
        wouldHaveCommentingPermission
        hideNotification()
        onCommentDelete()
        onCommentModify()
        onCommentSubmit()
        onEditErrorClick()
        onRenderFinished()
        onReplyErrorClick()
        setCommentEditError()
        setCommentError()
    }
```
