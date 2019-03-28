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

  getTopicList (item) {
    let topicList = item.topics.map((val) => {
      return this.props.topicChoices[val]
    })
    return topicList
  }

  renderTopics (item) {
    let topicsList = this.getTopicList(item)
    if (item.topics) {
      return (
        <div className={item.tile_image ? 'maplist-item__label-img' : 'maplist-item__label-spacer'}>
          {topicsList.map(topic => <span key={topic} className="label label--secondary maplist-item__label u-spacer-bottom">{topic}</span>)}
        </div>
      )
    }
  }

  getText (item) {
    if (item.length > 170) {
      return item.substr(0, 170) + '...'
    } else {
      return item
    }
  }

  renderListItem (item, i) {
    let statusClass = (item.participation_active === true) ? 'maplist-item__status-active' : 'maplist-item__status-inactive'
    return (
      <li className={this.props.isHorizontal ? 'maplist-item__horizontal' : 'maplist-item__vertical'} key={i}>

        <a href={item.url} target={item.subtype === 'external' ? '_blank' : '_self'}>
          {item.type === 'project' &&
            <div className="maplist-item__proj">
              {item.tile_image &&
              <div className={this.props.isHorizontal ? 'u-lg-only-display maplist-item__img' : 'maplist-item__img'} style={this.getImage(item)} alt="">
                {!this.props.isHorizontal && this.renderTopics(item)}
                { item.tile_image_copyright &&
                  <span className="maplist-item__img-copyright copyright">© {item.tile_image_copyright}</span>
                }
              </div>
              }
              <div className="maplist-item__content">
                {(this.props.isHorizontal || !item.tile_image) && this.renderTopics(item)}
                <span className="maplist-item__roofline">{item.district}</span>
                <h3 className="maplist-item__title">{item.title}</h3>
                {!this.props.isHorizontal &&
                <div className="maplist-item__description">
                  <span>{this.getText(item.description)}</span>
                </div>
                }
                <div className="maplist-item__link" />
                {item.subtype === 'container' &&
                  <div className="maplist-item__stats">
                    <span className="maplist-item__proj-count"><i className="fas fa-th" aria-hidden="true" />{django.gettext('Participation projects: ')}</span>
                    <span>{item.published_projects_count}</span>
                    <br />
                    <span className="maplist-item__status"><i className="fas fa-clock" aria-hidden="true" />{django.gettext('Participation: ')}</span>
                    <span className={statusClass}>{item.participation_string }</span>
                  </div>
                }
                {item.future_phase && !item.active_phase &&
                  <div className="status-item status__future">
                    <span className="maplist-item__status"><i className="fas fa-clock" aria-hidden="true" />{django.gettext('Participation: from ')}{item.future_phase}</span>
                  </div>
                }
                {item.active_phase &&
                <div className="status-item status__active">
                  <div className="status-bar__active"><span className="status-bar__active-fill" style={this.getWidth(item)} /></div>
                  <span className="maplist-item__status"><i className="fas fa-clock" aria-hidden="true" />{django.gettext('remaining')} {item.active_phase[1]}</span>
                </div>
                }
                {item.past_phase && !item.active_phase && !item.future_phase &&
                  <div className="status-item status-bar__past">
                    {django.gettext('Participation ended. Read result.')}
                  </div>
                }
              </div>
              <div className="status-item_spacer" />
            </div>
          }
          {item.type === 'plan' &&
            <div className="maplist-item__plan">
              {this.renderTopics(item)}
              <span className="maplist-item__roofline">{item.district}</span>
              <h3 className="maplist-item__title">{item.title}</h3>
              <div className="maplist-item__link" />
              <div className="maplist-item__stats">
                <span className="maplist-item__proj-count"><i className="fas fa-th" aria-hidden="true" />{django.gettext('Participation projects: ')}</span>
                <span>{item.published_projects_count}</span>
                <br />
                <span className="maplist-item__status"><i className="fas fa-clock" aria-hidden="true" />{django.gettext('Status: ')}</span>
                <span className={statusClass}>{item.participation_string }</span>
              </div>
              <div className="status-item_spacer" />
            </div>
          }
          {item.subtype === 'external' &&
          <div className="maplist-item__corner-badge maplist-item__corner-badge--external" />
          }
          {!item.is_public && item.type === 'project' &&
          <div className="maplist-item__corner-badge maplist-item__corner-badge--private" />
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
