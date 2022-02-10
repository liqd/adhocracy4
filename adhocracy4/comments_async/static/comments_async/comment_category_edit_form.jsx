import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import Alert from '../../../static/Alert'
import CategoryList from './category_list'

const translated = {
  writeContrib: django.gettext('Write contribution'),
  saveChanges: django.gettext('save changes'),
  cancel: django.gettext('cancel')
}

export default class CommentCategoryEditForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      comment: this.props.comment,
      selectedCategories: Object.keys(this.props.comment_categories)
    }
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

  displayCategories () {
    return this.props.content_type !== this.context.comments_contenttype
  }

  handleTextChange (e) {
    this.setState({ comment: e.target.value })
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
    this.props.onCommentSubmit(data)
  }

  render () {
    return (
      <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
        {this.props.error &&
          <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
        <CategoryList
          idPrefix={this.props.comment.id}
          categoriesChecked={this.state.selectedCategories}
          categoryChoices={this.props.commentCategoryChoices}
          handleControlFunc={this.handleCategorySelection.bind(this)}
        />
        <div className="form-group">
          <textarea
            rows={this.props.rows} className="a4-comments__textarea form-group"
            placeholder={translated.writeContrib}
            onChange={this.handleTextChange.bind(this)} required="required" defaultValue={this.state.comment}
          />
        </div>
        <input type="submit" value={translated.saveChanges} className="submit-button" />
        &nbsp;
        <input
          type="submit" value={translated.cancel} className="cancel-button"
          onClick={this.props.handleCancel}
        />
      </form>
    )
  }
}

CommentCategoryEditForm.contextTypes = {
  isAuthenticated: PropTypes.bool
}
