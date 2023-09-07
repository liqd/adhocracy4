import React from 'react'
import django from 'django'

import CategoryList from './category_list'
import { TermsOfUseCheckbox } from '../../../static/TermsOfUseCheckbox'

import * as config from '../../../static/config'
import Alert from '../../../static/Alert'

const translated = {
  yourComment: django.gettext('Your comment'),
  addComment: django.gettext('Please add a comment.'),
  yourReply: django.gettext('Your reply'),
  characters: django.gettext(' characters'),
  post: django.gettext('post'),
  comment: django.gettext('Comment'),
  pleaseComment: django.gettext('Please login to comment'),
  onlyInvited: django.gettext('Only invited users can actively participate.'),
  notAllowedComment: django.gettext('The currently active phase doesn\'t allow to comment.')
}

export default class CommentForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      comment: '',
      commentCharCount: 0,
      selectedCategories: [],
      textareaHeight: 46,
      agreedTermsOfUse: props.agreedTermsOfUse,
      showCommentError: false
    }
  }

  componentDidUpdate (prevProps) {
    if (this.props.agreedTermsOfUse !== prevProps.agreedTermsOfUse) {
      this.setState({
        agreedTermsOfUse: this.props.agreedTermsOfUse
      })
    }
  }

  handleTextareaGrow (e) {
    const newHeight = (e.target.scrollHeight)
    if (newHeight !== this.state.textareaHeight) {
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
      textareaHeight: 46,
      showCommentError: false
    })
  }

  handleSubmit (e) {
    e.preventDefault()
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
      this.props.setCommentError(translated.addComment)
      return
    }
    this.props.onCommentSubmit(data, this.props.parentIndex).then(() => {
      this.clearForm()
      if (this.props.useTermsOfUse && !this.state.agreedTermsOfUse && this.state.checkedTermsOfUse) {
        this.setState({ agreedTermsOfUse: true })
      }
      return null
    }).catch(error => console.warn(error))
  }

  render () {
    const textareaStyle = { height: (this.state.textareaHeight) + 'px' }
    const hasParent = this.props.parentIndex !== undefined
    const actionButton = (
      <button
        type="submit"
        className="btn a4-comments__submit-input ms-auto"
        disabled={this.props.useTermsOfUse && !this.state.agreedTermsOfUse && !this.state.checkedTermsOfUse}
      >
        {translated.post}
      </button>
    )

    if (this.props.hasCommentingPermission) {
      return (
        <form id="id-comment-form" className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          {this.props.error &&
            <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
          {this.props.commentCategoryChoices &&
            <CategoryList
              idPrefix="new"
              categoriesChecked={this.state.selectedCategories}
              categoryChoices={this.props.commentCategoryChoices}
              handleControlFunc={this.handleCategorySelection.bind(this)}
            />}
          <label className="sr-only" htmlFor="id_textarea-top">
            {translated.yourComment}
          </label>
          <textarea
            id="id_textarea-top"
            aria-describedby={this.state.showCommentError ? 'alert' : 'id_char-count'}
            aria-invalid={this.state.showCommentError}
            className={this.props.commentCategoryChoices ? 'a4-comments__textarea--small form-group' : 'a4-comments__textarea--big form-group'}
            placeholder={hasParent ? translated.yourReply : translated.yourComment}
            onChange={this.handleTextChange.bind(this)}
            value={this.state.comment}
            onInput={this.handleTextareaGrow.bind(this)}
            style={textareaStyle}
          />
          <div className="row">
            <div className="col-12 col-sm-9 col-lg-10">
              <p
                id="id_char-count"
                className="a4-comments__char-count"
                aria-live="polite"
              >
                {this.state.commentCharCount}/4000{translated.characters}
              </p>
              {this.props.useTermsOfUse && !this.state.agreedTermsOfUse &&
                <TermsOfUseCheckbox
                  id={'terms-of-use-checkbox-' + (typeof this.props.parentIndex === 'number' ? this.props.parentIndex : 'rootForm')}
                  onChange={val => this.setState({ checkedTermsOfUse: val })}
                  orgTermsUrl={this.props.orgTermsUrl}
                />}
            </div>
            <div className="d-flex col-12 col-sm-3 col-lg-2 align-items-center">
              {actionButton}
            </div>
          </div>
        </form>
      )
    } else if (this.props.wouldHaveCommentingPermission) {
      return (
        <div className="a4-comments__login">
          <a href={config.getLoginUrl()}>{translated.pleaseComment}</a>
        </div>
      )
    } else if (!this.props.projectIsPublic) {
      return (
        <div>
          {translated.onlyInvited}
        </div>
      )
    } else {
      return (
        <div>
          {translated.notAllowedComment}
        </div>
      )
    }
  }
}
