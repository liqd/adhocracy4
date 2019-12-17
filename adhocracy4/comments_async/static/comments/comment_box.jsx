import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'
import update from 'immutability-helper'
import axios from 'axios'

import CommentForm from './comment_form'
import CommentList from './comment_list'
import { getDocumentHeight } from '../util'

const api = require('../../../static/api')

const sorts = {
  new: django.gettext('Newest'),
  pos: django.gettext('Most up votes'),
  neg: django.gettext('Most down votes'),
  ans: django.gettext('Most answers'),
  dis: django.gettext('Last discussed')
}

const autoScrollThreshold = 500

export default class CommentBox extends React.Component {
  constructor (props) {
    super(props)

    this.anchoredCommentFound = this.anchoredCommentFound.bind(this)
    this.handleClickResult = this.handleClickResult.bind(this)
    this.handleClickSearch = this.handleClickSearch.bind(this)
    this.handleClickSorted = this.handleClickSorted.bind(this)
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

    this.state = {
      comments: [],
      nextComments: null,
      commentCount: 0,
      showSearch: 0,
      displayForm: false,
      filter: 'all',
      filterDisplay: django.gettext('all'),
      sort: 'new',
      loading: true,
      search: '',
      anchoredCommentId: props.anchoredCommentId ? parseInt(props.anchoredCommentId) : null,
      anchoredCommentParentId: 0,
      anchoredCommentFound: false
    }
  }

