import React from 'react'
import django from 'django'

import CategoryList from './category_list'
import Alert from '../../../static/Alert'
import { TermsOfUseCheckbox } from '../../../static/TermsOfUseCheckbox'

import * as config from '../../../static/config'

const translated = {
  yourComment: django.gettext('Your comment'),
  addComment: django.gettext('Please add a comment.'),
  errorComment: django.gettext('Something seems to have gone wrong, please try again.'),
  yourReply: django.gettext('Your reply'),
  characters: django.gettext(' characters'),
  post: django.gettext('Post'),
  reply: django.pgettext('verb', 'Reply'),
  pleaseComment: django.gettext('Please login to comment'),
  onlyInvited: django.gettext('Only invited users can actively participate.'),
  notAllowedComment: django.gettext('The currently active phase doesn\'t allow to comment.'),
  cancel: django.gettext('Cancel'),
  placeholder: django.gettext('Share your thoughts'),
  replyPlaceholder: django.gettext('Reply to the comment')
}

const textareaMinHeight = 75

export default class CommentForm extends React.Component {
  constructor (props) {
    super(props)
    this.textareaRef = React.createRef()
    this.state = {
      comment: this.props.comment || '',
      commentCharCount: this.props.commentLength || 0,
      selectedCategories: Object.keys(this.props.comment_categories || {}),
      textareaHeight: textareaMinHeight,
      agreedTermsOfUse: props.agreedTermsOfUse,
      showCommentError: false,
      submitting: false
    }
  }

  componentDidUpdate (prevProps) {
    if (this.props.agreedTermsOfUse !== prevProps.agreedTermsOfUse) {
      this.setState({
        agreedTermsOfUse: this.props.agreedTermsOfUse
      })
    }
  }

  componentDidMount () {
    if (this.props.autoFocus && this.textareaRef.current) {
      this.textareaRef.current.focus()
    }
  }

  handleTextareaGrow (e) {
    const newHeight = (e.target.scrollHeight)
    if (newHeight !== this.state.textareaHeight && newHeight > textareaMinHeight) {
      this.setState({ textareaHeight: newHeight })
    }
  }

  handleTextChange (e) {
    this.setState({ comment: e.target.value, commentCharCount: e.target.value.length })
  }

  handleCategorySelection (e) {
    const newSelection = e.target.id.split('_')[1]
    const newSelectionArray = this.state.selectedCategories
    const index = this.state.selectedCategories.indexOf(newSelection)
    if (index > -1) {
      newSelectionArray.splice(index, 1)
    } else {
      newSelectionArray.push(newSelection)
    }
    this.setState({ selectedCategories: newSelectionArray })
  }

  clearForm () {
    this.setState({
      comment: '',
      commentCharCount: 0,
      selectedCategories: [],
      textareaHeight: textareaMinHeight,
      showCommentError: false
    })
  }

  handleSubmit (e) {
    e.preventDefault()
    this.setState({
      submitting: true
    })
    const comment = this.state.comment.trim()
    const data = {
      comment,
      urlReplaces: {
        objectPk: this.props.subjectId,
        contentTypeId: this.props.subjectType
      }
    }
    if (this.props.useTermsOfUse && !this.state.agreedTermsOfUse && this.state.checkedTermsOfUse) {
      data.agreed_terms_of_use = true
    }
    if (this.props.commentCategoryChoices) {
      data.comment_categories = this.state.selectedCategories.toString()
    }

    if (!comment) {
      this.setState({ showCommentError: true })
      if (this.props.editing) {
        this.props.setCommentError(this.props.parentIndex, this.props.index, translated.addComment)
      } else {
        this.props.setCommentError(translated.addComment)
      }
      this.setState({
        submitting: false
      })
      return
    }
    this.props.onCommentSubmit(data, this.props.parentIndex).then(() => {
      this.clearForm()
      if (this.props.useTermsOfUse && !this.state.agreedTermsOfUse && this.state.checkedTermsOfUse) {
        this.setState({ agreedTermsOfUse: true })
      }
      this.setState({
        submitting: false
      })
      return null
    }).catch(error => {
      console.warn(error)
      this.setState({
        submitting: false
      })
    })
  }

  hasAgreedToTerms () {
    if (!this.props.useTermsOfUse) {
      return true
    }
    if (this.state.agreedTermsOfUse) {
      return true
    }
    return this.state.checkedTermsOfUse
  }

