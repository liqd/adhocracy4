import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi, Mock } from 'vitest';
import CommentBox from '../comment_box';
import api from '../../../../static/api';

// Mock jQuery deferred/promise interface
const mockJQueryDeferred = () => {
  const deferred = {
    done: vi.fn().mockReturnThis(),
    fail: vi.fn().mockReturnThis(),
    always: vi.fn().mockReturnThis(),
    then: vi.fn().mockReturnThis(),
    promise: vi.fn().mockReturnThis(),
    state: vi.fn(),
    pipe: vi.fn().mockReturnThis()
  };
  return deferred;
};

vi.mock('../../../../static/api', () => ({
  __esModule: true,
  default: {
    comments: {
      get: vi.fn(() => mockJQueryDeferred()),
      add: vi.fn(() => mockJQueryDeferred()),
      change: vi.fn(() => mockJQueryDeferred()),
      delete: vi.fn(() => mockJQueryDeferred())
    }
  }
}));

afterEach(() => {
  vi.clearAllMocks();
});

describe('CommentBox Component', () => {
  const defaultProps = {
    anchoredCommentId: null,
    id: 0,
    noControlBar: false,
    subjectId: 0,
    subjectType: 108,
    useModeratorMarked: null,
    withCategories: false
  };

  test('renders CommentBox', () => {
    // Setup mock response
    const deferred = mockJQueryDeferred();
    (api.comments.get as Mock).mockReturnValueOnce(deferred);
    
    render(<CommentBox {...defaultProps} />);
    
    // Simulate AJAX completion
    deferred.done.mock.calls[0][0]({ 
      results: [],
      comment_count: 0,
      has_commenting_permission: false,
      project_is_public: false,
      use_org_terms_of_use: false,
      user_has_agreed: false
    });
    
    expect(api.comments.get).toHaveBeenCalledTimes(1);
  });

  test('comments are fetched and loading spinner is hidden', async () => {
    const deferred = mockJQueryDeferred();
    (api.comments.get as Mock).mockReturnValueOnce(deferred);
    
    render(<CommentBox {...defaultProps} />);
    
    // Simulate successful response with all required fields
    deferred.done.mock.calls[0][0]({
      results: [],
      comment_count: 0,
      comment_found: false, // Added this
      has_commenting_permission: false,
      would_have_commenting_permission: false, // Added this
      project_is_public: false,
      use_org_terms_of_use: false,
      user_has_agreed: false,
      org_terms_url: '' // Added this
    });
    
    await waitFor(() => {
      expect(api.comments.get).toHaveBeenCalledTimes(1);
      // Check that loading state is false
      expect(screen.queryByText(/Loading.../i)?.closest('div')).toHaveClass('d-none');
    });
  });

  test('more comments are fetched on scroll', async () => {
    // Mock initial response with next page URL
    const mockResponse = {
      results: [],
      next: 'https://liqd.net/next_comments',
      comment_count: 0,
      has_commenting_permission: true, // Added this
      would_have_commenting_permission: true, // Added this
      project_is_public: true, // Added this
      use_org_terms_of_use: false,
      user_has_agreed: false,
      org_terms_url: '',
      comment_found: false
    };

    // Mock immediate resolution
    (api.comments.get as Mock).mockImplementation(() => ({
      done: (callback: any) => {
        callback(mockResponse);
        return { fail: vi.fn() };
      },
      fail: vi.fn()
    }));

    render(<CommentBox {...defaultProps} />);

    // Wait for initial load
    await waitFor(() => {
      expect(api.comments.get).toHaveBeenCalledTimes(1);
    });

    // Mock fetch for the next page
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ 
        results: [],
        comment_count: 0
      })
    });

    // Scroll to trigger loading more comments
    fireEvent.scroll(window, { 
      target: { 
        scrollY: 1000,
        clientHeight: 500,
        scrollHeight: 2000 
      } 
    });

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith('https://liqd.net/next_comments');
    });
  });
});