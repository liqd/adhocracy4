/* global django */
const React = require('react')

class Toggles extends React.Component {
  clickStatusButton () {
    this.props.changeStatusSelection(-1)
  }

  clickParticipationButton () {
    this.props.changeParticipationSelection(-1)
  }

  render () {
    if (this.props.isSlider) {
      return (
        <div>
          <div className="l-wrapper">
            { this.props.statusSelected &&
              <button
                className="btn btn--transparent btn--small"
                onClick={this.clickStatusButton.bind(this)}
                type="button">{this.props.statusString} <i className="fa fa-times" /></button>
            }
            { this.props.participationSelected &&
              <button
                className="btn btn--transparent btn--small"
                onClick={this.clickParticipationButton.bind(this)}
                type="button">{this.props.participationString} <i className="fa fa-times" /></button>
            }
            <div className="switch">
              <div className="switch-group" role="group" aria-labelledby="id-switch-label">
                <label htmlFor="switch-primary" className="switch-label">
                  <span className="switch-label__text">{django.gettext('Show map')}</span>
                  <input className="switch-input"
                    id="switch-primary"
                    onChange={this.props.toggleSwitch}
                    name="switch-primary"
                    type="checkbox" />
                  <span className="switch__toggle" />
                </label>
              </div>
            </div>
          </div>
        </div>
      )
    } else {
      return (
        <div>
          <div className="u-spacer-left u-spacer-right">
            <div className="btn-group switch-btn-group" role="group">
              <label className={!this.props.displayMap ? 'btn btn--light switch--btn active' : 'btn btn--light switch--btn'} onClick={this.props.showList} htmlFor="show_list">
                <span className="sr-only">{django.gettext('Show List')}</span>
                <input className="radio__input" type="radio" value="list" id="show_list" /> <i className="fa fa-list" />
              </label>
              <label className={this.props.displayMap ? 'btn btn--light switch--btn active' : 'btn btn--light switch--btn'} onClick={this.props.showMap} htmlFor="show_map">
                <span className="sr-only">{django.gettext('Show Map')}</span>
                <input className="radio__input" type="radio" value="map" id="show_map" /> <i className="fa fa-map" />
              </label>
            </div>
          </div>
        </div>
      )
    }
  }
}

module.exports = Toggles
