import { DatePipe, NgClass, NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import {
  AdminBlogPost,
  AdminBlogTag,
  AdminContactMessage,
  AdminDashboardSummary,
  AdminExperience,
  AdminGithubContributionDay,
  AdminGithubSnapshot,
  AdminMediaFile,
  AdminNavigationItem,
  AdminProfile,
  AdminProject,
  AdminReferenceData,
  AdminSkillCategory,
  AdminSkillOption,
  AdminSocialLink,
  AdminUser,
} from '../../shared/models/admin.model';
import { AdminPortfolioApiService } from '../../shared/services/admin-portfolio-api.service';
import { AdminSessionService } from '../../shared/services/admin-session.service';

interface ScopedUploadForm {
  title: string;
  altText: string;
  description: string;
  visibility: 'public' | 'private' | 'signed';
  file: File | null;
}

interface AdminProjectForm {
  id?: string | null;
  slug: string;
  title: string;
  teaser: string;
  summary: string;
  descriptionMarkdown: string;
  coverImageFileId: string | null;
  githubUrl: string;
  githubRepoOwner: string;
  githubRepoName: string;
  demoUrl: string;
  companyName: string;
  startedOn: string;
  endedOn: string;
  durationLabel: string;
  status: string;
  state: 'published' | 'archived' | 'completed' | 'paused';
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  skillIds: string[];
}

interface AdminBlogPostForm {
  id?: string | null;
  slug: string;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId: string | null;
  coverImageAlt: string;
  readingTimeMinutes: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt: string;
  seoTitle: string;
  seoDescription: string;
  tagIds: string[];
}

interface AdminProfileForm {
  id?: string;
  firstName: string;
  lastName: string;
  headline: string;
  shortIntro: string;
  longBio: string;
  location: string;
  email: string;
  phone: string;
  avatarFileId: string | null;
  heroImageFileId: string | null;
  resumeFileId: string | null;
  ctaPrimaryLabel: string;
  ctaPrimaryUrl: string;
  ctaSecondaryLabel: string;
  ctaSecondaryUrl: string;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
}

interface AdminSkillCategoryForm {
  id?: string | null;
  name: string;
  description: string;
  sortOrder: number;
}

interface AdminSkillForm {
  id?: string | null;
  categoryId: string;
  name: string;
  yearsOfExperience: number | null;
  iconKey: string;
  sortOrder: number;
  isHighlighted: boolean;
}

interface AdminBlogTagForm {
  id?: string | null;
  name: string;
  slug: string;
}

interface AdminExperienceForm {
  id?: string | null;
  organizationName: string;
  roleTitle: string;
  location: string;
  experienceType: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown: string;
  logoFileId: string | null;
  sortOrder: number;
  skillIds: string[];
}

interface AdminNavigationItemForm {
  id?: string | null;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

interface AdminUserForm {
  id?: string | null;
  email: string;
  displayName: string;
  password: string;
  isActive: boolean;
}

interface AdminGithubSnapshotForm {
  id?: string | null;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount: number | null;
  followingCount: number | null;
  totalStars: number | null;
  totalCommits: number | null;
  rawPayloadText: string;
  contributionDaysText: string;
}

@Component({
  selector: 'app-admin-page',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule, DatePipe],
  templateUrl: './admin.page.html'
})
export class AdminPageComponent implements OnInit {
  private readonly adminApi = inject(AdminPortfolioApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected readonly tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'projects', label: 'Projects' },
    { id: 'blog', label: 'Blog' },
    { id: 'taxonomy', label: 'Taxonomy' },
    { id: 'experience', label: 'Experience' },
    { id: 'navigation', label: 'Navigation' },
    { id: 'profile', label: 'Profile' },
    { id: 'stats', label: 'GitHub / Stats' },
    { id: 'admins', label: 'Admin users' },
    { id: 'messages', label: 'Messages' },
  ] as const;

  protected activeTab: typeof this.tabs[number]['id'] = 'overview';
  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected dashboard: AdminDashboardSummary = {
    projects: 0,
    blogPosts: 0,
    unreadMessages: 0,
    skills: 0,
    skillCategories: 0,
    mediaFiles: 0,
    experiences: 0,
    navigationItems: 0,
    blogTags: 0,
    adminUsers: 0,
    githubSnapshots: 0,
  };
  protected referenceData: AdminReferenceData = {
    skills: [],
    skillCategories: [],
    mediaFiles: [],
    blogTags: [],
    projectStates: ['published', 'archived', 'completed', 'paused'],
    publicationStatuses: ['draft', 'published', 'archived'],
  };
  protected projects: AdminProject[] = [];
  protected blogPosts: AdminBlogPost[] = [];
  protected experiences: AdminExperience[] = [];
  protected navigationItems: AdminNavigationItem[] = [];
  protected adminUsers: AdminUser[] = [];
  protected githubSnapshots: AdminGithubSnapshot[] = [];
  protected profile: AdminProfile | null = null;
  protected messages: AdminContactMessage[] = [];

  protected selectedProjectId: string | null = null;
  protected selectedBlogPostId: string | null = null;
  protected selectedSkillCategoryId: string | null = null;
  protected selectedSkillId: string | null = null;
  protected selectedBlogTagId: string | null = null;
  protected selectedExperienceId: string | null = null;
  protected selectedNavigationItemId: string | null = null;
  protected selectedAdminUserId: string | null = null;
  protected selectedGithubSnapshotId: string | null = null;

  protected projectForm: AdminProjectForm = this.createEmptyProjectForm();
  protected blogPostForm: AdminBlogPostForm = this.createEmptyBlogPostForm();
  protected profileForm: AdminProfileForm = this.createEmptyProfileForm();
  protected skillCategoryForm: AdminSkillCategoryForm = this.createEmptySkillCategoryForm();
  protected skillForm: AdminSkillForm = this.createEmptySkillForm();
  protected blogTagForm: AdminBlogTagForm = this.createEmptyBlogTagForm();
  protected experienceForm: AdminExperienceForm = this.createEmptyExperienceForm();
  protected navigationItemForm: AdminNavigationItemForm = this.createEmptyNavigationItemForm();
  protected adminUserForm: AdminUserForm = this.createEmptyAdminUserForm();
  protected githubSnapshotForm: AdminGithubSnapshotForm = this.createEmptyGithubSnapshotForm();

  protected projectUploadForm: ScopedUploadForm = this.createEmptyScopedUploadForm();
  protected blogUploadForm: ScopedUploadForm = this.createEmptyScopedUploadForm();
  protected experienceUploadForm: ScopedUploadForm = this.createEmptyScopedUploadForm();
  protected profileAvatarUploadForm: ScopedUploadForm = this.createEmptyScopedUploadForm();
  protected profileHeroUploadForm: ScopedUploadForm = this.createEmptyScopedUploadForm();
  protected profileResumeUploadForm: ScopedUploadForm = this.createEmptyScopedUploadForm();
  protected uploadInProgressKey: string | null = null;

  ngOnInit(): void {
    this.loadCms();
  }

  protected setActiveTab(tabId: typeof this.activeTab): void {
    this.activeTab = tabId;
  }

  protected logout(): void {
    this.adminSession.logout();
  }

  protected loadCms(): void {
    const currentSelections = {
      project: this.selectedProjectId,
      blogPost: this.selectedBlogPostId,
      skillCategory: this.selectedSkillCategoryId,
      skill: this.selectedSkillId,
      blogTag: this.selectedBlogTagId,
      experience: this.selectedExperienceId,
      navigation: this.selectedNavigationItemId,
      adminUser: this.selectedAdminUserId,
      github: this.selectedGithubSnapshotId,
    };

    this.isLoading = true;
    this.errorMessage = '';

    forkJoin({
      dashboard: this.adminApi.getDashboardSummary(),
      referenceData: this.adminApi.getReferenceData(),
      projects: this.adminApi.getProjects(),
      blogPosts: this.adminApi.getBlogPosts(),
      experiences: this.adminApi.getExperiences(),
      navigationItems: this.adminApi.getNavigationItems(),
      adminUsers: this.adminApi.listAdminUsers(),
      githubSnapshots: this.adminApi.getGithubSnapshots(),
      profile: this.adminApi.getProfile(),
      messages: this.adminApi.getContactMessages(),
    })
      .pipe(
        take(1),
        finalize(() => {
          this.isLoading = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: (result) => {
          this.dashboard = result.dashboard;
          this.referenceData = result.referenceData;
          this.projects = result.projects.items;
          this.blogPosts = result.blogPosts.items;
          this.experiences = result.experiences.items;
          this.navigationItems = result.navigationItems.items;
          this.adminUsers = result.adminUsers;
          this.githubSnapshots = result.githubSnapshots.items;
          this.profile = result.profile;
          this.messages = result.messages.items;

          this.selectedProjectId = this.resolveSelection(currentSelections.project, this.projects);
          this.selectedBlogPostId = this.resolveSelection(currentSelections.blogPost, this.blogPosts);
          this.selectedSkillCategoryId = this.resolveSelection(currentSelections.skillCategory, this.referenceData.skillCategories);
          this.selectedSkillId = this.resolveSelection(currentSelections.skill, this.referenceData.skills);
          this.selectedBlogTagId = this.resolveSelection(currentSelections.blogTag, this.referenceData.blogTags);
          this.selectedExperienceId = this.resolveSelection(currentSelections.experience, this.experiences);
          this.selectedNavigationItemId = this.resolveSelection(currentSelections.navigation, this.navigationItems);
          this.selectedAdminUserId = this.resolveSelection(currentSelections.adminUser, this.adminUsers);
          this.selectedGithubSnapshotId = this.resolveSelection(currentSelections.github, this.githubSnapshots);

          this.projectForm = this.selectedProjectId ? this.toProjectForm(this.projects.find((item) => item.id === this.selectedProjectId)!) : this.createEmptyProjectForm();
          this.blogPostForm = this.selectedBlogPostId ? this.toBlogPostForm(this.blogPosts.find((item) => item.id === this.selectedBlogPostId)!) : this.createEmptyBlogPostForm();
          this.profileForm = this.profile ? this.toProfileForm(this.profile) : this.createEmptyProfileForm();
          this.skillCategoryForm = this.selectedSkillCategoryId ? this.toSkillCategoryForm(this.referenceData.skillCategories.find((item) => item.id === this.selectedSkillCategoryId)!) : this.createEmptySkillCategoryForm();
          this.skillForm = this.selectedSkillId ? this.toSkillForm(this.referenceData.skills.find((item) => item.id === this.selectedSkillId)!) : this.createEmptySkillForm();
          this.blogTagForm = this.selectedBlogTagId ? this.toBlogTagForm(this.referenceData.blogTags.find((item) => item.id === this.selectedBlogTagId)!) : this.createEmptyBlogTagForm();
          this.experienceForm = this.selectedExperienceId ? this.toExperienceForm(this.experiences.find((item) => item.id === this.selectedExperienceId)!) : this.createEmptyExperienceForm();
          this.navigationItemForm = this.selectedNavigationItemId ? this.toNavigationItemForm(this.navigationItems.find((item) => item.id === this.selectedNavigationItemId)!) : this.createEmptyNavigationItemForm();
          this.adminUserForm = this.selectedAdminUserId ? this.toAdminUserForm(this.adminUsers.find((item) => item.id === this.selectedAdminUserId)!) : this.createEmptyAdminUserForm();
          this.githubSnapshotForm = this.selectedGithubSnapshotId ? this.toGithubSnapshotForm(this.githubSnapshots.find((item) => item.id === this.selectedGithubSnapshotId)!) : this.createEmptyGithubSnapshotForm();
        },
        error: (error) => {
          if (error?.status === 401) {
            this.adminSession.logout();
            return;
          }
          this.errorMessage = 'The CMS data could not be loaded. Check that the API is running and that your admin token is still valid.';
        }
      });
  }

  protected get adminDisplayName(): string {
    return this.adminSession.currentUser?.displayName ?? 'Admin';
  }

  protected get currentAdminId(): string | null {
    return this.adminSession.currentUser?.id ?? null;
  }

  protected mediaPreview(mediaId: string | null | undefined): AdminMediaFile | undefined {
    return this.referenceData.mediaFiles.find((item) => item.id === mediaId);
  }

  protected categoryName(categoryId: string): string {
    return this.referenceData.skillCategories.find((item) => item.id === categoryId)?.name ?? 'Unknown category';
  }

  protected contributionPreview(snapshot: AdminGithubSnapshot): string {
    return `${snapshot.contributionDays.length} day entries`;
  }

  protected formatTagSummary(post: AdminBlogPost): string {
    return post.tagNames.join(', ') || 'No tags';
  }

  protected formatSkillSummary(experience: AdminExperience): string {
    return experience.skills.map((skill) => skill.name).join(', ') || 'No skills';
  }

  protected selectProject(projectId: string): void {
    this.selectedProjectId = projectId;
    const project = this.projects.find((item) => item.id === projectId);
    if (project) {
      this.projectForm = this.toProjectForm(project);
      this.statusMessage = '';
    }
  }

  protected startNewProject(): void {
    this.selectedProjectId = null;
    this.projectForm = this.createEmptyProjectForm();
    this.projectUploadForm = this.createEmptyScopedUploadForm();
  }

  protected toggleProjectSkill(skillId: string): void {
    this.projectForm.skillIds = this.toggleSelection(this.projectForm.skillIds, skillId);
  }

  protected saveProject(): void {
    this.statusMessage = 'Saving project…';
    const payload = {
      slug: this.projectForm.slug || null,
      title: this.projectForm.title,
      teaser: this.projectForm.teaser,
      summary: this.projectForm.summary || null,
      descriptionMarkdown: this.projectForm.descriptionMarkdown || null,
      coverImageFileId: this.projectForm.coverImageFileId || null,
      githubUrl: this.projectForm.githubUrl || null,
      githubRepoOwner: this.projectForm.githubRepoOwner || null,
      githubRepoName: this.projectForm.githubRepoName || null,
      demoUrl: this.projectForm.demoUrl || null,
      companyName: this.projectForm.companyName || null,
      startedOn: this.projectForm.startedOn || null,
      endedOn: this.projectForm.endedOn || null,
      durationLabel: this.projectForm.durationLabel,
      status: this.projectForm.status,
      state: this.projectForm.state,
      isFeatured: this.projectForm.isFeatured,
      sortOrder: this.projectForm.sortOrder,
      publishedAt: this.projectForm.publishedAt || null,
      skillIds: [...this.projectForm.skillIds],
    };
    const request$ = this.selectedProjectId
      ? this.adminApi.updateProject(this.selectedProjectId, payload)
      : this.adminApi.createProject(payload);

    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedProjectId ? 'Project updated.' : 'Project created.';
        this.loadCms();
        this.activeTab = 'projects';
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the project failed.';
      }
    });
  }

  protected deleteProject(): void {
    if (!this.selectedProjectId || !confirm('Delete this project?')) {
      return;
    }
    this.adminApi.deleteProject(this.selectedProjectId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Project deleted.';
        this.startNewProject();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the project failed.';
      }
    });
  }

  protected selectBlogPost(postId: string): void {
    this.selectedBlogPostId = postId;
    const post = this.blogPosts.find((item) => item.id === postId);
    if (post) {
      this.blogPostForm = this.toBlogPostForm(post);
      this.statusMessage = '';
    }
  }

  protected startNewBlogPost(): void {
    this.selectedBlogPostId = null;
    this.blogPostForm = this.createEmptyBlogPostForm();
    this.blogUploadForm = this.createEmptyScopedUploadForm();
  }

  protected toggleBlogTag(tagId: string): void {
    this.blogPostForm.tagIds = this.toggleSelection(this.blogPostForm.tagIds, tagId);
  }

  protected saveBlogPost(): void {
    const payload = {
      slug: this.blogPostForm.slug || null,
      title: this.blogPostForm.title,
      excerpt: this.blogPostForm.excerpt,
      contentMarkdown: this.blogPostForm.contentMarkdown,
      coverImageFileId: this.blogPostForm.coverImageFileId || null,
      coverImageAlt: this.blogPostForm.coverImageAlt || null,
      readingTimeMinutes: this.blogPostForm.readingTimeMinutes,
      status: this.blogPostForm.status,
      isFeatured: this.blogPostForm.isFeatured,
      publishedAt: this.blogPostForm.publishedAt || null,
      seoTitle: this.blogPostForm.seoTitle || null,
      seoDescription: this.blogPostForm.seoDescription || null,
      tagIds: [...this.blogPostForm.tagIds],
    };
    const request$ = this.selectedBlogPostId
      ? this.adminApi.updateBlogPost(this.selectedBlogPostId, payload)
      : this.adminApi.createBlogPost(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedBlogPostId ? 'Blog post updated.' : 'Blog post created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the blog post failed.';
      }
    });
  }

  protected deleteBlogPost(): void {
    if (!this.selectedBlogPostId || !confirm('Delete this blog post?')) {
      return;
    }
    this.adminApi.deleteBlogPost(this.selectedBlogPostId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Blog post deleted.';
        this.startNewBlogPost();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the blog post failed.';
      }
    });
  }

  protected selectSkillCategory(categoryId: string): void {
    this.selectedSkillCategoryId = categoryId;
    const category = this.referenceData.skillCategories.find((item) => item.id === categoryId);
    if (category) {
      this.skillCategoryForm = this.toSkillCategoryForm(category);
    }
  }

  protected startNewSkillCategory(): void {
    this.selectedSkillCategoryId = null;
    this.skillCategoryForm = this.createEmptySkillCategoryForm();
  }

  protected saveSkillCategory(): void {
    const payload = {
      name: this.skillCategoryForm.name,
      description: this.skillCategoryForm.description || null,
      sortOrder: this.skillCategoryForm.sortOrder,
    };
    const request$ = this.selectedSkillCategoryId
      ? this.adminApi.updateSkillCategory(this.selectedSkillCategoryId, payload)
      : this.adminApi.createSkillCategory(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedSkillCategoryId ? 'Skill category updated.' : 'Skill category created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the skill category failed.';
      }
    });
  }

  protected deleteSkillCategory(): void {
    if (!this.selectedSkillCategoryId || !confirm('Delete this skill category?')) {
      return;
    }
    this.adminApi.deleteSkillCategory(this.selectedSkillCategoryId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Skill category deleted.';
        this.startNewSkillCategory();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the skill category failed.';
      }
    });
  }

  protected selectSkill(skillId: string): void {
    this.selectedSkillId = skillId;
    const skill = this.referenceData.skills.find((item) => item.id === skillId);
    if (skill) {
      this.skillForm = this.toSkillForm(skill);
    }
  }

  protected startNewSkill(): void {
    this.selectedSkillId = null;
    this.skillForm = this.createEmptySkillForm();
    this.skillForm.categoryId = this.referenceData.skillCategories[0]?.id ?? '';
  }

  protected saveSkill(): void {
    const payload = {
      categoryId: this.skillForm.categoryId,
      name: this.skillForm.name,
      yearsOfExperience: this.skillForm.yearsOfExperience,
      iconKey: this.skillForm.iconKey || null,
      sortOrder: this.skillForm.sortOrder,
      isHighlighted: this.skillForm.isHighlighted,
    };
    const request$ = this.selectedSkillId
      ? this.adminApi.updateSkill(this.selectedSkillId, payload)
      : this.adminApi.createSkill(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedSkillId ? 'Skill updated.' : 'Skill created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the skill failed.';
      }
    });
  }

  protected deleteSkill(): void {
    if (!this.selectedSkillId || !confirm('Delete this skill?')) {
      return;
    }
    this.adminApi.deleteSkill(this.selectedSkillId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Skill deleted.';
        this.startNewSkill();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the skill failed.';
      }
    });
  }

  protected selectBlogTag(tagId: string): void {
    this.selectedBlogTagId = tagId;
    const tag = this.referenceData.blogTags.find((item) => item.id === tagId);
    if (tag) {
      this.blogTagForm = this.toBlogTagForm(tag);
    }
  }

  protected startNewBlogTag(): void {
    this.selectedBlogTagId = null;
    this.blogTagForm = this.createEmptyBlogTagForm();
  }

  protected saveBlogTag(): void {
    const payload = { name: this.blogTagForm.name, slug: this.blogTagForm.slug || null };
    const request$ = this.selectedBlogTagId
      ? this.adminApi.updateBlogTag(this.selectedBlogTagId, payload)
      : this.adminApi.createBlogTag(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedBlogTagId ? 'Blog tag updated.' : 'Blog tag created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the blog tag failed.';
      }
    });
  }

  protected deleteBlogTag(): void {
    if (!this.selectedBlogTagId || !confirm('Delete this blog tag?')) {
      return;
    }
    this.adminApi.deleteBlogTag(this.selectedBlogTagId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Blog tag deleted.';
        this.startNewBlogTag();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the blog tag failed.';
      }
    });
  }

  protected selectExperience(experienceId: string): void {
    this.selectedExperienceId = experienceId;
    const experience = this.experiences.find((item) => item.id === experienceId);
    if (experience) {
      this.experienceForm = this.toExperienceForm(experience);
    }
  }

  protected startNewExperience(): void {
    this.selectedExperienceId = null;
    this.experienceForm = this.createEmptyExperienceForm();
    this.experienceUploadForm = this.createEmptyScopedUploadForm();
  }

  protected toggleExperienceSkill(skillId: string): void {
    this.experienceForm.skillIds = this.toggleSelection(this.experienceForm.skillIds, skillId);
  }

  protected saveExperience(): void {
    const payload = {
      organizationName: this.experienceForm.organizationName,
      roleTitle: this.experienceForm.roleTitle,
      location: this.experienceForm.location || null,
      experienceType: this.experienceForm.experienceType,
      startDate: this.experienceForm.startDate,
      endDate: this.experienceForm.endDate || null,
      isCurrent: this.experienceForm.isCurrent,
      summary: this.experienceForm.summary,
      descriptionMarkdown: this.experienceForm.descriptionMarkdown || null,
      logoFileId: this.experienceForm.logoFileId || null,
      sortOrder: this.experienceForm.sortOrder,
      skillIds: [...this.experienceForm.skillIds],
    };
    const request$ = this.selectedExperienceId
      ? this.adminApi.updateExperience(this.selectedExperienceId, payload)
      : this.adminApi.createExperience(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedExperienceId ? 'Experience updated.' : 'Experience created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the experience entry failed.';
      }
    });
  }

  protected deleteExperience(): void {
    if (!this.selectedExperienceId || !confirm('Delete this experience entry?')) {
      return;
    }
    this.adminApi.deleteExperience(this.selectedExperienceId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Experience deleted.';
        this.startNewExperience();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the experience entry failed.';
      }
    });
  }

  protected selectNavigationItem(itemId: string): void {
    this.selectedNavigationItemId = itemId;
    const item = this.navigationItems.find((entry) => entry.id === itemId);
    if (item) {
      this.navigationItemForm = this.toNavigationItemForm(item);
    }
  }

  protected startNewNavigationItem(): void {
    this.selectedNavigationItemId = null;
    this.navigationItemForm = this.createEmptyNavigationItemForm();
  }

  protected saveNavigationItem(): void {
    const payload = {
      label: this.navigationItemForm.label,
      routePath: this.navigationItemForm.routePath,
      isExternal: this.navigationItemForm.isExternal,
      sortOrder: this.navigationItemForm.sortOrder,
      isVisible: this.navigationItemForm.isVisible,
    };
    const request$ = this.selectedNavigationItemId
      ? this.adminApi.updateNavigationItem(this.selectedNavigationItemId, payload)
      : this.adminApi.createNavigationItem(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedNavigationItemId ? 'Navigation item updated.' : 'Navigation item created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the navigation item failed.';
      }
    });
  }

  protected deleteNavigationItem(): void {
    if (!this.selectedNavigationItemId || !confirm('Delete this navigation item?')) {
      return;
    }
    this.adminApi.deleteNavigationItem(this.selectedNavigationItemId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Navigation item deleted.';
        this.startNewNavigationItem();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the navigation item failed.';
      }
    });
  }

  protected addSocialLink(): void {
    this.profileForm.socialLinks = [
      ...this.profileForm.socialLinks,
      { platform: '', label: '', url: '', iconKey: null, sortOrder: this.profileForm.socialLinks.length, isVisible: true },
    ];
  }

  protected removeSocialLink(index: number): void {
    this.profileForm.socialLinks = this.profileForm.socialLinks.filter((_, itemIndex) => itemIndex !== index);
  }

  protected saveProfile(): void {
    const payload = {
      firstName: this.profileForm.firstName,
      lastName: this.profileForm.lastName,
      headline: this.profileForm.headline,
      shortIntro: this.profileForm.shortIntro,
      longBio: this.profileForm.longBio || null,
      location: this.profileForm.location || null,
      email: this.profileForm.email || null,
      phone: this.profileForm.phone || null,
      avatarFileId: this.profileForm.avatarFileId || null,
      heroImageFileId: this.profileForm.heroImageFileId || null,
      resumeFileId: this.profileForm.resumeFileId || null,
      ctaPrimaryLabel: this.profileForm.ctaPrimaryLabel || null,
      ctaPrimaryUrl: this.profileForm.ctaPrimaryUrl || null,
      ctaSecondaryLabel: this.profileForm.ctaSecondaryLabel || null,
      ctaSecondaryUrl: this.profileForm.ctaSecondaryUrl || null,
      isPublic: this.profileForm.isPublic,
      socialLinks: this.profileForm.socialLinks.map((link, index) => ({ ...link, sortOrder: index })),
    };
    this.adminApi.updateProfile(payload).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Profile updated.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the profile failed.';
      }
    });
  }

  protected selectAdminUser(adminUserId: string): void {
    this.selectedAdminUserId = adminUserId;
    const user = this.adminUsers.find((item) => item.id === adminUserId);
    if (user) {
      this.adminUserForm = this.toAdminUserForm(user);
    }
  }

  protected startNewAdminUser(): void {
    this.selectedAdminUserId = null;
    this.adminUserForm = this.createEmptyAdminUserForm();
  }

  protected saveAdminUser(): void {
    if (!this.selectedAdminUserId && !this.adminUserForm.password.trim()) {
      this.statusMessage = 'A password is required when creating a new admin user.';
      return;
    }
    const createPayload = {
      email: this.adminUserForm.email,
      displayName: this.adminUserForm.displayName,
      password: this.adminUserForm.password,
      isActive: this.adminUserForm.isActive,
    };
    const updatePayload = {
      email: this.adminUserForm.email,
      displayName: this.adminUserForm.displayName,
      password: this.adminUserForm.password.trim() ? this.adminUserForm.password : null,
      isActive: this.adminUserForm.isActive,
    };
    const request$ = this.selectedAdminUserId
      ? this.adminApi.updateAdminUser(this.selectedAdminUserId, updatePayload)
      : this.adminApi.createAdminUser(createPayload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedAdminUserId ? 'Admin user updated.' : 'Admin user created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the admin user failed.';
      }
    });
  }

  protected deleteAdminUser(): void {
    if (!this.selectedAdminUserId || !confirm('Delete this admin user?')) {
      return;
    }
    this.adminApi.deleteAdminUser(this.selectedAdminUserId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Admin user deleted.';
        this.startNewAdminUser();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the admin user failed.';
      }
    });
  }

  protected selectGithubSnapshot(snapshotId: string): void {
    this.selectedGithubSnapshotId = snapshotId;
    const snapshot = this.githubSnapshots.find((item) => item.id === snapshotId);
    if (snapshot) {
      this.githubSnapshotForm = this.toGithubSnapshotForm(snapshot);
    }
  }

  protected startNewGithubSnapshot(): void {
    this.selectedGithubSnapshotId = null;
    this.githubSnapshotForm = this.createEmptyGithubSnapshotForm();
  }

  protected saveGithubSnapshot(): void {
    let rawPayload: Record<string, unknown> | null = null;
    let contributionDays: AdminGithubContributionDay[] = [];
    try {
      rawPayload = this.parseJsonObject(this.githubSnapshotForm.rawPayloadText);
      contributionDays = this.parseContributionDays(this.githubSnapshotForm.contributionDaysText);
    } catch (error) {
      this.statusMessage = error instanceof Error ? error.message : 'GitHub snapshot JSON could not be parsed.';
      return;
    }

    const payload = {
      snapshotDate: this.githubSnapshotForm.snapshotDate,
      username: this.githubSnapshotForm.username,
      publicRepoCount: this.githubSnapshotForm.publicRepoCount,
      followersCount: this.githubSnapshotForm.followersCount,
      followingCount: this.githubSnapshotForm.followingCount,
      totalStars: this.githubSnapshotForm.totalStars,
      totalCommits: this.githubSnapshotForm.totalCommits,
      rawPayload,
      contributionDays,
    };
    const request$ = this.selectedGithubSnapshotId
      ? this.adminApi.updateGithubSnapshot(this.selectedGithubSnapshotId, payload)
      : this.adminApi.createGithubSnapshot(payload);
    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedGithubSnapshotId ? 'GitHub snapshot updated.' : 'GitHub snapshot created.';
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Saving the GitHub snapshot failed.';
      }
    });
  }

  protected deleteGithubSnapshot(): void {
    if (!this.selectedGithubSnapshotId || !confirm('Delete this GitHub snapshot?')) {
      return;
    }
    this.adminApi.deleteGithubSnapshot(this.selectedGithubSnapshotId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'GitHub snapshot deleted.';
        this.startNewGithubSnapshot();
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the GitHub snapshot failed.';
      }
    });
  }

  protected toggleMessageRead(message: AdminContactMessage): void {
    this.adminApi.updateContactMessage(message.id, !message.isRead).pipe(take(1)).subscribe({
      next: (updatedMessage) => {
        this.messages = this.messages.map((item) => item.id === updatedMessage.id ? updatedMessage : item);
        this.dashboard.unreadMessages = this.messages.filter((item) => !item.isRead).length;
        this.statusMessage = updatedMessage.isRead ? 'Message marked as read.' : 'Message marked as unread.';
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Updating message status failed.';
      }
    });
  }

  protected onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    const input = event.target as HTMLInputElement | null;
    form.file = input?.files?.[0] ?? null;
  }

  protected uploadProjectCover(): void {
    this.uploadScopedMedia('project-cover', this.projectUploadForm, this.buildProjectFolder(), (media) => {
      this.projectForm.coverImageFileId = media.id;
    });
  }

  protected uploadBlogCover(): void {
    this.uploadScopedMedia('blog-cover', this.blogUploadForm, this.buildBlogFolder(), (media) => {
      this.blogPostForm.coverImageFileId = media.id;
      if (!this.blogPostForm.coverImageAlt) {
        this.blogPostForm.coverImageAlt = this.blogUploadForm.altText;
      }
    });
  }

  protected uploadExperienceLogo(): void {
    this.uploadScopedMedia('experience-logo', this.experienceUploadForm, this.buildExperienceFolder(), (media) => {
      this.experienceForm.logoFileId = media.id;
    });
  }

  protected uploadProfileAvatar(): void {
    this.uploadScopedMedia('profile-avatar', this.profileAvatarUploadForm, this.buildProfileFolder(), (media) => {
      this.profileForm.avatarFileId = media.id;
    });
  }

  protected uploadProfileHero(): void {
    this.uploadScopedMedia('profile-hero', this.profileHeroUploadForm, this.buildProfileFolder(), (media) => {
      this.profileForm.heroImageFileId = media.id;
    });
  }

  protected uploadProfileResume(): void {
    this.uploadScopedMedia('profile-resume', this.profileResumeUploadForm, this.buildProfileFolder(), (media) => {
      this.profileForm.resumeFileId = media.id;
    });
  }

  protected buildProjectFolder(): string {
    return `projects/${this.slugify(this.projectForm.slug || this.projectForm.title || 'untitled-project')}`;
  }

  protected buildBlogFolder(): string {
    return `blog/${this.slugify(this.blogPostForm.slug || this.blogPostForm.title || 'untitled-post')}`;
  }

  protected buildProfileFolder(): string {
    const profileSlug = this.slugify(`${this.profileForm.firstName || 'profile'}-${this.profileForm.lastName || 'owner'}`);
    return `profiles/${profileSlug}`;
  }

  protected buildExperienceFolder(): string {
    return `experience/${this.slugify(this.experienceForm.organizationName || this.experienceForm.roleTitle || 'experience')}`;
  }

  private uploadScopedMedia(uploadKey: string, form: ScopedUploadForm, folder: string, onSuccess: (media: AdminMediaFile) => void): void {
    if (!form.file) {
      this.statusMessage = 'Choose a file before uploading.';
      return;
    }
    const formData = new FormData();
    formData.append('file', form.file);
    formData.append('folder', folder);
    formData.append('visibility', form.visibility);
    if (form.title.trim()) {
      formData.append('title', form.title.trim());
    }
    if (form.altText.trim()) {
      formData.append('altText', form.altText.trim());
    }
    if (form.description.trim()) {
      formData.append('description', form.description.trim());
    }

    this.uploadInProgressKey = uploadKey;
    this.statusMessage = 'Uploading media…';
    this.adminApi.uploadMedia(formData).pipe(
      take(1),
      finalize(() => {
        this.uploadInProgressKey = null;
        this.changeDetectorRef.detectChanges();
      })
    ).subscribe({
      next: (media) => {
        this.referenceData = {
          ...this.referenceData,
          mediaFiles: [media, ...this.referenceData.mediaFiles.filter((item) => item.id !== media.id)],
        };
        this.dashboard = {
          ...this.dashboard,
          mediaFiles: this.dashboard.mediaFiles + 1,
        };
        onSuccess(media);
        this.resetScopedUploadForm(form);
        this.statusMessage = `Media uploaded to ${folder} and selected automatically.`;
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Uploading media failed.';
      }
    });
  }

  private resetScopedUploadForm(form: ScopedUploadForm): void {
    form.title = '';
    form.altText = '';
    form.description = '';
    form.visibility = 'public';
    form.file = null;
  }

  private toggleSelection(items: string[], value: string): string[] {
    return items.includes(value) ? items.filter((item) => item !== value) : [...items, value];
  }

  private resolveSelection<T extends { id: string }>(currentId: string | null, items: T[]): string | null {
    if (currentId && items.some((item) => item.id === currentId)) {
      return currentId;
    }
    return items[0]?.id ?? null;
  }

  private slugify(value: string): string {
    return value
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '') || 'item';
  }

  private parseJsonObject(raw: string): Record<string, unknown> | null {
    if (!raw.trim()) {
      return null;
    }
    const parsed = JSON.parse(raw);
    if (parsed === null) {
      return null;
    }
    if (typeof parsed !== 'object' || Array.isArray(parsed)) {
      throw new Error('Raw payload must be a JSON object.');
    }
    return parsed as Record<string, unknown>;
  }

  private parseContributionDays(raw: string): AdminGithubContributionDay[] {
    if (!raw.trim()) {
      return [];
    }
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      throw new Error('Contribution days must be a JSON array.');
    }
    return parsed.map((item) => ({
      date: String(item?.date ?? ''),
      count: Number(item?.count ?? 0),
      level: Number(item?.level ?? 0),
    }));
  }

  private createEmptyScopedUploadForm(): ScopedUploadForm {
    return { title: '', altText: '', description: '', visibility: 'public', file: null };
  }

  private createEmptyProjectForm(): AdminProjectForm {
    return {
      slug: '',
      title: '',
      teaser: '',
      summary: '',
      descriptionMarkdown: '',
      coverImageFileId: null,
      githubUrl: '',
      githubRepoOwner: '',
      githubRepoName: '',
      demoUrl: '',
      companyName: '',
      startedOn: '',
      endedOn: '',
      durationLabel: '',
      status: '',
      state: 'published',
      isFeatured: false,
      sortOrder: 0,
      publishedAt: '',
      skillIds: []
    };
  }

  private createEmptyBlogPostForm(): AdminBlogPostForm {
    return {
      slug: '',
      title: '',
      excerpt: '',
      contentMarkdown: '',
      coverImageFileId: null,
      coverImageAlt: '',
      readingTimeMinutes: null,
      status: 'draft',
      isFeatured: false,
      publishedAt: '',
      seoTitle: '',
      seoDescription: '',
      tagIds: []
    };
  }

  private createEmptyProfileForm(): AdminProfileForm {
    return {
      firstName: '',
      lastName: '',
      headline: '',
      shortIntro: '',
      longBio: '',
      location: '',
      email: '',
      phone: '',
      avatarFileId: null,
      heroImageFileId: null,
      resumeFileId: null,
      ctaPrimaryLabel: '',
      ctaPrimaryUrl: '',
      ctaSecondaryLabel: '',
      ctaSecondaryUrl: '',
      isPublic: true,
      socialLinks: []
    };
  }

  private createEmptySkillCategoryForm(): AdminSkillCategoryForm {
    return { name: '', description: '', sortOrder: 0 };
  }

  private createEmptySkillForm(): AdminSkillForm {
    return { categoryId: '', name: '', yearsOfExperience: null, iconKey: '', sortOrder: 0, isHighlighted: false };
  }

  private createEmptyBlogTagForm(): AdminBlogTagForm {
    return { name: '', slug: '' };
  }

  private createEmptyExperienceForm(): AdminExperienceForm {
    return {
      organizationName: '',
      roleTitle: '',
      location: '',
      experienceType: 'work',
      startDate: '',
      endDate: '',
      isCurrent: false,
      summary: '',
      descriptionMarkdown: '',
      logoFileId: null,
      sortOrder: 0,
      skillIds: []
    };
  }

  private createEmptyNavigationItemForm(): AdminNavigationItemForm {
    return { label: '', routePath: '', isExternal: false, sortOrder: 0, isVisible: true };
  }

  private createEmptyAdminUserForm(): AdminUserForm {
    return { email: '', displayName: '', password: '', isActive: true };
  }

  private createEmptyGithubSnapshotForm(): AdminGithubSnapshotForm {
    return {
      snapshotDate: '',
      username: '',
      publicRepoCount: 0,
      followersCount: null,
      followingCount: null,
      totalStars: null,
      totalCommits: null,
      rawPayloadText: '',
      contributionDaysText: '[]'
    };
  }

  private toProjectForm(project: AdminProject): AdminProjectForm {
    return {
      id: project.id,
      slug: project.slug,
      title: project.title,
      teaser: project.teaser,
      summary: project.summary ?? '',
      descriptionMarkdown: project.descriptionMarkdown ?? '',
      coverImageFileId: project.coverImageFileId ?? null,
      githubUrl: project.githubUrl ?? '',
      githubRepoOwner: project.githubRepoOwner ?? '',
      githubRepoName: project.githubRepoName ?? '',
      demoUrl: project.demoUrl ?? '',
      companyName: project.companyName ?? '',
      startedOn: project.startedOn ?? '',
      endedOn: project.endedOn ?? '',
      durationLabel: project.durationLabel,
      status: project.status,
      state: project.state,
      isFeatured: project.isFeatured,
      sortOrder: project.sortOrder,
      publishedAt: project.publishedAt?.slice(0, 16) ?? '',
      skillIds: [...project.skillIds],
    };
  }

  private toBlogPostForm(post: AdminBlogPost): AdminBlogPostForm {
    return {
      id: post.id,
      slug: post.slug,
      title: post.title,
      excerpt: post.excerpt,
      contentMarkdown: post.contentMarkdown,
      coverImageFileId: post.coverImageFileId ?? null,
      coverImageAlt: post.coverImageAlt ?? '',
      readingTimeMinutes: post.readingTimeMinutes ?? null,
      status: post.status,
      isFeatured: post.isFeatured,
      publishedAt: post.publishedAt?.slice(0, 16) ?? '',
      seoTitle: post.seoTitle ?? '',
      seoDescription: post.seoDescription ?? '',
      tagIds: [...post.tagIds],
    };
  }

  private toProfileForm(profile: AdminProfile): AdminProfileForm {
    return {
      id: profile.id,
      firstName: profile.firstName,
      lastName: profile.lastName,
      headline: profile.headline,
      shortIntro: profile.shortIntro,
      longBio: profile.longBio ?? '',
      location: profile.location ?? '',
      email: profile.email ?? '',
      phone: profile.phone ?? '',
      avatarFileId: profile.avatarFileId ?? null,
      heroImageFileId: profile.heroImageFileId ?? null,
      resumeFileId: profile.resumeFileId ?? null,
      ctaPrimaryLabel: profile.ctaPrimaryLabel ?? '',
      ctaPrimaryUrl: profile.ctaPrimaryUrl ?? '',
      ctaSecondaryLabel: profile.ctaSecondaryLabel ?? '',
      ctaSecondaryUrl: profile.ctaSecondaryUrl ?? '',
      isPublic: profile.isPublic,
      socialLinks: profile.socialLinks.map((link) => ({ ...link })),
    };
  }

  private toSkillCategoryForm(category: AdminSkillCategory): AdminSkillCategoryForm {
    return { id: category.id, name: category.name, description: category.description ?? '', sortOrder: category.sortOrder };
  }

  private toSkillForm(skill: AdminSkillOption): AdminSkillForm {
    return {
      id: skill.id,
      categoryId: skill.categoryId,
      name: skill.name,
      yearsOfExperience: skill.yearsOfExperience ?? null,
      iconKey: skill.iconKey ?? '',
      sortOrder: skill.sortOrder,
      isHighlighted: skill.isHighlighted,
    };
  }

  private toBlogTagForm(tag: AdminBlogTag): AdminBlogTagForm {
    return { id: tag.id, name: tag.name, slug: tag.slug };
  }

  private toExperienceForm(experience: AdminExperience): AdminExperienceForm {
    return {
      id: experience.id,
      organizationName: experience.organizationName,
      roleTitle: experience.roleTitle,
      location: experience.location ?? '',
      experienceType: experience.experienceType,
      startDate: experience.startDate,
      endDate: experience.endDate ?? '',
      isCurrent: experience.isCurrent,
      summary: experience.summary,
      descriptionMarkdown: experience.descriptionMarkdown ?? '',
      logoFileId: experience.logoFileId ?? null,
      sortOrder: experience.sortOrder,
      skillIds: [...experience.skillIds],
    };
  }

  private toNavigationItemForm(item: AdminNavigationItem): AdminNavigationItemForm {
    return {
      id: item.id,
      label: item.label,
      routePath: item.routePath,
      isExternal: item.isExternal,
      sortOrder: item.sortOrder,
      isVisible: item.isVisible,
    };
  }

  private toAdminUserForm(user: AdminUser): AdminUserForm {
    return { id: user.id, email: user.email, displayName: user.displayName, password: '', isActive: user.isActive };
  }

  private toGithubSnapshotForm(snapshot: AdminGithubSnapshot): AdminGithubSnapshotForm {
    return {
      id: snapshot.id,
      snapshotDate: snapshot.snapshotDate,
      username: snapshot.username,
      publicRepoCount: snapshot.publicRepoCount,
      followersCount: snapshot.followersCount ?? null,
      followingCount: snapshot.followingCount ?? null,
      totalStars: snapshot.totalStars ?? null,
      totalCommits: snapshot.totalCommits ?? null,
      rawPayloadText: snapshot.rawPayload ? JSON.stringify(snapshot.rawPayload, null, 2) : '',
      contributionDaysText: JSON.stringify(snapshot.contributionDays, null, 2),
    };
  }
}
