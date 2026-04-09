export interface Skill {
  id: string;
  categoryId: string;
  name: string;
  yearsOfExperience?: number;
  iconKey?: string;
  sortOrder: number;
  isHighlighted: boolean;
}