  componentDidMount () {
    window.addEventListener('scroll', this.handleScroll)

    const params = {}
    if (this.state.anchoredCommentId) {
      params.commentID = this.state.anchoredCommentId
    }
    axios.get(this.props.commentsApiUrl, {
      params: params
    })
      .then(
        (result) => {
          const data = result.data

          if (this.state.anchoredCommentId && data.comment_found) {
            this.setState(
              {
                comments: data.results,
                nextComments: data.next,
                commentCount: data.count,
                showSearch: data.count,
                anchoredCommentParentId: data.comment_parent
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
                showSearch: data.count,
                loading: false
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
    var comments = this.state.comments
    var diff = {}
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
        var comments = this.state.comments
        var diff = {}
        if (typeof parentIndex !== 'undefined') {
          diff[parentIndex] = { child_comments: { $push: [comment] } }
        } else {
          diff = { $unshift: [comment] }
        }
        this.setState({
          comments: update(comments, diff),
          commentCount: (this.state.commentCount + 1),
          showSearch: (this.state.showSearch + 1)
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
        var errorMessage = xhr.responseJSON.comment[0]
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
    var comments = this.state.comments
    var comment = comments[index]
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
        var errorMessage = xhr.responseJSON.comment[0]
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
    var comments = this.state.comments
    var comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    var data = {
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
        var errorMessage = Object.values(xhr.responseJSON)[0]
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

  getChildContext () {
    return {
      isAuthenticated: this.props.isAuthenticated,
      isModerator: this.props.isModerator,
      comments_contenttype: this.props.comments_contenttype,
      user_name: this.props.user_name
    }
  }

  handleClickSearch (e) {
    var search = e.target.parentElement.firstChild.value
    this.fetchSearch(search)
    this.setState({
      loadingFilter: true
    })
  }

  handleEnterSearch (e) {
    var search = e.target.parentElement.firstChild.value
    if (e.key === 'Enter') {
      this.fetchSearch(search)
      this.setState({
        loadingFilter: true
      })
    }
  }

  handleClickResult (e) {
    var result = ''
    this.fetchSearch(result)
    document.getElementById('search-input').value = ''
    this.setState({
      loadingFilter: true
    })
  }

  handleClickSorted (e) {
    e.preventDefault()
    var order = e.target.id
    this.fetchSorted(order)
    this.setState({
      loadingFilter: true
    })
  }

  fetchSorted (order) {
    var commentCategory = this.state.filter
    if (commentCategory === 'all') {
      commentCategory = ''
    }
    axios.get(this.props.commentsApiUrl, {
      params: {
        ordering: order,
        comment_category: commentCategory,
        search: this.state.search
      }
    })
      .then(
        (result) => {
          var data = result.data
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

  fetchSearch (search) {
    var commentCategory = this.state.filter
    if (commentCategory === 'all') {
      commentCategory = ''
    }
    axios.get(this.props.commentsApiUrl, {
      params: {
        search: search,
        ordering: this.state.sort,
        comment_category: commentCategory
      }
    })
      .then(
        (result) => {
          var data = result.data
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

  anchoredCommentFound () {
    if (this.state.anchoredCommentId && !this.state.anchoredCommentFound) {
      let found = false

      this.state.comments.map((comment) => {
        if (comment.id === this.state.anchoredCommentId ||
            comment.id === this.state.anchoredCommentParentId) {
          found = true
        }
      })
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
    axios.get(this.state.nextComments, {
      params: {}
    })
      .then(
        (result) => {
          var data = result.data
          var newCommentList = this.state.comments.concat(data.results)
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

  render () {
    return (
      <div>
        <div className="a4-comments__box">
          <div className="container">
            <CommentForm
              subjectType={this.props.subjectType} subjectId={this.props.subjectId}
              onCommentSubmit={this.handleCommentSubmit}
              placeholder={django.gettext('Write contribution')}
              rows="5" isReadOnly={this.props.isReadOnly} error={this.state.error}
              errorMessage={this.state.errorMessage} handleErrorClick={this.hideNewError}
              commentCategoryChoices={this.props.commentCategoryChoices}
            />
          </div>
          <div className={(this.state.comments.length === 0 && this.state.loading) ? 'd-none' : 'a4-a4-comments__nav_parent'}>
            <nav className={this.state.showSearch === 0 ? 'd-none' : 'bg-faded a4-comments__nav'}>
              <div className="container">
                <div className="row px-sm-3">
                  <div className={this.state.search !== '' ? 'a4-comments__nav__text a4-comments__nav__text--wide' : 'd-none'}>
                    <span className="a4-comments__nav__span">{this.state.commentCount + ' ' + django.ngettext('entry found for ', 'entries found for ', this.state.commentCount)}</span>

                    <button className="btn btn--small a4-comments__nav__search-result" type="button" onClick={this.handleClickResult}>{this.state.search}<i className="fas fa-times" aria-label={django.gettext('Clear search')} /></button>
                  </div>

                  <div className={this.state.search === '' ? 'a4-comments__nav__text a4-comments__nav__text--wide' : 'd-none'}>
                    {this.state.commentCount + ' ' + django.ngettext('entry', 'entries', this.state.commentCount)}
                  </div>

                  <div className="input-group a4-comments__nav__search">
                    <input type="search" id="search-input" onKeyPress={this.handleEnterSearch} placeholder={django.gettext('SEARCH CONTRIBUTIONS')} className="a4-comments__nav__search-input mb-0" />
                    <button className="a4-comments__nav__search-btn btn" type="button" onClick={this.handleClickSearch}><i className="fas fa-search a4-comments__nav__search-icon" aria-label={django.gettext('Search contributions')} /></button>
                  </div>

                  <div className="a4-comments__nav__dropdown">
                    <div className="dropdown">
                      <button
                        className="btn dropdown-toggle a4-comments__nav__btn" type="button"
                        id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                      >
                        <span className={this.state.sort === 'new' ? 'a4-comments__nav__btn-text btn--upper' : 'd-none'}>{django.gettext('sorted by: ')}{sorts[this.state.sort]}</span>
                        <span className={this.state.sort !== 'new' ? 'a4-comments__nav__btn-text small-screen btn--capitalize' : 'd-none'}>{sorts[this.state.sort]}</span>
                        <i className={this.state.sort === 'new' ? 'icon-arrow_dropdown a4-comments__nav__btn-icon' : 'fas fa-checka4-comments__nav__btn-icon'} aria-hidden="true" />
                      </button>
                      <div className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
                        {Object.keys(sorts).map(objectKey => {
                          var name = sorts[objectKey]
                          if (objectKey !== this.state.sort) {
                            return (
                              <button
                                className="dropdown-item" onClick={this.handleClickSorted} id={objectKey}
                                key={objectKey} href="#"
                              >{name}
                              </button>
                            )
                          }
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </nav>
            <div className={this.state.loadingFilter ? 'row justify-content-center loading loading-nav' : 'd-none'}>
              <i className="fa fa-spinner fa-pulse" />
            </div>
          </div>
          <div className="a4-comments__list">
            <CommentList
              comments={this.state.comments}
              anchoredCommentId={this.state.anchoredCommentId}
              anchoredCommentParentId={this.state.anchoredCommentParentId}
              onCommentDelete={this.handleCommentDelete}
              onCommentSubmit={this.handleCommentSubmit}
              onCommentModify={this.handleCommentModify}
              isReadOnly={this.props.isReadOnly}
              onReplyErrorClick={this.handleHideReplyError}
              onEditErrorClick={this.handleHideEditError}
            />
          </div>
          <div className={this.state.loading ? 'row justify-content-center loading' : 'd-none'}>
            <i className="fa fa-spinner fa-pulse" />
          </div>
        </div>
      </div>
    )
  }
}

CommentBox.childContextTypes = {
  isAuthenticated: PropTypes.bool,
  isModerator: PropTypes.bool,
  comments_contenttype: PropTypes.number,
  user_name: PropTypes.string
}
