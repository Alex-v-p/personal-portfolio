import { describe, expect, it } from 'vitest';

import { getIconDefinition, getOrderedIconOptions, normalizeIconKey, resolveIconKey } from './icon-registry';

describe('icon registry', () => {
  it('normalizes icon keys and resolves aliases', () => {
    expect(normalizeIconKey(' Tailwind CSS ')).toBe('tailwind-css');
    expect(resolveIconKey('email')).toBe('mail');
    expect(resolveIconKey('tailwind')).toBe('tailwindcss');
    expect(resolveIconKey('x')).toBe('twitter');
  });

  it('returns icon definitions for supported keys', () => {
    const github = getIconDefinition('github');

    expect(github?.key).toBe('github');
    expect(github?.group).toBe('social');
    expect(github?.svg).toContain('<svg');
  });

  it('returns grouped icon options for future CMS pickers', () => {
    const groupedOptions = getOrderedIconOptions();

    expect(groupedOptions.social.some((option) => option.key === 'github')).toBe(true);
    expect(groupedOptions.contact.some((option) => option.key === 'mail')).toBe(true);
    expect(groupedOptions.expertise.some((option) => option.key === 'brain')).toBe(true);
    expect(groupedOptions.tech.some((option) => option.key === 'angular')).toBe(true);
  });
});
