import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import CategoryList from './category_list'

import * as config from '../../../static/config'
import Alert from '../../../static/Alert'

export default class CommentForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      comment: '',
      selectedCategories: []
    }
  }

  textareaHeight () {
    var e = document.getElementById('textarea-top')
    e.style.height = '50px'
  }

  handleTextareaGrow (e) {
    e.target.style.height = '50px'
    e.target.style.height = (e.target.scrollHeight) + 'px'
  }

  handleTextChange (e) {
    this.setState({ comment: e.target.value })
  }

  handleCategorySelection (e) {
    const newSelection = e.target.id.split('_')[1]
    var newSelectionArray = this.state.selectedCategories
    var index = this.state.selectedCategories.indexOf(newSelection)
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
      selectedCategories: []
    })
  }

  handleSubmit (e) {
    e.preventDefault()
    var comment = this.state.comment.trim()
    var data = {
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

  componentDidMount () {
    this.textareaHeight()
  }

  render () {
    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <div>
          <label htmlFor="id-comment-form" className="pt-3 pb-2"> {django.gettext('The maximal length of your contribution is 4000 characters')}</label>
          <form id="id-comment-form" className="general-form" onSubmit={this.handleSubmit.bind(this)}>
            {this.props.error &&
              <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
            <div className="">
              {this.props.commentCategoryChoices &&
                <CategoryList
                  idPrefix="new"
                  categoriesChecked={this.state.selectedCategories}
                  categoryChoices={this.props.commentCategoryChoices}
                  handleControlFunc={this.handleCategorySelection.bind(this)}
                />}
              <textarea
                id="textarea-top"
                className="a4-comments__textarea form-group"
                placeholder={django.gettext('Write contribution')}
                onChange={this.handleTextChange.bind(this)} required="required" value={this.state.comment}
                onInput={this.handleTextareaGrow}
                rows="1"
                autoFocus
              />
            </div>
            <div className="a4-comments__submit d-flex ">
              <button type="submit" value={django.gettext('post')} onClick={this.textareaHeight.bind(this)} className="btn a4-comments__submit-input ml-auto">{django.gettext('post')}</button>
            </div>
          </form>
        </div>
      )
    } else if (!this.props.isReadOnly) {
      return (
        <div className="a4-comments__login">
          <a href={config.getLoginUrl()}>{django.gettext('Please login to comment')}</a>
        </div>
      )
    } else {
      return (
        <div>
          {django.gettext('The currently active phase doesn\'t allow to comment.')}
        </div>
      )
    }
  }
}

CommentForm.contextTypes = {
  isAuthenticated: PropTypes.bool,
  comments_contenttype: PropTypes.number
}
