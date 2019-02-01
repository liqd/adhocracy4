/* global django */
const React = require('react')
const $ = require('jquery')

class PopUp extends React.Component {
  escapeHtml (unsafe) {
    return $('<div>').text(unsafe).html()
  }

  getWidth () {
    return { width: this.props.item.active_phase[0] + '%' }
  }

  renderTopics () {
    if (this.props.itemTopics) {
      return (
        <div className="maplist-item__labels">
          {this.props.itemTopics.map(topic => <span key={topic} className="label label--secondary maplist-item__label u-spacer-bottom-half">{topic}</span>)}
        </div>
      )
    }
  }

  render () {
    let statusClass = (this.props.item.participation_active === true) ? 'maplist-item__status-active' : 'maplist-item__status-inactive'
    if (this.props.item.type === 'project') {
      return (
        <div className="maps-popups-popup-text-content">
          {this.renderTopics()}
          <span className="maplist-popup-item__roofline">{this.props.item.district}</span>
          <div className="maps-popups-popup-name u-spacer-bottom-half">
            <a href={this.props.item.url}>{this.props.item.title}</a>
          </div>
          {this.props.item.future_phase &&
          <div className="status__future">
            <span className="maplist-item-popup__status"><i className="fas fa-clock" />{django.gettext('Participation: from ') + this.props.item.future_phase + django.gettext(' possible')}</span>
          </div>
          }
          {this.props.item.active_phase &&
          <div className="status__active">
            <div className="status-bar__active"><span className="status-bar__active-fill" style={this.getWidth(this.props.item)} /></div>
            <span className="maplist-item-popup__status"><i className="fas fa-clock" />{django.gettext('remaining')} {this.props.item.active_phase[1]}</span>
          </div>
          }
          {this.props.item.past_phase &&
            <div className="maplist-item-popup__status status-bar__past">
              {django.gettext('Participation ended. Read result.')}
            </div>
          }
          {this.props.item.plan_url &&
            <div className="maps-popups-popup-name maplist-item-popup__proj-plan">
              <span className="maplist-popup-item__roofline">{django.gettext('Project for the following plan: ') }</span>
              <br />
              <a href={this.props.item.plan_url}>{this.props.item.plan_title}</a>
            </div>
          }
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
              <i className="fas fa-th" />{django.gettext('Participation projects: ') }</span>
            <span>{this.props.item.published_projects_count}</span>
            <br />
            <span className="maplist-item-popup__status"><i className="fas fa-clock" />{django.gettext('Participation: ')}</span>
            <span className={statusClass}>{this.props.item.participation_string}</span>
          </div>
        </div>
      )
    }
  }
}

module.exports = PopUp
