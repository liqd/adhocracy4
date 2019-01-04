/* global django */
var FilterOptions = require('./FilterOptions')
const React = require('react')

class FilterNav extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      displayDistrictOptions: false,
      displayTopicOptions: false
    }
  }

  showDistrictOptions () {
    this.setState({
      displayTopicOptions: false,
      displayDistrictOptions: !this.state.displayDistrictOptions
    })
  }

  showTopicOptions () {
    this.setState({
      displayDistrictOptions: false,
      displayTopicOptions: !this.state.displayTopicOptions
    })
  }

  clickDistrict (event) {
    let district = event.currentTarget.value
    this.props.selectDistrict(district)
    this.setState({
      displayDistrictOptions: false
    })
  }

  clickTopic (event) {
    let topic = event.currentTarget.value
    this.props.selectTopic(topic)
    this.setState({
      displayTopicOptions: false
    })
  }

  getDistrictFilterName () {
    if (this.props.district === '-1') {
      return django.gettext('all')
    }
    return this.props.district
  }

  getTopicFilterName () {
    if (this.props.topic === '-1') {
      return django.gettext('all')
    }
    return this.props.topicChoices[this.props.topic]
  }

  render () {
    return (
      <div className="filter-bar-spacer">
        <div className="control-bar filter-bar" role="group" aria-label={django.gettext('Filter bar')}>
          <span>{django.gettext('I am interested in projects from')}</span>
          <div className="filter-bar__dropdown">
            <button type="button"
              className={this.props.district === '-1' ? 'dropdown-toggle btn btn--light btn--select btn--none filter-bar__dropdown-btn' : 'd-none'}
              data-flip="false"
              aria-haspopup="true"
              aria-expanded="false"
              onClick={this.showDistrictOptions.bind(this)}
              id="id_filter_district">
              {django.gettext('District')}: {this.getDistrictFilterName()}
              <i className="fa fa-caret-down" aria-hidden="true" />
            </button>
            <button type="button"
              className={this.props.district !== '-1' ? 'dropdown-toggle btn btn--light btn--none btn--select filter-bar__dropdown-selected' : 'd-none'}
              data-flip="false"
              aria-haspopup="true"
              aria-expanded="false"
              onClick={this.showDistrictOptions.bind(this)}
              id="id_filter_district">
              {this.getDistrictFilterName()}
              <i className="fa fa-times" aria-hidden="true" />
            </button>
          </div>
          <span>{django.gettext(' in the area of ')}</span>
          <div className="filter-bar__dropdown">
            <button type="button"
              className={this.props.topic === '-1' ? 'dropdown-toggle btn btn--light btn--select btn--none filter-bar__dropdown-btn' : 'd-none'}
              data-flip="false"
              aria-haspopup="true"
              onClick={this.showTopicOptions.bind(this)}
              aria-expanded="false"
              id="id_filter_topic">
              {django.gettext('Topic')}: {this.getTopicFilterName()}
              <i className="fa fa-caret-down" aria-hidden="true" />
            </button>
            <button type="button"
              className={this.props.topic !== '-1' ? 'dropdown-toggle btn btn--light btn--none btn--select filter-bar__dropdown-selected' : 'd-none'}
              data-flip="false"
              aria-haspopup="true"
              aria-expanded="false"
              onClick={this.showTopicOptions.bind(this)}
              id="id_filter_topic">
              {this.getTopicFilterName()}
              <i className="fa fa-times" aria-hidden="true" />
            </button>
          </div>
          <div>
            <button className="btn btn--light btn--small filter-bar__btn-light">{django.gettext('more filters')}</button>
          </div>
        </div>
        { this.state.displayDistrictOptions &&
          <FilterOptions
            title={django.gettext('Which district are you interested in?')}
            options={this.props.districtnames}
            onSelect={this.clickDistrict.bind(this)}
          />
        }
        { this.state.displayTopicOptions &&
          <FilterOptions
            title={django.gettext('Which topic are you interested in?')}
            options={this.props.topicChoices}
            onSelect={this.clickTopic.bind(this)}
          />
        }
      </div>
    )
  }
}

module.exports = FilterNav
