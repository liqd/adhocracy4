import React from 'react'
import django from 'django'

export default class QuestionModerator extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      is_on_shortlist: this.props.is_on_shortlist,
      is_live: this.props.is_live,
      likes: this.props.likes.count,
      session_like: this.props.likes.session_like,
      is_hidden: this.props.is_hidden,
      is_answered: this.props.is_answered
    }
  }

  toggleIsOnShortList () {
    const value = !this.state.is_on_shortlist
    const boolValue = (value) ? 1 : 0
    const data = { is_on_shortlist: boolValue }
    this.props.updateQuestion(data, this.props.id)
      .then((response) => response.json())
      .then(responseData => this.setState(
        {
          is_on_shortlist: responseData.is_on_shortlist
        }
      ))
      .then(() => this.props.togglePollingPaused())
  }

  toggleIslive () {
    const value = !this.state.is_live
    const boolValue = (value) ? 1 : 0
    const data = { is_live: boolValue }
    this.props.updateQuestion(data, this.props.id)
      .then((response) => response.json())
      .then(responseData => this.setState(
        {
          is_live: responseData.is_live
        }
      ))
      .then(() => this.props.togglePollingPaused())
  }

  toggleIsAnswered () {
    const value = !this.state.is_answered
    const boolValue = (value) ? 1 : 0
    const data = { is_answered: boolValue }
    this.props.removeFromList(this.props.id, data)
  }

  toggleIshidden () {
    const value = !this.state.is_hidden
    const boolValue = (value) ? 1 : 0
    const data = { is_hidden: boolValue }
    this.props.updateQuestion(data, this.props.id)
      .then((response) => response.json())
      .then(responseData => this.setState(
        {
          is_hidden: responseData.is_hidden
        }
      ))
      .then(() => this.props.togglePollingPaused())
  }

  componentDidUpdate (prevProps) {
    if (this.props.is_on_shortlist !== prevProps.is_on_shortlist) {
      this.setState({
        is_on_shortlist: this.props.is_on_shortlist
      })
    }
    if (this.props.is_live !== prevProps.is_live) {
      this.setState({
        is_live: this.props.is_live
      })
    }
    if (this.props.is_hidden !== prevProps.is_hidden) {
      this.setState({
        is_hidden: this.props.is_hidden
      })
    }
    if (this.props.is_answered !== prevProps.is_answered) {
      this.setState({
        is_answered: this.props.is_answered
      })
    }
    if (this.props.likes !== prevProps.likes) {
      this.setState({
        likes: this.props.likes.count,
        session_like: this.props.likes.session_like
      })
    }
  }

  render () {
    const hiddenText = django.gettext('mark as hidden')
    const undoHiddenText = django.gettext('undo mark as hidden')
    const doneText = django.gettext('mark as done')
    const addLiveText = django.gettext('added to live list')
    const removeLiveText = django.gettext('remove from live list')
    const addShortlistText = django.gettext('added to shortlist')
    const removeShortlistText = django.gettext('remove from shortlist')
    const supportStr = django.gettext('Support count')

    return (
      <div className="list-item">
        <div>
          <p className={this.props.is_hidden ? 'u-muted u-text-decoration-line-through live_questions__question' : 'live_questions__question'}>{this.props.children}</p>
        </div>
        {this.props.category &&
          <div>
            <span className="label label--big">{this.props.category}</span>
          </div>}
        <div className="live-question__action-bar">
          <div className="live_questions__like">
            <span
              className="rating-button rating-up is-read-only"
              title={supportStr}
            >
              <i className="far fa-thumbs-up" aria-hidden="true" />
              {this.state.likes}
              <span className="visually-hidden">{supportStr}</span>
            </span>
          </div>
          <div>
            {this.props.displayIsOnShortlist &&
              <button
                type="button"
                className="btn btn--light u-spacer-right"
                onClick={this.toggleIsOnShortList.bind(this)}
                aria-label={this.state.is_on_shortlist ? addShortlistText : removeShortlistText}
                title={this.state.is_on_shortlist ? addShortlistText : removeShortlistText}
              >
                <i className={this.state.is_on_shortlist ? 'far fa-list-alt u-primary' : 'far fa-list-alt u-muted'} aria-hidden="true" />
              </button>}
            {this.props.displayIsLive &&
              <button
                type="button"
                className="btn btn--light u-spacer-right"
                onClick={this.toggleIslive.bind(this)}
                aria-label={this.state.is_live ? addLiveText : removeLiveText}
                title={this.state.is_live ? addLiveText : removeLiveText}
              >
                <span className="fa-stack fa-1x">
                  <i className={this.state.is_live ? 'fas fa-tv fa-stack-2x u-primary' : 'fas fa-tv fa-stack-2x u-muted'} aria-hidden="true" />
                  <i className={this.state.is_live ? 'fas fa-check fa-stack-1x fa-inverse u-primary' : 'fas fa-check fa-stack-1x u-muted'} aria-hidden="true" />
                </span>
              </button>}
            {this.props.displayIsAnswered &&
              <button
                type="button" className="btn btn--light u-spacer-right"
                onClick={this.toggleIsAnswered.bind(this)}
                aria-label={doneText}
                title={doneText}
              >
                <i className={this.props.is_answered ? 'far fa-check-circle u-primary' : 'far fa-check-circle u-muted'} aria-hidden="true" />
              </button>}
            {this.props.displayIsHidden &&
              <button
                type="button"
                className="btn btn--light"
                onClick={this.toggleIshidden.bind(this)}
                aria-label={this.props.is_hidden ? hiddenText : undoHiddenText}
                title={this.props.is_hidden ? hiddenText : undoHiddenText}
              >
                <i className={this.props.is_hidden ? 'far fa-eye-slash u-muted' : 'far fa-eye u-primary'} aria-hidden="true" />
              </button>}
          </div>
        </div>
      </div>
    )
  }
}
