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

    return (
      <div className="list-item">
        <div>
          <p className={this.props.is_hidden ? 'text-muted u-text-decoration-line-through' : ''}>{this.props.children}</p>
        </div>
        {this.props.category &&
          <div>
            <span className="label label--big">{this.props.category}</span>
          </div>}
        <div className="live-question__action-bar">
          <div className="">
            <span><i className="far fa-eye-slash" />{this.state.likes}</span>
          </div>
          <div className="">
            {this.props.displayIsHidden &&
              <button
                type="button" className="btn btn--none"
                onClick={this.toggleIshidden.bind(this)}
              >
                <i className={this.props.is_hidden ? 'far fa-eye-slash text-muted' : 'far fa-eye u-text-tertiary'} aria-label={this.props.is_hidden ? hiddenText : undoHiddenText} />
              </button>}

            {this.props.displayIsAnswered &&
              <button
                type="button" className="btn btn--none"
                onClick={this.toggleIsAnswered.bind(this)}
              >
                <i
                  className={this.props.is_answered ? 'far fa-check-square' : 'far fa-check-square'}
                  aria-label={doneText}
                />
              </button>}
            {this.props.displayIsLive &&
              <button type="button" className="btn btn--none" onClick={this.toggleIslive.bind(this)}>
                <span className="fa-stack fa-1x">
                  <i className={this.state.is_live ? 'fas fa-tv fa-stack-2x text-muted' : 'fas fa-tv fa-stack-2x u-text-tertiary'} aria-label={this.state.is_live ? addLiveText : removeLiveText} />
                  <i className={this.state.is_live ? 'fas fa-arrow-up fa-stack-1x fa-inverse text-muted' : 'fas fa-arrow-up fa-stack-1x u-text-tertiary'} aria-hidden="true" />
                </span>
              </button>}
            {this.props.displayIsOnShortlist &&
              <button type="button" className="btn btn--none" onClick={this.toggleIsOnShortList.bind(this)}>
                <i className={this.state.is_on_shortlist ? 'fas fa-desktop text-muted' : 'fas fa-desktop u-text-tertiary'} aria-label={this.state.is_on_shortlist ? addShortlistText : removeShortlistText} />
              </button>}
          </div>
        </div>
      </div>)
  }
}
