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
      <div className="list-group-item border-top-0 border-right-0 border-bottom border-left-0 mb-2">
        <div>
          <p>{this.props.children}</p>
        </div>
        <div className="row">
          <div className="col-12">
            <div>
              <div className="float-right">
                <span className="text-muted">{this.state.likes}</span>
                <i className="icon-like text-muted ml-2" aria-hidden="true" />
                <span className="sr-only">{likesTag}</span>
              </div>
            </div>
          </div>
        </div>
      </div>)
  }
}
