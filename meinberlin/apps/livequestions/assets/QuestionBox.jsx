import django from 'django'
import { updateItem } from './helpers.js'
import React from 'react'
import QuestionForm from './QuestionForm'
import QuestionList from './QuestionList'
import InfoBox from './InfoBox'
import Filters from './Filters'
import StatisticsBox from './StatisticsBox'

export default class QuestionBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      questions: [],
      filteredQuestions: [],
      answeredQuestions: [],
      category: '-1',
      categoryName: django.gettext('select affiliation'),
      displayNotHiddenOnly: false,
      displayOnShortlist: false,
      orderedByLikes: false,
      filterChanged: false,
      orderingChanged: false,
      pollingPaused: false
    }
  }

  componentDidMount () {
    this.getItems()
    this.timer = setInterval(() => this.getItems(), 5000)
  }

  componentWillUnmount () {
    this.timer = null
  }

  componentDidUpdate () {
    if (this.state.filterChanged === true) {
      this.updateList()
    }
    if (this.state.orderingChanged === true) {
      this.getItems()
    }
  }

  setCategory (category) {
    const newName = (category === '-1') ? django.gettext('select affiliation') : category
    this.setState({
      filterChanged: true,
      categoryName: newName,
      category: category
    })
  }

  toggledisplayNotHiddenOnly () {
    const displayNotHiddenOnly = !this.state.displayNotHiddenOnly
    this.setState({
      filterChanged: true,
      displayNotHiddenOnly: displayNotHiddenOnly
    })
  }

  toggleDisplayOnShortlist () {
    const displayOnShortlist = !this.state.displayOnShortlist
    this.setState({
      filterChanged: true,
      displayOnShortlist: displayOnShortlist
    })
  }

  toggleOrdering () {
    const orderedByLikes = !this.state.orderedByLikes
    this.setState({
      orderingChanged: true,
      orderedByLikes: orderedByLikes
    })
  }

  isInFilter (item) {
    return (this.state.category === '-1' || this.state.category === item.category) &&
      (!this.state.displayOnShortlist || item.is_on_shortlist) && (!this.state.displayNotHiddenOnly || !item.is_hidden)
  }

  filterQuestions (questions) {
    const filteredQuestions = []
    questions.forEach((item) => {
      if (this.isInFilter(item) && !item.is_answered) {
        filteredQuestions.push(item)
      }
    })
    return filteredQuestions
  }

  getAnsweredQuestions (questions) {
    const answeredQuestions = []
    questions.forEach((item) => {
      if (item.is_answered) {
        answeredQuestions.push(item)
      }
    })
    return answeredQuestions
  }

  updateList () {
    const filteredQuestions = this.filterQuestions(this.state.questions)
    this.setState({
      filterChanged: false,
      filteredQuestions: filteredQuestions
    })
  }

  getUrl () {
    const url = this.props.questions_api_url
    if (this.state.orderedByLikes) {
      return url + '?ordering=-like_count'
    }
    return url
  }

  getItems () {
    if (!this.state.pollingPaused) {
      fetch(this.getUrl())
        .then(response => response.json())
        .then(data => this.setState({
          questions: data,
          filteredQuestions: this.filterQuestions(data),
          answeredQuestions: this.getAnsweredQuestions(data),
          orderingChanged: false
        }))
    }
  }

  updateQuestion (data, id) {
    this.setState({
      pollingPaused: true
    })
    const url = this.props.questions_api_url + id + '/'
    return updateItem(data, url, 'PATCH')
  }

  removeFromList (id, data) {
    this.updateQuestion(data, id)
      .then(response => this.setState(prevState => ({
        filteredQuestions: prevState.filteredQuestions.filter(question => question.id !== id),
        pollingPaused: false
      })))
  }

  handleLike (id, value) {
    const url = '/api/questions/' + id + '/likes/'
    const data = { value: value }
    return updateItem(data, url, 'POST')
  }

  togglePollingPaused () {
    const pollingPaused = !this.state.pollingPaused
    this.setState({
      pollingPaused: pollingPaused
    })
  }

  render () {
    return (
      <div>
        <div className="tablist tablist--bg-secondary mb-0">
          <div className="l-wrapper">
            <nav className="nav justify-content-center">
              <a
                id="tab-information"
                className="tab tab--bg-secondary"
                data-toggle="tab"
                href="#tabpanel-information"
                role="tab"
                aria-controls="tabpanel-information"
                aria-expanded="false"
              >
                {django.gettext('Information')}
              </a>
              <a
                id="tab-questions"
                className="tab tab--bg-secondary active"
                data-toggle="tab"
                href="#tabpanel-questions"
                role="tab"
                aria-controls="tabpanel-questions"
                aria-expanded="true"
              >
                {django.gettext('Questions')}
              </a>
              <a
                id="tab-statistics"
                className="tab tab--bg-secondary"
                data-toggle="tab"
                href="#tabpanel-statistics"
                role="tab"
                aria-controls="tabpanel-statistics"
                aria-expanded="false"
              >
                {django.gettext('Statistics')}
              </a>
            </nav>
          </div>
        </div>
        <div
          className="tabpanel"
          id="tabpanel-information"
          role="tabpanel"
          aria-labelledby="tab-information"
          aria-hidden="false"
        >
          <div className="l-wrapper">
            <div className="l-center-8">
              {this.props.information}
            </div>
          </div>
        </div>

        <div
          className="tabpanel active"
          id="tabpanel-questions"
          role="tabpanel"
          aria-labelledby="tab-questions"
          aria-hidden="true"
        >
          {this.props.hasAskQuestionsPermission &&
            <div className="l-wrapper">
              <div className="l-center-8">
                <QuestionForm
                  category_dict={this.props.category_dict}
                  questions_api_url={this.props.questions_api_url}
                  privatePolicyLabel={this.props.privatePolicyLabel}
                />
              </div>
            </div>}
          <div>
            <div className="l-wrapper">
              <div className="l-center-8">
                <InfoBox
                  isModerator={this.props.isModerator}
                />
                <div className="control-bar__top-overlap live_questions__filters--parent">
                  <Filters
                    categories={this.props.categories}
                    currentCategory={this.state.category}
                    currentCategoryName={this.state.categoryName}
                    setCategories={this.setCategory.bind(this)}
                    orderedByLikes={this.state.orderedByLikes}
                    toggleOrdering={this.toggleOrdering.bind(this)}
                    displayOnShortlist={this.state.displayOnShortlist}
                    displayNotHiddenOnly={this.state.displayNotHiddenOnly}
                    toggleDisplayOnShortlist={this.toggleDisplayOnShortlist.bind(this)}
                    toggledisplayNotHiddenOnly={this.toggledisplayNotHiddenOnly.bind(this)}
                    isModerator={this.props.isModerator}
                  />
                  {this.props.isModerator &&
                    <div>
                      <a className="btn btn--light live_questions__filters--screen-btn" rel="noopener noreferrer" href={this.props.present_url} target="_blank">
                        <span className="fa-stack fa-1x">
                          <i className="fas fa-tv fa-stack-2x" aria-label="hidden"> </i>
                          <i className="fas fa-arrow-up fa-stack-1x" aria-label="hidden"> </i>
                        </span>
                        {django.gettext('display on screen')}
                      </a>
                    </div>}
                </div>
              </div>
            </div>
            <div className="module-content u-spacer-bottom">
              <div className="l-wrapper">
                <div className="l-center-8">
                  <QuestionList
                    questions={this.state.filteredQuestions}
                    removeFromList={this.removeFromList.bind(this)}
                    updateQuestion={this.updateQuestion.bind(this)}
                    handleLike={this.handleLike.bind(this)}
                    isModerator={this.props.isModerator}
                    togglePollingPaused={this.togglePollingPaused.bind(this)}
                    hasLikingPermission={this.props.hasLikingPermission}
                  />
                </div>
              </div>
            </div>
            <span id="question-list-end" />
          </div>
        </div>
        <div
          className="tabpanel module-content"
          id="tabpanel-statistics"
          role="tabpanel"
          aria-labelledby="tab-statistics"
          aria-hidden="false"
        >
          <StatisticsBox
            answeredQuestions={this.state.answeredQuestions}
            questions_api_url={this.props.questions_api_url}
            categories={this.props.categories}
            isModerator={this.props.isModerator}
          />
        </div>
      </div>
    )
  }
}
