/* global django */
const React = require('react')

class MapListSwitch extends React.Component {
  render () {
    if (this.props.isSlider) {
      return (
        <div>
          <div className="l-wrapper">
            <div className="switch-group" role="group" aria-labelledby="id-switch-label">
              <div id="id-switch-label" className="switch-label">{django.gettext('Show map')}</div>
              <div className="switch">
                <input
                  id="switch-primary"
                  onChange={this.props.toggleSwitch}
                  name="switch-primary"
                  type="checkbox" />
                <label htmlFor="switch-primary" className="primary-color" />
              </div>
            </div>
          </div>
        </div>
      )
    } else {
      return (
        <div>
          <div className="u-spacer-left u-spacer-right">
            <div className="switch-group" role="group" aria-label={django.gettext('Map list switch')}>
              <div className="radio-group">
                <label className={!this.props.displayMap ? 'btn btn--light switch--btn active' : 'btn btn--light switch--btn'} onClick={this.props.showList} htmlFor="show_list">
                  <input className="radio__input" type="radio" value="list" id="show_list" /> <i className="fa fa-list" />
                </label>
                <label className={this.props.displayMap ? 'btn btn--light switch--btn active' : 'btn btn--light switch--btn'} onClick={this.props.showMap} htmlFor="show_map">
                  <input className="radio__input" type="radio" value="map" id="show_map" /> <i className="fa fa-map" />
                </label>
              </div>
            </div>
          </div>
        </div>
      )
    }
  }
}

module.exports = MapListSwitch
