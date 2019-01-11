/* global django */
const React = require('react')

class PlansList extends React.Component {
  bindList (element) {
    this.listElement = element
  }

  getWidth (item) {
    return { width: item.active_phase[0] + '%' }
  }

  getImage (item) {
    return {
      backgroundImage: `url(` + item.tile_image + ')',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat'
    }
  }

  getText (item) {
    if (item.length > 100) {
      return item.substr(0, 100) + '...'
    } else {
      return item
    }
  }

  renderListItem (item, i) {
    let statusClass = (item.participation_active === true) ? 'maplist-item__status-active' : 'maplist-item__status-inactive'
    return (
      <li className={this.props.isHorizontal ? 'maplist-item__horizontal' : 'maplist-item__vertical'} key={i} tabIndex="0">
        <a href={item.url}>
          {item.type === 'project' &&
            <div className="maplist-item__proj">
              {item.tile_image &&
              <div className="maplist-item__img" style={this.getImage(item)} alt="">
                { item.tile_image_copyright &&
                  <span className="maplist-item__img-copyright copyright">© {item.tile_image_copyright}</span>
                }
              </div>
              }
              <div className="maplist-item__content">
                {item.topic &&
                <div className={item.tile_image ? 'malist-item__label-nospacer' : 'maplist-item__label-spacer'}>
                  <span className="label label--secondary maplist-item__label">{this.props.topicChoices[item.topic]}</span>
                </div>
                }
                <span className="maplist-item__roofline">{item.district}</span>
                <h3 className="maplist-item__title">{item.title}</h3>
                <div className="maplist-item__description">
                  <span>{this.getText(item.description)}</span>
                </div>
                {item.future_phase &&
                <div>
                  <div className="status-item status__future">
                    <span className="maplist-item__status"><i className="fas fa-clock" />{django.gettext('Participation: from ')}{item.future_phase}{django.gettext(' possible')}</span>
                  </div>
                  <div className="status-item_spacer" />
                </div>
                }
                {item.active_phase &&
                  <div>
                    <div className="status-item status__active">
                      <div className="status-bar__active"><span className="status-bar__active-fill" style={this.getWidth(item)} /></div>
                      <span className="maplist-item__status"><i className="fas fa-clock" />{item.active_phase[1]} {django.gettext('remaining')}</span>
                    </div>
                    <div className="status-item_spacer" />
                  </div>
                }
                {item.past_phase &&
                <div>
                  <div className="status-item status-bar__past">
                    {django.gettext('Participation ended. Read result.')}
                  </div>
                  <div className="status-item_spacer" />
                </div>
                }
              </div>
            </div>
          }
          {item.type === 'plan' &&
            <div className="maplist-item__plan">
              {item.theme &&
              <div className="maplist-item__labels u-spacer-bottom-half">
                <span className="label label--secondary">{item.theme}</span>
              </div>
              }
              <span className="maplist-item__roofline">{item.district}</span>
              <h3 className="maplist-item__title">{item.title}</h3>
              <div className="maplist-item__stats">
                <span className="maplist-item__proj-count"><i className="fas fa-th" />{django.gettext('Participation projects: ')}</span>
                <span>{item.published_projects_count}</span>
                <br />
                <span className="maplist-item__status"><i className="fas fa-clock" />{django.gettext('Participation: ')}</span>
                <span className={statusClass}>{item.participation_string }</span>
              </div>
              <div className="status-item_spacer" />
            </div>
          }
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
        <ul className="u-list-reset maplist-list">
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
