/* global django */
const React = require('react')

class OptionButton extends React.Component {
  render () {
    return (
      <button
        type="button"
        value={this.props.identifier}
        onClick={this.props.onSelect}>
        {this.props.name}
      </button>
    )
  }
}

class OptionList extends React.Component {
  render () {
    return (
      <div key={'list' + this.props.name}>
        {this.props.listItems.map((key, i) =>
          <div key={i.toString()}
            className={this.props.getClassNameInput(key, this.props.options[key])}>
            <OptionButton
              identifier={key}
              onSelect={this.props.onSelect.bind(this)}
              name={this.props.options[key]}
            />
          </div>
        )}
      </div>
    )
  }
}

class OptionListLast extends React.Component {
  render () {
    return (
      <div key={'lastList'}>
        {this.props.listItems.map((key, i) => (
          <div key={key}
            className={this.props.getClassNameInput(key, this.props.options[key])}>
            <OptionButton
              identifier={key}
              onSelect={this.props.onSelect.bind(this)}
              name={this.props.options[key]}
            />
          </div>
        ))}
        <div className="filter-bar__option-divider" />
        {this.props.hasNoneValue &&
          Object.keys(this.props.options).slice(-1).map((key, i) => {
            return (
              <div key={key}
                className={this.props.getClassNameInput(key, this.props.options[key])}>
                <OptionButton
                  identifier={key}
                  onSelect={this.props.onSelect.bind(this)}
                  name={this.props.options[key]}
                />
              </div>
            )
          })
        }
        <div className={this.props.getClassNameInput('-1', '-1')}>
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
}

class FilterOptions extends React.Component {
  getMenuClassName () {
    if (this.props.isStacked) {
      return 'filter-bar__menu'
    }
    if (this.props.isPartOfForm) {
      return ''
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

  getList (sliceStart, sliceEnd, i) {
    let slicedList = Object.keys(this.props.options).slice(sliceStart, sliceEnd)
    return (
      <OptionList
        key={i.toString()}
        name={i.toString()}
        listItems={slicedList}
        onSelect={this.props.onSelect.bind(this)}
        options={this.props.options}
        selectedChoice={this.props.selectedChoice}
        getClassNameInput={this.getClassNameInput.bind(this)} />
    )
  }

  getLastList (sliceStart, sliceEnd, i) {
    let sliceEndLast = sliceEnd
    if (this.props.hasNoneValue) {
      sliceEndLast = -1
    }
    let slicedList = Object.keys(this.props.options).slice(sliceStart, sliceEndLast)
    return (
      <OptionListLast
        key={i.toString()}
        listItems={slicedList}
        onSelect={this.props.onSelect.bind(this)}
        hasNoneValue={this.props.hasNoneValue}
        options={this.props.options}
        selectedChoice={this.props.selectedChoice}
        getClassNameInput={this.getClassNameInput.bind(this)} />
    )
  }

  getLists () {
    let lists = []
    for (let i = 0; i < this.props.numColumns; i++) {
      let sliceStart = 0 + i * this.getListLength()
      let sliceEnd = this.getListLength() + i * this.getListLength()
      if (i < this.props.numColumns - 1) {
        lists.push(this.getList(sliceStart, sliceEnd, i))
      } else {
        lists.push(this.getLastList(sliceStart, sliceEnd, i))
      }
    }
    return lists
  }

  getClassNameInput (choice1, choice2) {
    if (this.props.selectedChoice === choice1 || this.props.selectedChoice === choice2) {
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
