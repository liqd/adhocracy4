/* global django */
const React = require('react')

class Toggles extends React.Component {
  clickStatusButton () {
    this.props.changeStatusSelection(-1)
  }

  clickParticipationButton () {
    this.props.changeParticipationSelection(-1)
  }

  clickOrganisationButton () {
    this.props.changeOrganisationSelection('-1')
  }

  clickTitleSearchButton () {
    this.props.changeTitleSearchSelection('-1')
  }

  titleSearchButtonString () {
    if (this.props.titleSearchString.length > 20) {
      return this.props.titleSearchString.substr(0, 20) + '...'
    }
    return this.props.titleSearchString
  }

  render () {
    if (this.props.isSlider) {
      return (
        <div>
          <div className="switch-container">
            <div className={this.props.displayButtons && (this.props.statusSelected || this.props.participationSelected || this.props.organisationSelected || this.props.titleSearchSelected) ? 'switch-filter__label' : 'd-none'}>{django.gettext('Set filters')}</div>
            <div>
              { this.props.displayButtons && this.props.statusSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickStatusButton.bind(this)}
                  type="button">{this.props.statusString} <i className="fa fa-times" /></button>
              }
              { this.props.displayButtons && this.props.participationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickParticipationButton.bind(this)}
                  type="button">{this.props.participationString} <i className="fa fa-times" /></button>
              }
              { this.props.displayButtons && this.props.organisationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickOrganisationButton.bind(this)}
                  type="button">{this.props.organisationString} <i className="fa fa-times" /></button>
              }
              { this.props.displayButtons && this.props.titleSearchSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickTitleSearchButton.bind(this)}
                  type="button">{this.titleSearchButtonString()} <i className="fa fa-times" /></button>
              }
            </div>
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
          <div className="switch-container">
            <div className={this.props.displayButtons && (this.props.statusSelected || this.props.participationSelected || this.props.organisationSelected || this.props.titleSearchSelected) ? 'switch-filter__label' : 'd-none'}>{django.gettext('Set filters')}</div>
            <div>
              { this.props.displayButtons && this.props.statusSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickStatusButton.bind(this)}
                  type="button">{this.props.statusString} <i className="fa fa-times" /></button>
              }
              { this.props.displayButtons && this.props.participationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickParticipationButton.bind(this)}
                  type="button">{this.props.participationString} <i className="fa fa-times" /></button>
              }
              { this.props.displayButtons && this.props.organisationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickOrganisationButton.bind(this)}
                  type="button">{this.props.organisationString} <i className="fa fa-times" /></button>
              }
              { this.props.displayButtons && this.props.titleSearchSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickTitleSearchButton.bind(this)}
                  type="button">{this.titleSearchButtonString()} <i className="fa fa-times" /></button>
              }
            </div>
            <div className="switch-btn-group-container">
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
        </div>
      )
    }
  }
}

module.exports = Toggles
