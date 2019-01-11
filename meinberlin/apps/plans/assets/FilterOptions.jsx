/* global django */
const React = require('react')

class FilterOptions extends React.Component {
  getMenuClassName () {
    if (this.props.isStacked) {
      return 'filter-bar__menu'
    }
    return 'filter-bar__dropdown-menu filter-bar__menu'
  }

  getOptionsClassName () {
    if (this.props.isStacked) {
      return ''
    }
    return 'filter-bar__options--horizontal'
  }

  getOptionClassName () {
    if (this.props.isStacked) {
      return 'filter-bar__option'
    }
    return 'filter-bar__option filter-bar__option--horizontal'
  }

  render () {
    return (
      <div aria-labelledby={this.props.ariaLabelledby} className={this.getMenuClassName()}>
        <h2 className="filter-bar__question">{this.props.question}</h2>
        <div className={this.getOptionsClassName()}>
          <div className={this.getOptionClassName()}>
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
                <div key={key} className={this.getOptionClassName()}>
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
