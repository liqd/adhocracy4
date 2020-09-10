import React from 'react'
import django from 'django'

const textDisplayQuestion = django.gettext('display question on screen')
const textAddQuestion = django.gettext('add question to shortlist')
const textHideQuestion = django.gettext('hide question from audience')
const textMarkAnswered = django.gettext('mark question as answered')
const textMarkedModeration = django.gettext('is shown in front of a question? It has been marked by the moderation.')
const ariaCloseInfo = django.gettext('Close information')
const ariaOpenInfo = django.gettext('Open information')
const btnHide = django.gettext('Hide')

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
            <div className="u-spacer-bottom">
              {this.props.isModerator &&
                <div className="alert-dismissible">
                  <div className="u-align-right">
                    <button type="button" className="u-muted" onClick={this.toggleInformation.bind(this)}>
                      <span aria-label={ariaCloseInfo}>{btnHide} <i className="fa fa-times" /></span>
                    </button>
                  </div>
                  <div className="infobox u-inline-flex">
                    <div className="infobox__box">
                      <i className="far fa-list-alt" />
                      <div>{textAddQuestion}</div>
                    </div>
                    <div className="infobox__box">
                      <i className="fas fa-tv" />
                      <div>{textDisplayQuestion}</div>
                    </div>
                    <div className="infobox__box">
                      <i className="far fa-check-square" />
                      <div>{textMarkAnswered}</div>
                    </div>
                    <div className="infobox__box infobox__box--last">
                      <i className="far fa-eye" />
                      <div>{textHideQuestion}</div>
                    </div>
                  </div>
                </div>}
              {!this.props.isModerator &&
                <div className="alert-dismissible">
                  <div className="u-align-right">
                    <button type="button" className="u-muted" onClick={this.toggleInformation.bind(this)}>
                      <span aria-label={ariaCloseInfo}>{btnHide} <i className="fa fa-times" /></span>
                    </button>
                  </div>
                  <div className="infobox__box infobox__box--last">
                    <i className="far fa-list-alt" />
                    <div>
                      {textMarkedModeration}
                    </div>
                  </div>
                </div>}
            </div>
          )
          : (
            <div>
              <div className="u-align-right">
                <button type="button" className="btn btn--none u-muted" onClick={this.toggleInformation.bind(this)}>
                  <span aria-label={ariaOpenInfo}><i className="fas fa-info-circle" /></span>
                </button>
              </div>
            </div>
          )}
      </div>
    )
  }
}
