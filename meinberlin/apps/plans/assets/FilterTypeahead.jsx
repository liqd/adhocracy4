/* global django */
const Typeahead = require('react-bootstrap-typeahead').Typeahead
const React = require('react')

const orgaStr = django.gettext('Organisation')
const enterOrgaNameStr = django.gettext('Enter the name of the organisation')

class FilterTypeahead extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      organisationChoice: this.props.organisation
    }
  }

  handleChange (organisation) {
    this.setState({
      organisationChoice: organisation
    })
  }

  render () {
    return (
      <div className="form-group filter-bar__typeahead">
        <div className="typeahead__input-label">
          <h2 className="u-no-margin">{orgaStr}</h2>
        </div>
        <span className="typeahead__input-group">
          <span className="typeahead__input-group-prepend">
            <span className="typeahead__input-group-text">
              <i className="fas fa-sort-alpha-down" />
            </span>
          </span>
          <Typeahead
            id="organisation-typeahead-id-2"
            className=""
            onChange={this.handleChange.bind(this)}
            labelKey="name"
            multiple={false}
            options={this.props.organisations}
            selected={this.state.organisationChoice}
            placeholder={enterOrgaNameStr}
          />
        </span>
      </div>
    )
  }
}

module.exports = FilterTypeahead
