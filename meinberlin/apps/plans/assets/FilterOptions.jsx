/* global django */
const React = require('react')

class FilterOptions extends React.Component {
  render () {
    return (
      <div className="filter-bar__dropdown-menu">
        <h2 className="filter-bar__question">{this.props.question}</h2>
        <div className="filter-bar__options--horizontal">
          <div className="filter-bar__option filter-bar__option--horizontal">
            <button
              type="button"
              value="-1"
              onClick={this.props.onSelect}>
              {django.gettext('all')}
            </button>
          </div>
          {
            Object.keys(this.props.options).map((key, i) => {
              return (
                <div key={key} className="filter-bar__option filter-bar__option--horizontal">
                  <button
                    type="button"
                    value={key}
                    onClick={this.props.onSelect}>
                    {this.props.options[key]}
                  </button>
                </div>
              )
            })
          }
        </div>
      </div>
    )
  }
}

module.exports = FilterOptions
