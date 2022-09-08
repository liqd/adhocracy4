import React, { useEffect, useState } from 'react'
import django from 'django'
import { BudgetingProposalListItem } from './BudgetingProposalListItem'
import { Pagination } from './Pagination'
import { CountDown } from '../../contrib/assets/CountDown'
import { FilterBar } from './FilterBar'

const nothingStr = django.gettext('Nothing to show')

export const BudgetingProposalList = (props) => {
  const [data, setData] = useState([])
  const [meta, setMeta] = useState()
  const [queryString, setQueryString] = useState('')

  const fetchProposals = (newIndex) => {
    const pageNumber = newIndex || 1
    const url = `${props.proposals_api_url}?page=${pageNumber}${queryString}`
    fetch(url)
      .then(resp => resp.json())
      .then(json => {
        setData(json.results)
        setMeta({
          current_page: pageNumber,
          page_count: json.page_count,
          is_paginated: json.page_count > 1,
          previous: json.previous,
          next: json.next,
          filters: json.filters,
          locale: json.locale,
          token_info: json.token_info
        })
      })
      .catch(error => console.log(error))
  }

  const onPaginate = (selectedPage) => {
    fetchProposals(selectedPage)
  }

  const onChangeFilters = (filterString) => {
    setQueryString(filterString)
  }

  const onVoteChange = (selectedPage) => {
    fetchProposals(selectedPage)
  }

  useEffect(fetchProposals, [queryString])

  const renderList = (data) => {
    let list
    if (data.length > 0) {
      list = (
        <>
          <ul className="u-list-reset">
            {data.map((proposal, idx) =>
              <BudgetingProposalListItem
                key={`budgeting-proposal-${idx}`}
                proposal={proposal}
                locale={meta?.locale}
                isVotingPhase={props.is_voting_phase}
                tokenvoteApiUrl={props.tokenvote_api_url}
                onVoteChange={onVoteChange}
                currentPage={meta?.current_page}
                votesLeft={meta?.token_info ? meta?.token_info.votes_left : false}
              />)}
          </ul>
          {meta?.is_paginated &&
            <Pagination
              currPageIndex={meta.current_page}
              pageCount={meta.page_count}
              onPaginate={newUrl => onPaginate(newUrl)}
            />}
        </>
      )
    } else {
      list = (
        <span>{nothingStr}</span>
      )
    }
    return list
  }

  const getVoteCountText = (votes) => {
    const countText = django.ngettext('you have 1 vote left', 'you have %s votes left', votes)
    return django.interpolate(countText, [votes])
  }

  return (
    <>
      {(props.is_voting_phase && meta?.token_info) &&
        <div className="module-content--light">
          <div className="container">
            <div className="offset-lg-3 col-lg-6">
              <CountDown
                countText={getVoteCountText(meta?.token_info.num_votes_left)}
                activeClass="btn btn--transparent btn--full u-spacer-bottom btn--huge u-primary"
                inactiveClass="btn btn--full btn--light u-spacer-bottom btn--huge"
                counter={meta?.token_info.num_votes_left}
              />
            </div>
          </div>
        </div>}
      <FilterBar
        filters={meta?.filters}
        onChangeFilters={filterString => onChangeFilters(filterString)}
      />
      <div className="module-content--light">
        <div className="container">
          <div className="offset-lg-2 col-lg-8">
            {renderList(data)}
          </div>
        </div>
      </div>
    </>
  )
}
