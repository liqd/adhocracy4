/* global django */
const React = require('react')

class FilterAccordeon extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      selected: false
    }
  }

  unselect (e) {
    this.props.onSelect(e)
    this.setState({
      selected: false
    })
  }

  select (e) {
    this.props.onSelect(e)
    this.setState({
      selected: true
    })
  }

  render () {
    return (
      <div className="">
        { this.state.selected
          ? <a id={'accordion-' + this.props.identifier + '-title'}
            href={'#accordion-' + this.props.identifier + '-body'}
            className="collapsed btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
            aria-haspopup="true" aria-expanded="false" data-toggle="collapse">
            {this.props.title}
            <i className="fa fa-times" aria-hidden="true" />
          </a>
          : <a id={'accordion-' + this.props.identifier + '-title'}
            href={'#accordion-' + this.props.identifier + '-body'}
            className="collapsed btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--unselected"
            aria-haspopup="true" aria-expanded="false" data-toggle="collapse">
            {this.props.titlePrefix}: {this.props.title}
            <i className="fa fa-chevron-down" aria-hidden="true" />
          </a>
        }
        <div className="accordion__body collapse"
          id={'accordion-' + this.props.identifier + '-body'}
          aria-labelledby={'accordion-' + this.props.identifier + '-title'}>
          <h1 className="u-spacer-left u-spacer-right">{this.props.question}</h1>
          <ul>
            <li>
              <button
                type="button"
                value="-1"
                onClick={this.unselect.bind(this)}>
                {django.gettext('all')}
              </button>
            </li>
            {
              Object.keys(this.props.options).map((key, i) => {
                return (
                  <li key={key}>
                    <button
                      type="button"
                      value={key}
                      onClick={this.select.bind(this)}>
                      {this.props.options[key]}
                    </button>
                  </li>
                )
              })
            }
          </ul>
        </div>
      </div>
    )
  }
}

module.exports = FilterAccordeon
