/* global fetch */
import $ from 'jquery'
import React from 'react'
import QuestionPresent from './QuestionPresent'

export default class PresentBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      questions: []
    }
  }

  getListAndFooter (data) {
    this.setState({
      questions: data
    })
    this.displayFooterOrInfo()
  }

  getItems () {
    fetch(this.props.questions_api_url + '?is_live=1&is_answered=0')
      .then(response => response.json())
      .then(data => this.getListAndFooter(data))
  }

  componentDidMount () {
    this.getItems()
    this.timer = setInterval(() => this.getItems(), 5000)
  }

  componentWillUnmount () {
    this.timer = null
  }

  displayFooterOrInfo () {
    if (this.state.questions.length > 0) {
      $('#id-present-infographic').removeClass('d-none')
      $('#id-present-infographic').addClass('infographic__info-footer')
      $('#id-present-infographic').removeClass('infographic__info-screen')
    } else {
      $('#id-present-infographic').removeClass('d-none')
      $('#id-present-infographic').removeClass('infographic__info-footer')
      $('#id-present-infographic').addClass('infographic__info-screen')
    }
  }

  render () {
    if (this.state.questions.length > 0) {
      return (
        <div className="container">
          <div className="offset-lg-2 col-lg-8">
            <div className="item-detail-2__content live_question__presentation" />
            {this.state.questions.map((question, index) => {
              return (
                <QuestionPresent
                  key={question.id}
                  id={question.id}
                  likes={question.likes}
                >
                  {question.text}
                </QuestionPresent>
              )
            })}
          </div>
        </div>
      )
    } else {
      return (
        <div className="container">
          <div className="offset-lg-3 col-lg-6 live_question__presentation u-spacer-bottom-double">
            <h1 className="u-align-center">{this.props.title}</h1>
          </div>
        </div>
      )
    }
  }
}
