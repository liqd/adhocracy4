/* global django */
const React = require('react')

class MapListSwitch extends React.Component {
  render () {
    if (this.props.isSlider) {
      return (
        <div>
          <div className="l-wrapper">
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
            <div className="switch-group" role="group" aria-label={django.gettext('Map list switch')}>
              <div className="btn-group">
                <button className={!this.props.displayMap ? 'btn btn--light switch--btn active' : 'btn btn--light switch--btn'} onClick={this.props.showList}><i className="fa fa-list" /></button>
                <button className={this.props.displayMap ? 'btn btn--light switch--btn active' : 'btn btn--light switch--btn'} onClick={this.props.showMap}><i className="fa fa-map" /></button>
              </div>
            </div>
          </div>
        </div>
      )
    }
  }
}

module.exports = MapListSwitch
