import React, { useEffect, useState } from 'react'
import django from 'django'
import update, { type Spec } from 'immutability-helper'

import CommentForm from './comment_form'
import CommentList from './comment_list'
import { CommentControlBar } from './comment_control_bar'
import { CommentFilters } from './comment_filters'
import { getDocumentHeight } from '../util'

import api from '../../../static/api'
import type { Comment, CommentListResponse, CommentPayload, CommentQueryParams } from '../../../static/api/types'

const sorts: Record<string, string> = {
  new: django.gettext('Newest'),
  pos: django.gettext('Most up votes'),
  neg: django.gettext('Most down votes'),
  ans: django.gettext('Most answers'),
  dis: django.gettext('Last discussed')
}

const translated = {
  discussion: django.gettext('Discussion')
}

const autoScrollThreshold = 500

interface CommentBoxProps {
  subjectId: number
  subjectType: number
  id?: number | string
  anchoredCommentId?: string
  useModeratorMarked?: boolean
  withCategories?: boolean
  noControlBar?: boolean
}

export const CommentBox = (props: CommentBoxProps) => {
  const urlReplaces = {
    objectPk: props.subjectId,
    contentTypeId: props.subjectType
  }
  const anchoredCommentId = props.anchoredCommentId
    ? parseInt(props.anchoredCommentId)
    : null
  const [comments, setComments] = useState<Comment[]>([])
  const [nextComments, setNextComments] = useState<string | null>(null)
  const [commentCount, setCommentCount] = useState(0)
  const [showFilters, setShowFilters] = useState(false)
  const [filter, setFilter] = useState('')
  const [filterDisplay, setFilterDisplay] = useState(django.gettext('all'))
  const [sort, setSort] = useState(props.useModeratorMarked ? 'mom' : 'new')
  const [loading, setLoading] = useState(true)
  const [loadingFilter, setLoadingFilter] = useState(false)
  const [search, setSearch] = useState('')
  const [anchoredCommentParentId, setAnchoredCommentParentId] = useState(0)
  const [anchoredCommentFound, setAnchoredCommentFound] = useState(false)
  const [hasCommentingPermission, setHasCommentingPermission] = useState(false)
  const [wouldHaveCommentingPermission, setWouldHaveCommentingPermission] =
    useState(false)
  const [projectIsPublic, setProjectIsPublic] = useState(false)
  const [useTermsOfUse, setUseTermsOfUse] = useState(false)
  const [agreedTermsOfUse, setAgreedTermsOfUse] = useState(false)
  const [orgTermsUrl, setOrgTermsUrl] = useState('')
  const [error, setError] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | undefined>(undefined)
  const [anchorRendered, setAnchorRendered] = useState(false)
  const [categoryChoices, setCategoryChoices] = useState<Record<string, string>>({})
  const noControlBar = props.noControlBar || false

  useEffect(() => {
    if (props.useModeratorMarked) {
      sorts.mom = django.gettext('Highlighted')
    }
    const params: CommentQueryParams = {}
    params.ordering = sort
    params.urlReplaces = urlReplaces
    if (props.anchoredCommentId) {
      params.commentID = props.anchoredCommentId
    }
    if (props.withCategories) {
      params.categories = true
    }
    api.comments.get(params).done(handleComments).fail(() => {
      setLoading(false)
      setError(true)
      setErrorMessage(django.gettext('Failed to load comments. Please try again.'))
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading, nextComments, comments, anchoredCommentParentId])

  useEffect(() => {
    window.addEventListener('agreedTos', handleTermsOfUse)
    return () => {
      window.removeEventListener('agreedTos', handleTermsOfUse)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agreedTermsOfUse])

  useEffect(() => {
    if (anchorRendered === true) {
      const el = document.getElementById('comment_' + anchoredCommentId)
      if (el !== null) {
        const top = el.getBoundingClientRect().top
        window.scrollTo(0, top)
      }
    }
  }, [anchorRendered, anchoredCommentId])

  function handleComments (result: CommentListResponse) {
    const data = result

    setComments(data.results)
    setNextComments(data.next)
    setCommentCount(data.comment_count)
    setHasCommentingPermission(data.has_commenting_permission)
    setProjectIsPublic(data.project_is_public)
    setUseTermsOfUse(data.use_org_terms_of_use)
    setAgreedTermsOfUse(data.user_has_agreed)
    setOrgTermsUrl(data.org_terms_url)
    if (props.withCategories) {
      setCategoryChoices(data.categories)
    }
    if (props.anchoredCommentId && data.comment_found) {
      setAnchoredCommentParentId(data.comment_parent)
      if (
        findAnchoredComment(data.results, data.comment_parent) ||
        !data.next
      ) {
        setLoading(false)
      } else {
        fetchComments(data.next, data.results, data.comment_parent)
      }
    } else {
      if (props.anchoredCommentId) {
        /* display something like: django.gettext('We are sorry, this comment does not exist.')
         * probably using a modal
         */
      }
      setLoading(false)
      setWouldHaveCommentingPermission(data.would_have_commenting_permission)
    }
  }

  // handles update of the comment state
  // called in handleCommentSubmit, handleCommentModify, handleCommentDelete,
  // handleHideReplyError, handleHideEditeError
  function updateStateComment (parentIndex: number | undefined, index: number | undefined, updatedComment: Partial<Comment>) {
    let diff: Spec<Comment[]>
    if (parentIndex !== undefined) {
      diff = {
        [parentIndex]: {
          child_comments: {
            [index as number]: { $merge: updatedComment }
          }
        }
      }
    } else {
      diff = {
        [index as number]: { $merge: updatedComment }
      }
    }
    setComments(update(comments, diff))
  }

  function addComment (parentIndex: number | undefined, comment: Comment) {
    let diff: Spec<Comment[]>
    if (parentIndex !== undefined) {
      diff = {
        [parentIndex]: {
          child_comments: { $push: [comment] },
          $merge: {
            replyError: false,
            errorMessage: undefined
          }
        }
      }
    } else {
      diff = { $unshift: [comment] }
      setMainError(undefined)
    }
    setComments(update(comments, diff))
    setCommentCount(commentCount + 1)
  }

  function setReplyError (parentIndex: number | undefined, index: number | undefined, message?: string) {
    updateError(parentIndex, index, message, 'replyError')
  }

  function setEditError (parentIndex: number | undefined, index: number | undefined, message?: string) {
    updateError(parentIndex, index, message, 'editError')
  }

  function setMainError (message?: string) {
    updateError(undefined, undefined, message, undefined)
  }

  function updateError (parentIndex: number | undefined, index: number | undefined, message: string | undefined, type: 'replyError' | 'editError' | undefined) {
    if (index !== undefined && type) {
      updateStateComment(parentIndex, index, {
        [type]: message !== undefined,
        errorMessage: message
      })
    } else if (index !== undefined) {
      updateStateComment(parentIndex, index, { errorMessage: message })
    } else {
      setError(message !== undefined)
      setErrorMessage(message)
    }
  }

  function handleCommentSubmit (comment: CommentPayload, parentIndex?: number) {
    return api.comments
      .add(comment)
      .done((comment: Comment) => {
        comment.displayNotification = true
        addComment(parentIndex, comment)
        updateAgreedTOS()
      })
      .fail((xhr: JQuery.jqXHR<Comment>, _status: any, _err: any) => {
        const newErrorMessage = Object.values(xhr.responseJSON as Record<string, unknown>)[0]
        setReplyError(parentIndex, undefined, String(newErrorMessage))
      })
  }

  function handleCommentModify (modifiedComment: CommentPayload, index: number, parentIndex?: number) {
    let comment: Comment = comments[index]
    if (parentIndex !== undefined) {
      comment = comments[parentIndex].child_comments[index]
    }
    return api.comments
      .change(modifiedComment, comment.id)
      .done((changed: Comment) => {
        updateStateComment(parentIndex, index, {
          ...changed,
          editError: false,
          errorMessage: undefined
        })
        updateAgreedTOS()
      })
      .fail((xhr: JQuery.jqXHR<Comment>, _status: any, _err: any) => {
        const newErrorMessage = Object.values(xhr.responseJSON as Record<string, unknown>)[0]
        setEditError(parentIndex, index, String(newErrorMessage))
      })
  }

  function handleCommentDelete (index: number, parentIndex?: number) {
    const newComments = comments
    let comment: Comment = newComments[index]
    if (parentIndex !== undefined) {
      comment = newComments[parentIndex].child_comments[index]
    }

    const data = {
      urlReplaces: {
        contentTypeId: comment.content_type,
        objectPk: comment.object_pk
      }
    }
    return api.comments
      .delete(data, comment.id)
      .done((changed: Comment) => {
        updateStateComment(parentIndex, index, {
          ...changed,
          editError: false,
          errorMessage: undefined
        })
      })
      .fail((xhr: JQuery.jqXHR<Comment>, _status: any, _err: any) => {
        const newErrorMessage = Object.values(xhr.responseJSON as Record<string, unknown>)[0]
        setEditError(parentIndex, index, String(newErrorMessage))
      })
  }

  function hideNewError () {
    setMainError(undefined)
  }

  function handleHideReplyError (index: number, parentIndex?: number) {
    setReplyError(index, parentIndex, undefined)
  }

  function handleHideEditError (index: number, parentIndex?: number) {
    setEditError(parentIndex, index, undefined)
  }

  function handleHideNotification (index: number, parentIndex?: number) {
    updateStateComment(parentIndex, index, { displayNotification: false })
  }

  function handleToggleFilters (e: any) {
    e.preventDefault()
    setShowFilters(!showFilters)
  }

  function handleClickFilter (e: any) {
    e.preventDefault()
    const filter = e.target.id
    fetchFiltered(filter)
    setLoadingFilter(true)
  }

  function fetchFiltered (filter: string) {
    let commentCategory = filter
    let displayFilter = categoryChoices[filter]
    if (filter === 'all') {
      displayFilter = django.gettext('all')
      commentCategory = ''
    }
    const params: CommentQueryParams = {
      comment_category: commentCategory,
      ordering: sort,
      search,
      urlReplaces
    }
    api.comments.get(params).done((result: CommentListResponse) => {
      const data = result
      setComments(data.results)
      setNextComments(data.next)
      setCommentCount(data.comment_count)
      setFilter(filter)
      setFilterDisplay(displayFilter)
      setLoadingFilter(false)
    })
  }

  function handleClickSortedOld (e: any) {
    e.preventDefault()
    const order = e.target.id
    fetchSorted(order)
    setLoadingFilter(true)
  }

  function handleClickSorted (choice: string[]) {
    fetchSorted(choice[0])
    setLoadingFilter(true)
  }

  function fetchSorted (order: string) {
    let commentCategory = filter
    if (commentCategory === 'all') {
      commentCategory = ''
    }
    const params: CommentQueryParams = {
      ordering: order,
      comment_category: commentCategory,
      search,
      urlReplaces
    }
    api.comments.get(params).done((result: CommentListResponse) => {
      const data = result
      setComments(data.results)
      setNextComments(data.next)
      setCommentCount(data.comment_count)
      setSort(order)
      setLoadingFilter(false)
    })
  }

  function handleSearch (search: string) {
    fetchSearch(search)
    setLoadingFilter(true)
  }

  function fetchSearch (search: string) {
    let commentCategory = filter
    if (commentCategory === 'all') {
      commentCategory = ''
    }
    const params: CommentQueryParams = {
      search,
      ordering: sort,
      comment_category: commentCategory,
      urlReplaces
    }
    api.comments.get(params).done((result: CommentListResponse) => {
      const data = result
      setComments(data.results)
      setNextComments(data.next)
      setCommentCount(data.comment_count)
      setSearch(search)
      setLoadingFilter(false)
    })
  }

  function findAnchoredComment (newComments: Comment[], parentId: number) {
    if (props.anchoredCommentId && !anchoredCommentFound) {
      let found = false

      for (const comment of newComments) {
        if (comment.id === anchoredCommentId || comment.id === parentId) {
          setAnchoredCommentFound(true)
          found = true
          break
        }
      }
      return found
    }
    return true
  }

  function fetchComments (nextCommentsUrl: string, comments: Comment[], anchoredCommentParentId: number) {
    fetch(nextCommentsUrl)
      .then((response) => response.json())
      .then((data) => {
        const newComments = comments.concat(data.results)
        setComments(newComments)
        setNextComments(data.next)
        setCommentCount(data.comment_count)
        if (
          findAnchoredComment(newComments, anchoredCommentParentId) ||
          !data.next
        ) {
          setLoading(false)
        } else {
          fetchComments(data.next, newComments, anchoredCommentParentId)
        }
        return null
      })
      .catch((error) => {
        console.warn(error)
      })
  }

  function handleScroll () {
    const html = document.documentElement
    if (
      html.scrollTop + html.clientHeight >
      getDocumentHeight() - autoScrollThreshold
    ) {
      if (nextComments && !loading) {
        setLoading(true)
        fetchComments(nextComments, comments, anchoredCommentParentId)
      }
    }
  }

  function commentCategoryChoices (): Record<string, string> | undefined {
    if (props.withCategories === true) {
      return categoryChoices
    }
    return undefined
  }

  function handleTermsOfUse () {
    if (!agreedTermsOfUse) {
      setAgreedTermsOfUse(true)
    }
  }

  function updateAgreedTOS () {
    if (useTermsOfUse && !agreedTermsOfUse) {
      setAgreedTermsOfUse(true)
      const event = new Event('agreedTos')
      dispatchEvent(event)
    }
  }

  function onRenderFinished () {
    setAnchorRendered(true)
  }

  return (
    <section>
      <div className="a4-comments__commentbox__form">
        {/* Main comment form */}
        <CommentForm
          subjectType={props.subjectType}
          subjectId={props.subjectId}
          onCommentSubmit={handleCommentSubmit}
          commentId={props.id}
          rows="5"
          error={error}
          errorMessage={errorMessage}
          handleErrorClick={hideNewError}
          commentCategoryChoices={commentCategoryChoices()}
          withCategories={props.withCategories}
          hasCommentingPermission={hasCommentingPermission}
          wouldHaveCommentingPermission={wouldHaveCommentingPermission}
          projectIsPublic={projectIsPublic}
          useTermsOfUse={useTermsOfUse}
          agreedTermsOfUse={agreedTermsOfUse}
          orgTermsUrl={orgTermsUrl}
          setCommentError={setMainError}
          hideNotification={handleHideNotification}
        />
      </div>
      <div>
        <h2 className="a4-comments__commentbox__subtitle title-3">
          {translated.discussion}
        </h2>
        {noControlBar
          ? (
            <CommentFilters
              showFilters={showFilters}
              commentCount={commentCount}
              commentCategoryChoices={commentCategoryChoices}
              filterDisplay={filterDisplay}
              handleToggleFilters={handleToggleFilters}
              handleClickFilters={handleClickFilter}
              handleSearch={handleSearch}
              handleClickSorted={handleClickSortedOld}
              search={search}
              sort={sort}
              sorts={sorts}
              loadingFilter={loadingFilter}
            />
            )
          : (
            <CommentControlBar
              sort={sort}
              sorts={sorts}
              search={search}
              handleClickFilter={handleClickSorted}
              handleSearch={handleSearch}
            />
            )}
      </div>
      <CommentList
        comments={comments}
        anchoredCommentId={anchoredCommentId}
        anchoredCommentParentId={anchoredCommentParentId}
        onCommentDelete={handleCommentDelete}
        onCommentSubmit={handleCommentSubmit}
        onCommentModify={handleCommentModify}
        commentCategoryChoices={commentCategoryChoices()}
        onReplyErrorClick={handleHideReplyError}
        onEditErrorClick={handleHideEditError}
        onRenderFinished={onRenderFinished}
        withCategories={props.withCategories}
        hasCommentingPermission={hasCommentingPermission}
        wouldHaveCommentingPermission={wouldHaveCommentingPermission}
        projectIsPublic={projectIsPublic}
        useTermsOfUse={useTermsOfUse}
        agreedTermsOfUse={agreedTermsOfUse}
        orgTermsUrl={orgTermsUrl}
        setCommentError={setMainError}
        setCommentEditError={setEditError}
        hideNotification={handleHideNotification}
      />
      <div className={loading ? 'u-spinner__container' : 'd-none'}>
        <i className="fa fa-spinner fa-pulse" aria-hidden="true" />
        <span className="a4-sr-only">Loading...</span>
      </div>
    </section>
  )
}

export default CommentBox
