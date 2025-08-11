import $ from 'jquery';
import cookie from 'js-cookie';

// Initialize CSRF token setup
function init() {
  $.ajaxSetup({
    headers: { 'X-CSRFToken': cookie.get('csrftoken') }
  });
}

document.addEventListener('DOMContentLoaded', init, false);
document.addEventListener('a4.embed.ready', init, false);

const baseURL = '/api/';

interface ApiConfig {
  url: string;
  type: string;
  data?: any;
  dataType?: string;
  contentType?: string;
  error?: (xhr: JQuery.jqXHR, status: string, err: string) => void;
  complete?: () => void;
}

interface ApiResponse<T = any> {
  results: T[];
  next?: string;
  [key: string]: any;
}

interface Comment {
  id: number;
  content: string;
  // Add other comment properties as needed
}

class ApiClient {
  private urls = {
    report: baseURL + 'reports/',
    document: baseURL + 'modules/$moduleId/documents/',
    poll: baseURL + 'polls/',
    pollvote: baseURL + 'polls/$pollId/vote/',
    follow: baseURL + 'follows/',
    comment: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/comments/',
    commentmoderate: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/comment-moderate/',
    rating: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/ratings/',
    moderatorremark: baseURL + 'contenttypes/$contentTypeId/objects/$objectPk/moderatorremarks/'
  };

  private _sendRequest<T>(endpoint: string, id: string | number | object, options: any, data?: any): JQuery.jqXHR<T> {
    const $body = $('body');

    if (typeof id === 'object') {
      // there's no id, switch parameters
      data = options;
      options = id;
      id = null as any;
    }

    let url = this.urls[endpoint as keyof typeof this.urls];
    if (data?.urlReplaces) {
      url = url.replace(/\$(\w+?)\b/g, (match, group) => {
        return data.urlReplaces[group];
      });
      data = { ...data };
      delete data.urlReplaces;
    }

    if (typeof id === 'number' || typeof id === 'string') {
      url = url + id + '/';
    }

    const defaultParams: ApiConfig = {
      url,
      type: 'json',
      dataType: 'json',
      data,
      error: (xhr, status, err) => {
        console.error(url, status, err.toString());
      },
      complete: () => {
        $body.removeClass('loading');
      }
    };

    const params = { ...defaultParams, ...options };

    if (typeof params.data !== 'undefined') {
      if (params.type === 'PUT' || params.type === 'POST' || params.type === 'PATCH') {
        params.contentType = 'application/json; charset=utf-8';
        params.data = JSON.stringify(params.data);
      }
    }

    $body.addClass('loading');
    return $.ajax(params);
  }

  public comments = {
    get: (data: any): JQuery.jqXHR<ApiResponse<Comment>> => {
      return this._sendRequest('comment', { type: 'GET' }, data);
    },
    add: (data: any): JQuery.jqXHR<Comment> => {
      return this._sendRequest('comment', { type: 'POST' }, data);
    },
    change: (data: any, id: number): JQuery.jqXHR<Comment> => {
      return this._sendRequest('comment', id, { type: 'PATCH' }, data);
    },
    delete: (data: any, id: number): JQuery.jqXHR<void> => {
      return this._sendRequest('comment', id, { type: 'DELETE' }, data);
    }
  };

  public follow = {
    get: (project: string): JQuery.jqXHR<{ enabled: boolean }> => {
      return this._sendRequest('follow', project, { type: 'GET' }, {});
    },
    change: (data: { enabled: boolean }, project: string): JQuery.jqXHR<{ enabled: boolean }> => {
      return this._sendRequest('follow', project, { type: 'PUT' }, data);
    },
    setFollowing: (data: { enabled: boolean }): void => {
      // Mock function for testing if needed
    }
  };
  // Add other endpoints with proper typing as needed
  // ...
}

const api = new ApiClient();
export default api;