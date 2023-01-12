import React from 'react'
import django from 'django'

export default class QuestionPresent extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      likes: this.props.likes.count
    }
  }

  componentDidUpdate (prevProps) {
    if (this.props.likes !== prevProps.likes) {
      this.setState({
        likes: this.props.likes.count
      })
    }
  }

  handleErrors (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response
  }

  render () {
    const likesTag = django.gettext('likes')
    return (
      <div className="u-top-divider">
        <div className="u-space-between">
          <p>{this.props.children}</p>
          <span
            className="rating-button rating-up is-read-only u-no-padding"
            title={likesTag}
            aria-label={likesTag}
          >
            <i className="far fa-thumbs-up" aria-hidden="true" />
            {this.state.likes}
          </span>
        </div>
      </div>
    )
  }
}
