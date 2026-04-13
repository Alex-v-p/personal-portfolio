import { Injectable, inject } from '@angular/core';

import { AdminAuthApiService } from './admin-api/admin-auth-api.service';
import { AdminContentApiService } from './admin-api/admin-content-api.service';
import { AdminMediaApiService } from './admin-api/admin-media-api.service';
import { AdminMessagesApiService } from './admin-api/admin-messages-api.service';
import { AdminOverviewApiService } from './admin-api/admin-overview-api.service';
import { AdminProfileApiService } from './admin-api/admin-profile-api.service';
import { AdminStatsApiService } from './admin-api/admin-stats-api.service';
import { AdminTaxonomyApiService } from './admin-api/admin-taxonomy-api.service';

@Injectable({ providedIn: 'root' })
export class AdminPortfolioApiService {
  private readonly authApi = inject(AdminAuthApiService);
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly mediaApi = inject(AdminMediaApiService);
  private readonly taxonomyApi = inject(AdminTaxonomyApiService);
  private readonly contentApi = inject(AdminContentApiService);
  private readonly profileApi = inject(AdminProfileApiService);
  private readonly statsApi = inject(AdminStatsApiService);
  private readonly messagesApi = inject(AdminMessagesApiService);

  readonly login = this.authApi.login.bind(this.authApi);
  readonly getCurrentAdmin = this.authApi.getCurrentAdmin.bind(this.authApi);

  readonly getAssistantKnowledgeStatus = this.overviewApi.getAssistantKnowledgeStatus.bind(this.overviewApi);
  readonly getSiteActivity = this.overviewApi.getSiteActivity.bind(this.overviewApi);
  readonly rebuildAssistantKnowledge = this.overviewApi.rebuildAssistantKnowledge.bind(this.overviewApi);
  readonly getDashboardSummary = this.overviewApi.getDashboardSummary.bind(this.overviewApi);
  readonly getReferenceData = this.overviewApi.getReferenceData.bind(this.overviewApi);

  readonly listMediaFiles = this.mediaApi.listMediaFiles.bind(this.mediaApi);
  readonly uploadMedia = this.mediaApi.uploadMedia.bind(this.mediaApi);
  readonly deleteMediaFile = this.mediaApi.deleteMediaFile.bind(this.mediaApi);

  readonly listSkillCategories = this.taxonomyApi.listSkillCategories.bind(this.taxonomyApi);
  readonly createSkillCategory = this.taxonomyApi.createSkillCategory.bind(this.taxonomyApi);
  readonly updateSkillCategory = this.taxonomyApi.updateSkillCategory.bind(this.taxonomyApi);
  readonly deleteSkillCategory = this.taxonomyApi.deleteSkillCategory.bind(this.taxonomyApi);
  readonly listSkills = this.taxonomyApi.listSkills.bind(this.taxonomyApi);
  readonly createSkill = this.taxonomyApi.createSkill.bind(this.taxonomyApi);
  readonly updateSkill = this.taxonomyApi.updateSkill.bind(this.taxonomyApi);
  readonly deleteSkill = this.taxonomyApi.deleteSkill.bind(this.taxonomyApi);
  readonly listBlogTags = this.taxonomyApi.listBlogTags.bind(this.taxonomyApi);
  readonly createBlogTag = this.taxonomyApi.createBlogTag.bind(this.taxonomyApi);
  readonly updateBlogTag = this.taxonomyApi.updateBlogTag.bind(this.taxonomyApi);
  readonly deleteBlogTag = this.taxonomyApi.deleteBlogTag.bind(this.taxonomyApi);

  readonly getProjects = this.contentApi.getProjects.bind(this.contentApi);
  readonly createProject = this.contentApi.createProject.bind(this.contentApi);
  readonly updateProject = this.contentApi.updateProject.bind(this.contentApi);
  readonly deleteProject = this.contentApi.deleteProject.bind(this.contentApi);
  readonly getBlogPosts = this.contentApi.getBlogPosts.bind(this.contentApi);
  readonly createBlogPost = this.contentApi.createBlogPost.bind(this.contentApi);
  readonly updateBlogPost = this.contentApi.updateBlogPost.bind(this.contentApi);
  readonly deleteBlogPost = this.contentApi.deleteBlogPost.bind(this.contentApi);
  readonly getExperiences = this.contentApi.getExperiences.bind(this.contentApi);
  readonly createExperience = this.contentApi.createExperience.bind(this.contentApi);
  readonly updateExperience = this.contentApi.updateExperience.bind(this.contentApi);
  readonly deleteExperience = this.contentApi.deleteExperience.bind(this.contentApi);
  readonly getNavigationItems = this.contentApi.getNavigationItems.bind(this.contentApi);
  readonly createNavigationItem = this.contentApi.createNavigationItem.bind(this.contentApi);
  readonly updateNavigationItem = this.contentApi.updateNavigationItem.bind(this.contentApi);
  readonly deleteNavigationItem = this.contentApi.deleteNavigationItem.bind(this.contentApi);

  readonly getGithubSnapshots = this.statsApi.getGithubSnapshots.bind(this.statsApi);
  readonly createGithubSnapshot = this.statsApi.createGithubSnapshot.bind(this.statsApi);
  readonly refreshGithubSnapshot = this.statsApi.refreshGithubSnapshot.bind(this.statsApi);
  readonly updateGithubSnapshot = this.statsApi.updateGithubSnapshot.bind(this.statsApi);
  readonly deleteGithubSnapshot = this.statsApi.deleteGithubSnapshot.bind(this.statsApi);

  readonly listAdminUsers = this.messagesApi.listAdminUsers.bind(this.messagesApi);
  readonly createAdminUser = this.messagesApi.createAdminUser.bind(this.messagesApi);
  readonly updateAdminUser = this.messagesApi.updateAdminUser.bind(this.messagesApi);
  readonly deleteAdminUser = this.messagesApi.deleteAdminUser.bind(this.messagesApi);
  readonly getProfile = this.profileApi.getProfile.bind(this.profileApi);
  readonly updateProfile = this.profileApi.updateProfile.bind(this.profileApi);
  readonly getContactMessages = this.messagesApi.getContactMessages.bind(this.messagesApi);
  readonly updateContactMessage = this.messagesApi.updateContactMessage.bind(this.messagesApi);
}
