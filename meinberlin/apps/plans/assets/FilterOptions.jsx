/* global django */
const React = require('react')

class Filteroptions extends React.Component {
  render () {
    return (
      <div className="filter-bar__options">
        <h2>{this.props.title}</h2>
        <div className="u-display-flex u-flex-wrap">
          <div className="filter-bar__options__option">
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
                <div key={key} className="filter-bar__options__option">
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

module.exports = Filteroptions
