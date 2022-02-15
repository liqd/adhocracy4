import React from 'react'
import django from 'django'
import update from 'immutability-helper'

import CommentForm from './comment_form'
import CommentList from './comment_list'
import { FilterCategory } from './filter_category'
import { FilterSearch } from './filter_search'
import { FilterSort } from './filter_sort'
import { getDocumentHeight } from '../util'

const api = require('../../../static/api')

const sorts = {
  new: django.gettext('Newest'),
  pos: django.gettext('Most up votes'),
  neg: django.gettext('Most down votes'),
  ans: django.gettext('Most answers'),
  dis: django.gettext('Last discussed')
}

const translated = {
  showFilters: django.gettext('Show filters'),
  filters: django.gettext('Filters'),
  hideFilters: django.gettext('Hide filters'),
  searchContrib: django.gettext('Search contributions'),
  clearSearch: django.gettext('Clear search'),
  display: django.gettext('display: '),
  all: django.gettext('all'),
  sortedBy: django.gettext('sorted by: ')
}

const autoScrollThreshold = 500

export default class CommentBox extends React.Component {
  constructor (props) {
    super(props)

    this.anchoredCommentFound = this.anchoredCommentFound.bind(this)
    this.handleClickFilter = this.handleClickFilter.bind(this)
    this.handleClickResult = this.handleClickResult.bind(this)
    this.handleClickSorted = this.handleClickSorted.bind(this)
    this.handleClickSearch = this.handleClickSearch.bind(this)
    this.handleEnterSearch = this.handleEnterSearch.bind(this)
    this.fetchComments = this.fetchComments.bind(this)
    this.handleCommentDelete = this.handleCommentDelete.bind(this)
    this.handleCommentModify = this.handleCommentModify.bind(this)
    this.handleCommentSubmit = this.handleCommentSubmit.bind(this)
    this.handleScroll = this.handleScroll.bind(this)
    this.handleHideEditError = this.handleHideEditError.bind(this)
    this.hideNewError = this.hideNewError.bind(this)
    this.handleHideReplyError = this.handleHideReplyError.bind(this)
    this.updateStateComment = this.updateStateComment.bind(this)
    this.handleToggleFilters = this.handleToggleFilters.bind(this)
    this.urlReplaces = {
      objectPk: this.props.subjectId,
      contentTypeId: this.props.subjectType
    }

    this.state = {
      comments: [],
      nextComments: null,
      commentCount: 0,
      showFilters: false,
      filter: 'all',
      filterDisplay: django.gettext('all'),
      sort: 'new',
      loading: true,
      search: '',
      anchoredCommentId: props.anchoredCommentId ? parseInt(props.anchoredCommentId) : null,
      anchoredCommentParentId: 0,
      anchoredCommentFound: false,
      hasCommentingPermission: false,
      wouldHaveCommentingPermission: false
    }
  }

  componentDidMount () {
    window.addEventListener('scroll', this.handleScroll, { passive: true })
    const params = {}
    params.ordering = this.state.sort
    params.urlReplaces = this.urlReplaces
    if (this.state.anchoredCommentId) {
      params.commentID = this.state.anchoredCommentId
    }
    api.comments.get(params)
      .done(
        (result) => {
          const data = result

          translated.entries =
            django.ngettext('entry', 'entries', data.count)

          translated.entriesFound =
            django.ngettext('entry found for ', 'entries found for ', data.count)

          if (this.state.anchoredCommentId && data.comment_found) {
            this.setState(
              {
                comments: data.results,
                nextComments: data.next,
                commentCount: data.count,
                anchoredCommentParentId: data.comment_parent,
                hasCommentingPermission: data.has_commenting_permission,
                wouldHaveCommentingPermission: data.would_have_commenting_permission
              }
            )
            if (this.anchoredCommentFound()) {
              this.setState(
                {
                  loading: false
                }
              )
            } else {
              this.fetchComments()
            }
          } else {
            if (this.state.anchoredCommentId) {
              /* display something like: django.gettext('We are sorry, this comment does not exist.')
               * probably using a modal
               */
            }
            this.setState(
              {
                comments: data.results,
                nextComments: data.next,
                commentCount: data.count,
                loading: false,
                hasCommentingPermission: data.has_commenting_permission,
                wouldHaveCommentingPermission: data.would_have_commenting_permission
              }
            )
          }
        }
      )
  }

