import { DatePipe, NgClass, NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import {
  AdminBlogPost,
  AdminContactMessage,
  AdminDashboardSummary,
  AdminMediaFile,
  AdminProfile,
  AdminProject,
  AdminReferenceData,
  AdminSocialLink,
} from '../../shared/models/admin.model';
import { AdminPortfolioApiService } from '../../shared/services/admin-portfolio-api.service';
import { AdminSessionService } from '../../shared/services/admin-session.service';

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
  tagNames: string;
}

interface AdminMediaUploadForm {
  folder: string;
  title: string;
  altText: string;
  description: string;
  visibility: 'public' | 'private' | 'signed';
  file: File | null;
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

@Component({
  selector: 'app-admin-page',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule, DatePipe],
  templateUrl: './admin.page.html'
})
export class AdminPageComponent implements OnInit {
  private readonly adminApi = inject(AdminPortfolioApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly router = inject(Router);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected readonly tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'projects', label: 'Projects' },
    { id: 'blog', label: 'Blog' },
    { id: 'profile', label: 'Profile' },
    { id: 'messages', label: 'Messages' },
  ] as const;

  protected activeTab: 'overview' | 'projects' | 'blog' | 'profile' | 'messages' = 'overview';
  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected dashboard: AdminDashboardSummary = { projects: 0, blogPosts: 0, unreadMessages: 0, skills: 0, mediaFiles: 0 };
  protected referenceData: AdminReferenceData = {
    skills: [],
    mediaFiles: [],
    blogTags: [],
    projectStates: ['published', 'archived', 'completed', 'paused'],
    publicationStatuses: ['draft', 'published', 'archived']
  };
  protected projects: AdminProject[] = [];
  protected blogPosts: AdminBlogPost[] = [];
  protected profile: AdminProfile | null = null;
  protected messages: AdminContactMessage[] = [];

  protected selectedProjectId: string | null = null;
  protected selectedBlogPostId: string | null = null;
  protected projectForm: AdminProjectForm = this.createEmptyProjectForm();
  protected blogPostForm: AdminBlogPostForm = this.createEmptyBlogPostForm();
  protected profileForm: AdminProfileForm = this.createEmptyProfileForm();
  protected mediaUploadForm: AdminMediaUploadForm = this.createEmptyMediaUploadForm();
  protected isUploadingMedia = false;

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
    this.isLoading = true;
    this.errorMessage = '';
    this.statusMessage = '';

    forkJoin({
      dashboard: this.adminApi.getDashboardSummary(),
      referenceData: this.adminApi.getReferenceData(),
      projects: this.adminApi.getProjects(),
      blogPosts: this.adminApi.getBlogPosts(),
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
          this.profile = result.profile;
          this.messages = result.messages.items;

          this.selectedProjectId = this.projects[0]?.id ?? null;
          this.selectedBlogPostId = this.blogPosts[0]?.id ?? null;
          this.projectForm = this.selectedProjectId ? this.toProjectForm(this.projects.find((item) => item.id === this.selectedProjectId)!) : this.createEmptyProjectForm();
          this.blogPostForm = this.selectedBlogPostId ? this.toBlogPostForm(this.blogPosts.find((item) => item.id === this.selectedBlogPostId)!) : this.createEmptyBlogPostForm();
          this.profileForm = this.profile ? this.toProfileForm(this.profile) : this.createEmptyProfileForm();
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
    this.statusMessage = '';
  }

  protected toggleProjectSkill(skillId: string): void {
    this.projectForm.skillIds = this.projectForm.skillIds.includes(skillId)
      ? this.projectForm.skillIds.filter((item) => item !== skillId)
      : [...this.projectForm.skillIds, skillId];
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
      next: (project) => {
        this.statusMessage = this.selectedProjectId ? 'Project updated.' : 'Project created.';
        this.selectedProjectId = project.id;
        this.loadCms();
        this.activeTab = 'projects';
      },
      error: () => {
        this.statusMessage = 'Saving the project failed.';
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
      error: () => {
        this.statusMessage = 'Deleting the project failed.';
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
    this.statusMessage = '';
  }

  protected saveBlogPost(): void {
    this.statusMessage = 'Saving blog post…';
    const tagNames = this.blogPostForm.tagNames
      .split(',')
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
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
      tagNames,
    };
    const request$ = this.selectedBlogPostId
      ? this.adminApi.updateBlogPost(this.selectedBlogPostId, payload)
      : this.adminApi.createBlogPost(payload);

    request$.pipe(take(1)).subscribe({
      next: (post) => {
        this.statusMessage = this.selectedBlogPostId ? 'Blog post updated.' : 'Blog post created.';
        this.selectedBlogPostId = post.id;
        this.loadCms();
        this.activeTab = 'blog';
      },
      error: () => {
        this.statusMessage = 'Saving the blog post failed.';
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
      error: () => {
        this.statusMessage = 'Deleting the blog post failed.';
      }
    });
  }

  protected addSocialLink(): void {
    this.profileForm.socialLinks = [
      ...this.profileForm.socialLinks,
      { platform: '', label: '', url: '', iconKey: '', sortOrder: this.profileForm.socialLinks.length + 1, isVisible: true }
    ];
  }

  protected removeSocialLink(index: number): void {
    this.profileForm.socialLinks = this.profileForm.socialLinks.filter((_, currentIndex) => currentIndex !== index);
  }

  protected saveProfile(): void {
    this.statusMessage = 'Saving profile…';
    const payload: AdminProfile = {
      id: this.profileForm.id ?? '',
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
      socialLinks: this.profileForm.socialLinks.map((link) => ({ ...link, id: link.id || null, iconKey: link.iconKey || null })),
      createdAt: this.profile?.createdAt ?? '',
      updatedAt: this.profile?.updatedAt ?? '',
      avatar: this.profile?.avatar,
      heroImage: this.profile?.heroImage,
      resume: this.profile?.resume,
    };
    this.adminApi.updateProfile(payload).pipe(take(1)).subscribe({
      next: (profile) => {
        this.profile = profile;
        this.profileForm = this.toProfileForm(profile);
        this.statusMessage = 'Profile updated.';
        this.loadCms();
      },
      error: () => {
        this.statusMessage = 'Saving the profile failed.';
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
      error: () => {
        this.statusMessage = 'Updating message status failed.';
      }
    });
  }

  protected get adminDisplayName(): string {
    return this.adminSession.currentUser?.displayName ?? 'Admin';
  }

  protected mediaPreview(mediaId: string | null | undefined): AdminMediaFile | undefined {
    return this.referenceData.mediaFiles.find((item) => item.id === mediaId);
  }

  protected onMediaFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement | null;
    this.mediaUploadForm.file = input?.files?.[0] ?? null;
  }

  protected uploadMedia(): void {
    if (!this.mediaUploadForm.file || this.isUploadingMedia) {
      this.statusMessage = 'Choose a file before uploading.';
      return;
    }

    const formData = new FormData();
    formData.append('file', this.mediaUploadForm.file);
    formData.append('folder', this.mediaUploadForm.folder || 'uploads');
    formData.append('visibility', this.mediaUploadForm.visibility);
    if (this.mediaUploadForm.title.trim()) {
      formData.append('title', this.mediaUploadForm.title.trim());
    }
    if (this.mediaUploadForm.altText.trim()) {
      formData.append('altText', this.mediaUploadForm.altText.trim());
    }
    if (this.mediaUploadForm.description.trim()) {
      formData.append('description', this.mediaUploadForm.description.trim());
    }

    this.isUploadingMedia = true;
    this.statusMessage = 'Uploading media…';
    this.adminApi.uploadMedia(formData).pipe(
      take(1),
      finalize(() => {
        this.isUploadingMedia = false;
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
        this.mediaUploadForm = this.createEmptyMediaUploadForm();
        this.statusMessage = 'Media uploaded. It is now available in the selectors below.';
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Uploading media failed.';
      }
    });
  }

  private createEmptyMediaUploadForm(): AdminMediaUploadForm {
    return {
      folder: 'uploads',
      title: '',
      altText: '',
      description: '',
      visibility: 'public',
      file: null,
    };
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
      tagNames: ''
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
      publishedAt: project.publishedAt ? project.publishedAt.slice(0, 16) : '',
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
      publishedAt: post.publishedAt ? post.publishedAt.slice(0, 16) : '',
      seoTitle: post.seoTitle ?? '',
      seoDescription: post.seoDescription ?? '',
      tagNames: post.tagNames.join(', '),
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
}
