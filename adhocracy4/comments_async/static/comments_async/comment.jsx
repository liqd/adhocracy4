
import React from 'react'
import ReactMarkdown from 'react-markdown'
import PropTypes from 'prop-types'
import django from 'django'
import gfm from 'remark-gfm'

import Modal from '../modals/modal'
import ReportModal from '../modals/report_modal'
import UrlModal from '../modals/url_modal'
import CommentEditForm from './comment_edit_form'
import CommentCategoryEditForm from './comment_category_edit_form'
import CommentForm from './comment_form'
import CommentManageDropdown from './comment_manage_dropdown'
import CommentList from './comment_list'

import { RatingBox } from '../../../ratings/static/ratings/react_ratings'

const successMessage = django.gettext('Entry successfully created')
const readMore = django.gettext('Read more...')
const readLess = django.gettext('Read less')
const share = django.gettext('Share')
const report = django.gettext(' Report')

function localeDate (dateStr) {
  var options = { day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric' }
  return new Date(dateStr).toLocaleString(document.documentElement.lang, options)
}

function getAnswerForm (hide, number) {
  let result
  if (hide) {
    result = django.gettext('hide comments')
  } else {
    if (number > 0) {
      const tmp = django.ngettext('1 comment', '%s comments', number)
      result = django.interpolate(tmp, [number])
    } else {
      result = django.pgettext('verb', 'Comment')
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

  commentCategoryChoices () {
    if (this.props.withCategories === true) {
      return this.props.commentCategoryChoices
    }
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
      if (!this.props.commentCategoryChoices) {
        comment = (
          <CommentEditForm
            subjectType={this.props.content_type}
            subjectId={this.props.object_pk}
            comment={this.props.children}
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
        comment = (
          <CommentCategoryEditForm
            subjectType={this.props.content_type}
            subjectId={this.props.object_pk}
            comment={this.props.children}
            withCategories={this.props.withCategories}
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
      }
    } else {
      let content
      if (this.props.children.length > 400 && this.state.shorten) {
        content = this.props.children.substring(0, 400) + '...'
      } else {
        content = this.props.children
      }
      comment = (
        <div className={'a4-comments__text' + (this.state.anchored ? ' a4-comments__text--highlighted' : '')}>
          <ReactMarkdown disallowedTypes={['heading']} plugins={[[gfm, { singleTilde: false }]]} children={content} />
        </div>
      )
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
      moderatorLabel = <span className="a4-comments__moderator">{django.gettext('Moderator')}</span>
    }

    let userImage
    if (!this.props.is_deleted) {
      if (this.props.user_image) {
        var sectionStyle = {
          backgroundImage: 'url(' + this.props.user_image + ')'
        }
        userImage = <div className="user-avatar user-avatar--small user-avatar--shadow mb-1 userindicator__btn-img" style={sectionStyle} />
      }
    }

    const userProfile = this.props.user_profile_url

    return (
      <div>
        {this.state.displayNotification &&
          <div className="alert alert--success a4-comments__success-notification"><i className="fas fa-check" /> {successMessage}</div>}
        <div className={(this.isOwner() ? 'a4-comments__comment a4-comments__comment-owner' : 'a4-comments__comment')}>
          <a className="a4-comments__anchor" id={`comment_${this.props.id}`} href={`./?comment=${this.props.id}`}>{`Comment ${this.props.id}`}</a>
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
          <div className="a4-comments__box">
            <div className="a4-comments__box--user">
              <div className="row">

                <div className={this.props.is_deleted ? 'd-none' : 'col-2 col-md-1'}>
                  {userImage}
                </div>
                <div className="col-7 col-md-8">
                  <h5 className={this.props.is_deleted ? 'a4-comments__deleted-author' : 'a4-comments__author'}>
                    {userProfile === '' ? this.props.user_name
                      : <a href={userProfile}>{this.props.user_name}</a>}
                  </h5>
                  {moderatorLabel}
                  <div className="a4-comments__submission-date">{lastDate}</div>
                </div>

                <div className="col-1 col-md-1 ml-auto">
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
            </div>

            <div className="row">
              <div className={this.state.anchored ? 'a4-comments__box--comment a4-comments__box--highlighted' : 'a4-comments__box--comment'}>
                <div className="col-12">
                  <span className="sr-only">{django.gettext('Categories: ')}</span>
                  {this.renderCategories()}
                </div>
              </div>
            </div>

            <div className="row">
              <div className="col-12">
                {this.renderComment()}
              </div>
            </div>

            <div className="row">
              <div className="col-6 col-md-4">
                {this.props.children.length > 400 && this.state.shorten && <button className="btn btn--none text-muted px-0" onClick={this.showMore.bind(this)}>{readMore}</button>}
                {this.props.children.length > 400 && !this.state.shorten && <button className="btn btn--none text-muted px-0" onClick={this.showLess.bind(this)}>{readLess}</button>}
              </div>

            </div>

            <div className="row">
              <nav className="col-12 navbar navbar-default navbar-static">
                {this.renderRatingBox()}

                <div className="a4-comments__action-bar">
                  {((this.allowForm() && !this.props.is_deleted) || (this.props.child_comments && this.props.child_comments.length > 0)) &&
                    <button className="btn btn--no-border a4-comments__action-bar__btn" type="button" onClick={this.toggleShowComments.bind(this)}>
                      <a href="#child-comment-form">
                        <i className={this.state.showChildComments ? 'fa fa-minus' : 'far fa-comment-alt'} aria-hidden="true" /> {getAnswerForm(this.state.showChildComments, this.props.child_comments.length)}
                      </a>
                    </button>}

                  {!this.props.is_deleted &&
                    <a
                      className="btn btn--no-border a4-comments__action-bar__btn" href={`?comment_${this.props.id}`}
                      data-toggle="modal" data-target={`#share_comment_${this.props.id}`}
                    ><i className="fas fa-share" /> {share}
                    </a>}

                  {!this.props.is_deleted && this.context.isAuthenticated && !this.isOwner() &&
                    <a
                      className="btn btn--no-border a4-comments__action-bar__btn" href={`#report_comment_${this.props.id}`}
                      data-toggle="modal"
                    ><i className="fas fa-exclamation-triangle" />{report}
                    </a>}

                </div>
              </nav>
            </div>

          </div>
        </div>

        <div className="container">
          {this.state.showChildComments
            ? (
              <div className="a4-comments__child--list">
                <div className="row a4-comments__list">
                  <div className="col-12 ml-3">
                    <CommentList
                      filter="all"
                      comments={this.props.child_comments}
                      anchoredCommentId={this.props.anchoredCommentId}
                      anchoredCommentParentId={this.props.anchoredCommentParentId}
                      parentIndex={this.props.index}
                      onCommentDelete={this.props.onCommentDelete}
                      onCommentModify={this.props.onCommentModify}
                      isReadOnly={this.props.isReadOnly}
                      onEditErrorClick={this.props.handleEditErrorClick}
                    />
                  </div>
                </div>
                <div className="row">
                  <div className="col-12 ml-3">
                    <CommentForm
                      subjectType={this.context.comments_contenttype}
                      subjectId={this.props.id}
                      onCommentSubmit={this.props.onCommentSubmit}
                      parentIndex={this.props.index}
                      placeholder={django.gettext('Your reply here')}
                      error={this.props.replyError}
                      errorMessage={this.props.errorMessage}
                      handleErrorClick={() => this.props.handleReplyErrorClick(this.props.index, this.props.parentIndex)}
                      rows="1"
                      autoFocus
                      isReadOnly={this.props.isReadOnly}
                      isContextMember={this.props.isContextMember}
                    />
                  </div>
                </div>
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
