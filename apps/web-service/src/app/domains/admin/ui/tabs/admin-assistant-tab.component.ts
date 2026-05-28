import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminAssistantContextNote, AdminAssistantContextNotePayload, AdminAssistantKnowledgeStatus } from '@domains/admin/model/admin.model';

interface AssistantContextNoteForm {
  title: string;
  titleNl: string;
  contentMarkdown: string;
  contentMarkdownNl: string;
  category: string;
  isActive: boolean;
  sortOrder: number;
}

interface AssistantContextNotePreset {
  label: string;
  category: string;
  title: string;
  titleNl: string;
  contentMarkdown: string;
  contentMarkdownNl: string;
}

@Component({
  selector: 'app-admin-assistant-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-assistant-tab.component.html'
})
export class AdminAssistantTabComponent implements OnInit {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly adminSession = inject(AdminSessionService);

  @Input({ required: true }) assistantKnowledgeStatus!: AdminAssistantKnowledgeStatus;
  @Input() isRebuildingAssistantKnowledge = false;

  @Output() readonly rebuildRequested = new EventEmitter<void>();

  protected contextNotes: AdminAssistantContextNote[] = [];
  protected selectedContextNoteId: string | null = null;
  protected contextNoteForm: AssistantContextNoteForm = this.createEmptyContextNoteForm();
  protected isLoadingContextNotes = false;
  protected isSavingContextNote = false;
  protected isGeneratingDutchDraft = false;
  protected contextNoteMessage = '';
  protected contextNoteError = '';

  readonly contextCategories = [
    { value: 'overall_skills', label: 'Overall skills' },
    { value: 'working_style', label: 'Working style' },
    { value: 'faq', label: 'FAQ' },
    { value: 'availability', label: 'Availability' },
    { value: 'career_goals', label: 'Career goals' },
    { value: 'communication', label: 'Communication' },
    { value: 'extra_background', label: 'Extra background' },
  ];

  readonly notePresets: AssistantContextNotePreset[] = [
    {
      label: 'Overall skills',
      category: 'overall_skills',
      title: 'Overall skills and strengths',
      titleNl: 'Algemene vaardigheden en sterktes',
      contentMarkdown: '## Strongest areas\n- Add the core technical strengths the assistant may mention.\n- Include skills that are important but not obvious from public cards.\n\n## Evidence\n- Connect each strength to projects, coursework, internships, or real examples.\n\n## How to phrase it\n- Keep answers factual, warm, and not overhyped.',
      contentMarkdownNl: '## Sterkste gebieden\n- Voeg de belangrijkste technische sterktes toe die de assistant mag noemen.\n- Vermeld vaardigheden die belangrijk zijn maar niet direct zichtbaar zijn op publieke kaarten.\n\n## Bewijs\n- Koppel elke sterkte aan projecten, studies, stages of echte voorbeelden.\n\n## Formulering\n- Houd antwoorden feitelijk, warm en niet overdreven.',
    },
    {
      label: 'Recruiter FAQ',
      category: 'faq',
      title: 'Recruiter FAQ',
      titleNl: 'Recruiter FAQ',
      contentMarkdown: '## Questions the assistant should answer\n- What kind of role is a good fit?\n- What technologies should visitors associate with this portfolio?\n- What should recruiters know before reaching out?\n\n## Boundaries\n- Add anything the assistant should avoid guessing about.',
      contentMarkdownNl: '## Vragen die de assistant moet beantwoorden\n- Welk soort rol past goed?\n- Welke technologieën moeten bezoekers aan dit portfolio koppelen?\n- Wat moeten recruiters weten voordat ze contact opnemen?\n\n## Grenzen\n- Voeg toe waarover de assistant niet mag gokken.',
    },
    {
      label: 'Working style',
      category: 'working_style',
      title: 'Working style and collaboration',
      titleNl: 'Werkstijl en samenwerking',
      contentMarkdown: '## Working style\n- Describe how you approach planning, communication, debugging, and collaboration.\n\n## Good examples\n- Add concrete examples from team projects, client work, school work, or internships.\n\n## Tone\n- Let the assistant sound confident but approachable.',
      contentMarkdownNl: '## Werkstijl\n- Beschrijf hoe je planning, communicatie, debugging en samenwerking aanpakt.\n\n## Goede voorbeelden\n- Voeg concrete voorbeelden toe uit teamprojecten, klantwerk, schoolwerk of stages.\n\n## Toon\n- Laat de assistant zelfverzekerd maar toegankelijk klinken.',
    },
  ];

  ngOnInit(): void {
    this.loadContextNotes();
  }

  rebuildAssistantKnowledge(): void {
    this.rebuildRequested.emit();
  }

  protected selectContextNote(note: AdminAssistantContextNote): void {
    this.selectedContextNoteId = note.id;
    this.contextNoteForm = {
      title: note.title,
      titleNl: note.titleNl ?? '',
      contentMarkdown: note.contentMarkdown,
      contentMarkdownNl: note.contentMarkdownNl ?? '',
      category: note.category || 'overall_skills',
      isActive: note.isActive,
      sortOrder: note.sortOrder,
    };
    this.contextNoteMessage = '';
    this.contextNoteError = '';
  }

  protected startNewContextNote(): void {
    this.selectedContextNoteId = null;
    this.contextNoteForm = this.createEmptyContextNoteForm();
    this.contextNoteMessage = '';
    this.contextNoteError = '';
  }

