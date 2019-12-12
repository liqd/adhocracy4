import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import { alert as Alert, config } from 'adhocracy4'

import CategoryList from './category_list'

export default class CommentForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      comment: '',
      selectedCategories: []
    }
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

  render () {
    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <div>
          <label htmlFor="id-comment-form" className="mt-3 mb-2"> {django.gettext('The maximal length of your contribution is 4000 characters')}</label>
          <form id="id-comment-form" className="general-form" onSubmit={this.handleSubmit.bind(this)}>
            {this.props.error &&
              <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
            <div className="form-group">
              {this.props.commentCategoryChoices &&
                <CategoryList
                  idPrefix="new"
                  categoriesChecked={this.state.selectedCategories}
                  categoryChoices={this.props.commentCategoryChoices}
                  handleControlFunc={this.handleCategorySelection.bind(this)}
                />}
              <textarea
                rows={this.props.rows}
                className="form-control"
                placeholder={django.gettext('Write contribution')}
                onChange={this.handleTextChange.bind(this)} required="required" value={this.state.comment}
              />
            </div>
            <div className="a4-comments__submit">
              <input type="submit" value={django.gettext('post')} className="a4-comments__submit-input" />
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
