/* global django */
const React = require('react')

class FilterNav extends React.Component {
  clickDistrict (event) {
    let district = event.currentTarget.value
    this.props.selectDistrict(district)
  }

  getDistrictFilterName () {
    if (this.props.district === '-1') {
      return django.gettext('all')
    }
    return this.props.district
  }

  render () {
    return (
      <div className="u-spacer-left u-spacer-right">
        <div className="control-bar proj-map__filter-bar" role="group" aria-label={django.gettext('Filter bar')}>
          <span>{django.gettext('I am interested in projects from ')}</span>
          <div className="dropdown ">
            <button type="button"
              className="dropdown-toggle btn btn--light btn--select btn--none proj-map__dropdown"
              data-flip="false"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="id_filter_district">
              {django.gettext('District')}: {this.getDistrictFilterName()}
              <i className="fa fa-caret-down" aria-hidden="true" />
            </button>
            <ul aria-labelledby="id_filter_district" className="dropdown-menu">
              <li>
                <button
                  type="button"
                  className="dropdown-item"
                  value="-1"
                  onClick={this.clickDistrict.bind(this)}>
                  {django.gettext('All')}
                </button>
              </li>
              {
                this.props.districtnames.map((name, i) => {
                  return (
                    <li key={name}>
                      <button
                        type="button"
                        className="dropdown-item"
                        value={name}
                        onClick={this.clickDistrict.bind(this)}>
                        {name}
                      </button>
                    </li>
                  )
                })
              }
            </ul>
          </div>
          <span>{django.gettext(' and the area ')}</span>
        </div>
      </div>
    )
  }
}

module.exports = FilterNav
