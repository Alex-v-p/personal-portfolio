import {
  AdminBlogPost,
  AdminExperience,
  AdminGithubSnapshot,
  AdminMediaFile,
  AdminSkillCategory,
} from '../../shared/models/admin.model';

export type AdminMediaKind = 'image' | 'document' | 'video' | 'audio' | 'archive' | 'other';

export function isImageMedia(media: AdminMediaFile): boolean {
  if (!media.mimeType && !media.originalFilename) {
    return false;
  }

  return media.mimeType?.startsWith('image/') ?? /\.(png|jpe?g|gif|webp|svg)$/i.test(media.originalFilename || media.objectKey || '');
}

export function mediaFolder(media: AdminMediaFile): string {
  const parts = (media.objectKey || '').split('/').filter(Boolean);
  if (parts.length <= 1) {
    return 'root';
  }

  return parts.slice(0, -1).join('/');
}

export function mediaKind(media: AdminMediaFile): AdminMediaKind {
  if (isImageMedia(media)) {
    return 'image';
  }

  const mimeType = (media.mimeType || '').toLowerCase();
  const fileName = (media.originalFilename || media.objectKey || '').toLowerCase();

  if (mimeType.startsWith('video/') || /\.(mp4|mov|avi|m4v|webm)$/i.test(fileName)) {
    return 'video';
  }
  if (mimeType.startsWith('audio/') || /\.(mp3|wav|ogg|m4a|flac)$/i.test(fileName)) {
    return 'audio';
  }
  if (
    mimeType.includes('pdf')
    || mimeType.includes('officedocument')
    || mimeType.includes('msword')
    || mimeType.startsWith('text/')
    || /\.(pdf|docx?|xlsx?|pptx?|txt|md)$/i.test(fileName)
  ) {
    return 'document';
  }
  if (mimeType.includes('zip') || mimeType.includes('tar') || /\.(zip|rar|7z|tar|gz)$/i.test(fileName)) {
    return 'archive';
  }

  return 'other';
}

export function mediaKindLabel(media: AdminMediaFile): string {
  const kind = mediaKind(media);
  return kind.charAt(0).toUpperCase() + kind.slice(1);
}

export function categoryName(skillCategories: AdminSkillCategory[], categoryId: string): string {
  return skillCategories.find((item) => item.id === categoryId)?.name ?? 'Unknown category';
}

export function contributionPreview(snapshot: AdminGithubSnapshot): string {
  return `${snapshot.contributionDays.length} day entries`;
}

export function formatTagSummary(post: AdminBlogPost): string {
  return post.tagNames.join(', ') || 'No tags';
}

export function formatSkillSummary(experience: AdminExperience): string {
  return experience.skills.map((skill) => skill.name).join(', ') || 'No skills';
}
