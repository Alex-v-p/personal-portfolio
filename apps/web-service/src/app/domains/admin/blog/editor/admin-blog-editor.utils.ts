export interface TextSelectionRange {
  start: number;
  end: number;
}

export interface TextSelectionUpdate {
  value: string;
  selection: TextSelectionRange;
}

export function countMarkdownWords(markdown: string | null | undefined): number {
  const matches = (markdown || '').match(/\b[\p{L}\p{N}][\p{L}\p{N}'’-]*\b/gu);
  return matches?.length ?? 0;
}

export function suggestReadingTimeMinutes(markdown: string | null | undefined, wordsPerMinute = 200): number {
  const wordCount = countMarkdownWords(markdown);
  return wordCount > 0 ? Math.max(1, Math.ceil(wordCount / wordsPerMinute)) : 0;
}

export function wrapSelection(
  content: string,
  selection: TextSelectionRange,
  prefix: string,
  suffix = '',
  placeholder = 'text',
): TextSelectionUpdate {
  const selectedText = content.slice(selection.start, selection.end);
  const replacement = `${prefix}${selectedText || placeholder}${suffix}`;
  const value = `${content.slice(0, selection.start)}${replacement}${content.slice(selection.end)}`;
  const highlightStart = selection.start + prefix.length;
  const highlightEnd = highlightStart + (selectedText || placeholder).length;

  return {
    value,
    selection: { start: highlightStart, end: highlightEnd },
  };
}

const getSelectedLineBlock = (content: string, selection: TextSelectionRange): { lineStart: number; lineEnd: number; lines: string[] } => {
  const lineStart = content.lastIndexOf('\n', Math.max(0, selection.start - 1)) + 1;
  let lineEnd = content.indexOf('\n', selection.end);
  if (lineEnd === -1) {
    lineEnd = content.length;
  }

  return {
    lineStart,
    lineEnd,
    lines: content.slice(lineStart, lineEnd).split('\n'),
  };
};

const applyLineBlockReplacement = (content: string, lineStart: number, lineEnd: number, replacement: string): TextSelectionUpdate => ({
  value: `${content.slice(0, lineStart)}${replacement}${content.slice(lineEnd)}`,
  selection: { start: lineStart, end: lineStart + replacement.length },
});

const orderedListPrefixPattern = /^(\s*)\d+[.)]\s+/;

export function toggleLinePrefix(content: string, selection: TextSelectionRange, prefix: string): TextSelectionUpdate {
  const { lineStart, lineEnd, lines } = getSelectedLineBlock(content, selection);
  const populatedLines = lines.filter((line) => line.trim().length > 0);
  const allPrefixed = populatedLines.length > 0 && populatedLines.every((line) => line.startsWith(prefix));
  const replacement = lines
    .map((line) => {
      if (!line.trim()) {
        return line;
      }

      return allPrefixed ? line.slice(prefix.length) : `${prefix}${line}`;
    })
    .join('\n');

  return applyLineBlockReplacement(content, lineStart, lineEnd, replacement);
}

export function toggleOrderedListPrefix(content: string, selection: TextSelectionRange): TextSelectionUpdate {
  const { lineStart, lineEnd, lines } = getSelectedLineBlock(content, selection);
  const populatedLines = lines.filter((line) => line.trim().length > 0);
  const allNumbered = populatedLines.length > 0 && populatedLines.every((line) => orderedListPrefixPattern.test(line));
  let itemNumber = 1;

  const replacement = lines
    .map((line) => {
      if (!line.trim()) {
        return line;
      }

      if (allNumbered) {
        return line.replace(orderedListPrefixPattern, '$1');
      }

      const normalizedLine = line.replace(orderedListPrefixPattern, '$1');
      const leadingWhitespace = normalizedLine.match(/^\s*/)?.[0] ?? '';
      const contentWithoutIndent = normalizedLine.slice(leadingWhitespace.length);
      return `${leadingWhitespace}${itemNumber++}. ${contentWithoutIndent}`;
    })
    .join('\n');

  return applyLineBlockReplacement(content, lineStart, lineEnd, replacement);
}

export function insertSnippet(content: string, selection: TextSelectionRange, snippet: string, selectLength = 0): TextSelectionUpdate {
  const value = `${content.slice(0, selection.start)}${snippet}${content.slice(selection.end)}`;
  const caretEnd = selection.start + snippet.length;
  const caretStart = selectLength > 0 ? caretEnd - selectLength : caretEnd;

  return {
    value,
    selection: { start: caretStart, end: caretEnd },
  };
}

export function insertCodeBlock(content: string, selection: TextSelectionRange): TextSelectionUpdate {
  const snippet = '\n```\nconst example = true;\n```\n';
  const value = `${content.slice(0, selection.start)}${snippet}${content.slice(selection.end)}`;
  const codeStart = selection.start + '\n```\n'.length;

  return {
    value,
    selection: { start: codeStart, end: codeStart + 'const example = true;'.length },
  };
}

export function insertImageTemplate(content: string, selection: TextSelectionRange): TextSelectionUpdate {
  const snippet = '\n![Describe image](https://example.com/image.jpg)\n';
  const value = `${content.slice(0, selection.start)}${snippet}${content.slice(selection.end)}`;
  const urlStart = selection.start + '\n![Describe image]('.length;

  return {
    value,
    selection: { start: urlStart, end: urlStart + 'https://example.com/image.jpg'.length },
  };
}
