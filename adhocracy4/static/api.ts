import $ from 'jquery'
import cookie from 'js-cookie'
import type {
  Comment,
  CommentListResponse,
  CommentPayload,
  CommentQueryParams,
  FollowState,
  Poll,
  PollEditPayload,
  PollVotePayload,
  RatingResponse,
  ReportPayload,
  UrlReplaces
} from './api/types'

function init () {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': cookie.get('csrftoken') }
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)

const baseURL = '/api/'

const api = (function () {
  const urls: Record<string, string> = {
    report: baseURL + 'reports/',
    document: baseURL + 'modules/$moduleId/documents/',
    poll: baseURL + 'polls/',
    pollvote: baseURL + 'polls/$pollId/vote/',
    follow: baseURL + 'follows/',
    comment: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/comments/',
    commentmoderate: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/comment-moderate/',
    rating: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/ratings/',
    moderatorremark: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/moderatorremarks/'
  }

  interface RequestData {
    urlReplaces?: UrlReplaces
    [key: string]: unknown
  }

  function _sendRequest<T> (endpoint: string, id: string | number | null | undefined, options?: JQuery.AjaxSettings, data?: object): JQuery.jqXHR<T> {
    const $body = $('body')

    let payload: RequestData | undefined = data as RequestData | undefined
    let url = urls[endpoint]
    if (payload && payload.urlReplaces) {
      const urlReplaces = payload.urlReplaces
      url = url.replace(/\$(\w+?)\b/g, (match, group) => {
        return String(urlReplaces[group])
      })
      payload = $.extend({}, payload)
      delete payload.urlReplaces
    }

    if (id !== null) {
      url = url + id + '/'
    }
    const defaultParams: JQuery.AjaxSettings = {
      url,
      dataType: 'json',
      data: payload,
      error: function (xhr: JQuery.jqXHR<T>, status: string, err: unknown) {
        console.error(url, status, String(err))
      },
      complete: function () {
        $body.removeClass('loading')
      }
    }
    const params = $.extend(defaultParams, options)

    if (typeof params.data !== 'undefined') {
      if (params.type === 'PUT' || params.type === 'POST' || params.type === 'PATCH') {
        if (params.data instanceof FormData) {
          params.processData = false
          params.contentType = false
        } else {
          params.contentType = 'application/json; charset=utf-8'
          params.data = JSON.stringify(params.data)
        }
      }
    }

    $body.addClass('loading')
    return $.ajax(params) as JQuery.jqXHR<T>
  }

  return {
    comments: {
      get: function (data?: CommentQueryParams) {
        return _sendRequest<CommentListResponse>('comment', null, {
          type: 'GET'
        }, data)
      },
      add: function (data?: CommentPayload) {
        return _sendRequest<Comment>('comment', null, {
          type: 'POST'
        }, data)
      },

      change: function (data: CommentPayload, id: number) {
        return _sendRequest<Comment>('comment', id, {
          type: 'PATCH'
        }, data)
      },

      delete: function (data: CommentPayload, id: number) {
        return _sendRequest<Comment>('comment', id, {
          type: 'DELETE'
        }, data)
      }
    },
    commentmoderate: {
      change: function (data: RequestData, id: number) {
        return _sendRequest<Comment>('commentmoderate', id, {
          type: 'PATCH'
        }, data)
      }
    },
    rating: {
      add: function (data: RequestData) {
        return _sendRequest<RatingResponse>('rating', null, {
          type: 'POST'
        }, data)
      },
      change: function (data: RequestData, id: number | null | undefined) {
        return _sendRequest<RatingResponse>('rating', id, {
          type: 'PATCH'
        }, data)
      }
    },
    report: {
      submit: function (data?: ReportPayload) {
        return _sendRequest<Record<string, unknown>>('report', null, {
          type: 'POST'
        }, data)
      }
    },
    document: {
      add: function (data?: RequestData) {
        return _sendRequest<Record<string, unknown>>('document', null, {
          type: 'POST'
        }, data)
      },
      change: function (data: RequestData, id: number) {
        return _sendRequest<Record<string, unknown>>('document', id, {
          type: 'PUT'
        }, data)
      }
    },
    follow: {
      get: function (slug: string) {
        return _sendRequest<FollowState>('follow', slug, {
          type: 'GET'
        }, {})
      },
      change: function (data: { enabled: boolean }, slug: string) {
        return _sendRequest<FollowState>('follow', slug, {
          type: 'PUT'
        }, data)
      }
    },
    poll: {
      get: function (id: number) {
        return _sendRequest<Poll>('poll', id, {
          type: 'GET'
        }, {})
      },
      change: function (data: PollEditPayload, id: number) {
        return _sendRequest<Poll>('poll', id, {
          type: 'PUT'
        }, data)
      },
      vote: function (data: PollVotePayload) {
        return _sendRequest<Poll>('pollvote', null, {
          type: 'POST'
        }, data)
      }
    },
    moderatorremark: {
      add: function (data?: RequestData) {
        return _sendRequest<Record<string, unknown>>('moderatorremark', null, {
          type: 'POST'
        }, data)
      },
      change: function (data: RequestData, id: number) {
        return _sendRequest<Record<string, unknown>>('moderatorremark', id, {
          type: 'PUT'
        }, data)
      }
    }
  }
}())

export default api