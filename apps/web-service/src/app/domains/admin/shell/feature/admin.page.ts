import { NgClass, NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, Input, OnDestroy, OnInit, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription, forkJoin, timer } from 'rxjs';
import { finalize, switchMap, take, takeWhile } from 'rxjs/operators';

import {
  AdminAssistantConversationSummary,
  AdminAssistantKnowledgeStatus,
  AdminAsyncTaskAccepted,
  AdminAsyncTaskStatus,
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
} from '@domains/admin/model/admin.model';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminContentApiService } from '@domains/admin/data/api/admin-content-api.service';
import { AdminMediaApiService } from '@domains/admin/data/api/admin-media-api.service';
import { AdminMessagesApiService } from '@domains/admin/data/api/admin-messages-api.service';
import { AdminProfileApiService } from '@domains/admin/data/api/admin-profile-api.service';
import { AdminStatsApiService } from '@domains/admin/data/api/admin-stats-api.service';
import { AdminTaxonomyApiService } from '@domains/admin/data/api/admin-taxonomy-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminTasksApiService } from '@domains/admin/data/api/admin-tasks-api.service';
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
} from '@domains/admin/model/forms/index';
import { ADMIN_TABS, AdminTabId } from '@domains/admin/shell/state/admin-page.tabs';
import {
  ActivityTimelineEventFilter,
  ActivityVisitorFocus,
  ensureActivitySelections as ensureActivitySelectionsState,
  filterActivityVisitors,
  filterSelectedActivityEvents,
  resolveSelectedActivityVisit,
  resolveSelectedActivityVisitor,
  selectedActivityConversations,
  visitsForVisitor,
} from '@domains/admin/activity/state/admin-activity.state';
import { buildMessageSourceOptions, countUnreadMessages, filterMessages } from '@domains/admin/messages/state/admin-messages.filters';
import {
  buildBlogMediaFolder,
  buildExperienceMediaFolder,
  buildMediaFolderOptions,
  buildProfileMediaFolder,
  buildProjectMediaFolder,
  countMediaByKind,
  filterMediaFiles,
  resetScopedUploadForm,
  resolveSelectedMediaFile,
} from '@domains/admin/media/state/admin-media.filters';
import { AdminBlogTabComponent } from '@domains/admin/ui/tabs/admin-blog-tab.component';
import { AdminAdminsTabComponent } from '@domains/admin/ui/tabs/admin-admins-tab.component';
import { AdminExperienceTabComponent } from '@domains/admin/ui/tabs/admin-experience-tab.component';
import { AdminNavigationTabComponent } from '@domains/admin/ui/tabs/admin-navigation-tab.component';
import { AdminProjectsTabComponent } from '@domains/admin/ui/tabs/admin-projects-tab.component';
import { AdminTaxonomyTabComponent } from '@domains/admin/ui/tabs/admin-taxonomy-tab.component';
import { parseContributionDays, parseJsonObject, resolveSelection, toggleSelection } from '@domains/admin/shell/state/admin-page.utils';

