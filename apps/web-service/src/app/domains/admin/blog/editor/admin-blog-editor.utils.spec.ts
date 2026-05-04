import { describe, expect, it } from 'vitest';

import {
  countMarkdownWords,
  insertCodeBlock,
  insertImageTemplate,
  insertSnippet,
  suggestReadingTimeMinutes,
  toggleLinePrefix,
  toggleOrderedListPrefix,
  wrapSelection,
} from './admin-blog-editor.utils';

describe('admin-blog-editor.utils', () => {
  it('counts words in markdown content', () => {
    expect(countMarkdownWords('# Hello world\n\nThis is a test.')).toBe(6);
  });

  it('suggests reading time from markdown content', () => {
    const markdown = new Array(401).fill('word').join(' ');
    expect(suggestReadingTimeMinutes(markdown)).toBe(3);
  });

  it('wraps the current selection with markdown syntax', () => {
    expect(wrapSelection('hello world', { start: 0, end: 5 }, '**', '**')).toEqual({
      value: '**hello** world',
      selection: { start: 2, end: 7 },
    });
  });

  it('toggles list prefixes for selected lines', () => {
    expect(toggleLinePrefix('first\nsecond', { start: 0, end: 12 }, '- ')).toEqual({
      value: '- first\n- second',
      selection: { start: 0, end: 16 },
    });
    expect(toggleLinePrefix('- first\n- second', { start: 0, end: 16 }, '- ')).toEqual({
      value: 'first\nsecond',
      selection: { start: 0, end: 12 },
    });
  });

  it('toggles ordered list prefixes with sequential numbering', () => {
    expect(toggleOrderedListPrefix('first\nsecond', { start: 0, end: 12 })).toEqual({
      value: '1. first\n2. second',
      selection: { start: 0, end: 18 },
    });
    expect(toggleOrderedListPrefix('1. first\n2. second', { start: 0, end: 18 })).toEqual({
      value: 'first\nsecond',
      selection: { start: 0, end: 12 },
    });
    expect(toggleOrderedListPrefix('1. first\n1. second', { start: 0, end: 18 })).toEqual({
      value: 'first\nsecond',
      selection: { start: 0, end: 12 },
    });
  });

  it('inserts generic snippets and editor templates at the current selection', () => {
    expect(insertSnippet('hello', { start: 5, end: 5 }, '\n---\n')).toEqual({
      value: 'hello\n---\n',
      selection: { start: 10, end: 10 },
    });

    expect(insertCodeBlock('', { start: 0, end: 0 })).toEqual({
      value: '\n```\nconst example = true;\n```\n',
      selection: { start: 5, end: 26 },
    });

    expect(insertImageTemplate('', { start: 0, end: 0 })).toEqual({
      value: '\n![Describe image](https://example.com/image.jpg)\n',
      selection: { start: 19, end: 48 },
    });
  });
});
