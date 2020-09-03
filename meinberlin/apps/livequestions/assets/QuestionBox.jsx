import django from 'django'
import { updateItem } from './helpers.js'
import React from 'react'
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
      categoryName: django.gettext('select category'),
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
    const newName = (category === '-1') ? django.gettext('select category') : category
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
          <div className="container">
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
          className="tabpanel tabpanel--bg-secondary"
          id="tabpanel-information"
          role="tabpanel"
          aria-labelledby="tab-information"
          aria-hidden="false"
        >
          <div className="container">
            <div className="col-md-10 col-lg-8 offset-md-1 offset-lg-2">
              {this.props.information}
            </div>
          </div>
        </div>

        <div
          className="tabpanel tabpanel--bg-secondary active"
          id="tabpanel-questions"
          role="tabpanel"
          aria-labelledby="tab-questions"
          aria-hidden="true"
        >
          <div className="container">
            <div className="row mb-5">
              <div className="col-12">
                {this.props.isModerator &&
                  <div className="d-flex justify-content-center justify-content-lg-end">
                    <a className="btn btn--secondary" rel="noopener noreferrer" href={this.props.present_url} target="_blank">
                      <span className="fa-stack fa-1x">
                        <i className="fas fa-tv fa-stack-2x" aria-label="hidden"> </i>
                        <i className="fas fa-arrow-up fa-stack-1x" aria-label="hidden"> </i>
                      </span>
                      {django.gettext('display on screen')}
                    </a>
                  </div>}
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
                <InfoBox
                  isModerator={this.props.isModerator}
                />
                <QuestionList
                  questions={this.state.filteredQuestions}
                  removeFromList={this.removeFromList.bind(this)}
                  updateQuestion={this.updateQuestion.bind(this)}
                  handleLike={this.handleLike.bind(this)}
                  isModerator={this.props.isModerator}
                  togglePollingPaused={this.togglePollingPaused.bind(this)}
                  hasLikingPermission={this.props.hasLikingPermission}
                />
                {this.props.hasAskQuestionsPermission &&
                  <a
                    href={this.props.askQuestionUrl}
                    className="btn btn--primary btn--full btn--huge question-list-button mb-4"
                    id="question-create"
                  >
                    <i className="fa fa-plus question-list-button-icon" aria-hidden="true" />
                    {django.gettext('Add Question')}
                  </a>}
              </div>
            </div>
          </div>
        </div>
        <div
          className="tabpanel tabpanel--bg-secondary"
          id="tabpanel-statistics"
          role="tabpanel"
          aria-labelledby="tab-statistics"
          aria-hidden="false"
        >
          <div className="container">
            <div className="col-md-10 col-lg-8 offset-md-1 offset-lg-2">
              <StatisticsBox
                answeredQuestions={this.state.answeredQuestions}
                questions_api_url={this.props.questions_api_url}
                categories={this.props.categories}
                isModerator={this.props.isModerator}
              />
            </div>
          </div>
        </div>
      </div>
    )
  }
}
