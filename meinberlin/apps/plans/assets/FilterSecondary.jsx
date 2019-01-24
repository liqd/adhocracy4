/* global django */
const React = require('react')

class FilterSecondary extends React.Component {
  render () {
    return (
      <form className="filter-bar__menu">
        {django.gettext('These are the secondary filters!')}
      </form>
    )
  }
}

module.exports = FilterSecondary
