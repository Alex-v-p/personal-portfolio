export interface AdminSkillCategory {
  id: string;
  name: string;
  nameNl?: string | null;
  description?: string | null;
  descriptionNl?: string | null;
  iconKey?: string | null;
  sortOrder: number;
}

export interface AdminSkillCategoryUpsert {
  name: string;
  nameNl?: string | null;
  description?: string | null;
  descriptionNl?: string | null;
  iconKey?: string | null;
  sortOrder: number;
}

export interface AdminSkillOption {
  id: string;
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface AdminSkillUpsert {
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface AdminBlogTag {
  id: string;
  name: string;
  slug: string;
}

export interface AdminBlogTagUpsert {
  name: string;
  slug?: string | null;
}
