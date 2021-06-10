import React from 'react'
import django from 'django'

export default class QuestionUser extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      is_on_shortlist: this.props.is_on_shortlist,
      is_live: this.props.is_live,
      likes: this.props.likes.count,
      session_like: this.props.likes.session_like
    }
  }

  componentDidUpdate (prevProps) {
    if (this.props.is_on_shortlist !== prevProps.is_on_shortlist) {
      this.setState({
        is_on_shortlist: this.props.is_on_shortlist
      })
    }
    if (this.props.likes !== prevProps.likes) {
      this.setState({
        likes: this.props.likes.count,
        session_like: this.props.likes.session_like
      })
    }
  }

  handleErrors (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response
  }

  handleLike () {
    const value = !this.state.session_like
    this.props.handleLike(this.props.id, value)
      .then(this.handleErrors)
      .then((response) => this.setState(
        {
          session_like: value,
          likes: value ? this.state.likes + 1 : this.state.likes - 1
        }
      ))
      .catch((response) => { console.log(response.message) })
  }

  render () {
    const shortlistText = django.gettext('on shortlist')
    const likesTag = django.gettext('likes')
    const addLikeTag = django.gettext('add like')
    const undoLikeTag = django.gettext('undo like')

    return (
      <div className="list-item">
        <div>
          {this.props.is_on_shortlist &&
            <i className="far fa-list-alt u-primary" aria-label={shortlistText} />}
          <p className="live_questions__question">
            {this.props.children}
          </p>
        </div>
        {this.props.category &&
          <div>
            <span className="label label--big u-spacer-bottom-half">{this.props.category}</span>
          </div>}
        <div className="live-question__action-bar">
          {this.props.hasLikingPermission
            ? (
              <button type="button" className={this.state.session_like ? 'btn btn--none btn--align-left u-success' : 'btn btn--none btn--align-left'} onClick={this.handleLike.bind(this)}>
                <span>{this.state.likes} </span>
                <span className="visually-hidden">{likesTag}</span>
                <i className="far fa-thumbs-up" aria-label={this.state.session_like ? addLikeTag : undoLikeTag} />
              </button>
              )
            : (
              <div>
                <span className="u-muted">{this.state.likes} </span>
                <span className="visually-hidden">{likesTag}</span>
                <i className="far fa-thumbs-up u-muted" aria-hidden="true" />
              </div>
              )}
        </div>
      </div>
    )
  }
}
