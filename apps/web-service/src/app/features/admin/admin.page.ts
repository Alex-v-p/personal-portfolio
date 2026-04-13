import { NgClass, NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import {
  AdminAssistantConversationSummary,
  AdminAssistantKnowledgeStatus,
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
  AdminSiteActivity,
  AdminSiteEvent,
  AdminVisitSessionSummary,
  AdminVisitorActivitySummary,
  AdminSkillCategory,
  AdminSkillOption,
  AdminSocialLink,
  AdminUser,
} from '../../shared/models/admin.model';
import { AdminPortfolioApiService } from '../../shared/services/admin-portfolio-api.service';
import { AdminSessionService } from '../../shared/services/admin-session.service';
import {
  AdminBlogPostForm,
  AdminBlogTagForm,
  AdminExperienceForm,
  AdminGithubSnapshotForm,
  AdminNavigationItemForm,
  AdminProfileForm,
  AdminProjectForm,
  AdminSkillCategoryForm,
  AdminSkillForm,
  AdminUserForm,
  ScopedUploadForm,
  createEmptyAdminUserForm,
  createEmptyBlogPostForm,
  createEmptyBlogTagForm,
  createEmptyExperienceForm,
  createEmptyGithubSnapshotForm,
  createEmptyNavigationItemForm,
  createEmptyProfileForm,
  createEmptyProjectForm,
  createEmptyScopedUploadForm,
  createEmptySkillCategoryForm,
  createEmptySkillForm,
  toAdminUserForm,
  toBlogPostForm,
  toBlogTagForm,
  toExperienceForm,
  toGithubSnapshotForm,
  toNavigationItemForm,
  toProfileForm,
  toProjectForm,
  toSkillCategoryForm,
  toSkillForm,
} from './admin-page.forms';
import { ADMIN_TABS, AdminTabId } from './admin-page.tabs';
import {
  categoryName,
  contributionPreview,
  formatSkillSummary,
  mediaFolder,
  mediaKind,
  mediaKindLabel,
} from './admin-page.display.utils';
import { AdminActivityTabComponent } from './tab-sections/admin-activity-tab.component';
import { AdminBlogTabComponent } from './tab-sections/admin-blog-tab.component';
import { AdminAdminsTabComponent } from './tab-sections/admin-admins-tab.component';
import { AdminAssistantTabComponent } from './tab-sections/admin-assistant-tab.component';
import { AdminExperienceTabComponent } from './tab-sections/admin-experience-tab.component';
import { AdminMediaTabComponent } from './tab-sections/admin-media-tab.component';
import { AdminMessagesTabComponent } from './tab-sections/admin-messages-tab.component';
import { AdminNavigationTabComponent } from './tab-sections/admin-navigation-tab.component';
import { AdminOverviewTabComponent } from './tab-sections/admin-overview-tab.component';
import { AdminProfileTabComponent } from './tab-sections/admin-profile-tab.component';
import { AdminProjectsTabComponent } from './tab-sections/admin-projects-tab.component';
import { AdminStatsTabComponent } from './tab-sections/admin-stats-tab.component';
import { AdminTaxonomyTabComponent } from './tab-sections/admin-taxonomy-tab.component';
import { matchesSearch, parseContributionDays, parseJsonObject, resolveSelection, slugify, toggleSelection } from './admin-page.utils';

@Component({
  selector: 'app-admin-page',
  standalone: true,
  imports: [
    NgIf,
    NgFor,
    NgClass,
    FormsModule,
    AdminOverviewTabComponent,
    AdminMediaTabComponent,
    AdminProjectsTabComponent,
    AdminBlogTabComponent,
    AdminTaxonomyTabComponent,
    AdminExperienceTabComponent,
    AdminNavigationTabComponent,
    AdminProfileTabComponent,
    AdminStatsTabComponent,
    AdminAssistantTabComponent,
    AdminActivityTabComponent,
    AdminAdminsTabComponent,
    AdminMessagesTabComponent,
  ],
  templateUrl: './admin.page.html'
})
export class AdminPageComponent implements OnInit {
  private readonly adminApi = inject(AdminPortfolioApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  @ViewChild(AdminBlogTabComponent) private blogTabComponent?: AdminBlogTabComponent;

  protected readonly tabs = ADMIN_TABS;

  protected activeTab: AdminTabId = 'overview';
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
  protected assistantKnowledgeStatus: AdminAssistantKnowledgeStatus = {
    totalDocuments: 0,
    totalChunks: 0,
    documentsBySourceType: {},
    latestUpdatedAt: null,
  };
  protected siteActivity: AdminSiteActivity = {
    summary: { totalEvents: 0, uniqueVisitors: 0, pageViews: 0, assistantMessages: 0, contactSubmissions: 0 },
    visitors: [],
    visits: [],
    events: [],
    assistantConversations: [],
  };
  protected selectedActivityVisitorId: string | null = null;
  protected selectedActivityVisitSessionId: string | null = null;
  protected activityVisitorSearchTerm = '';
  protected activityVisitorFocus: 'all' | 'withAssistant' | 'withContacts' | 'withPageViews' = 'all';
  protected activityTimelineEventFilter: 'all' | 'page_view' | 'assistant_message' | 'contact_submit' = 'all';
  protected messageSearchTerm = '';
  protected messageStatusFilter: 'all' | 'unread' | 'read' = 'all';
  protected messageSourceFilter = 'all';
  protected updatingMessageIds: string[] = [];

  protected selectedMediaFileId: string | null = null;
  protected selectedProjectId: string | null = null;
  protected selectedBlogPostId: string | null = null;
  protected selectedSkillCategoryId: string | null = null;
  protected selectedSkillId: string | null = null;
  protected selectedBlogTagId: string | null = null;
  protected selectedExperienceId: string | null = null;
  protected selectedNavigationItemId: string | null = null;
  protected selectedAdminUserId: string | null = null;
  protected selectedGithubSnapshotId: string | null = null;

  protected projectForm: AdminProjectForm = createEmptyProjectForm();
  protected blogPostForm: AdminBlogPostForm = createEmptyBlogPostForm();
  protected profileForm: AdminProfileForm = createEmptyProfileForm();
  protected skillCategoryForm: AdminSkillCategoryForm = createEmptySkillCategoryForm();
  protected skillForm: AdminSkillForm = createEmptySkillForm();
  protected blogTagForm: AdminBlogTagForm = createEmptyBlogTagForm();
  protected experienceForm: AdminExperienceForm = createEmptyExperienceForm();
  protected navigationItemForm: AdminNavigationItemForm = createEmptyNavigationItemForm();
  protected adminUserForm: AdminUserForm = createEmptyAdminUserForm();
  protected githubSnapshotForm: AdminGithubSnapshotForm = createEmptyGithubSnapshotForm();
  protected isRefreshingGithub = false;
  protected isRebuildingAssistantKnowledge = false;

  protected projectUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected blogUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected blogInlineImageUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected experienceUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected profileAvatarUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected profileHeroUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected profileResumeUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected uploadInProgressKey: string | null = null;
  protected mediaSearchTerm = '';
  protected mediaVisibilityFilter: 'all' | 'public' | 'private' | 'signed' = 'all';
  protected mediaKindFilter: 'all' | 'image' | 'document' | 'video' | 'audio' | 'archive' | 'other' = 'all';
  protected mediaFolderFilter = 'all';
  protected deletingMediaFileIds: string[] = [];

  ngOnInit(): void {
    this.loadCms();
  }

  protected setActiveTab(tabId: typeof this.activeTab): void {
    this.activeTab = tabId;
    if (tabId === 'media' && !this.selectedMediaFileId) {
      this.selectedMediaFileId = this.filteredMediaFiles[0]?.id ?? this.referenceData.mediaFiles[0]?.id ?? null;
    }
  }

  protected logout(): void {
    this.adminSession.logout();
  }

  protected loadCms(): void {
    const currentSelections = {
      mediaFile: this.selectedMediaFileId,
      project: this.selectedProjectId,
      blogPost: this.selectedBlogPostId,
      skillCategory: this.selectedSkillCategoryId,
      skill: this.selectedSkillId,
      blogTag: this.selectedBlogTagId,
      experience: this.selectedExperienceId,
      navigation: this.selectedNavigationItemId,
      adminUser: this.selectedAdminUserId,
      github: this.selectedGithubSnapshotId,
      activityVisitor: this.selectedActivityVisitorId,
      activityVisit: this.selectedActivityVisitSessionId,
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
      assistantKnowledgeStatus: this.adminApi.getAssistantKnowledgeStatus(),
      siteActivity: this.adminApi.getSiteActivity(),
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
          this.assistantKnowledgeStatus = result.assistantKnowledgeStatus;
          this.siteActivity = result.siteActivity;

          this.selectedMediaFileId = resolveSelection(currentSelections.mediaFile, this.referenceData.mediaFiles) ?? this.referenceData.mediaFiles[0]?.id ?? null;
          this.selectedProjectId = resolveSelection(currentSelections.project, this.projects);
          this.selectedBlogPostId = resolveSelection(currentSelections.blogPost, this.blogPosts);
          this.selectedSkillCategoryId = resolveSelection(currentSelections.skillCategory, this.referenceData.skillCategories);
          this.selectedSkillId = resolveSelection(currentSelections.skill, this.referenceData.skills);
          this.selectedBlogTagId = resolveSelection(currentSelections.blogTag, this.referenceData.blogTags);
          this.selectedExperienceId = resolveSelection(currentSelections.experience, this.experiences);
          this.selectedNavigationItemId = resolveSelection(currentSelections.navigation, this.navigationItems);
          this.selectedAdminUserId = resolveSelection(currentSelections.adminUser, this.adminUsers);
          this.selectedGithubSnapshotId = resolveSelection(currentSelections.github, this.githubSnapshots);
          this.selectedActivityVisitorId = currentSelections.activityVisitor;
          this.selectedActivityVisitSessionId = currentSelections.activityVisit;
          this.ensureActivitySelections();

          this.projectForm = this.selectedProjectId ? toProjectForm(this.projects.find((item) => item.id === this.selectedProjectId)!) : createEmptyProjectForm();
          this.blogPostForm = this.selectedBlogPostId ? toBlogPostForm(this.blogPosts.find((item) => item.id === this.selectedBlogPostId)!) : createEmptyBlogPostForm();
          this.profileForm = this.profile ? toProfileForm(this.profile) : createEmptyProfileForm();
          this.skillCategoryForm = this.selectedSkillCategoryId ? toSkillCategoryForm(this.referenceData.skillCategories.find((item) => item.id === this.selectedSkillCategoryId)!) : createEmptySkillCategoryForm();
          this.skillForm = this.selectedSkillId ? toSkillForm(this.referenceData.skills.find((item) => item.id === this.selectedSkillId)!) : createEmptySkillForm();
          this.blogTagForm = this.selectedBlogTagId ? toBlogTagForm(this.referenceData.blogTags.find((item) => item.id === this.selectedBlogTagId)!) : createEmptyBlogTagForm();
          this.experienceForm = this.selectedExperienceId ? toExperienceForm(this.experiences.find((item) => item.id === this.selectedExperienceId)!) : createEmptyExperienceForm();
          this.navigationItemForm = this.selectedNavigationItemId ? toNavigationItemForm(this.navigationItems.find((item) => item.id === this.selectedNavigationItemId)!) : createEmptyNavigationItemForm();
          this.adminUserForm = this.selectedAdminUserId ? toAdminUserForm(this.adminUsers.find((item) => item.id === this.selectedAdminUserId)!) : createEmptyAdminUserForm();
          this.githubSnapshotForm = this.selectedGithubSnapshotId ? toGithubSnapshotForm(this.githubSnapshots.find((item) => item.id === this.selectedGithubSnapshotId)!) : createEmptyGithubSnapshotForm();
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

  protected get mediaFolderOptions(): string[] {
    return Array.from(
      new Set(
        this.referenceData.mediaFiles
          .map((media) => this.mediaFolder(media))
          .filter((folder) => folder !== 'root')
      )
    ).sort((left, right) => left.localeCompare(right));
  }

  protected get filteredMediaFiles(): AdminMediaFile[] {
    return [...this.referenceData.mediaFiles]
      .filter((media) => this.mediaVisibilityFilter === 'all' || media.visibility === this.mediaVisibilityFilter)
      .filter((media) => this.mediaKindFilter === 'all' || this.mediaKind(media) === this.mediaKindFilter)
      .filter((media) => this.mediaFolderFilter === 'all' || this.mediaFolder(media) === this.mediaFolderFilter)
      .filter((media) => matchesSearch([media.title, media.altText, media.originalFilename, media.objectKey, this.mediaFolder(media)], this.mediaSearchTerm))
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  }

  protected get filteredMediaCount(): number {
    return this.filteredMediaFiles.length;
  }

  protected get imageMediaCount(): number {
    return this.referenceData.mediaFiles.filter((media) => this.mediaKind(media) === 'image').length;
  }

  protected get documentMediaCount(): number {
    return this.referenceData.mediaFiles.filter((media) => this.mediaKind(media) === 'document').length;
  }

  protected get selectedMediaFile(): AdminMediaFile | null {
    return this.referenceData.mediaFiles.find((media) => media.id === this.selectedMediaFileId) ?? null;
  }

  protected get messageSourceOptions(): string[] {
    return Array.from(new Set(this.messages.map((message) => message.sourcePage).filter(Boolean))).sort((left, right) => left.localeCompare(right));
  }

  protected get filteredMessages(): AdminContactMessage[] {
    const searchNeedle = this.messageSearchTerm.trim().toLowerCase();
    return [...this.messages]
      .filter((message) => {
        if (this.messageStatusFilter === 'read' && !message.isRead) {
          return false;
        }
        if (this.messageStatusFilter === 'unread' && message.isRead) {
          return false;
        }
        if (this.messageSourceFilter !== 'all' && message.sourcePage !== this.messageSourceFilter) {
          return false;
        }
        if (!searchNeedle) {
          return true;
        }
        return matchesSearch([message.name, message.email, message.subject, message.message, message.sourcePage], searchNeedle);
      })
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  }

  protected get filteredMessageCount(): number {
    return this.filteredMessages.length;
  }

  protected get unreadFilteredMessageCount(): number {
    return this.filteredMessages.filter((message) => !message.isRead).length;
  }

  protected get filteredActivityVisitors(): AdminVisitorActivitySummary[] {
    const searchNeedle = this.activityVisitorSearchTerm.trim().toLowerCase();
    return this.siteActivity.visitors.filter((visitor) => {
      if (this.activityVisitorFocus === 'withAssistant' && visitor.assistantMessages === 0) {
        return false;
      }
      if (this.activityVisitorFocus === 'withContacts' && visitor.contactSubmissions === 0) {
        return false;
      }
      if (this.activityVisitorFocus === 'withPageViews' && visitor.pageViews === 0) {
        return false;
      }
      if (!searchNeedle) {
        return true;
      }
      return matchesSearch([visitor.visitorId, visitor.latestPagePath, visitor.latestIpAddress], searchNeedle);
    });
  }

  protected get selectedActivityVisitor(): AdminVisitorActivitySummary | null {
    return this.filteredActivityVisitors.find((visitor) => visitor.visitorId === this.selectedActivityVisitorId) ?? null;
  }

  protected get selectedActivityVisits(): AdminVisitSessionSummary[] {
    return this.visitsForVisitor(this.selectedActivityVisitorId);
  }

  protected get selectedActivityVisit(): AdminVisitSessionSummary | null {
    return this.selectedActivityVisits.find((visit) => visit.sessionId === this.selectedActivityVisitSessionId) ?? null;
  }

  protected get selectedActivityEvents(): AdminSiteEvent[] {
    const visitorId = this.selectedActivityVisitorId;
    if (!visitorId) {
      return [];
    }
    return this.siteActivity.events.filter((event) => {
      if (event.visitorId !== visitorId) {
        return false;
      }
      if (this.selectedActivityVisitSessionId && event.sessionId !== this.selectedActivityVisitSessionId) {
        return false;
      }
      if (this.activityTimelineEventFilter !== 'all' && event.eventType !== this.activityTimelineEventFilter) {
        return false;
      }
      return true;
    });
  }

  protected get selectedActivityConversations(): AdminAssistantConversationSummary[] {
    const visitorId = this.selectedActivityVisitorId;
    if (!visitorId) {
      return [];
    }
    return this.siteActivity.assistantConversations.filter((conversation) => {
      if (conversation.visitorId !== visitorId) {
        return false;
      }
      if (this.selectedActivityVisitSessionId && conversation.siteSessionId !== this.selectedActivityVisitSessionId) {
        return false;
      }
      return true;
    });
  }

  protected get selectedActivityEventCount(): number {
    return this.selectedActivityEvents.length;
  }

  protected mediaPreview(mediaId: string | null | undefined): AdminMediaFile | undefined {
    return this.referenceData.mediaFiles.find((item) => item.id === mediaId);
  }

  protected selectMediaFile(mediaId: string): void {
    this.selectedMediaFileId = mediaId;
    this.statusMessage = '';
  }

  protected clearMediaFilters(): void {
    this.mediaSearchTerm = '';
    this.mediaVisibilityFilter = 'all';
    this.mediaKindFilter = 'all';
    this.mediaFolderFilter = 'all';
  }

  protected isDeletingMediaFile(mediaId: string): boolean {
    return this.deletingMediaFileIds.includes(mediaId);
  }

  protected deleteSelectedMediaFile(): void {
    const media = this.selectedMediaFile;
    if (!media) {
      return;
    }

    const confirmed = window.confirm(
      `Delete "${media.title || media.originalFilename}"? This removes the media record from the CMS and attempts to delete the stored file too. Existing blog markdown or content pointing at this file may break.`
    );
    if (!confirmed) {
      return;
    }

    this.deletingMediaFileIds = [...this.deletingMediaFileIds, media.id];
    this.statusMessage = 'Deleting media file…';
    this.adminApi.deleteMediaFile(media.id).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Media file deleted.';
        this.selectedMediaFileId = null;
        this.deletingMediaFileIds = this.deletingMediaFileIds.filter((id) => id !== media.id);
        this.loadCms();
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Deleting the media file failed.';
        this.deletingMediaFileIds = this.deletingMediaFileIds.filter((id) => id !== media.id);
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  protected mediaFolder(media: AdminMediaFile): string {
    return mediaFolder(media);
  }

  protected mediaKind(media: AdminMediaFile): 'image' | 'document' | 'video' | 'audio' | 'archive' | 'other' {
    return mediaKind(media);
  }

  protected mediaKindLabel(media: AdminMediaFile): string {
    return mediaKindLabel(media);
  }

  protected categoryName(categoryId: string): string {
    return categoryName(this.referenceData.skillCategories, categoryId);
  }

  protected contributionPreview(snapshot: AdminGithubSnapshot): string {
    return contributionPreview(snapshot);
  }


  protected formatSkillSummary(experience: AdminExperience): string {
    return formatSkillSummary(experience);
  }

  protected selectProject(projectId: string): void {
    this.selectedProjectId = projectId;
    const project = this.projects.find((item) => item.id === projectId);
    if (project) {
      this.projectForm = toProjectForm(project);
      this.statusMessage = '';
    }
  }

  protected startNewProject(): void {
    this.selectedProjectId = null;
    this.projectForm = createEmptyProjectForm();
    this.projectUploadForm = createEmptyScopedUploadForm();
  }

  protected toggleProjectSkill(skillId: string): void {
    this.projectForm.skillIds = toggleSelection(this.projectForm.skillIds, skillId);
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
      this.blogPostForm = toBlogPostForm(post);
      this.blogUploadForm = createEmptyScopedUploadForm();
      this.blogInlineImageUploadForm = createEmptyScopedUploadForm();
      this.statusMessage = '';
    }
  }

  protected startNewBlogPost(): void {
    this.selectedBlogPostId = null;
    this.blogPostForm = createEmptyBlogPostForm();
    this.blogUploadForm = createEmptyScopedUploadForm();
    this.blogInlineImageUploadForm = createEmptyScopedUploadForm();
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
      this.skillCategoryForm = toSkillCategoryForm(category);
    }
  }

  protected startNewSkillCategory(): void {
    this.selectedSkillCategoryId = null;
    this.skillCategoryForm = createEmptySkillCategoryForm();
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
      this.skillForm = toSkillForm(skill);
    }
  }

  protected startNewSkill(): void {
    this.selectedSkillId = null;
    this.skillForm = createEmptySkillForm();
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
      this.blogTagForm = toBlogTagForm(tag);
    }
  }

  protected startNewBlogTag(): void {
    this.selectedBlogTagId = null;
    this.blogTagForm = createEmptyBlogTagForm();
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
      this.experienceForm = toExperienceForm(experience);
    }
  }

  protected startNewExperience(): void {
    this.selectedExperienceId = null;
    this.experienceForm = createEmptyExperienceForm();
    this.experienceUploadForm = createEmptyScopedUploadForm();
  }

  protected toggleExperienceSkill(skillId: string): void {
    this.experienceForm.skillIds = toggleSelection(this.experienceForm.skillIds, skillId);
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
      this.navigationItemForm = toNavigationItemForm(item);
    }
  }

  protected startNewNavigationItem(): void {
    this.selectedNavigationItemId = null;
    this.navigationItemForm = createEmptyNavigationItemForm();
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
      this.adminUserForm = toAdminUserForm(user);
    }
  }

  protected startNewAdminUser(): void {
    this.selectedAdminUserId = null;
    this.adminUserForm = createEmptyAdminUserForm();
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
      this.githubSnapshotForm = toGithubSnapshotForm(snapshot);
    }
  }

  protected startNewGithubSnapshot(): void {
    this.selectedGithubSnapshotId = null;
    this.githubSnapshotForm = createEmptyGithubSnapshotForm();
  }


  protected rebuildAssistantKnowledge(): void {
    this.isRebuildingAssistantKnowledge = true;
    this.statusMessage = '';
    this.adminApi.rebuildAssistantKnowledge().pipe(take(1)).subscribe({
      next: (status) => {
        this.assistantKnowledgeStatus = status;
        this.statusMessage = 'Assistant knowledge index rebuilt from the latest portfolio content.';
        this.refreshAssistantKnowledgeStatus();
      },
      error: (error) => {
        this.isRebuildingAssistantKnowledge = false;
        this.statusMessage = error?.error?.detail || 'Rebuilding the assistant knowledge index failed.';
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  private refreshAssistantKnowledgeStatus(): void {
    this.adminApi.getAssistantKnowledgeStatus().pipe(take(1)).subscribe({
      next: (status) => {
        this.assistantKnowledgeStatus = status;
        this.isRebuildingAssistantKnowledge = false;
        this.changeDetectorRef.detectChanges();
      },
      error: () => {
        this.isRebuildingAssistantKnowledge = false;
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  protected refreshGithubSnapshot(): void {
    this.isRefreshingGithub = true;
    this.statusMessage = '';
    this.adminApi.refreshGithubSnapshot({
      username: this.githubSnapshotForm.username.trim() || null,
      pruneHistory: true,
    }).pipe(take(1)).subscribe({
      next: (snapshot) => {
        this.isRefreshingGithub = false;
        this.selectedGithubSnapshotId = snapshot.id;
        this.githubSnapshotForm = toGithubSnapshotForm(snapshot);
        this.statusMessage = 'GitHub stats refreshed from the latest public profile data.';
        this.loadCms();
      },
      error: (error) => {
        this.isRefreshingGithub = false;
        this.statusMessage = error?.error?.detail || 'Refreshing GitHub stats failed.';
      }
    });
  }

  protected saveGithubSnapshot(): void {
    let rawPayload: Record<string, unknown> | null = null;
    let contributionDays: AdminGithubContributionDay[] = [];
    try {
      rawPayload = parseJsonObject(this.githubSnapshotForm.rawPayloadText);
      contributionDays = parseContributionDays(this.githubSnapshotForm.contributionDaysText);
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

  protected selectActivityVisitor(visitorId: string): void {
    this.selectedActivityVisitorId = visitorId;
    this.selectedActivityVisitSessionId = this.visitsForVisitor(visitorId)[0]?.sessionId ?? null;
  }

  protected selectActivityVisit(sessionId: string | null): void {
    this.selectedActivityVisitSessionId = sessionId;
  }

  protected onActivityFiltersChanged(): void {
    this.ensureActivitySelections();
  }

  protected isMessageUpdating(messageId: string): boolean {
    return this.updatingMessageIds.includes(messageId);
  }

  protected toggleMessageRead(message: AdminContactMessage): void {
    const nextIsRead = !message.isRead;
    const previousMessages = this.messages.map((item) => ({ ...item }));
    this.updatingMessageIds = [...this.updatingMessageIds, message.id];
    this.messages = this.messages.map((item) => item.id === message.id ? { ...item, isRead: nextIsRead } : item);
    this.dashboard.unreadMessages = this.messages.filter((item) => !item.isRead).length;
    this.statusMessage = nextIsRead ? 'Marking message as read…' : 'Marking message as unread…';
    this.changeDetectorRef.detectChanges();

    this.adminApi.updateContactMessage(message.id, nextIsRead).pipe(take(1)).subscribe({
      next: (updatedMessage) => {
        this.messages = this.messages.map((item) => item.id === updatedMessage.id ? updatedMessage : item);
        this.dashboard.unreadMessages = this.messages.filter((item) => !item.isRead).length;
        this.statusMessage = updatedMessage.isRead ? 'Message marked as read.' : 'Message marked as unread.';
        this.updatingMessageIds = this.updatingMessageIds.filter((id) => id !== message.id);
        this.changeDetectorRef.detectChanges();
      },
      error: (error) => {
        this.messages = previousMessages;
        this.dashboard.unreadMessages = this.messages.filter((item) => !item.isRead).length;
        this.statusMessage = error?.error?.detail || 'Updating message status failed.';
        this.updatingMessageIds = this.updatingMessageIds.filter((id) => id !== message.id);
        this.changeDetectorRef.detectChanges();
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

  protected uploadBlogInlineImage(): void {
    this.uploadScopedMedia(
      'blog-inline-image',
      this.blogInlineImageUploadForm,
      this.buildBlogFolder(),
      (media) => this.blogTabComponent?.insertImageFromMedia(media),
      (media) => `Image uploaded to ${this.buildBlogFolder()} and inserted into the article.`
    );
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
    return `projects/${slugify(this.projectForm.slug || this.projectForm.title || 'untitled-project')}`;
  }

  protected buildBlogFolder(): string {
    return `blog/${slugify(this.blogPostForm.slug || this.blogPostForm.title || 'untitled-post')}`;
  }

  protected buildProfileFolder(): string {
    const profileSlug = slugify(`${this.profileForm.firstName || 'profile'}-${this.profileForm.lastName || 'owner'}`);
    return `profiles/${profileSlug}`;
  }

  protected buildExperienceFolder(): string {
    return `experience/${slugify(this.experienceForm.organizationName || this.experienceForm.roleTitle || 'experience')}`;
  }

  private uploadScopedMedia(
    uploadKey: string,
    form: ScopedUploadForm,
    folder: string,
    onSuccess: (media: AdminMediaFile) => void,
    successMessageBuilder?: (media: AdminMediaFile) => string,
  ): void {
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
        this.statusMessage = successMessageBuilder?.(media) ?? `Media uploaded to ${folder} and selected automatically.`;
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


  private visitsForVisitor(visitorId: string | null): AdminVisitSessionSummary[] {
    if (!visitorId) {
      return [];
    }
    return this.siteActivity.visits
      .filter((visit) => visit.visitorId === visitorId)
      .sort((left, right) => right.lastActivityAt.localeCompare(left.lastActivityAt));
  }

  private ensureActivitySelections(): void {
    const visitors = this.filteredActivityVisitors;
    if (!visitors.length) {
      this.selectedActivityVisitorId = null;
      this.selectedActivityVisitSessionId = null;
      return;
    }
    if (!this.selectedActivityVisitorId || !visitors.some((visitor) => visitor.visitorId === this.selectedActivityVisitorId)) {
      this.selectedActivityVisitorId = visitors[0].visitorId;
    }
    const visits = this.visitsForVisitor(this.selectedActivityVisitorId);
    if (!visits.length) {
      this.selectedActivityVisitSessionId = null;
      return;
    }
    if (this.selectedActivityVisitSessionId === null) {
      return;
    }
    if (!visits.some((visit) => visit.sessionId === this.selectedActivityVisitSessionId)) {
      this.selectedActivityVisitSessionId = visits[0].sessionId;
    }
  }


























}
