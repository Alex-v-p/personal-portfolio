import { ContactMethod } from '@domains/profile/model/contact-method.model';
import { ExpertiseGroup, ExpertiseSkill, Profile } from '@domains/profile/model/profile.model';
import { NavigationItem, SiteShellData } from '@domains/profile/model/site-shell.model';
import { SocialLink } from '@domains/profile/model/social-link.model';

import { normalizeMedia } from './common.mappers';
import { ContactMethodApi, NavigationItemApi, ProfileApi, SiteShellApi, SocialLinkApi } from './profile.contracts';
import { ExpertiseGroupApi, ExpertiseSkillApi } from './common.contracts';

export function normalizeNavigationItem(item: NavigationItemApi): NavigationItem {
  return {
    id: item.id,
    label: item.label,
    routePath: item.routePath,
    isExternal: item.isExternal,
    sortOrder: item.sortOrder,
    isVisible: item.isVisible,
  };
}

export function normalizeSocialLinks(items: SocialLinkApi[] | null | undefined): SocialLink[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((link) => ({
    id: link.id,
    profileId: link.profileId,
    platform: link.platform,
    label: link.label,
    url: link.url,
    iconKey: link.iconKey ?? '',
    sortOrder: link.sortOrder,
    isVisible: link.isVisible,
  }));
}

export function normalizeContactMethods(items: ContactMethodApi[] | null | undefined): ContactMethod[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((item) => ({
    id: item.id,
    platform: item.platform,
    label: item.label,
    value: item.value,
    href: item.href,
    actionLabel: item.actionLabel,
    iconKey: item.iconKey ?? undefined,
    description: item.description ?? undefined,
    sortOrder: item.sortOrder,
    isVisible: item.isVisible,
  }));
}

export function normalizeExpertiseSkill(skill: ExpertiseSkillApi | null | undefined): ExpertiseSkill | null {
  if (!skill?.name) {
    return null;
  }

  return {
    name: skill.name,
    yearsOfExperience: skill.yearsOfExperience ?? null,
    iconKey: skill.iconKey ?? undefined,
  };
}

export function normalizeExpertiseGroups(items: ExpertiseGroupApi[] | null | undefined): ExpertiseGroup[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((group) => {
    const normalizedSkills = Array.isArray(group.skills)
      ? group.skills
          .map((skill) => normalizeExpertiseSkill(skill))
          .filter((skill): skill is ExpertiseSkill => skill !== null)
      : [];

    const fallbackSkills = normalizedSkills.length
      ? normalizedSkills
      : (group.tags ?? []).map((tag) => parseExpertiseSkillFromTag(tag));

    return {
      title: group.title,
      iconKey: group.iconKey ?? undefined,
      tags: Array.isArray(group.tags) ? group.tags : [],
      skills: fallbackSkills,
    };
  });
}

export function normalizeProfile(profile: ProfileApi): Profile {
  const fullName = [profile.firstName, profile.lastName].filter(Boolean).join(' ').trim();
  const longBio = profile.longBio ?? '';
  const shortIntro = profile.shortIntro ?? '';
  const headline = profile.headline ?? 'Portfolio Builder';
  const socialLinks = normalizeSocialLinks(profile.socialLinks);
  const heroActions = [
    toHeroAction(profile.ctaPrimaryLabel, profile.ctaPrimaryUrl, 'primary'),
    toHeroAction(profile.ctaSecondaryLabel, profile.ctaSecondaryUrl, 'secondary'),
  ].filter((action): action is Profile['heroActions'][number] => action !== null);

  const longBioParagraphs = longBio
    .split(/\n\s*\n/g)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  const introParagraphs = (Array.isArray(profile.introParagraphs) && profile.introParagraphs.length
    ? profile.introParagraphs
    : longBioParagraphs
  )
    .map((paragraph) => paragraph.trim())
    .filter(Boolean)
    .filter((paragraph, index, items) => items.indexOf(paragraph) === index)
    .filter((paragraph) => paragraph !== shortIntro.trim());

  return {
    id: profile.id,
    firstName: profile.firstName,
    lastName: profile.lastName,
    name: fullName,
    headline,
    role: headline,
    greeting: `Hi, I'm ${profile.firstName} !`,
    location: profile.location ?? '',
    email: profile.email ?? '',
    phone: profile.phone ?? '',
    shortIntro,
    longBio,
    heroTitle: `I’m ${headline}`,
    summary: shortIntro || longBio,
    shortBio: shortIntro || longBio,
    footerDescription: shortIntro || profile.footerDescription || longBio,
    avatarFileId: profile.avatarFileId ?? null,
    heroImageFileId: profile.heroImageFileId ?? null,
    resumeFileId: profile.resumeFileId ?? null,
    avatarUrl: normalizeMedia(profile.avatar)?.url ?? '',
    heroImageUrl: normalizeMedia(profile.heroImage)?.url ?? '',
    resumeUrl: normalizeMedia(profile.resume)?.url ?? '',
    skills: Array.isArray(profile.skills) ? profile.skills : [],
    expertiseGroups: normalizeExpertiseGroups(profile.expertiseGroups),
    introParagraphs,
    availability: Array.isArray(profile.availability) ? profile.availability : [],
    heroActions,
    socialLinks,
    createdAt: profile.createdAt,
    updatedAt: profile.updatedAt,
  };
}

export function normalizeSiteShell(shell: SiteShellApi): SiteShellData {
  return {
    navigation: (shell.navigation.items ?? []).map((item) => normalizeNavigationItem(item)),
    profile: normalizeProfile(shell.profile),
    footerText: shell.footerText ?? '',
    contactMethods: normalizeContactMethods(shell.contactMethods),
  };
}

function parseExpertiseSkillFromTag(tag: string): ExpertiseSkill {
  const trimmedTag = tag.trim();
  const match = trimmedTag.match(/^(.*?)\s*[-·]\s*(\d+)y$/i);

  if (!match) {
    return { name: trimmedTag, yearsOfExperience: null, iconKey: undefined };
  }

  return {
    name: match[1].trim(),
    yearsOfExperience: Number.parseInt(match[2], 10) || null,
    iconKey: undefined,
  };
}

function toHeroAction(
  label: string | null | undefined,
  url: string | null | undefined,
  appearance: 'primary' | 'secondary' | 'ghost'
): Profile['heroActions'][number] | null {
  if (!label || !url) {
    return null;
  }

  if (url.startsWith('/')) {
    return {
      label,
      appearance,
      routerLink: url,
      openInNewTab: false,
    };
  }

  return {
    label,
    appearance,
    href: url,
    openInNewTab: true,
  };
}
