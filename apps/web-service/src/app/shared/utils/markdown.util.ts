const escapeHtml = (value: string): string => value
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;');

const isSafeUrl = (url: string): boolean => /^(https?:\/\/|mailto:|\/)/i.test(url.trim());

const isExternalUrl = (url: string): boolean => /^https?:\/\//i.test(url.trim());

const splitMarkdownTarget = (rawTarget: string): { url: string; title: string } => {
  const target = rawTarget.trim();
  const titleMatch = target.match(/^(\S+)\s+(?:"([^"]+)"|&quot;([^&]+)&quot;)\s*$/);
  if (titleMatch) {
    return { url: titleMatch[1], title: titleMatch[2] ?? titleMatch[3] ?? '' };
  }
  return { url: target, title: '' };
};

const isDownloadLink = (label: string, url: string, title: string): boolean => {
  const normalizedTitle = title.trim().toLowerCase();
  const normalizedLabel = label.trim().toLowerCase();
  return (
    normalizedTitle === 'download' ||
    normalizedTitle.includes('download') ||
    normalizedLabel.startsWith('download ') ||
    /[?&]download(?:=1|=true)?(?:&|$)/i.test(url)
  );
};

const renderImage = (altText: string, rawTarget: string): string => {
  const { url } = splitMarkdownTarget(rawTarget);
  const safeUrl = isSafeUrl(url) ? escapeHtml(url.trim()) : '#';
  const safeAltText = altText.trim();
  return `<img src="${safeUrl}" alt="${safeAltText}" loading="lazy" />`;
};

const renderLink = (label: string, rawTarget: string): string => {
  const { url, title } = splitMarkdownTarget(rawTarget);
  const safeUrl = isSafeUrl(url) ? escapeHtml(url.trim()) : '#';
  const safeLabel = label.trim();
  const externalAttrs = isExternalUrl(url) ? ' target="_blank" rel="noreferrer noopener"' : '';

  if (isDownloadLink(label, url, title)) {
    const downloadAttr = isExternalUrl(url) ? '' : ' download';
    return `<a class="markdown-download" href="${safeUrl}"${externalAttrs}${downloadAttr}><span class="markdown-download__icon" aria-hidden="true">↓</span><span>${safeLabel}</span></a>`;
  }

  return `<a href="${safeUrl}"${externalAttrs}>${safeLabel}</a>`;
};

const renderInline = (value: string): string => {
  let text = escapeHtml(value);

  text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_match, altText: string, target: string) => renderImage(altText, target));
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label: string, target: string) => renderLink(label, target));

  return text;
};

const renderParagraph = (lines: string[]): string => `<p>${renderInline(lines.join(' '))}</p>`;

const renderList = (items: string[], ordered = false): string => {
  const tag = ordered ? 'ol' : 'ul';
  const inner = items.map((item) => `<li>${renderInline(item)}</li>`).join('');
  return `<${tag}>${inner}</${tag}>`;
};

const renderBlockquote = (lines: string[]): string => {
  const inner = lines.map((line) => `<p>${renderInline(line)}</p>`).join('');
  return `<blockquote>${inner}</blockquote>`;
};

const renderCodeBlock = (lines: string[]): string => `<pre><code>${escapeHtml(lines.join('\n'))}</code></pre>`;

const isOrderedListLine = (line: string): boolean => /^\d+\.\s+/.test(line);
const isUnorderedListLine = (line: string): boolean => /^[-*]\s+/.test(line);

export const buildMarkdownDownloadLink = (label: string, url: string): string => {
  const safeLabel = label.replace(/[\r\n]+/g, ' ').replace(/\]/g, '\\]').trim() || 'Download file';
  return `[${safeLabel}](${url.trim()} "download")`;
};

export const renderMarkdownToHtml = (markdown: string): string => {
  const lines = markdown.replace(/\r\n/g, '\n').trim().split('\n');

  if (!lines.filter((line) => line.trim()).length) {
    return '<p>No content available yet.</p>';
  }

  const blocks: string[] = [];
  let index = 0;

  while (index < lines.length) {
    const rawLine = lines[index] ?? '';
    const line = rawLine.trimEnd();
    const trimmed = line.trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    if (trimmed.startsWith('```')) {
      index += 1;
      const codeLines: string[] = [];
      while (index < lines.length && !lines[index].trim().startsWith('```')) {
        codeLines.push(lines[index]);
        index += 1;
      }
      index += 1;
      blocks.push(renderCodeBlock(codeLines));
      continue;
    }

    if (/^---+$/.test(trimmed)) {
      blocks.push('<hr />');
      index += 1;
      continue;
    }

    if (/^###\s+/.test(trimmed)) {
      blocks.push(`<h3>${renderInline(trimmed.replace(/^###\s+/, ''))}</h3>`);
      index += 1;
      continue;
    }

    if (/^##\s+/.test(trimmed)) {
      blocks.push(`<h2>${renderInline(trimmed.replace(/^##\s+/, ''))}</h2>`);
      index += 1;
      continue;
    }

    if (/^#\s+/.test(trimmed)) {
      blocks.push(`<h1>${renderInline(trimmed.replace(/^#\s+/, ''))}</h1>`);
      index += 1;
      continue;
    }

    if (trimmed.startsWith('>')) {
      const quoteLines: string[] = [];
      while (index < lines.length && lines[index].trim().startsWith('>')) {
        quoteLines.push(lines[index].trim().replace(/^>\s?/, ''));
        index += 1;
      }
      blocks.push(renderBlockquote(quoteLines));
      continue;
    }

    if (isUnorderedListLine(trimmed)) {
      const items: string[] = [];
      while (index < lines.length && isUnorderedListLine(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^[-*]\s+/, ''));
        index += 1;
      }
      blocks.push(renderList(items));
      continue;
    }

    if (isOrderedListLine(trimmed)) {
      const items: string[] = [];
      while (index < lines.length && isOrderedListLine(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^\d+\.\s+/, ''));
        index += 1;
      }
      blocks.push(renderList(items, true));
      continue;
    }

    const paragraphLines: string[] = [];
    while (index < lines.length) {
      const candidate = lines[index].trim();
      if (!candidate) {
        break;
      }
      if (
        candidate.startsWith('```') ||
        /^---+$/.test(candidate) ||
        /^#{1,3}\s+/.test(candidate) ||
        candidate.startsWith('>') ||
        isUnorderedListLine(candidate) ||
        isOrderedListLine(candidate)
      ) {
        break;
      }
      paragraphLines.push(candidate);
      index += 1;
    }
    blocks.push(renderParagraph(paragraphLines));
  }

  return blocks.join('');
};