  componentWillUnmount () {
    window.removeEventListener('scroll', this.handleScroll)
  }

  updateStateComment (index, parentIndex, updatedComment) {
    let comments = this.state.comments
    const diff = {}
    if (typeof parentIndex !== 'undefined') {
      diff[parentIndex] = { child_comments: {} }
      diff[parentIndex].child_comments[index] = { $merge: updatedComment }
    } else {
      diff[index] = { $merge: updatedComment }
    }
    comments = update(comments, diff)
    this.setState({ comments: comments })
  }

  handleCommentSubmit (comment, parentIndex) {
    return api.comments.add(comment)
      .done(comment => {
        comment.displayNotification = true
        const comments = this.state.comments
        let diff = {}
        let commentCount = this.state.commentCount
        if (typeof parentIndex !== 'undefined') {
          diff[parentIndex] = { child_comments: { $push: [comment] } }
        } else {
          diff = { $unshift: [comment] }
          commentCount++
        }
        this.setState({
          comments: update(comments, diff),
          commentCount: commentCount
        })
        if (typeof parentIndex !== 'undefined') {
          this.updateStateComment(
            parentIndex,
            undefined,
            {
              replyError: false,
              errorMessage: undefined
            })
        } else {
          this.setState({
            error: false,
            errorMessage: undefined
          })
        }
      })
      .fail((xhr, status, err) => {
        const errorMessage = (Object.values(xhr.responseJSON))[0]
        if (typeof parentIndex !== 'undefined') {
          this.updateStateComment(
            parentIndex,
            undefined, {
              replyError: true,
              errorMessage: errorMessage
            })
        } else {
          this.setState({
            error: true,
            errorMessage: errorMessage
          })
        }
      })
  }

  handleCommentModify (modifiedComment, index, parentIndex) {
    const comments = this.state.comments
    let comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    return api.comments.change(modifiedComment, comment.id)
      .done(changed => {
        this.updateStateComment(
          index,
          parentIndex,
          changed)
        this.updateStateComment(
          index,
          parentIndex, {
            editError: false,
            errorMessage: undefined
          }
        )
      })
      .fail((xhr, status, err) => {
        const errorMessage = Object.values(xhr.responseJSON)[0]
        this.updateStateComment(
          index,
          parentIndex,
          {
            editError: true,
            errorMessage: errorMessage
          })
      })
  }

  handleCommentDelete (index, parentIndex) {
    const comments = this.state.comments
    let comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    const data = {
      urlReplaces: {
        contentTypeId: comment.content_type,
        objectPk: comment.object_pk
      }
    }
    return api.comments.delete(data, comment.id)
      .done(changed => {
        this.updateStateComment(
          index,
          parentIndex,
          changed)
        this.updateStateComment(
          index,
          parentIndex,
          {
            editError: false,
            errorMessage: undefined
          })
      })
      .fail((xhr, status, err) => {
        const errorMessage = Object.values(xhr.responseJSON)[0]
        this.updateStateComment(
          index,
          parentIndex,
          {
            editError: true,
            errorMessage: errorMessage
          })
      })
  }

  hideNewError () {
    this.setState({
      error: false,
      errorMessage: undefined
    })
  }

  handleHideReplyError (index, parentIndex) {
    this.updateStateComment(
      index,
      parentIndex,
      {
        replyError: false,
        errorMessage: undefined
      }
    )
  }

  handleHideEditError (index, parentIndex) {
    this.updateStateComment(
      index,
      parentIndex,
      {
        editError: false,
        errorMessage: undefined
      }
    )
  }

  handleToggleFilters (e) {
    e.preventDefault()
    this.setState(s => ({ showFilters: !s.showFilters }))
  }

