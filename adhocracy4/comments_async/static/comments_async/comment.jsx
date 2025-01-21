import React from 'react'
import ReactMarkdown from 'react-markdown'
import django from 'django'

import Modal from '../../../static/Modal'
import { ReportModal } from '../../../reports/static/reports/react_reports'
import { UrlModal } from '../modals/UrlModal'
import CommentForm from './comment_form'
import CommentManageDropdown from './comment_manage_dropdown'
import CommentList from './comment_list'
import { ModeratorFeedback } from './moderator_feedback'
import AiReport from './ai_report'
import RatingBox from '../../../ratings/static/ratings/RatingBox'
import Alert from '../../../static/Alert'

const translated = {
  reportTitle: django.gettext('You want to report this content? Your message will be sent to the moderation. The moderation will look at the reported content. The content will be deleted if it does not meet our discussion rules (netiquette).'),
  shareLink: django.gettext('Share link'),
  categories: django.gettext('Categories: '),
  successMessage: django.gettext('Entry successfully created'),
  readMore: django.gettext('Read more...'),
  readLess: django.gettext('Read less'),
  showModStatement: django.gettext('Show moderator\'s feedback'),
  hideModStatement: django.gettext('Hide moderator\'s feedback'),
  deleteCommentQuestion: django.gettext('Do you really want to delete this comment?'),
  deleteComment: django.gettext('Delete comment'),
  delete: django.gettext('Delete'),
  deletedyByCreatorOn: django.gettext('Deleted by creator on'),
  deletedByModeratorOn: django.gettext('Deleted by moderator on'),
  blockedByModerator: django.gettext('Blocked by moderator'),
  lastEditOn: django.gettext('Latest edit on'),
  moderator: django.gettext('Moderator'),
  hideReplies: django.gettext('hide replies'),
  reply: django.pgettext('verb', 'Reply'),
  ariaReadMore: django.gettext('Click to view rest of comment text.'),
  ariaReadLess: django.gettext('Click to hide expanded text.')
}

function getAnswerForm (hide, number) {
  let result
  if (hide) {
    result = translated.hideReplies
  } else {
    if (number > 0) {
      const tmp = django.ngettext('1 reply', '%s replies', number)
      result = django.interpolate(tmp, [number])
    } else {
      result = translated.reply
    }
  }
  return result
}

