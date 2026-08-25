import React from 'react'
import config from '../../../static/config'
import Alert from '../../../static/Alert'
import django from 'django'

interface CommentFormProps {
  id?: string
  onCommentSubmit: (comment: any, parentIndex?: number) => any
  placeholder: string
  rows: number
  isReadOnly: boolean
  error?: any
  errorMessage?: string
  handleErrorClick: () => void
  isContextMember?: boolean
  grabFocus?: boolean
  parentIndex?: number
  subjectId?: number
  subjectType?: number
}

interface CommentFormState {
  comment: string
}

interface CommentFormContext {
  isAuthenticated: boolean
  isModerator: boolean
  comments_contenttype: number
  user_name: string
}

class CommentForm extends React.Component<CommentFormProps, CommentFormState> {
  static contextType = React.createContext<CommentFormContext>({} as CommentFormContext)

  declare context: CommentFormContext

  constructor (props: CommentFormProps) {
    super(props)

    this.state = { comment: '' }
  }

  handleTextChange (e: React.ChangeEvent<HTMLTextAreaElement>) {
    this.setState({ comment: e.target.value })
  }

  handleSubmit (e: React.FormEvent) {
    e.preventDefault()
    const comment = this.state.comment.trim()
    if (!comment) {
      return
    }
    this.props.onCommentSubmit({
      comment,
      urlReplaces: {
        objectPk: this.props.subjectId,
        contentTypeId: this.props.subjectType
      }
    }, this.props.parentIndex)
      .then(() => {
        this.setState({ comment: '' })
        return null
      })
      .catch((error: Error) => console.warn(error))
  }

  render () {
    const postTag = django.gettext('post')
    const loginCommentText = django.gettext('Please login to comment')
    const noCommentText = django.gettext('The currently active phase doesn\'t allow to comment.')
    const noCommentTextSemiPub = django.gettext('Only invited users can actively participate.')

    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <form id={this.props.id} className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          {this.props.error &&
            <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
          <div className="form-group">
            <textarea
              autoFocus={this.props.grabFocus} // eslint-disable-line jsx-a11y/no-autofocus
              rows={this.props.rows}
              className="form-control"
              placeholder={this.props.placeholder}
              onChange={this.handleTextChange.bind(this)} required value={this.state.comment}
            />
          </div>
          <input type="submit" value={postTag} className="submit-button" />
        </form>
      )
    } else if (!this.props.isReadOnly) {
      return (
        <div className="comments_login">
          <a href={config.getLoginUrl()}>{loginCommentText}</a>
        </div>
      )
    } else if (!this.props.isContextMember) {
      return (
        <div>
          {noCommentTextSemiPub}
        </div>
      )
    } else {
      return (
        <div>
          {noCommentText}
        </div>
      )
    }
  }
}

export default CommentForm