  handleClickFilter (e) {
    e.preventDefault()
    const filter = e.target.id
    this.fetchFiltered(filter)
    this.setState({
      loadingFilter: true
    })
  }

  fetchFiltered (filter) {
    let commentCategory = filter
    let displayFilter = this.props.commentCategoryChoices[filter]
    if (filter === 'all') {
      displayFilter = django.gettext('all')
      commentCategory = ''
    }
    const params = {
      comment_category: commentCategory,
      ordering: this.state.sort,
      search: this.state.search,
      urlReplaces: this.urlReplaces
    }
    api.comments.get(params)
      .done(
        (result) => {
          const data = result
          this.setState({
            comments: data.results,
            nextComments: data.next,
            commentCount: data.count,
            filter: filter,
            filterDisplay: displayFilter,
            loadingFilter: false
          })
        }
      )
  }

  handleClickSorted (e) {
    e.preventDefault()
    const order = e.target.id
    this.fetchSorted(order)
    this.setState({
      loadingFilter: true
    })
  }

  fetchSorted (order) {
    let commentCategory = this.state.filter
    if (commentCategory === 'all') {
      commentCategory = ''
    }
    const params = {
      ordering: order,
      comment_category: commentCategory,
      search: this.state.search,
      urlReplaces: this.urlReplaces
    }
    api.comments.get(params)
      .done(
        (result) => {
          const data = result
          this.setState({
            comments: data.results,
            nextComments: data.next,
            commentCount: data.count,
            sort: order,
            loadingFilter: false
          })
        }
      )
  }

  handleClickSearch (e) {
    e.preventDefault()
    const search = e.currentTarget.parentElement.firstChild.value
    this.fetchSearch(search)
    this.setState({
      loadingFilter: true
    })
  }

  handleEnterSearch (e) {
    const search = e.currentTarget.value
    if (e.key === 'Enter') {
      this.fetchSearch(search)
      this.setState({
        loadingFilter: true
      })
    }
  }

  fetchSearch (search) {
    let commentCategory = this.state.filter
    if (commentCategory === 'all') {
      commentCategory = ''
    }
    const params = {
      search: search,
      ordering: this.state.sort,
      comment_category: commentCategory,
      urlReplaces: this.urlReplaces
    }
    api.comments.get(params)
      .done(
        (result) => {
          const data = result
          this.setState({
            comments: data.results,
            nextComments: data.next,
            commentCount: data.count,
            search: search,
            loadingFilter: false
          })
        }
      )
  }

  handleClickResult (e) {
    const result = ''
    this.fetchSearch(result)
    document.getElementById('search-input').value = ''
    this.setState({
      loadingFilter: true
    })
  }

  anchoredCommentFound () {
    if (this.state.anchoredCommentId && !this.state.anchoredCommentFound) {
      let found = false

      this.state.comments.map((comment) => (
        (comment.id === this.state.anchoredCommentId || comment.id === this.state.anchoredCommentParentId) && (
          found = true
        )
      ))

      if (found) {
        this.setState(
          {
            anchoredCommentFound: true
          }
        )

        const top = document.getElementById('comment_' + this.state.anchoredCommentId).getBoundingClientRect().top
        window.scrollTo(0, top)
      }
      return found
    }
    return true
  }

  fetchComments () {
    fetch(this.state.nextComments)
      .then(response => response.json())
      .then(data => {
        const newCommentList = this.state.comments.concat(data.results)
        this.setState({
          comments: newCommentList,
          nextComments: data.next,
          commentCount: data.count
        })
        if (this.anchoredCommentFound()) {
          this.setState(
            {
              loading: false
            }
          )
        } else {
          this.fetchComments()
        }
      }
      )
  }

  handleScroll () {
    const html = document.documentElement
    if (html.scrollTop + html.clientHeight > getDocumentHeight() - autoScrollThreshold) {
      if (this.state.nextComments && !this.state.loading) {
        this.setState(
          {
            loading: true
          }
        )
        this.fetchComments()
      }
    }
  }

