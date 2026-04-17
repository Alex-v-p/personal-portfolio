export interface CollectionResponse<T> {
  items?: T[] | null;
  total?: number;
}

export interface MediaApi {
  id: string;
  url: string;
  alt?: string | null;
  fileName?: string | null;
  mimeType?: string | null;
  width?: number | null;
  height?: number | null;
}

export interface SkillApi {
  id: string;
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface ExpertiseSkillApi {
  name: string;
  yearsOfExperience?: number | null;
}

export interface ExpertiseGroupApi {
  title: string;
  tags: string[];
  skills?: ExpertiseSkillApi[] | null;
}
