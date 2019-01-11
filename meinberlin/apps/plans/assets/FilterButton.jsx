const React = require('react')

class FilterButton extends React.Component {
  render () {
    return (
      <button type="button"
        className={this.props.className}
        data-flip="false"
        aria-haspopup="true"
        aria-expanded={this.props.ariaExpanded}
        onClick={this.props.showOptions}
        id={this.props.id}>
        {this.props.buttonText}
        <i className={this.props.iClassName} aria-hidden="true" />
      </button>
    )
  }
}

module.exports = FilterButton
