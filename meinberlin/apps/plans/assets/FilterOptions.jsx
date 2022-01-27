/* global django */
const React = require('react')
const allStr = django.gettext('all')

class OptionButton extends React.Component {
  render () {
    return (
      <button
        type="button"
        value={this.props.identifier}
        onClick={this.props.onSelect}
      >
        {this.props.name}
      </button>
    )
  }
}

class OptionList extends React.Component {
  render () {
    return (
      <div key={this.props.keyProp}>
        {this.props.firstElement &&
          <div className={this.props.getClassNameInput('-1')}>
            <button
              type="button"
              value="-1"
              onClick={this.props.onSelect}
            >
              {allStr}
            </button>
          </div>}
        {this.props.firstElement &&
          <div className="filter-bar__option-divider" />}
        {this.props.listItems.map((key, i) => (
          <div
            key={key}
            className={this.props.getClassNameInput(this.props.options[key])}
          >
            <OptionButton
              identifier={key}
              onSelect={this.props.onSelect.bind(this)}
              name={this.props.options[key]}
            />
          </div>
        ))}
        {this.props.hasNoneValue && this.props.lastElement &&
          <div className="filter-bar__option-divider" />}
        {this.props.hasNoneValue && this.props.lastElement &&
          Object.keys(this.props.options).slice(-1).map((key, i) => {
            return (
              <div
                key={key}
                className={this.props.getClassNameInput(this.props.options[key])}
              >
                <OptionButton
                  identifier={key}
                  onSelect={this.props.onSelect.bind(this)}
                  name={this.props.options[key]}
                />
              </div>
            )
          })}
      </div>
    )
  }
}

class FilterOptions extends React.Component {
  getMenuClassName () {
    if (this.props.isStacked) {
      return 'filter-bar__menu'
    }
    return 'l-frame filter-bar__dropdown-menu filter-bar__menu'
  }

  getGridClassName () {
    if (this.props.numColumns === 3) {
      return 'l-tiles-4'
    } else if (this.props.numColumns > 1) {
      return 'l-tiles-' + this.props.numColumns
    }
    return ''
  }

  getListLength () {
    let elements = Object.keys(this.props.options).length + 2
    if (this.props.hasNoneValue) {
      elements += 2
    }
    const elementsPerColumn = Math.ceil(elements / this.props.numColumns)
    return elementsPerColumn
  }

  getList (sliceStart, sliceEnd, i, firstElement, lastElement) {
    let sliceEndLast = sliceEnd
    if (lastElement && this.props.hasNoneValue) {
      sliceEndLast = -1
    }
    const slicedList = Object.keys(this.props.options).slice(sliceStart, sliceEndLast)
    return (
      <OptionList
        key={'list-' + i.toString()}
        keyProp={'list-' + i.toString()}
        listItems={slicedList}
        onSelect={this.props.onSelect.bind(this)}
        hasNoneValue={this.props.hasNoneValue}
        options={this.props.options}
        selectedChoice={this.props.selectedChoice}
        getClassNameInput={this.getClassNameInput.bind(this)}
        firstElement={firstElement}
        lastElement={lastElement}
      />
    )
  }

  getLists () {
    const lists = []
    for (let i = 0; i < this.props.numColumns; i++) {
      const firstElement = (i === 0)
      const lastElement = (i === (this.props.numColumns - 1))
      let sliceStart = i * this.getListLength()
      if (!firstElement) {
        sliceStart -= 2
      }
      const sliceEnd = (this.getListLength() - 2) + i * this.getListLength()
      lists.push(this.getList(sliceStart, sliceEnd, i, firstElement, lastElement))
    }
    return lists
  }

  getClassNameInput (choice) {
    if (this.props.selectedChoice === choice) {
      return 'filter-bar__option active'
    }
    return 'filter-bar__option'
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
