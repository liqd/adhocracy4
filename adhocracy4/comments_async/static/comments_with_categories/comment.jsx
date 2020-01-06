import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import Modal from '../modals/modal'
import ModerateModal from '../modals/moderate_modal'
import ReportModal from '../modals/report_modal'
import UrlModal from '../modals/url_modal'
import CommentEditForm from './comment_edit_form'
import CommentForm from './comment_form'
import CommentManageDropdown from './comment_manage_dropdown'
import CommentList from './comment_list'

const RatingBox = require('../../../ratings/static/ratings/react_ratings').RatingBox

const safeHtml = function (text) {
  return { __html: text }
}

const successMessage = django.gettext('Entry successfully created')

const localeDate = function (dateStr) {
  var options = { day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric' }
  return new Date(dateStr).toLocaleString(document.documentElement.lang, options)
}

const getViewRepliesText = function (number, hide) {
  var fmts
  if (hide) {
    fmts = django.ngettext('hide one reply', 'hide %s replies', number)
  } else {
    fmts = django.ngettext('view one reply', 'view %s replies', number)
  }
  return django.interpolate(fmts, [number])
}

export default class Comment extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      edit: false,
      showChildComments: false,
      displayNotification: this.props.displayNotification,
      shorten: true,
      anchored: false
    }

    setTimeout(
      function () {
        this.setState({ displayNotification: false })
      }
        .bind(this),
      2000
    )
  }

  componentDidMount () {
    this.setState({
      showChildComments: this.props.id === this.props.anchoredCommentParentId,
      shorten: this.props.id !== this.props.anchoredCommentId,
      anchored: this.props.id === this.props.anchoredCommentId
    })
  }

  toggleEdit (e) {
    if (e) {
      e.preventDefault()
    }
    var newEdit = !this.state.edit
    this.setState({ edit: newEdit })
  }

  toggleShowComments (e) {
    e.preventDefault()
    var newShowChildComment = !this.state.showChildComments
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
    return !this.props.isReadOnly && this.props.content_type !== this.context.comments_contenttype
  }

  displayCategories () {
    return this.props.content_type !== this.context.comments_contenttype
  }

  isOwner () {
    return this.props.user_pk === this.context.user_name
  }

  showMore () {
    this.setState({
      shorten: false
    })
  }

  showLess () {
    this.setState({
      shorten: true
    })
  }

  renderRatingBox () {
    if (!this.props.is_deleted) {
      return (
        <RatingBox
          contentType={this.context.comments_contenttype}
          objectId={this.props.id}
          authenticatedAs={this.context.isAuthenticated ? this.context.user_name : null}
          positiveRatings={this.props.positiveRatings}
          negativeRatings={this.props.negativeRatings}
          userRating={this.props.userRating}
          userRatingId={this.props.userRatingId}
          isReadOnly={this.props.isReadOnly}
        />
      )
    }
  }

  renderComment () {
    let comment
    if (this.state.edit) {
      comment = (
        <CommentEditForm
          subjectType={this.props.content_type}
          subjectId={this.props.object_pk}
          comment={this.props.children}
          displayCategories={this.displayCategories()}
          commentCategoryChoices={this.props.commentCategoryChoices}
          comment_categories={this.props.comment_categories}
          error={this.props.editError}
          errorMessage={this.props.errorMessage}
          handleErrorClick={() => this.props.handleEditErrorClick(this.props.index, this.props.parentIndex)}
          rows="5"
          handleCancel={this.toggleEdit.bind(this)}
          onCommentSubmit={newComment => {
            this.props.onCommentModify(newComment, this.props.index, this.props.parentIndex)
              .then(() => {
                this.setState({
                  edit: false
                })
              })
          }}
        />
      )
    } else {
      if (this.props.children.length > 400 && this.state.shorten) {
        comment = <div className={'a4-comments__text' + (this.state.anchored ? ' a4-comments__text--highlighted' : '')} dangerouslySetInnerHTML={safeHtml(this.props.children.substring(0, 400) + '...')} />
      } else {
        comment = <div className={'a4-comments__text' + (this.state.anchored ? ' a4-comments__text--highlighted' : '')} dangerouslySetInnerHTML={safeHtml(this.props.children)} />
      }
    }
    return comment
  }

  renderCategories () {
    if (!this.state.edit && this.displayCategories()) {
      var categories = this.props.comment_categories
      let categoryValue = ''
      let categoryClassName = ''

      var categoryHtml = Object.keys(categories).map(function (objectKey, index) {
        categoryValue = categories[objectKey]
        categoryClassName = 'badge a4-comments__badge a4-comments__badge--' + objectKey

        return (
          <span className={categoryClassName} key={objectKey}>
            {categoryValue}
          </span>
        )
      })

      return categoryHtml
    }
  }

  renderDeleteModal () {
    if (this.isOwner() || this.context.isModerator) {
      return (
        <Modal
          name={`comment_delete_${this.props.id}`}
          partials={{ title: django.gettext('Do you really want to delete this comment?') }}
          handleSubmit={() => this.props.onCommentDelete(this.props.index, this.props.parentIndex)}
          action={django.gettext('Delete')}
          abort={django.gettext('Abort')}
          btnStyle="cta"
        />
      )
    }
  }

  renderModerateModal () {
    if (this.context.isModerator && this.displayCategories()) {
      return (
        <ModerateModal
          onCommentModerate={this.props.onCommentModerate}
          is_moderator_marked={this.props.is_moderator_marked}
          content_type={this.props.content_type}
          object_pk={this.props.object_pk}
          index={this.props.index}
          parentIndex={this.props.parentIndex}
          id={this.props.id}
        />
      )
    }
  }

  getCommentUrl () {
    return window.location.href.split('?')[0].split('#')[0] + '?comment=' + `${this.props.id}`
  }

  render () {
    let lastDate
    if (this.props.modified === null || this.props.is_deleted) {
      lastDate = localeDate(this.props.created)
    } else {
      lastDate = django.gettext('Latest edit on') + ' ' + localeDate(this.props.modified)
    }

    let moderatorLabel
    if (this.props.authorIsModerator && !this.props.is_deleted) {
      moderatorLabel = <span className="label a4-comments__label">{django.gettext('Moderator')}</span>
    }

    let userImage
    if (this.props.user_image && this.displayCategories()) {
      var sectionStyle = {
        backgroundImage: 'url(' + this.props.user_image + ')'
      }
      userImage = <span className="user-avatar user-avatar--small user-avatar--shadow mb-1" style={sectionStyle} />
    } else if (!this.props.is_deleted && this.displayCategories()) {
      userImage = <span className="user-avatar user-initial user-avatar--small user-avatar--shadow mb-2">{this.props.user_fallback}</span>
    }

    const userProfile = '/profile/' + this.props.user_pk

    return (
      <div>
        <div className={(this.isOwner() ? 'a4-comments__comment a4-comments__comment-owner' : 'a4-comments__comment')}>
          <a className="a4-comments__anchor" id={`comment_${this.props.id}`} href={`./?comment=${this.props.id}`}>{`Comment ${this.props.id}`}</a>
          <div className="container">
            <ReportModal
              name={`report_comment_${this.props.id}`}
              title={django.gettext('You want to report this content? Your message will be sent to the moderation. The moderation will look at the reported content. The content will be deleted if it does not meet our discussion rules (netiquette).')}
              btnStyle="cta"
              objectId={this.props.id}
              contentType={this.context.comments_contenttype}
            />
            <UrlModal
              name={`share_comment_${this.props.id}`}
              title={django.gettext('Share link')}
              btnStyle="cta"
              objectId={this.props.id}
              url={this.getCommentUrl()}
            />
            {this.renderDeleteModal()}
            {this.renderModerateModal()}
            <div className="a4-comments__box row">
              {(this.props.is_moderator_marked && this.displayCategories()) &&
                <span className={this.context.isAuthenticated && !this.props.is_deleted && (this.isOwner() || this.context.isModerator) ? 'a4-comments__featured--menu' : 'a4-comments__featured'}>
                  <i className="fas fa-bookmark" alt="Featured comment" />
                </span>}
              <div className="a4-comments__box--left">
                {this.props.userImage &&
                  { userImage }}
                <h5 className={this.props.is_deleted ? 'a4-comments__deleted-author' : 'a4-comments__author'}>
                  {this.props.is_deleted ? this.props.user_name
                    : <a href={userProfile}>{this.props.user_name}</a>}
                </h5>
                <div className="a4-comments__moderator">{moderatorLabel}</div>
                <div className="a4-comments__submission-date">{lastDate}</div>
              </div>
              <div className={this.state.anchored ? 'a4-comments__box--right a4-comments__border--highlighted' : 'a4-comments__box--right'}>
                <div class="row">
                  <div class="col-10">
                    <span className="sr-only">{django.gettext('Categories: ')}</span>
                    {this.renderCategories()}
                  </div>
                  <div class="col-2">
                    {this.context.isAuthenticated && !this.props.is_deleted && (this.isOwner() || this.context.isModerator) &&
                      <CommentManageDropdown
                        id={this.props.id}
                        handleToggleEdit={this.toggleEdit.bind(this)}
                        renderOwnerOptions={this.isOwner() && !this.props.isReadOnly}
                        renderModeratorOptions={this.context.isModerator && !this.props.isReadOnly}
                        isParentComment={this.displayCategories()}
                      />}
                  </div>
                </div>
                {this.renderComment()}
                {this.props.children.length > 400 && this.state.shorten && <button className="btn btn--link" onClick={this.showMore.bind(this)}>{django.gettext('Read more...')}</button>}
                {this.props.children.length > 400 && !this.state.shorten && <button className="btn btn--link" onClick={this.showLess.bind(this)}>{django.gettext('Read less')}</button>}
                <div className="action-bar">
                  <nav className="navbar navbar-default navbar-static a4-comments__navbar">
                    {this.renderRatingBox()}
                    <div className="a4-comments__nav">
                      {this.props.child_comments && this.props.child_comments.length > 0 &&
                        <button className="btn a4-comments__nav-btn" type="button" onClick={this.toggleShowComments.bind(this)}>
                          <i className={this.state.showChildComments ? 'fa fa-minus' : 'far fa-comment'} aria-hidden="true" /> {getViewRepliesText(this.props.child_comments.length, this.state.showChildComments)}
                        </button>}
                      {this.allowForm() && !this.props.is_deleted &&
                        <button
                          disabled={this.state.showChildComments}
                          className="btn a4-comments__nav-btn"
                          type="button"
                          onClick={this.replyComments.bind(this)}
                        >
                          <i className="fa fa-reply" aria-hidden="true" /> {django.gettext('Answer')}
                        </button>}
                      {!this.props.is_deleted &&
                        <a
                          className="btn a4-comments__nav-btn" href={`?comment_${this.props.id}`}
                          data-toggle="modal" data-target={`#share_comment_${this.props.id}`}
                        ><i className="fas fa-share" /> {django.gettext('Share')}
                        </a>}
                      {!this.props.is_deleted && !this.isOwner() &&
                        <a
                          className="btn a4-comments__nav-btn" href={`#report_comment_${this.props.id}`}
                          data-toggle="modal"
                        >{django.gettext('Report')}
                        </a>}
                    </div>
                  </nav>
                </div>
              </div>
            </div>
            {this.state.displayNotification &&
              <div className="a4-comments__success-notification"><i className="fas fa-check" /> {successMessage}</div>}
          </div>
        </div>
        <div className="container">
          {this.state.showChildComments
            ? (
              <div className="a4-comments__child--list">
                <div className="a4-comments__list">
                  <CommentList
                    filter="all"
                    comments={this.props.child_comments}
                    anchoredCommentId={this.props.anchoredCommentId}
                    anchoredCommentParentId={this.props.anchoredCommentParentId}
                    parentIndex={this.props.index}
                    onCommentDelete={this.props.onCommentDelete}
                    onCommentModify={this.props.onCommentModify}
                    onCommentModerate={this.props.onCommentModerate}
                    isReadOnly={this.props.isReadOnly}
                    onEditErrorClick={this.props.handleEditErrorClick}
                  />
                </div>
                <CommentForm
                  subjectType={this.context.comments_contenttype}
                  subjectId={this.props.id}
                  onCommentSubmit={this.props.onCommentSubmit}
                  parentIndex={this.props.index}
                  placeholder={django.gettext('Your reply here')}
                  error={this.props.replyError}
                  errorMessage={this.props.errorMessage}
                  handleErrorClick={() => this.props.handleReplyErrorClick(this.props.index, this.props.parentIndex)}
                  rows="3"
                />
              </div>) : null}
        </div>
      </div>
    )
  }
}

Comment.contextTypes = {
  comments_contenttype: PropTypes.number,
  isAuthenticated: PropTypes.bool,
  isModerator: PropTypes.bool,
  user_name: PropTypes.string,
  contentType: PropTypes.number
}
