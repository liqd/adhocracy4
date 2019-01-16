/* global django */
const React = require('react')

class FilterOptions extends React.Component {
  getMenuClassName () {
    if (this.props.isStacked) {
      return 'filter-bar__menu'
    }
    return 'filter-bar__dropdown-menu filter-bar__menu'
  }

  getGridClassName () {
    if (this.props.numColumns > 1) {
      return 'l-tiles-' + this.props.numColumns
    }
    return ''
  }

  getListLength () {
    const elements = Object.keys(this.props.options).length + 2
    const elementsPerColumn = Math.ceil(elements / this.props.numColumns)
    return elementsPerColumn
  }

  getListElement (key) {
    return (
      <button
        type="button"
        value={key}
        onClick={this.props.onSelect}>
        {this.props.options[key]}
      </button>
    )
  }

  getList (sliceStart, sliceEnd) {
    const slicedList = Object.keys(this.props.options).slice(sliceStart, sliceEnd)
    const listItems =
      slicedList.map((key, i) =>
        <div key={key} className="filter-bar__option">
          {this.getListElement(key)}
        </div>
      )
    return (
      <div>
        {listItems}
      </div>
    )
  }

  getLastList (sliceStart, sliceEnd) {
    let sliceEndLast = sliceEnd
    if (this.props.hasNoneValue) {
      sliceEndLast = -1
    }
    return (
      <div>
        {
          Object.keys(this.props.options).slice(sliceStart, sliceEndLast).map((key, i) => {
            return (
              <div key={key} className="filter-bar__option">
                {this.getListElement(key)}
              </div>
            )
          })
        }
        <div className="filter-bar__option-divider" />
        {this.props.hasNoneValue &&
          Object.keys(this.props.options).slice(-1).map((key, i) => {
            return (
              <div key={key} className="filter-bar__option">
                {this.getListElement(key)}
              </div>
            )
          })
        }
        <div className="filter-bar__option">
          <button
            type="button"
            value="-1"
            onClick={this.props.onSelect}>
            {django.gettext('all')}
          </button>
        </div>
      </div>
    )
  }

  getLists () {
    let lists = []
    for (var i = 0; i < this.props.numColumns; i++) {
      let sliceStart = 0 + i * this.getListLength()
      let sliceEnd = this.getListLength() + i * this.getListLength()
      if (i < this.props.numColumns - 1) {
        lists.push(this.getList(sliceStart, sliceEnd))
      } else {
        lists.push(this.getLastList(sliceStart, sliceEnd))
      }
    }
    return lists
  }

  render () {
    return (
      <div aria-labelledby={this.props.ariaLabelledby} className={this.getMenuClassName()}>
        <h2 className="filter-bar__question">{this.props.question}</h2>
        <div className={this.getGridClassName()}>
          {this.getLists()}
        </div>
      </div>
    )
  }
}

module.exports = FilterOptions
