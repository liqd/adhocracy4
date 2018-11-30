/* global django */
const React = require('react')

class PlansList extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      filters: {
        status: -1,
        participation: -1,
        district: -1
      }
    }
  }

  bindList (element) {
    this.listElement = element
  }

  componentDidMount () {

  }

  componentDidUpdate (prevProps, prevState) {
    if (prevState.selected !== this.state.selected || prevState.filters !== this.state.filters) {
      // filter markers
      this.props.items.forEach((item, i) => {
        if (item.point !== '') {
          if (!this.isInFilter(item)) {
            this.setMarkerFiltered(i)
          } else if (i === this.state.selected) {
            this.setMarkerSelected(i, item)
          } else {
            this.setMarkerDefault(i, item)
          }
        }
      })
    }
  }

  renderListItem (item, i) {
    let itemClass = 'list-item list-item--squashed'
    if (i === this.state.selected) {
      itemClass += ' selected'
    }
    let statusClass = (item.participation_active === true) ? 'list-item__status--active' : 'list-item__status--inactive'
    return (
      <li className={itemClass} key={i} tabIndex="0">
        <div className="list-item__labels">
          {
            <span className="label label--secondary">{item.status_display}</span>
          } {item.district &&
            <span className="label"><i className="fas fa-map-marker-alt" aria-hidden="true" /> {item.district}</span>
          }
        </div>
        <h3 className="list-item__title"><a href={item.url}>{item.title}</a></h3>
        <div className="list-item__subtitle"><b>{django.gettext('Theme: ')}</b><span>{item.theme}</span></div>
        <div className="list-item__subtitle"><b>{django.gettext('Participation: ')}</b><span className={statusClass}>{item.participation_string}</span></div>
      </li>
    )
  }

  renderList () {
    let list = []
    this.props.items.forEach((item, i) => {
      list.push(this.renderListItem(item, i))
    })

    if (list.length > 0) {
      return (
        <ul className="u-list-reset">
          {list}
        </ul>
      )
    } else {
      return (
        <div className="list-item-empty">{django.gettext('Nothing to show')}</div>
      )
    }
  }

  render () {
    return (
      <div ref={this.bindList.bind(this)}>
        {this.renderList()}
      </div>
    )
  }
}

module.exports = PlansList
