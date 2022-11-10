import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import ChapterForm from '../ChapterForm'

// This mocks the child component <ParagraphForm> since we do not
// want to provide all props to this child component
// FIXME: Because of mocking ParagraphForm, some things cannot be tested
// E.g. not able to reach 100% coverage for this component at the moment.
// Note: () => () => {} to unwrap it properly.
// eslint-disable-next-line react/display-name
jest.mock('../ParagraphForm', () => () => <div>MockedParagraphForm</div>)

test('Chapter Form without paragraphs', () => {
  const mockedChapter = {
    key: 'chapter_key',
    name: 'chapter_name',
    paragraphs: []
  }
  render(<ChapterForm id="chapter-form-id" chapter={mockedChapter} />)
  const chapterLabel = screen.queryByLabelText('Chapter title')
  expect(chapterLabel).toBeTruthy()
})

test('Chapter Form with paragraph', () => {
  const mockedChapter = {
    key: 'chapter_key',
    name: 'chapter_name',
    paragraphs: [
      {
        id: 1,
        name: 'paragraph_title',
        text: '<p>paragraph body text</p>'
      }
    ]
  }
  render(<ChapterForm id="chapter-form-id" chapter={mockedChapter} />)
  const chapterLabel = screen.queryByLabelText('Chapter title')
  expect(chapterLabel).toBeTruthy()
})

test('Chapter Form changing chapter title', () => {
  const mockedFn = jest.fn()
  const mockedChapter = {
    key: 'chapter_key',
    name: 'chapter_name',
    paragraphs: []
  }
  render(
    <ChapterForm
      id="chapter-form-id"
      chapter={mockedChapter}
      onChapterNameChange={mockedFn}
    />
  )
  const chapterNameInput = screen.getByDisplayValue('chapter_name')
  fireEvent.change(chapterNameInput, { target: { value: 'changed_name_to_this' } })
  expect(mockedFn).toHaveBeenCalledTimes(1)
})