  commentCategoryChoices () {
    if (this.props.withCategories === true) {
      return this.props.commentCategoryChoices
    }
  }

  render () {
    return (
      <div>
        <div className="a4-comments__commentbox__form">
          <CommentForm
            subjectType={this.props.subjectType}
            subjectId={this.props.subjectId}
            onCommentSubmit={this.handleCommentSubmit}
            rows="5"
            error={this.state.error}
            errorMessage={this.state.errorMessage}
            handleErrorClick={this.hideNewError}
            commentCategoryChoices={this.commentCategoryChoices()}
            withCategories={this.props.withCategories}
            isContextMember={this.props.isContextMember}
            hasCommentingPermission={this.state.hasCommentingPermission}
            wouldHaveCommentingPermission={this.state.wouldHaveCommentingPermission}
          />
        </div>

        <div className={(this.state.comments.length === 0 && this.state.loading) ? 'd-none' : 'a4-comments__filters__parent'}>
          <div className="a4-comments__filters__parent--closed">
            <div className={this.state.search === '' ? 'a4-comments__filters__text' : 'd-none'}>
              {this.state.commentCount + ' ' + translated.entries}
            </div>

            <div className={this.state.search !== '' ? 'a4-comments__filters__text' : 'd-none'}>
              <span className="a4-comments__filters__span">{this.state.commentCount + ' ' + translated.entriesFound}{this.state.search}</span>
            </div>

            {!this.state.showFilters && this.state.commentCount > 0 &&
              <button className="btn a4-comments__filters__show-btn pe-0" type="button" onClick={this.handleToggleFilters}>
                <i className="fas fa-sliders-h ms-2" aria-label={translated.showFilters} />
                {translated.filters}
              </button>}
            {this.state.showFilters && this.state.commentCount > 0 &&
              <button className="btn a4-comments__filters__show-btn pe-0" type="button" onClick={this.handleToggleFilters}>
                <i className="fas fa-times ms-2" aria-label={translated.hideFilters} />
                {translated.hideFilters}
              </button>}
          </div>

          {this.state.showFilters &&
            <div className="a4-comments__filters">
              <FilterSearch
                search={this.state.search}
                translated={translated}
                onEnterSearch={this.handleEnterSearch}
                onClickSearch={this.handleClickSearch}
                onClickResult={this.handleClickResult}
              />
              {this.props.withCategories
                ? <FilterCategory
                    translated={translated}
                    filter={this.state.filter}
                    filterDisplay={this.state.filterDisplay}
                    onClickFilter={this.handleClickFilter}
                    commentCategoryChoices={this.props.commentCategoryChoices}
                  />
                : <div className="col-lg-3" />}
              <FilterSort
                translated={translated}
                sort={this.state.sort}
                sorts={sorts}
                onClickSorted={this.handleClickSorted}
              />
            </div>}

          <div className={this.state.loadingFilter ? 'a4-comments__loading' : 'd-none'}>
            <i className="fa fa-spinner fa-pulse" />
          </div>

        </div>

        <div className="a4-comments__box">
          <div className="a4-comments__list">
            <CommentList
              comments={this.state.comments}
              anchoredCommentId={this.state.anchoredCommentId}
              anchoredCommentParentId={this.state.anchoredCommentParentId}
              onCommentDelete={this.handleCommentDelete}
              onCommentSubmit={this.handleCommentSubmit}
              onCommentModify={this.handleCommentModify}
              isContextMember={this.props.isContextMember}
              commentCategoryChoices={this.commentCategoryChoices()}
              onReplyErrorClick={this.handleHideReplyError}
              onEditErrorClick={this.handleHideEditError}
              withCategories={this.props.withCategories}
              hasCommentingPermission={this.state.hasCommentingPermission}
              wouldHaveCommentingPermission={this.state.wouldHaveCommentingPermission}
            />
          </div>
        </div>
        <div className={this.state.loading ? 'a4-comments__loading' : 'd-none'}>
          <i className="fa fa-spinner fa-pulse" />
        </div>
      </div>
    )
  }
}
