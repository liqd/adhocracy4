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
      <div className="item-detail-2__content">
        <div>
          <p>{this.props.children}</p>
        </div>
        <div>
          <div>
            <div className="u-align-right">
              <span className="u-muted">{this.state.likes} </span>
              <i className="far fa-thumbs-up" aria-hidden="true" />
              <span className="visually-hidden">{likesTag}</span>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
