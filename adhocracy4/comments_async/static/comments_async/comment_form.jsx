import React from 'react'
import django from 'django'

import CategoryList from './category_list'

import * as config from '../../../static/config'
import Alert from '../../../static/Alert'

const translated = {
  yourComment: django.gettext('Your comment'),
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
      textareaHeight: 46
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
      textareaHeight: 46
    })
  }

  handleSubmit (e) {
    e.preventDefault()
    const comment = this.state.comment.trim()
    const data = {
      comment: comment,
      urlReplaces: {
        objectPk: this.props.subjectId,
        contentTypeId: this.props.subjectType
      }
    }
    if (this.props.commentCategoryChoices) {
      data.comment_categories = this.state.selectedCategories.toString()
    }

    if (!comment) {
      return
    }
    this.props.onCommentSubmit(data, this.props.parentIndex).then(() => {
      this.clearForm()
    }
    )
  }

  render () {
    const textareaStyle = { height: (this.state.textareaHeight) + 'px' }
    const hasParent = this.props.parentIndex !== undefined

    if (this.props.hasCommentingPermission) {
      return (
        <div>
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
            <textarea
              id="textarea-top"
              className={this.props.commentCategoryChoices ? 'a4-comments__textarea--small form-group' : 'a4-comments__textarea--big form-group'}
              placeholder={hasParent ? translated.yourReply : translated.yourComment}
              onChange={this.handleTextChange.bind(this)}
              required="required"
              value={this.state.comment}
              onInput={this.handleTextareaGrow.bind(this)}
              style={textareaStyle}
            />
            <div className="row">
              <label htmlFor="id-comment-form" className="col-6 a4-comments__char-count">{this.state.commentCharCount}/4000{translated.characters}</label>
              <div className="a4-comments__submit d-flex col-6">
                {this.props.commentCategoryChoices
                  ? <button type="submit" value={translated.post} className="btn a4-comments__submit-input ms-auto">{translated.post}</button>
                  : <button type="submit" value={translated.comment} className="btn a4-comments__submit-input ms-auto">{translated.post}</button>}
              </div>
            </div>
          </form>
        </div>
      )
    } else if (this.props.wouldHaveCommentingPermission) {
      return (
        <div className="a4-comments__login">
          <a href={config.getLoginUrl()}>{translated.pleaseComment}</a>
        </div>
      )
    } else if (!this.props.isContextMember) {
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