export default class Comment extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      edit: false,
      showChildComments: false,
      shorten: true,
      anchored: false,
      showModStatement: true,
      moderatorFeedback: this.props.moderatorFeedback
    }

    if (this.props.displayNotification) {
      setTimeout(
        () => {
          props.hideNotification(this.props.index, this.props.parentIndex)
        }, 2000)
    }
  }

  componentDidMount () {
    this.setState({
      showChildComments: this.props.id === this.props.anchoredCommentParentId,
      shorten: this.props.id !== this.props.anchoredCommentId,
      anchored: this.props.id === this.props.anchoredCommentId
    })
    if (this.props.id === this.props.anchoredCommentId) {
      this.props.onRenderFinished()
    }
  }

  toggleEdit (e) {
    if (e) {
      e.preventDefault()
    }
    const newEdit = !this.state.edit
    this.setState({ edit: newEdit })
  }

  toggleShowComments (e) {
    e.preventDefault()
    const newShowChildComment = !this.state.showChildComments
    this.setState({
      showChildComments: newShowChildComment
    })
  }

  replyComments (e) {
    e.preventDefault()
    this.setState({
      showChildComments: true
    })
  }

  allowForm () {
    return this.props.has_comment_commenting_permission && this.props.content_type !== this.props.comment_content_type
  }

  displayCategories () {
    return this.props.content_type !== this.props.comment_content_type
  }

  toggleExpand (e) {
    e.preventDefault()
    const newShorten = !this.state.shorten
    this.setState({
      shorten: newShorten
    })
  }

  renderReadMore () {
    if (this.props.children.length > 400) {
      return (
        <button
          className="btn btn--none text-muted px-0 a4-comments__read-btn"
          type="button"
          onClick={this.toggleExpand.bind(this)}
        >
          {this.state.shorten ? translated.readMore : translated.readLess}
        </button>
      )
    }
  }

  renderRatingBox () {
    if (!this.props.is_deleted) {
      return (
        <RatingBox
          contentType={this.props.comment_content_type}
          objectId={this.props.id}
          authenticatedAs={this.props.authenticated_user_pk}
          positiveRatings={this.props.positiveRatings}
          negativeRatings={this.props.negativeRatings}
          userRating={this.props.userRating}
          userRatingId={this.props.userRatingId}
          isReadOnly={!this.props.has_rating_permission}
          isComment
        />
      )
    }
  }

  renderComment () {
    let comment
    if (this.state.edit) {
      comment = (
        // Edit comment form
        <CommentForm
          editing
          subjectType={this.props.content_type}
          subjectId={this.props.object_pk}
          comment={this.props.children}
          commentLength={this.props.children.length}
          commentId={this.props.id}
          commentCategoryChoices={this.props.commentCategoryChoices}
          comment_categories={this.props.comment_categories}
          hasCommentingPermission={this.props.hasCommentingPermission}
          wouldHaveCommentingPermission={this.props.wouldHaveCommentingPermission}
          useTermsOfUse={this.props.useTermsOfUse}
          agreedTermsOfUse={this.props.agreedTermsOfUse}
          orgTermsUrl={this.props.orgTermsUrl}
          error={this.props.editError}
          errorMessage={this.props.errorMessage}
          handleErrorClick={() => this.props.onEditErrorClick(this.props.index, this.props.parentIndex)}
          rows="5"
          handleCancel={this.toggleEdit.bind(this)}
          index={this.props.index}
          parentIndex={this.props.parentIndex}
          showCancel
          setCommentError={this.props.setCommentEditError}
          onCommentSubmit={newComment => {
            return this.props.onCommentModify(newComment, this.props.index, this.props.parentIndex)
              .then(() => {
                this.setState({
                  edit: false
                })
                return null
              }).catch(error => {
                console.warn(error)
              })
          }}
        />
      )
    } else {
      let content
      if (this.props.children.length > 400 && this.state.shorten) {
        content = this.props.children.substring(0, 400) + '...'
      } else {
        content = this.props.children
      }
      comment = (
        <div className={'a4-comments__text' + (this.state.anchored ? ' a4-comments__text--highlighted' : '')}>
          {this.props.is_moderator_marked
            ? <mark>
              <ReactMarkdown
                disallowedElements={['h1', 'h2', 'h3', 'h4', 'input', 'table', 'thead', 'tr', 'th']}
                unwrapDisallowed
              >
                {content}
              </ReactMarkdown>
            </mark>// eslint-disable-line react/jsx-closing-tag-location
            : <ReactMarkdown
                disallowedElements={['h1', 'h2', 'h3', 'h4', 'input', 'table', 'thead', 'tr', 'th']}
                unwrapDisallowed
              >
              {content}
            </ReactMarkdown>/* eslint-disable-line react/jsx-closing-tag-location */}
        </div>
      )
    }
    return comment
  }

  renderCategories () {
    if (!this.state.edit && this.props.withCategories) {
      const categories = this.props.comment_categories
      const categoryHeading = <p className="sr-only">{translated.categories}</p>
      let categoryValue = ''
      let categoryClassName = ''

      const categoryHtml = Object.keys(categories).map(function (objectKey, index) {
        categoryValue = categories[objectKey]
        categoryClassName = 'badge a4-comments__badge a4-comments__badge--' + objectKey

        return (
          <span className={categoryClassName} key={objectKey}>
            {categoryValue}
          </span>
        )
      })

      return (
        <div className="col-12">
          {categoryHeading}
          {categoryHtml}
        </div>
      )
    }
  }

  getCommentUrl () {
    return window.location.href.split('?')[0].split('#')[0] + '?comment=' + this.props.id
  }

  render () {
    let lastDate
    if (this.props.is_blocked) {
      lastDate = translated.blockedByModerator
    } else if (this.props.modified === null) {
      lastDate = this.props.created
    } else if (this.props.is_removed) {
      lastDate = translated.deletedyByCreatorOn + ' ' + this.props.modified
    } else if (this.props.is_censored) {
      lastDate = translated.deletedByModeratorOn + ' ' + this.props.modified
    } else {
      lastDate = translated.lastEditOn + ' ' + this.props.modified
    }

    let moderatorLabel
    if (this.props.authorIsModerator && !this.props.is_deleted) {
      moderatorLabel = <span className="a4-comments__moderator">{translated.moderator}</span>
    }

    let userImage
    if (!this.props.is_deleted) {
      if (this.props.user_image) {
        const sectionStyle = {
          backgroundImage: 'url(' + this.props.user_image + ')'
        }
        userImage = <div className="user-avatar user-avatar--small user-avatar--shadow mb-1 userindicator__btn-img" style={sectionStyle} />
      }
    }

    const userProfile = this.props.user_profile_url

    const modals = {
      deleteModal: (
        <Modal
          partials={{
            title: translated.deleteComment,
            description: translated.deleteCommentQuestion
          }}
          handleSubmit={() => this.props.onCommentDelete(this.props.index, this.props.parentIndex)}
          action={translated.delete}
          toggle={translated.delete}
        />
      ),
      reportModal: (
        <ReportModal
          description={translated.reportTitle}
          btnStyle="cta"
          contentType={this.props.comment_content_type}
        />
      ),
      urlModal: (
        <UrlModal
          title={translated.shareLink}
          btnStyle="cta"
          url={this.getCommentUrl()}
        />
      )
    }

    return (
      <li>
        {this.props.displayNotification && <Alert type="success" message={translated.successMessage} />}
        <div className={(this.props.is_users_own_comment ? 'a4-comments__comment a4-comments__comment-owner' : 'a4-comments__comment')}>
          <a className="a4-comments__anchor" id={'comment_' + this.props.id} href={'./?comment=' + this.props.id}>{'Comment ' + this.props.id}</a>
          <div className="a4-comments__box">
            <div className="row">
              <div className={this.props.is_deleted ? 'd-none' : 'col-2 col-lg-1 a4-comments__user-img'}>
                {userImage}
              </div>
              <div className="col-7 col-md-8 a4-comments__author-container">
                <div className={this.props.is_deleted ? 'a4-comments__deleted-author' : 'a4-comments__author'}>
                  {userProfile === ''
                    ? this.props.user_name
                    : <a href={userProfile}>{this.props.user_name}</a>}
                </div>
                {moderatorLabel}
                <time className="a4-comments__submission-date">
                  {lastDate}
                </time>
              </div>

              <div className="col-1 ms-auto a4-comments__dropdown-container">
                {!this.props.is_deleted && (this.props.has_changing_permission || this.props.has_deleting_permission) &&
                  <CommentManageDropdown
                    id={this.props.id}
                    handleToggleEdit={this.toggleEdit.bind(this)}
                    has_changing_permission={this.props.has_changing_permission}
                    has_deleting_permission={this.props.has_deleting_permission}
                    isParentComment={this.displayCategories()}
                    modals={modals}
                  />}
              </div>

              {this.renderCategories()}

              <div className="col-12">
                {this.renderComment()}
              </div>
              <div className="col-6 a4-comments__read-btn-container">
                {this.renderReadMore()}
              </div>
              {this.state.moderatorFeedback &&
                <div className="col-6 text-end">
                  <button
                    className="btn btn--none text-muted px-0 a4-comments__read-btn"
                    onClick={
                      () => this.setState(
                        { showModStatement: !this.state.showModStatement }
                      )
                    }
                  >
                    {this.state.showModStatement
                      ? translated.hideModStatement
                      : translated.showModStatement}
                  </button>
                </div>}
            </div>
          </div>

          {this.props.aiReport && this.props.aiReport.show_in_discussion &&
            <AiReport
              report={this.props.aiReport}
            />}

          {this.state.showModStatement && this.state.moderatorFeedback &&
            <ModeratorFeedback
              lastEdit={this.state.moderatorFeedback.last_edit}
              feedbackText={this.state.moderatorFeedback.feedback_text}
            />}
          <div className="a4-comments__action">
            <div className="row">
              <div className="col-12 a4-comments__action-bar-container">
                {this.renderRatingBox()}

                <div className="a4-comments__action-bar">
                  {((this.allowForm() && !this.props.is_deleted) || (this.props.child_comments && this.props.child_comments.length > 0)) &&
                    <button className="btn btn--no-border a4-comments__action-bar__btn" type="button" onClick={this.toggleShowComments.bind(this)}>
                      <a href="#child-comment-form">
                        <i className={this.state.showChildComments ? 'fa fa-minus' : 'far fa-comment'} aria-hidden="true" /> {getAnswerForm(this.state.showChildComments, this.props.child_comments.length)}
                      </a>
                    </button>}

                  {!this.props.is_deleted && modals.urlModal}

                  {!this.props.is_deleted && this.props.authenticated_user_pk && !this.props.is_users_own_comment && modals.reportModal}
                </div>
              </div>
            </div>
          </div>
        </div>

        <>
          {this.state.showChildComments
            ? (
              <div className="a4-comments__child--list">
                <div className="row a4-comments__list">
                  <div className="col-12 ms-3">
                    <CommentList
                      filter="all"
                      comments={this.props.child_comments}
                      anchoredCommentId={this.props.anchoredCommentId}
                      anchoredCommentParentId={this.props.anchoredCommentParentId}
                      hasCommentingPermission={this.props.hasCommentingPermission}
                      wouldHaveCommentingPermission={this.props.wouldHaveCommentingPermission}
                      parentIndex={this.props.index}
                      onRenderFinished={this.props.onRenderFinished}
                      onCommentDelete={this.props.onCommentDelete}
                      onCommentModify={this.props.onCommentModify}
                      onEditErrorClick={this.props.onEditErrorClick}
                      useTermsOfUse={this.props.useTermsOfUse}
                      agreedTermsOfUse={this.props.agreedTermsOfUse}
                      orgTermsUrl={this.props.orgTermsUrl}
                      setCommentError={this.props.setCommentError}
                      setCommentEditError={this.props.setCommentEditError}
                      hideNotification={this.props.hideNotification}
                    />
                  </div>
                </div>
                <div className="row">
                  <div className="col-12 ms-3">
                    {/* Child comment form */}
                    <CommentForm
                      subjectType={this.props.comment_content_type}
                      subjectId={this.props.id}
                      commentId={'reply' + this.props.id}
                      onCommentSubmit={this.props.onCommentSubmit}
                      parentIndex={this.props.index}
                      error={this.props.replyError}
                      errorMessage={this.props.errorMessage}
                      handleErrorClick={() => this.props.onReplyErrorClick(this.props.index, this.props.parentIndex)}
                      // we need the autoFocus here after clicking reply
                      autoFocus // eslint-disable-line jsx-a11y/no-autofocus
                      hasCommentingPermission={this.props.hasCommentingPermission}
                      wouldHaveCommentingPermission={this.props.wouldHaveCommentingPermission}
                      projectIsPublic={this.props.projectIsPublic}
                      useTermsOfUse={this.props.useTermsOfUse}
                      agreedTermsOfUse={this.props.agreedTermsOfUse}
                      orgTermsUrl={this.props.orgTermsUrl}
                      setCommentError={this.props.setCommentError}
                    />
                  </div>
                </div>
              </div>)
            : null}
        </>
      </li>
    )
  }
}