  render () {
    const textareaStyle = { height: (this.state.textareaHeight) + 'px' }
    const hasParent = this.props.parentIndex !== undefined

    let userImage
    if (this.props.userImage) {
      const sectionStyle = {
        backgroundImage: 'url(' + this.props.userImage + ')'
      }
      userImage = (
        <div className="a4-comments__comment-form__avatar">
          <div className="user-avatar user-avatar--small user-avatar--shadow userindicator__btn-img" style={sectionStyle} />
        </div>
      )
    }

    const placeholder = this.props.editing
      ? undefined
      : (hasParent ? translated.replyPlaceholder : translated.placeholder)

    const submitLabel = hasParent ? translated.reply : translated.post

    const actionButton = (
      <button
        type="submit"
        className="btn btn--transparent-bordered a4-comments__submit-input"
        disabled={!this.hasAgreedToTerms() || this.state.submitting}
      >
        {submitLabel}
      </button>
    )
    const cancelButton = this.props.showCancel && (
      <button
        type="button"
        className="btn btn--none a4-comments__cancel-edit-input"
        value={translated.cancel}
        onClick={this.props.handleCancel}
      >
        {translated.cancel}
      </button>
    )

    if (this.props.hasCommentingPermission) {
      return (
        <>
          <form id={'id-comment-form' + this.props.commentId} className="a4-comments__comment-form__form" onSubmit={this.handleSubmit.bind(this)}>
            {this.props.error &&
              <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
            {this.props.commentCategoryChoices && !hasParent &&
              <div>
                <CategoryList
                  idPrefix={this.props.commentId ? this.props.commentId : 'new'}
                  categoriesChecked={this.state.selectedCategories}
                  categoryChoices={this.props.commentCategoryChoices}
                  handleControlFunc={this.handleCategorySelection.bind(this)}
                />
              </div>}
            <div className="a4-comments__comment-form__input">
              {userImage}
              <div className="form-group a4-comments__comment-form__textarea-container" id={'group_id_textarea-top' + this.props.commentId}>
                <label className="a4-sr-only" htmlFor={'id_textarea-top' + this.props.commentId}>
                  {hasParent ? translated.yourReply : translated.yourComment}
                </label>
                <textarea
                  id={'id_textarea-top' + this.props.commentId}
                  name={'id_textarea-top' + this.props.commentId}
                  ref={this.textareaRef}
                  aria-describedby={this.state.showCommentError ? 'alert' : ('id_char-count' + this.props.commentId)}
                  aria-invalid={this.state.showCommentError}
                  className={'form-control ' + this.props.commentCategoryChoices ? 'a4-comments__textarea--small' : 'a4-comments__textarea--big'}
                  onChange={this.handleTextChange.bind(this)}
                  value={this.state.comment}
                  onInput={this.handleTextareaGrow.bind(this)}
                  style={textareaStyle}
                  maxLength="4000"
                  placeholder={placeholder}
                />
                <p
                  id={'id_char-count' + this.props.commentId}
                  className="a4-comments__char-count"
                  aria-live="polite"
                >
                  <span aria-hidden="true">{this.state.commentCharCount}/4000<span className="a4-comments__char-count-word">{translated.characters}</span></span>
                  <span className="a4-sr-only">{this.state.commentCharCount}/4000{translated.characters}</span>
                </p>
              </div>
            </div>
            <div className="row a4-comments__comment-form__terms-and-buttons">
              <div className="a4-comments__comment-form__terms-of-use">
                {this.props.useTermsOfUse && !this.state.agreedTermsOfUse &&
                  <div className="form-group" id={'group_terms-of-use-checkbox' + (typeof this.props.parentIndex === 'number' ? this.props.parentIndex : 'rootForm')}>
                    <TermsOfUseCheckbox
                      id={'terms-of-use-checkbox-' + (typeof this.props.parentIndex === 'number' ? this.props.parentIndex : 'rootForm')}
                      onChange={val => this.setState({ checkedTermsOfUse: val })}
                      orgTermsUrl={this.props.orgTermsUrl}
                    />
                  </div>}
              </div>
              <div className="a4-comments__comment-form__actions">
                <div className="a4-comments__comment-form__actions__left">
                  {cancelButton}
                </div>
                <div className="a4-comments__comment-form__actions__right">
                  {actionButton}
                </div>
              </div>
            </div>
          </form>
        </>
      )
    } else if (this.props.wouldHaveCommentingPermission) {
      return (
        <div className="a4-comments__login">
          <a href={config.getLoginUrl()}>{translated.pleaseComment}</a>
        </div>
      )
    } else if (!this.props.projectIsPublic && this.state.agreedTermsOfUse) {
      return (
        <div className="a4-comments__alert">
          {translated.onlyInvited}
        </div>
      )
    } else {
      return (
        <div className="a4-comments__alert">
          {translated.notAllowedComment}
        </div>
      )
    }
  }
}
