/* global django */
const React = require('react')

var styles = {
  backgroundImage: `url(https://placeimg.com/250/250/any/grayscale)`,
  backgroundPosition: 'center'
}

class PlansList extends React.Component {
  bindList (element) {
    this.listElement = element
  }
  renderListItem (item, i) {
    let itemClass = 'list-item maplist-item list-item--squashed'
    let statusClass = (item.participation_active === true) ? 'list-item__status--active' : 'list-item__status--inactive'
    return (

      <li className={itemClass} key={i} tabIndex="0">
        <div className={item.type === 'project' ? 'maplist-proj' : 'd-none'} >
          <div className="maplist__image" style={styles} alt="">
            <span className="maplist__copyright copyright">© copyright</span>
          </div>

          <div className="maplist__info">
            <div className="maplist-item__labels">
              <span className="label label--secondary">{item.status_display}</span>
            </div>

            <p>{item.district}</p>

            <h2 className="maplist-item__title"><a href={item.url}>{item.title}</a></h2>
            <div className="maplist-item__subtitle"><b>{django.gettext('Theme: ')}</b><span>{item.theme}</span></div>
            <div className="maplist-item__subtitle"><b>{django.gettext('Participation: ')}</b><span className={statusClass}>{item.participation_string}</span></div>
          </div>
        </div>

        <div className={item.type === 'plan' ? 'maplist-plan' : 'd-none'} >
          Im a plan!!!!
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
        </div>

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