@Component({
  selector: 'app-admin-page',
  standalone: true,
  imports: [
    NgIf,
    NgFor,
    NgClass,
    FormsModule,
    AdminProjectsTabComponent,
    AdminTaxonomyTabComponent,
    AdminExperienceTabComponent,
    AdminNavigationTabComponent,
    AdminAdminsTabComponent,
  ],
  templateUrl: './admin.page.html'
})
export class AdminPageComponent implements OnInit, OnDestroy {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly contentApi = inject(AdminContentApiService);
  private readonly mediaApi = inject(AdminMediaApiService);
  private readonly messagesApi = inject(AdminMessagesApiService);
  private readonly profileApi = inject(AdminProfileApiService);
  private readonly statsApi = inject(AdminStatsApiService);
  private readonly taxonomyApi = inject(AdminTaxonomyApiService);
  private readonly tasksApi = inject(AdminTasksApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  @ViewChild(AdminBlogTabComponent) private blogTabComponent?: AdminBlogTabComponent;

  private githubRefreshTaskSubscription?: Subscription;
  private assistantRebuildTaskSubscription?: Subscription;

  @Input() initialTab: AdminTabId = 'projects';
  @Input() compactMode = false;

  protected readonly tabs = ADMIN_TABS;

  protected activeTab: AdminTabId = 'projects';
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
    summary: { totalEvents: 0, uniqueVisitors: 0, pageViews: 0, assistantMessages: 0, contactSubmissions: 0, siteEventsRetentionDays: 0, assistantActivityRetentionDays: 0},
    visitors: [],
    visits: [],
    events: [],
    assistantConversations: [],
  };
  protected selectedActivityVisitorId: string | null = null;
  protected selectedActivityVisitSessionId: string | null = null;
  protected activityVisitorSearchTerm = '';
  protected activityVisitorFocus: ActivityVisitorFocus = 'all';
  protected activityTimelineEventFilter: ActivityTimelineEventFilter = 'all';
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
  protected profileResumeNlUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected uploadInProgressKey: string | null = null;
  protected mediaSearchTerm = '';
  protected mediaVisibilityFilter: 'all' | 'public' | 'private' | 'signed' = 'all';
  protected mediaKindFilter: 'all' | 'image' | 'document' | 'video' | 'audio' | 'archive' | 'other' = 'all';
  protected mediaFolderFilter = 'all';
  protected deletingMediaFileIds: string[] = [];

  ngOnInit(): void {
    this.activeTab = this.initialTab;
    this.loadCms();
  }

  ngOnDestroy(): void {
    this.githubRefreshTaskSubscription?.unsubscribe();
    this.assistantRebuildTaskSubscription?.unsubscribe();
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
      dashboard: this.overviewApi.getDashboardSummary(),
      referenceData: this.overviewApi.getReferenceData(),
      projects: this.contentApi.getProjects(),
      blogPosts: this.contentApi.getBlogPosts(),
      experiences: this.contentApi.getExperiences(),
      navigationItems: this.contentApi.getNavigationItems(),
      adminUsers: this.messagesApi.listAdminUsers(),
      githubSnapshots: this.statsApi.getGithubSnapshots(),
      profile: this.profileApi.getProfile(),
      messages: this.messagesApi.getContactMessages(),
      assistantKnowledgeStatus: this.overviewApi.getAssistantKnowledgeStatus(),
      siteActivity: this.overviewApi.getSiteActivity(),
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
          const activitySelections = ensureActivitySelectionsState(
            this.siteActivity,
            {
              visitorSearchTerm: this.activityVisitorSearchTerm,
              visitorFocus: this.activityVisitorFocus,
              timelineEventFilter: this.activityTimelineEventFilter,
            },
            this.selectedActivityVisitorId,
            this.selectedActivityVisitSessionId,
          );
          this.selectedActivityVisitorId = activitySelections.selectedVisitorId;
          this.selectedActivityVisitSessionId = activitySelections.selectedVisitSessionId;

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
    return buildMediaFolderOptions(this.referenceData.mediaFiles);
  }

  protected get filteredMediaFiles(): AdminMediaFile[] {
    return filterMediaFiles(this.referenceData.mediaFiles, {
      searchTerm: this.mediaSearchTerm,
      visibility: this.mediaVisibilityFilter,
      kind: this.mediaKindFilter,
      folder: this.mediaFolderFilter,
    });
  }

  protected get filteredMediaCount(): number {
    return this.filteredMediaFiles.length;
  }

  protected get imageMediaCount(): number {
    return countMediaByKind(this.referenceData.mediaFiles, 'image');
  }

  protected get documentMediaCount(): number {
    return countMediaByKind(this.referenceData.mediaFiles, 'document');
  }

  protected get selectedMediaFile(): AdminMediaFile | null {
    return resolveSelectedMediaFile(this.referenceData.mediaFiles, this.selectedMediaFileId);
  }

  protected get messageSourceOptions(): string[] {
    return buildMessageSourceOptions(this.messages);
  }

