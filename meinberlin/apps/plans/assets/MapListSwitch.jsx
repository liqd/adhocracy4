/* global django */
const React = require('react')

class MapListSwitch extends React.Component {
  render () {
    return (
      <div>
        <div className="u-spacer-left u-spacer-right">
          <div className="switch-group" role="group" aria-label={django.gettext('Filter bar')}>
            <div className="switch-label u-sm-down-display-none">{django.gettext('Show map')}</div>
            <div className="switch u-sm-down-display-none">
              <input
                id="switch-primary"
                onChange={this.props.toggleSwitch}
                name="switch-primary"
                type="checkbox" />
              <label htmlFor="switch-primary" className="primary-color" />
            </div>
            <div className="btn-group u-lg-up-display-none">
              <button className="btn btn--light" onClick={this.props.hideMap}><i className="fa fa-list" /></button>
              <button className="btn btn--light" onClick={this.props.hideList}><i className="fa fa-map" /></button>
            </div>
          </div>
        </div>
      </div>

    )
  }
}

module.exports = MapListSwitch
