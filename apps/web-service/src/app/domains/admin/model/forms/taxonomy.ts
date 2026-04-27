import { AdminBlogTag, AdminSkillCategory, AdminSkillOption } from '@domains/admin/model/admin.model';

export interface AdminSkillCategoryForm {
  id?: string | null;
  name: string;
  nameNl: string;
  description: string;
  descriptionNl: string;
  iconKey: string;
  sortOrder: number;
}

export interface AdminSkillForm {
  id?: string | null;
  categoryId: string;
  name: string;
  yearsOfExperience: number | null;
  proficiencyLabel: string;
  proficiencyLabelNl: string;
  iconKey: string;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface AdminBlogTagForm {
  id?: string | null;
  name: string;
  slug: string;
}

export function createEmptySkillCategoryForm(): AdminSkillCategoryForm {
  return { name: '', nameNl: '', description: '', descriptionNl: '', iconKey: '', sortOrder: 0 };
}

export function createEmptySkillForm(): AdminSkillForm {
  return { categoryId: '', name: '', yearsOfExperience: null, proficiencyLabel: '', proficiencyLabelNl: '', iconKey: '', sortOrder: 0, isHighlighted: false };
}

export function createEmptyBlogTagForm(): AdminBlogTagForm {
  return { name: '', slug: '' };
}

export function toSkillCategoryForm(category: AdminSkillCategory): AdminSkillCategoryForm {
  return {
    id: category.id,
    name: category.name,
    nameNl: category.nameNl ?? '',
    description: category.description ?? '',
    descriptionNl: category.descriptionNl ?? '',
    iconKey: category.iconKey ?? '',
    sortOrder: category.sortOrder,
  };
}

export function toSkillForm(skill: AdminSkillOption): AdminSkillForm {
  return {
    id: skill.id,
    categoryId: skill.categoryId,
    name: skill.name,
    yearsOfExperience: skill.yearsOfExperience ?? null,
    proficiencyLabel: skill.proficiencyLabel ?? '',
    proficiencyLabelNl: skill.proficiencyLabelNl ?? '',
    iconKey: skill.iconKey ?? '',
    sortOrder: skill.sortOrder,
    isHighlighted: skill.isHighlighted,
  };
}

export function toBlogTagForm(tag: AdminBlogTag): AdminBlogTagForm {
  return { id: tag.id, name: tag.name, slug: tag.slug };
}