  protected get filteredMessages(): AdminContactMessage[] {
    return filterMessages(this.messages, {
      searchTerm: this.messageSearchTerm,
      status: this.messageStatusFilter,
      source: this.messageSourceFilter,
    });
  }

  protected get filteredMessageCount(): number {
    return this.filteredMessages.length;
  }

  protected get unreadFilteredMessageCount(): number {
    return countUnreadMessages(this.filteredMessages);
  }

  protected get filteredActivityVisitors(): AdminVisitorActivitySummary[] {
    return filterActivityVisitors(this.siteActivity, {
      visitorSearchTerm: this.activityVisitorSearchTerm,
      visitorFocus: this.activityVisitorFocus,
      timelineEventFilter: this.activityTimelineEventFilter,
    });
  }

  protected get selectedActivityVisitor(): AdminVisitorActivitySummary | null {
    return resolveSelectedActivityVisitor(this.filteredActivityVisitors, this.selectedActivityVisitorId);
  }

  protected get selectedActivityVisits(): AdminVisitSessionSummary[] {
    return visitsForVisitor(this.siteActivity, this.selectedActivityVisitorId);
  }

  protected get selectedActivityVisit(): AdminVisitSessionSummary | null {
    return resolveSelectedActivityVisit(this.selectedActivityVisits, this.selectedActivityVisitSessionId);
  }

  protected get selectedActivityEvents(): AdminSiteEvent[] {
    return filterSelectedActivityEvents(
      this.siteActivity,
      this.selectedActivityVisitorId,
      this.selectedActivityVisitSessionId,
      this.activityTimelineEventFilter,
    );
  }

