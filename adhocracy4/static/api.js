var $ = require('jquery')
var cookie = require('js-cookie')

var init = function () {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': cookie.get('csrftoken') }
  })
}

$(init)
$(document).on('a4.embed.ready', init)

var baseURL = '/api/'

var api = (function () {
  var urls = {
    report: baseURL + 'reports/',
    document: baseURL + 'modules/$moduleId/documents/',
    poll: baseURL + 'polls/',
    pollvote: baseURL + 'polls/question/$questionId/vote/',
    follow: baseURL + 'follows/',
    comment: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/comments/',
    rating: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/ratings/',
    moderatorremark: baseURL + 'moderatorremarks/'
  }

  function _sendRequest (endpoint, id, options, data, contentType) {
    var $body = $('body')

    if (typeof id === 'object') {
      // there's no id, switch parameters
      data = options
      options = id
      id = null
    }

    var url = urls[endpoint]
    if (data.urlReplaces) {
      url = url.replace(/\$(\w+?)\b/g, (match, group) => {
        return data.urlReplaces[group]
      })
      data = $.extend({}, data)
      delete data.urlReplaces
    }

    if (typeof id === 'number' || typeof id === 'string') {
      url = url + id + '/'
    }
    var defaultParams = {
      url: url,
      dataType: 'json',
      data: data,
      error: function (xhr, status, err) {
        console.error(url, status, err.toString())
      },
      complete: function () {
        $body.removeClass('loading')
      }
    }
    var params = $.extend(defaultParams, options)

    if (typeof params.data !== 'undefined') {
      if (params.type === 'PUT' || params.type === 'POST' ||
          params.type === 'PATCH'
      ) {
        params.contentType = 'application/json; charset=utf-8'
        params.data = JSON.stringify(params.data)
      }
    }

    $body.addClass('loading')
    return $.ajax(params)
  }

  return {
    comments: {
      add: function (data) {
        return _sendRequest('comment', {
          type: 'POST'
        }, data)
      },

      change: function (data, id) {
        return _sendRequest('comment', id, {
          type: 'PATCH'
        }, data)
      },

      delete: function (data, id) {
        return _sendRequest('comment', id, {
          type: 'DELETE'
        }, data)
      }
    },
    rating: {
      add: function (data) {
        return _sendRequest('rating', {
          type: 'POST'
        }, data)
      },
      change: function (data, id) {
        return _sendRequest('rating', id, {
          type: 'PATCH'
        }, data)
      }
    },
    report: {
      submit: function (data) {
        return _sendRequest('report', {
          type: 'POST'
        }, data)
      }
    },
    document: {
      add: function (data) {
        return _sendRequest('document', {
          type: 'POST'
        }, data)
      },
      change: function (data, id) {
        return _sendRequest('document', id, {
          type: 'PUT'
        }, data)
      }
    },
    follow: {
      get: function (slug) {
        return _sendRequest('follow', slug, {
          type: 'GET'
        }, {})
      },
      change: function (data, slug) {
        return _sendRequest('follow', slug, {
          type: 'PUT'
        }, data)
      }
    },
    poll: {
      change: function (data, id) {
        return _sendRequest('poll', id, {
          type: 'PUT'
        }, data)
      },
      vote: function (data) {
        return _sendRequest('pollvote', {
          type: 'POST'
        }, data)
      }
    },
    moderatorremark: {
      get: function (slug) {
        return _sendRequest('moderatorremark', slug, {
          type: 'GET'
        }, {})
      },
      change: function (data, slug) {
        return _sendRequest('moderatorremark', slug, {
          type: 'PUT'
        }, data)
      }
    },
  }
}())
module.exports = api
