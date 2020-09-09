import React from 'react'
import django from 'django'

const textDisplayQuestion = django.gettext('display question on screen')
const textAddQuestion = django.gettext('add question to shortlist')
const textHideQuestion = django.gettext('hide question from audience')
const textMarkAnswered = django.gettext('mark question as answered')
const textMarkedModeration = django.gettext('is shown in front of a question? It has been marked by the moderation.')
const ariaCloseInfo = django.gettext('Close information')
const ariaOpenInfo = django.gettext('Open information')

export default class InfoBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      displayInfo: false
    }
  }

  toggleInformation () {
    const displayInfo = !this.state.displayInfo
    this.setState({
      displayInfo: displayInfo
    })
  }

  render () {
    return (
      <div>
        {this.state.displayInfo
          ? (
            <div className="">
              {this.props.isModerator &&
                <div className="alert-dismissible">
                  <button type="button" className="close" onClick={this.toggleInformation.bind(this)}>
                    <span aria-label={ariaCloseInfo}>&times;</span>
                  </button>
                  <div className="infobox u-inline-flex">
                    <div className="infobox__box">
                      <i className="far fa-thumbs-up" />
                      <div>{textAddQuestion}</div>
                    </div>
                    <div className="infobox__box">
                      <span className="fa-stack fa-1x"><i className="fas fa-tv fa-stack-2x" /><i className="fas fa-arrow-up fa-stack-1x" /></span> <div>{textDisplayQuestion}</div>
                    </div>
                    <div className="infobox__box">
                      <i className="far fa-thumbs-up" />
                      <div>{textMarkAnswered}</div>
                    </div>
                    <div className="infobox__box">
                      <i className="far fa-eye" />
                      <div>{textHideQuestion}</div>
                    </div>
                  </div>
                </div>}
              {!this.props.isModerator &&
                <div className="infobox__box">
                  <div className="">
                    <i className="far fa-thumbs-up" /> {textMarkedModeration}
                  </div>
                </div>}
            </div>
          )
          : (
            <div className="">
              <div className="u-align-right">
                <button type="button" className="btn btn--none" onClick={this.toggleInformation.bind(this)}>
                  <span aria-label={ariaOpenInfo}><i className="fas fa-info-circle" /></span>
                </button>
              </div>
            </div>
          )}
      </div>
    )
  }
}
