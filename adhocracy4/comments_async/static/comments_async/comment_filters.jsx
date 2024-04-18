import React from 'react'
import django from 'django'

import { FilterCategory } from './filter_category'
import { FilterSearch } from './filter_search'
import { FilterSort } from './filter_sort'

/*
 Alternative comment filters to be used in CommentBox if you don't want
 to use the CommentControlBar. This should not be used for new projects.
*/

const translated = {
  showFilters: django.gettext('Show more'),
  hideFilters: django.gettext('Show less'),
  filters: django.gettext('Filters'),
  ordering: django.gettext('Ordering')
}

function translatedEntries (entries) {
  return django.ngettext('entry', 'entries', entries)
}

function translatedEntriesFound (entriesFound) {
  return django.ngettext('entry found for ', 'entries found for ', entriesFound)
}

export const CommentFilters = (props) => {
  return (
    <div
      className={
        props.commentCount === 0 && props.loading
          ? 'd-none'
          : 'a4-comments__filters__parent'
      }
    >
      <div className="a4-comments__filters__parent--closed">
        <div
          className={
            props.search === '' ? 'a4-comments__filters__text' : 'd-none'
          }
        >
          {props.commentCount + ' ' + translatedEntries(props.commentCount)}
        </div>

        <div
          className={
            props.search !== '' ? 'a4-comments__filters__text' : 'd-none'
          }
        >
          <span className="a4-comments__filters__span">
            {props.commentCount +
              ' ' +
              translatedEntriesFound(props.commentCount)}
            {props.search}
          </span>
        </div>

        {!props.showFilters && props.commentCount > 0 && (
          <button
            className="btn a4-comments__filters__show-btn"
            type="button"
            onClick={props.handleToggleFilters}
          >
            <i className="fas fa-sliders-h ms-2" aria-hidden="true" />
            {translated.filters}
          </button>
        )}
        {props.showFilters && props.commentCount > 0 && (
          <button
            className="btn a4-comments__filters__show-btn"
            type="button"
            onClick={props.handleToggleFilters}
          >
            <i className="fas fa-times ms-2" aria-hidden="true" />
            {translated.hideFilters}
          </button>
        )}
      </div>
      {props.showFilters && (
        <div className="a4-comments__filters">
          <FilterSearch
            search={props.search}
            translated={translated}
            onSearch={props.handleSearch}
          />
          {props.withCategories
            ? (
              <FilterCategory
                translated={translated}
                filter={props.filter}
                filterDisplay={props.filterDisplay}
                onClickFilter={props.handleClickFilter}
                commentCategoryChoices={props.commentCategoryChoices}
              />
              )
            : (
              <div className="col-lg-3" />
              )}
          <FilterSort
            translated={translated}
            sort={props.sort}
            sorts={props.sorts}
            onClickSorted={props.handleClickSorted}
          />
        </div>
      )}
      <div className={props.loadingFilter ? 'u-spinner__container' : 'd-none'}>
        <i className="fa fa-spinner fa-pulse" aria-hidden="true" />
        <span className="a4-sr-only">Loading...</span>
      </div>
    </div>
  )
}