  protected get selectedActivityConversations(): AdminAssistantConversationSummary[] {
    return selectedActivityConversations(this.siteActivity, this.selectedActivityVisitorId, this.selectedActivityVisitSessionId);
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
    if (!media.canDelete) {
      this.statusMessage = 'This media file is still referenced by portfolio content. Remove those references before deleting it.';
      return;
    }

    const confirmed = window.confirm(
      `Delete "${media.title || media.originalFilename}"? This removes the media record from the CMS and attempts to delete the stored file too.`
    );
    if (!confirmed) {
      return;
    }

    this.deletingMediaFileIds = [...this.deletingMediaFileIds, media.id];
    this.statusMessage = 'Deleting media file…';
    this.mediaApi.deleteMediaFile(media.id).pipe(take(1)).subscribe({
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
      titleNl: this.projectForm.titleNl || null,
      teaser: this.projectForm.teaser,
      teaserNl: this.projectForm.teaserNl || null,
      summary: this.projectForm.summary || null,
      summaryNl: this.projectForm.summaryNl || null,
      descriptionMarkdown: this.projectForm.descriptionMarkdown || null,
      descriptionMarkdownNl: this.projectForm.descriptionMarkdownNl || null,
      coverImageFileId: this.projectForm.coverImageFileId || null,
      githubUrl: this.projectForm.githubUrl || null,
      githubRepoOwner: this.projectForm.githubRepoOwner || null,
      githubRepoName: this.projectForm.githubRepoName || null,
      demoUrl: this.projectForm.demoUrl || null,
      companyName: this.projectForm.companyName || null,
      startedOn: this.projectForm.startedOn || null,
      endedOn: this.projectForm.endedOn || null,
      durationLabel: this.projectForm.durationLabel,
      durationLabelNl: this.projectForm.durationLabelNl || null,
      status: this.projectForm.status,
      statusNl: this.projectForm.statusNl || null,
      state: this.projectForm.state,
      isFeatured: this.projectForm.isFeatured,
      sortOrder: this.projectForm.sortOrder,
      publishedAt: this.projectForm.publishedAt || null,
      skillIds: [...this.projectForm.skillIds],
    };
    const request$ = this.selectedProjectId
      ? this.contentApi.updateProject(this.selectedProjectId, payload)
      : this.contentApi.createProject(payload);

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
    this.contentApi.deleteProject(this.selectedProjectId).pipe(take(1)).subscribe({
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
      ? this.contentApi.updateBlogPost(this.selectedBlogPostId, payload)
      : this.contentApi.createBlogPost(payload);
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
    this.contentApi.deleteBlogPost(this.selectedBlogPostId).pipe(take(1)).subscribe({
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
      nameNl: this.skillCategoryForm.nameNl || null,
      description: this.skillCategoryForm.description || null,
      descriptionNl: this.skillCategoryForm.descriptionNl || null,
      iconKey: this.skillCategoryForm.iconKey || null,
      sortOrder: this.skillCategoryForm.sortOrder,
    };
    const request$ = this.selectedSkillCategoryId
      ? this.taxonomyApi.updateSkillCategory(this.selectedSkillCategoryId, payload)
      : this.taxonomyApi.createSkillCategory(payload);
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
    this.taxonomyApi.deleteSkillCategory(this.selectedSkillCategoryId).pipe(take(1)).subscribe({
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
      proficiencyLabel: this.skillForm.proficiencyLabel || null,
      proficiencyLabelNl: this.skillForm.proficiencyLabelNl || null,
      iconKey: this.skillForm.iconKey || null,
      sortOrder: this.skillForm.sortOrder,
      isHighlighted: this.skillForm.isHighlighted,
    };
    const request$ = this.selectedSkillId
      ? this.taxonomyApi.updateSkill(this.selectedSkillId, payload)
      : this.taxonomyApi.createSkill(payload);
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
    this.taxonomyApi.deleteSkill(this.selectedSkillId).pipe(take(1)).subscribe({
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
      ? this.taxonomyApi.updateBlogTag(this.selectedBlogTagId, payload)
      : this.taxonomyApi.createBlogTag(payload);
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
    this.taxonomyApi.deleteBlogTag(this.selectedBlogTagId).pipe(take(1)).subscribe({
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
      roleTitleNl: this.experienceForm.roleTitleNl || null,
      location: this.experienceForm.location || null,
      experienceType: this.experienceForm.experienceType,
      startDate: this.experienceForm.startDate,
      endDate: this.experienceForm.endDate || null,
      isCurrent: this.experienceForm.isCurrent,
      summary: this.experienceForm.summary,
      summaryNl: this.experienceForm.summaryNl || null,
      descriptionMarkdown: this.experienceForm.descriptionMarkdown || null,
      descriptionMarkdownNl: this.experienceForm.descriptionMarkdownNl || null,
      logoFileId: this.experienceForm.logoFileId || null,
      sortOrder: this.experienceForm.sortOrder,
      skillIds: [...this.experienceForm.skillIds],
    };
    const request$ = this.selectedExperienceId
      ? this.contentApi.updateExperience(this.selectedExperienceId, payload)
      : this.contentApi.createExperience(payload);
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
    this.contentApi.deleteExperience(this.selectedExperienceId).pipe(take(1)).subscribe({
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
      labelNl: this.navigationItemForm.labelNl || null,
      routePath: this.navigationItemForm.routePath,
      isExternal: this.navigationItemForm.isExternal,
      sortOrder: this.navigationItemForm.sortOrder,
      isVisible: this.navigationItemForm.isVisible,
    };
    const request$ = this.selectedNavigationItemId
      ? this.contentApi.updateNavigationItem(this.selectedNavigationItemId, payload)
      : this.contentApi.createNavigationItem(payload);
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
    this.contentApi.deleteNavigationItem(this.selectedNavigationItemId).pipe(take(1)).subscribe({
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
      headlineNl: this.profileForm.headlineNl || null,
      shortIntro: this.profileForm.shortIntro,
      shortIntroNl: this.profileForm.shortIntroNl || null,
      longBio: this.profileForm.longBio || null,
      longBioNl: this.profileForm.longBioNl || null,
      location: this.profileForm.location || null,
      email: this.profileForm.email || null,
      phone: this.profileForm.phone || null,
      avatarFileId: this.profileForm.avatarFileId || null,
      heroImageFileId: this.profileForm.heroImageFileId || null,
      resumeFileId: this.profileForm.resumeFileId || null,
      resumeFileIdNl: this.profileForm.resumeFileIdNl || null,
      ctaPrimaryLabel: this.profileForm.ctaPrimaryLabel || null,
      ctaPrimaryLabelNl: this.profileForm.ctaPrimaryLabelNl || null,
      ctaPrimaryUrl: this.profileForm.ctaPrimaryUrl || null,
      ctaSecondaryLabel: this.profileForm.ctaSecondaryLabel || null,
      ctaSecondaryLabelNl: this.profileForm.ctaSecondaryLabelNl || null,
      ctaSecondaryUrl: this.profileForm.ctaSecondaryUrl || null,
      isPublic: this.profileForm.isPublic,
      socialLinks: this.profileForm.socialLinks.map((link, index) => ({ ...link, sortOrder: index })),
    };
    this.profileApi.updateProfile(payload).pipe(take(1)).subscribe({
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
      ? this.messagesApi.updateAdminUser(this.selectedAdminUserId, updatePayload)
      : this.messagesApi.createAdminUser(createPayload);
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
    this.messagesApi.deleteAdminUser(this.selectedAdminUserId).pipe(take(1)).subscribe({
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
    this.overviewApi.rebuildAssistantKnowledge().pipe(take(1)).subscribe({
      next: (response) => {
        if (this.isAsyncTaskAccepted(response)) {
          this.statusMessage = 'Assistant knowledge rebuild queued. Waiting for the worker to finish indexing…';
          this.pollAssistantRebuildTask(response.taskId, response.pollAfterMs);
          return;
        }
        this.assistantKnowledgeStatus = response;
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

  private pollAssistantRebuildTask(taskId: string, pollAfterMs: number): void {
    this.assistantRebuildTaskSubscription?.unsubscribe();
    this.assistantRebuildTaskSubscription = timer(pollAfterMs, pollAfterMs)
      .pipe(
        switchMap(() => this.tasksApi.getTask(taskId)),
        takeWhile((task) => task.status === 'queued' || task.status === 'running', true),
      )
      .subscribe({
        next: (task) => {
          if (task.status === 'succeeded') {
            this.statusMessage = 'Assistant knowledge index rebuilt from the latest portfolio content.';
            this.refreshAssistantKnowledgeStatus();
            return;
          }
          if (task.status === 'failed') {
            this.isRebuildingAssistantKnowledge = false;
            this.statusMessage = task.errorMessage || 'Rebuilding the assistant knowledge index failed.';
            this.changeDetectorRef.detectChanges();
          }
        },
        error: (error) => {
          this.isRebuildingAssistantKnowledge = false;
          this.statusMessage = error?.error?.detail || 'Checking assistant rebuild progress failed.';
          this.changeDetectorRef.detectChanges();
        }
      });
  }

  private refreshAssistantKnowledgeStatus(): void {
    this.overviewApi.getAssistantKnowledgeStatus().pipe(take(1)).subscribe({
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
    this.statsApi.refreshGithubSnapshot({
      username: this.githubSnapshotForm.username.trim() || null,
      pruneHistory: true,
    }).pipe(take(1)).subscribe({
      next: (response) => {
        if (this.isAsyncTaskAccepted(response)) {
          this.statusMessage = 'GitHub refresh queued. Waiting for the Redis worker to fetch the latest profile data…';
          this.pollGithubRefreshTask(response.taskId, response.pollAfterMs);
          return;
        }
        this.applyRefreshedGithubSnapshot(response);
      },
      error: (error) => {
        this.isRefreshingGithub = false;
        this.statusMessage = error?.error?.detail || 'Refreshing GitHub stats failed.';
      }
    });
  }

  private pollGithubRefreshTask(taskId: string, pollAfterMs: number): void {
    this.githubRefreshTaskSubscription?.unsubscribe();
    this.githubRefreshTaskSubscription = timer(pollAfterMs, pollAfterMs)
      .pipe(
        switchMap(() => this.tasksApi.getTask(taskId)),
        takeWhile((task) => task.status === 'queued' || task.status === 'running', true),
      )
      .subscribe({
        next: (task) => {
          if (task.status === 'succeeded') {
            this.finishGithubRefreshFromTask(task);
            return;
          }
          if (task.status === 'failed') {
            this.isRefreshingGithub = false;
            this.statusMessage = task.errorMessage || 'Refreshing GitHub stats failed.';
          }
        },
        error: (error) => {
          this.isRefreshingGithub = false;
          this.statusMessage = error?.error?.detail || 'Checking GitHub refresh progress failed.';
        }
      });
  }

  private finishGithubRefreshFromTask(task: AdminAsyncTaskStatus): void {
    const result = task.result;
    if (!result) {
      this.isRefreshingGithub = false;
      this.statusMessage = 'GitHub refresh finished, but the snapshot payload was missing.';
      return;
    }
    this.applyRefreshedGithubSnapshot(result as unknown as AdminGithubSnapshot);
  }

  private applyRefreshedGithubSnapshot(snapshot: AdminGithubSnapshot): void {
    this.isRefreshingGithub = false;
    this.selectedGithubSnapshotId = snapshot.id;
    this.githubSnapshotForm = toGithubSnapshotForm(snapshot);
    this.statusMessage = 'GitHub stats refreshed from the latest public profile data.';
    this.loadCms();
  }

  private isAsyncTaskAccepted(value: AdminGithubSnapshot | AdminAssistantKnowledgeStatus | AdminAsyncTaskAccepted): value is AdminAsyncTaskAccepted {
    return !!value && typeof value === 'object' && 'taskId' in value;
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
      ? this.statsApi.updateGithubSnapshot(this.selectedGithubSnapshotId, payload)
      : this.statsApi.createGithubSnapshot(payload);
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
    this.statsApi.deleteGithubSnapshot(this.selectedGithubSnapshotId).pipe(take(1)).subscribe({
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
    this.selectedActivityVisitSessionId = visitsForVisitor(this.siteActivity, visitorId)[0]?.sessionId ?? null;
  }

  protected selectActivityVisit(sessionId: string | null): void {
    this.selectedActivityVisitSessionId = sessionId;
  }

  protected onActivityFiltersChanged(): void {
    const activitySelections = ensureActivitySelectionsState(this.siteActivity, {
      visitorSearchTerm: this.activityVisitorSearchTerm,
      visitorFocus: this.activityVisitorFocus,
      timelineEventFilter: this.activityTimelineEventFilter,
    }, this.selectedActivityVisitorId, this.selectedActivityVisitSessionId);
    this.selectedActivityVisitorId = activitySelections.selectedVisitorId;
    this.selectedActivityVisitSessionId = activitySelections.selectedVisitSessionId;
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

    this.messagesApi.updateContactMessage(message.id, nextIsRead).pipe(take(1)).subscribe({
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

  protected uploadProfileResumeNl(): void {
    this.uploadScopedMedia('profile-resume-nl', this.profileResumeNlUploadForm, this.buildProfileFolder(), (media) => {
      this.profileForm.resumeFileIdNl = media.id;
    });
  }

  protected buildProjectFolder(): string {
    return buildProjectMediaFolder(this.projectForm.slug || this.projectForm.title);
  }

  protected buildBlogFolder(): string {
    return buildBlogMediaFolder(this.blogPostForm.slug || this.blogPostForm.title);
  }

  protected buildProfileFolder(): string {
    return buildProfileMediaFolder(this.profileForm.firstName, this.profileForm.lastName);
  }

  protected buildExperienceFolder(): string {
    return buildExperienceMediaFolder(this.experienceForm.organizationName, this.experienceForm.roleTitle);
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
    this.mediaApi.uploadMedia(formData).pipe(
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
        resetScopedUploadForm(form);
        this.statusMessage = successMessageBuilder?.(media) ?? `Media uploaded to ${folder} and selected automatically.`;
      },
      error: (error) => {
        this.statusMessage = error?.error?.detail || 'Uploading media failed.';
      }
    });
  }



























}
