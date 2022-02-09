import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import { alert as Alert } from 'adhocracy4'

const translated = {
  writeContrib: django.gettext('Write contribution'),
  saveChanges: django.gettext('save changes'),
  cancel: django.gettext('cancel')
}

export default class CommentEditForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      comment: this.props.comment
    }
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

CommentEditForm.contextTypes = {
  isAuthenticated: PropTypes.bool
}
