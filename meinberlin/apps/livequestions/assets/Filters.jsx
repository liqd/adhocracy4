import React from 'react'
import django from 'django'

export default class Filter extends React.Component {
  selectCategory (e) {
    e.preventDefault()
    const category = e.target.getAttribute('data-value')
    this.props.setCategories(category)
  }

  getButtonClass () {
    if (this.props.currentCategory === '-1') {
      return 'btn btn--primary btn-round dropdown-toggle'
    } else {
      return 'btn btn--secondary btn-round dropdown-toggle'
    }
  }

  render () {
    const allTag = django.gettext('all')
    const onlyShowMarkedText = django.gettext('only show marked questions')
    const displayNotHiddenText = django.gettext('display only questions which are not hidden')
    const orderLikesText = django.gettext('order by likes')
    return (
      <div className="mb-4">
        <div className="justify-content-center form-inline">
          <div className="dropdown mt-3">
            <button
              className={this.getButtonClass()} type="button" id="dropdownMenuButton"
              data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
            >
              {this.props.currentCategoryName}
            </button>
            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <button className="dropdown-item" data-value={-1} onClick={this.selectCategory.bind(this)} href="#">{allTag}</button>
              {this.props.categories.map((category, index) => {
                return <button className="dropdown-item" key={index} data-value={category} onClick={this.selectCategory.bind(this)} href="#">{category}</button>
              })}
            </div>
          </div>
          {this.props.isModerator &&
            <div>
              <div className="checkbox-btn mt-3">
                <label htmlFor="markedCheck" className="checkbox-btn__label--primary pl-3">
                  <input
                    className="checkbox-btn__input"
                    type="checkbox"
                    id="markedCheck"
                    name="markedCheck"
                    checked={this.props.displayOnShortlist}
                    onChange={this.props.toggleDisplayOnShortlist} // eslint-disable-line react/jsx-handler-names
                  />
                  <span className="checkbox-btn__text">
                    <i className="icon-in-list" aria-label={onlyShowMarkedText} />
                  </span>
                </label>
              </div>
              <div className="checkbox-btn mt-3">
                <label htmlFor="displayNotHiddenOnly" className="checkbox-btn__label--primary pl-3">
                  <input
                    className="checkbox-btn__input"
                    type="checkbox"
                    id="displayNotHiddenOnly"
                    name="displayNotHiddenOnly"
                    checked={this.props.displayNotHiddenOnly}
                    onChange={this.props.toggledisplayNotHiddenOnly} // eslint-disable-line react/jsx-handler-names
                  />
                  <span className="checkbox-btn__text">
                    <i className="far fa-eye" aria-label={displayNotHiddenText} />
                  </span>
                </label>
              </div>
              <div className="checkbox-btn mt-3">
                <label htmlFor="orderedByLikes" className="checkbox-btn__label--primary">
                  <input
                    className="checkbox-btn__input"
                    type="checkbox"
                    id="orderedByLikes"
                    name="orderedByLikes"
                    checked={this.props.orderedByLikes}
                    onChange={this.props.toggleOrdering} // eslint-disable-line react/jsx-handler-names
                  />
                  <span className="checkbox-btn__text">
                    <i className="icon-like" aria-label={orderLikesText} /> likes
                  </span>
                </label>
              </div>
            </div>}
        </div>
      </div>
    )
  }
}