  protected usePreset(preset: AssistantContextNotePreset): void {
    this.selectedContextNoteId = null;
    this.contextNoteForm = {
      title: preset.title,
      titleNl: preset.titleNl,
      contentMarkdown: preset.contentMarkdown,
      contentMarkdownNl: preset.contentMarkdownNl,
      category: preset.category,
      isActive: true,
      sortOrder: this.contextNotes.length + 1,
    };
    this.contextNoteMessage = `Started a new ${preset.label.toLowerCase()} note from a CMS template. Review and save it when ready.`;
    this.contextNoteError = '';
  }

  protected saveContextNote(rebuildAfterSave = false): void {
    this.contextNoteError = '';
    this.contextNoteMessage = '';
    const payload = this.buildContextNotePayload();
    if (!payload.title || !payload.contentMarkdown) {
      this.contextNoteError = 'Add at least an English title and assistant-only markdown content.';
      return;
    }

    this.isSavingContextNote = true;
    const request = this.selectedContextNoteId
      ? this.overviewApi.updateAssistantContextNote(this.selectedContextNoteId, payload)
      : this.overviewApi.createAssistantContextNote(payload);

    request.pipe(take(1)).subscribe({
      next: (note) => {
        this.isSavingContextNote = false;
        this.contextNoteMessage = this.selectedContextNoteId ? 'Assistant-only context note updated.' : 'Assistant-only context note created.';
        this.selectedContextNoteId = note.id;
        this.loadContextNotes(note.id);
        if (rebuildAfterSave) {
          this.contextNoteMessage = 'Assistant-only context note saved. Rebuilding the assistant knowledge index…';
          this.rebuildRequested.emit();
        }
      },
      error: (error) => this.handleContextNoteError(error, 'Saving the assistant-only context note failed.'),
    });
  }

  protected saveContextNoteAndRebuild(): void {
    this.saveContextNote(true);
  }

  protected deleteContextNote(): void {
    if (!this.selectedContextNoteId) {
      return;
    }
    this.contextNoteError = '';
    this.contextNoteMessage = '';
    this.isSavingContextNote = true;
    this.overviewApi.deleteAssistantContextNote(this.selectedContextNoteId).pipe(take(1)).subscribe({
      next: () => {
        this.isSavingContextNote = false;
        this.contextNoteMessage = 'Assistant-only context note deleted.';
        this.startNewContextNote();
        this.loadContextNotes();
      },
      error: (error) => this.handleContextNoteError(error, 'Deleting the assistant-only context note failed.'),
    });
  }

  protected generateDutchContextDraft(): void {
    this.contextNoteError = '';
    this.contextNoteMessage = '';
    if (!this.contextNoteForm.title.trim() && !this.contextNoteForm.contentMarkdown.trim()) {
      this.contextNoteError = 'Add English content before generating a Dutch draft.';
      return;
    }

    this.isGeneratingDutchDraft = true;
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'assistant_context_note',
      context: 'Translate private assistant guidance for a developer portfolio. Keep names, URLs, technology names, and proficiency labels unchanged unless they are ordinary prose.',
      fields: {
        titleNl: this.contextNoteForm.title,
        contentMarkdownNl: this.contextNoteForm.contentMarkdown,
      },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.isGeneratingDutchDraft = false;
        this.contextNoteForm.titleNl = response.translatedFields['titleNl'] ?? this.contextNoteForm.titleNl;
        this.contextNoteForm.contentMarkdownNl = response.translatedFields['contentMarkdownNl'] ?? this.contextNoteForm.contentMarkdownNl;
        this.contextNoteMessage = 'Dutch assistant-only draft generated. Review it before saving.';
      },
      error: (error) => {
        this.isGeneratingDutchDraft = false;
        this.contextNoteError = error?.error?.detail || 'Generating the Dutch assistant-only draft failed.';
      },
    });
  }

  private loadContextNotes(selectNoteId?: string): void {
    this.isLoadingContextNotes = true;
    this.overviewApi.getAssistantContextNotes().pipe(take(1)).subscribe({
      next: (response) => {
        this.contextNotes = response.items;
        this.isLoadingContextNotes = false;
        const targetId = selectNoteId ?? this.selectedContextNoteId;
        const selected = targetId ? this.contextNotes.find((note) => note.id === targetId) : null;
        if (selected) {
          this.selectContextNote(selected);
        } else if (!this.contextNotes.length) {
          this.startNewContextNote();
        }
      },
      error: (error) => {
        this.isLoadingContextNotes = false;
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }
        this.contextNoteError = error?.error?.detail || 'Loading assistant-only context notes failed.';
      },
    });
  }

  private handleContextNoteError(error: any, fallback: string): void {
    this.isSavingContextNote = false;
    if (error?.status === 401) {
      this.adminSession.logout();
      return;
    }
    this.contextNoteError = error?.error?.detail || fallback;
  }

  private buildContextNotePayload(): AdminAssistantContextNotePayload {
    return {
      title: this.contextNoteForm.title.trim(),
      titleNl: this.contextNoteForm.titleNl.trim() || null,
      contentMarkdown: this.contextNoteForm.contentMarkdown.trim(),
      contentMarkdownNl: this.contextNoteForm.contentMarkdownNl.trim() || null,
      category: this.contextNoteForm.category || 'overall_skills',
      isActive: this.contextNoteForm.isActive,
      sortOrder: Number(this.contextNoteForm.sortOrder) || 0,
    };
  }

  private createEmptyContextNoteForm(): AssistantContextNoteForm {
    return {
      title: '',
      titleNl: '',
      contentMarkdown: '',
      contentMarkdownNl: '',
      category: 'overall_skills',
      isActive: true,
      sortOrder: this.contextNotes.length + 1,
    };
  }
}
