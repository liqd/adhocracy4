/* global django */
const React = require('react')

var styles = {
  backgroundImage: `url(https://placeimg.com/500/500/any/grayscale)`,
  backgroundPosition: 'center',
  backgroundSize: 'contain'
}

class PlansList extends React.Component {
  bindList (element) {
    this.listElement = element
  }
  renderListItem (item, i) {
    let itemClass = 'maplist-item'
    let statusClass = (item.participation_active === true) ? 'maplist-item__status--active' : 'maplist-item__status--inactive'
    return (

      <li className={itemClass} key={i} tabIndex="0">
        <a href={item.url}>
          <div className={item.type === 'project' ? 'maplist-item__proj' : 'd-none'}>
            <div className="maplist-item__img" style={styles} alt="">
              <span className="maplist-item__img-copyright copyright">© copyright</span>
            </div>

            <div className="maplist-item__info">
              <div className="maplist-item__labels u-spacer-bottom">
                <span className="label label--secondary">{this.props.topicChoices[item.topic]}</span>
              </div>
              <span className="maplist-item__roofline">{item.district}</span>
              <h3 className="maplist-item__title">{item.title}</h3>
              <span>{item.description}</span>
            </div>
          </div>

          <div className={item.type === 'plan' ? 'maplist-item__plan' : 'd-none'}>
            <div className="maplist-item__labels u-spacer-bottom">
              <span className="label label--secondary">{item.theme}</span>
            </div>
            <span className="maplist-item__roofline">{item.district}</span>
            <h3 className="maplist-item__title">{item.title}</h3>
            <div>
              <span className="maplist-item__proj-count"><i className="fas fa-th" />{django.gettext('Participation projects: ')}</span>
              <span className="maplist-item__status--inactive">{item.published_projects_count}</span>
            </div>
            <div>
              <span className="maplist-item__status"><i className="fas fa-clock" />{django.gettext('Participation: ')}</span>
              <span className={statusClass}>{item.participation_string }</span>
            </div>
          </div>
        </a>
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
