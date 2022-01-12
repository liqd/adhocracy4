import React from 'react'
import django from 'django'
import { IconSwitch } from '../../contrib/assets/IconSwitch'

const searchResultsStr = django.gettext(' search results')
const showMapStr = django.gettext('Show map')
const showMapAriaStr = django.gettext('show map')
const hideMapStr = django.gettext('hide map')
const listStr = django.gettext('List')
const mapStr = django.gettext('Map')
const showListStr = django.gettext('show list')

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

  organisationButtonString () {
    if (this.props.organisationString.length > 20) {
      return this.props.organisationString.substr(0, 20) + '...'
    }
    return this.props.organisationString
  }

  render () {
    if (this.props.isSlider) {
      return (
        <div>
          <div className="l-frame switch-container">
            <div className={this.props.displayButtons ? 'switch-filter__label' : 'd-none'}>{this.props.projectCount}{searchResultsStr}</div>
            <div className="switch-filter__btn-group">
              {this.props.displayButtons && this.props.statusSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickStatusButton.bind(this)}
                  type="button"
                >{this.props.statusString} {this.props.statusCount} <i className="fa fa-times" />
                </button>}
              {this.props.displayButtons && this.props.participationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickParticipationButton.bind(this)}
                  type="button"
                >{this.props.participationString} {this.props.participationCount} <i className="fa fa-times" />
                </button>}
              {this.props.displayButtons && this.props.organisationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickOrganisationButton.bind(this)}
                  type="button"
                >{this.organisationButtonString()} {this.props.organisationCount} <i className="fa fa-times" />
                </button>}
              {this.props.displayButtons && this.props.titleSearchSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickTitleSearchButton.bind(this)}
                  type="button"
                >{this.titleSearchButtonString()} {this.props.titleSearchCount} <i className="fa fa-times" />
                </button>}
            </div>
            <div className="switch">
              <div className="switch-group" role="group" aria-labelledby="switch-primary">
                <label htmlFor="switch-primary" className="switch-label">
                  <span className="switch-label__text">{showMapStr}</span>
                  <input
                    className="switch-input"
                    id="switch-primary"
                    onChange={this.props.toggleSwitch} /* eslint-disable-line react/jsx-handler-names */
                    name="switch-primary"
                    type="checkbox"
                    aria-label={hideMapStr}
                  />
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
          <div className="l-frame switch-container">
            <div className={this.props.displayButtons ? 'switch-filter__label' : 'd-none'}>{this.props.projectCount}{searchResultsStr}</div>
            <div className="switch-filter__btn-group">
              {this.props.displayButtons && this.props.statusSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickStatusButton.bind(this)}
                  type="button"
                >{this.props.statusString} <i className="fa fa-times" />
                </button>}
              {this.props.displayButtons && this.props.participationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickParticipationButton.bind(this)}
                  type="button"
                >{this.props.participationString} <i className="fa fa-times" />
                </button>}
              {this.props.displayButtons && this.props.organisationSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickOrganisationButton.bind(this)}
                  type="button"
                >{this.props.organisationString} <i className="fa fa-times" />
                </button>}
              {this.props.displayButtons && this.props.titleSearchSelected &&
                <button
                  className="btn btn--transparent btn--small"
                  onClick={this.clickTitleSearchButton.bind(this)}
                  type="button"
                >{this.titleSearchButtonString()} <i className="fa fa-times" />
                </button>}
            </div>
            <IconSwitch
              activeClass="btn btn--icon btn--light switch--btn active"
              inactiveClass="btn btn--icon btn--light"
              startText={listStr}
              endText={mapStr}
              startAria={showListStr}
              endAria={showMapAriaStr}
              startIconClass="fa fa-list"
              endIconClass="fa fa-map"
              startID="show_list"
              endID="show_map"
              displayStartObject={this.props.displayMap}
              showStartObject={this.props.showList}
              showEndObject={this.props.showMap}
            />
          </div>
        </div>
      )
    }
  }
}

module.exports = Toggles
