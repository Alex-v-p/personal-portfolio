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

export interface MarkdownRenderOptions {
  transformLinkUrl?: (url: string) => string;
  enableImageLightbox?: boolean;
}

export interface MarkdownImageReference {
  url: string;
  alt: string;
  title: string;
}

const renderImage = (altText: string, rawTarget: string, options: MarkdownRenderOptions): string => {
  const { url } = splitMarkdownTarget(rawTarget);
  const trimmedUrl = url.trim();
  const safeUrl = isSafeUrl(trimmedUrl) ? escapeHtml(trimmedUrl) : '#';
  const safeAltText = altText.trim();

  if (!options.enableImageLightbox || safeUrl === '#') {
    return `<img src="${safeUrl}" alt="${safeAltText}" loading="lazy" />`;
  }

  const ariaLabel = safeAltText ? `Open larger image: ${safeAltText}` : 'Open larger image';
  return `<img src="${safeUrl}" alt="${safeAltText}" loading="lazy" class="markdown-lightbox-image" role="button" tabindex="0" data-lightbox-src="${safeUrl}" data-lightbox-alt="${safeAltText}" aria-label="${ariaLabel}" />`;
};

const renderLink = (label: string, rawTarget: string, options: MarkdownRenderOptions): string => {
  const { url, title } = splitMarkdownTarget(rawTarget);
  const rawUrl = url.trim();
  const resolvedUrl = options.transformLinkUrl?.(rawUrl) ?? rawUrl;
  const safeUrl = isSafeUrl(resolvedUrl) ? escapeHtml(resolvedUrl) : '#';
  const safeLabel = label.trim();
  const externalAttrs = isExternalUrl(resolvedUrl) ? ' target="_blank" rel="noreferrer noopener"' : '';

  if (isDownloadLink(label, resolvedUrl, title)) {
    const downloadAttr = isExternalUrl(resolvedUrl) ? '' : ' download';
    return `<a class="markdown-download" href="${safeUrl}"${externalAttrs}${downloadAttr}><span class="markdown-download__icon" aria-hidden="true">↓</span><span>${safeLabel}</span></a>`;
  }

  return `<a href="${safeUrl}"${externalAttrs}>${safeLabel}</a>`;
};

const renderInline = (value: string, options: MarkdownRenderOptions): string => {
  let text = escapeHtml(value);

  text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_match, altText: string, target: string) => renderImage(altText, target, options));
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label: string, target: string) => renderLink(label, target, options));

  return text;
};

const renderParagraph = (lines: string[], options: MarkdownRenderOptions): string => `<p>${renderInline(lines.join(' '), options)}</p>`;

const renderList = (items: string[], options: MarkdownRenderOptions, ordered = false): string => {
  const tag = ordered ? 'ol' : 'ul';
  const inner = items.map((item) => `<li>${renderInline(item, options)}</li>`).join('');
  return `<${tag}>${inner}</${tag}>`;
};

const renderBlockquote = (lines: string[], options: MarkdownRenderOptions): string => {
  const inner = lines.map((line) => `<p>${renderInline(line, options)}</p>`).join('');
  return `<blockquote>${inner}</blockquote>`;
};

const renderCodeBlock = (lines: string[]): string => `<pre><code>${escapeHtml(lines.join('\n'))}</code></pre>`;

const isOrderedListLine = (line: string): boolean => /^\s*\d+[.)]\s+/.test(line);
const isUnorderedListLine = (line: string): boolean => /^\s*[-*]\s+/.test(line);


export const extractMarkdownImages = (markdown: string): MarkdownImageReference[] => {
  const images: MarkdownImageReference[] = [];
  const imagePattern = /!\[([^\]]*)\]\(([^)]+)\)/g;
  let match: RegExpExecArray | null;

  while ((match = imagePattern.exec(markdown)) !== null) {
    const { url, title } = splitMarkdownTarget(match[2] ?? '');
    const trimmedUrl = url.trim();

    if (!isSafeUrl(trimmedUrl)) {
      continue;
    }

    images.push({
      url: trimmedUrl,
      alt: (match[1] ?? '').trim(),
      title,
    });
  }

  return images;
};

export const buildMarkdownDownloadLink = (label: string, url: string): string => {
  const safeLabel = label.replace(/[\r\n]+/g, ' ').replace(/\]/g, '\\]').trim() || 'Download file';
  return `[${safeLabel}](${url.trim()} "download")`;
};

export const renderMarkdownToHtml = (markdown: string, options: MarkdownRenderOptions = {}): string => {
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
      blocks.push(`<h3>${renderInline(trimmed.replace(/^###\s+/, ''), options)}</h3>`);
      index += 1;
      continue;
    }

    if (/^##\s+/.test(trimmed)) {
      blocks.push(`<h2>${renderInline(trimmed.replace(/^##\s+/, ''), options)}</h2>`);
      index += 1;
      continue;
    }

    if (/^#\s+/.test(trimmed)) {
      blocks.push(`<h1>${renderInline(trimmed.replace(/^#\s+/, ''), options)}</h1>`);
      index += 1;
      continue;
    }

    if (trimmed.startsWith('>')) {
      const quoteLines: string[] = [];
      while (index < lines.length && lines[index].trim().startsWith('>')) {
        quoteLines.push(lines[index].trim().replace(/^>\s?/, ''));
        index += 1;
      }
      blocks.push(renderBlockquote(quoteLines, options));
      continue;
    }

    if (isUnorderedListLine(trimmed)) {
      const items: string[] = [];
      while (index < lines.length && isUnorderedListLine(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^[-*]\s+/, ''));
        index += 1;
      }
      blocks.push(renderList(items, options));
      continue;
    }

    if (isOrderedListLine(trimmed)) {
      const items: string[] = [];
      while (index < lines.length && isOrderedListLine(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^\d+[.)]\s+/, ''));
        index += 1;
      }
      blocks.push(renderList(items, options, true));
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
    blocks.push(renderParagraph(paragraphLines, options));
  }

  return blocks.join('');
};
