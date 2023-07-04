/* global django */
import { toLocaleDate } from '../../contrib/assets/helpers'
const React = require('react')
const $ = require('jquery')

const moreThanStr = django.gettext('More than 1 year remaining')
const remainingStr = django.gettext('remaining')
const futureParticipationStr = django.gettext('Participation: from ')
const endedParticipationStr = django.gettext('Participation ended. Read result.')
const superordProjectStr = django.gettext('Superordinate project: ')
const participationProjectsStr = django.gettext('Participation projects: ')
const participationStr = django.gettext('Participation: ')

class PopUp extends React.Component {
  escapeHtml (unsafe) {
    return $('<div>').text(unsafe).html()
  }

  getWidth () {
    return { width: this.props.item.active_phase[0] + '%' }
  }

  getTimespan () {
    const timeRemaining = this.props.item.active_phase[1].split(' ')
    const daysRemaining = parseInt(timeRemaining[0])
    if (daysRemaining > 365) {
      return (
        <span>{moreThanStr}</span>
      )
    } else {
      return (
        <span>{remainingStr} {this.props.item.active_phase[1]}</span>
      )
    }
  }

  getTranslation (item) {
    const date = this.props.item.future_phase
    const dateStyle = {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }
    return futureParticipationStr + toLocaleDate(date, undefined, dateStyle)
  }

  renderTopics () {
    if (this.props.itemTopics) {
      return (
        <div className="maplist-item__labels">
          {this.props.itemTopics.map(topic => <span key={topic} className="label label--secondary maplist-item__label">{topic}</span>)}
        </div>
      )
    }
  }

  render () {
    const statusClass = (this.props.item.participation_active === true) ? 'participation-tile__status-active' : 'participation-tile__status-inactive'
    if (this.props.item.type === 'project') {
      return (
        <div className="maps-popups-popup-text-content">
          {this.renderTopics()}
          <span className="maplist-popup-item__roofline">{this.props.item.district}</span>
          <div className="maps-popups-popup-name u-spacer-bottom-half">
            <a href={this.props.item.url} target={this.props.item.subtype === 'external' ? '_blank' : '_self'} rel="noreferrer">
              {this.props.item.title}
            </a>
          </div>
          {this.props.item.future_phase && !this.props.item.active_phase &&
            <div className="status__future">
              <span className="maplist-item-popup__status"><i className="fas fa-clock" />{this.getTranslation()}</span>
            </div>}
          {this.props.item.active_phase &&
            <div className="status__active">
              <div className="status-bar__active"><span className="status-bar__active-fill" style={this.getWidth(this.props.item)} /></div>
              <span className="maplist-item-popup__status"><i className="fas fa-clock" />{this.getTimespan()}</span>
            </div>}
          {this.props.item.past_phase && !this.props.item.active_phase && !this.props.item.future_phase &&
            <div className="maplist-item-popup__status status-bar__past">
              <span className="maplist-item-popup__status">{endedParticipationStr}</span>
            </div>}
          {this.props.item.plan_url &&
            <div className="maps-popups-popup-name maplist-item-popup__proj-plan">
              <span className="maplist-popup-item__roofline">{superordProjectStr}</span>
              <br />
              <a href={this.props.item.plan_url}>{this.props.item.plan_title}</a>
            </div>}
        </div>
      )
    } else {
      return (
        <div className="maps-popups-popup-text-content">
          {this.renderTopics()}
          <span className="maplist-popup-item__roofline">{this.props.item.district}</span>
          <div className="maps-popups-popup-name u-spacer-bottom-half">
            <a href={this.props.item.url}>{this.props.item.title}</a>
          </div>
          <div className="maplist-popup-item__stats">
            <span className="maplist-item-popup__proj-count">
              <i className="fas fa-th" />{participationProjectsStr}
            </span>
            <span>{this.props.item.published_projects_count}</span>
            <br />
            <span className="maplist-item-popup__status"><i className="fas fa-clock" />{participationStr}</span>
            <span className={statusClass}>{this.props.item.participation_string}</span>
          </div>
        </div>
      )
    }
  }
}

module.exports = PopUp
