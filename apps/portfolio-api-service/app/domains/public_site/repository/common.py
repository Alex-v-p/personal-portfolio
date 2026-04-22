from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import select

from app.db.models import BlogPost, MediaFile, Project, ProjectState, PublicationStatus
from app.domains.public_site.schema import PublicMediaAssetOut
from app.domains.media.resolver import PublicMediaUrlResolver

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


PublicLocale = Literal['en', 'nl']
DEFAULT_PUBLIC_LOCALE: PublicLocale = 'en'

_PUBLIC_COPY: dict[PublicLocale, dict[str, str]] = {
    'en': {
        'avatar_suffix': 'avatar',
        'hero_image_suffix': 'hero image',
        'resume_suffix': 'resume',
        'availability_internships': 'Open to internships',
        'availability_remote': 'Remote friendly',
        'availability_portfolio': 'Portfolio projects',
        'availability_jobs': 'Job opportunities',
        'availability_meeting': 'Scheduling a meeting',
        'contact_email_label': 'Email',
        'contact_email_action': 'Send Email',
        'contact_email_description': 'Best for project enquiries, internships, and collaboration.',
        'contact_phone_label': 'Phone',
        'contact_phone_action': 'Call',
        'contact_phone_description': 'Useful for quick coordination or planning a meeting.',
        'contact_social_action_connect': 'Connect +',
        'contact_social_action_open': 'Open',
        'contact_social_description_github': 'Code samples, experiments, and project work.',
        'contact_social_description_linkedin': 'Professional background and experience.',
        'contact_social_description_default': 'Direct line for portfolio contact.',
        'contact_location_label': 'Location',
        'contact_location_action': 'View Map',
        'contact_location_description': 'Available for on-site, hybrid, or remote collaboration.',
        'years_suffix': 'y',
    },
    'nl': {
        'avatar_suffix': 'profielfoto',
        'hero_image_suffix': 'hero-afbeelding',
        'resume_suffix': 'cv',
        'availability_internships': 'Open voor stages',
        'availability_remote': 'Remote vriendelijk',
        'availability_portfolio': 'Portfolio-projecten',
        'availability_jobs': 'Jobkansen',
        'availability_meeting': 'Een gesprek inplannen',
        'contact_email_label': 'E-mail',
        'contact_email_action': 'E-mail sturen',
        'contact_email_description': 'Ideaal voor projectvragen, stages en samenwerking.',
        'contact_phone_label': 'Telefoon',
        'contact_phone_action': 'Bellen',
        'contact_phone_description': 'Handig voor snelle afstemming of het plannen van een gesprek.',
        'contact_social_action_connect': 'Verbinden +',
        'contact_social_action_open': 'Openen',
        'contact_social_description_github': 'Codevoorbeelden, experimenten en projectwerk.',
        'contact_social_description_linkedin': 'Professionele achtergrond en ervaring.',
        'contact_social_description_default': 'Rechtstreeks contact via mijn portfolio.',
        'contact_location_label': 'Locatie',
        'contact_location_action': 'Kaart bekijken',
        'contact_location_description': 'Beschikbaar voor samenwerking op locatie, hybride of remote.',
        'years_suffix': 'j',
    },
}


class PublicRepositoryCommonMixin:
    session: Session
    media_resolver: PublicMediaUrlResolver
    locale: PublicLocale

    @staticmethod
    def _publication_cutoff() -> datetime:
        return datetime.now(UTC)

    def _public_project_query(self):
        return select(Project).where(
            Project.state != ProjectState.ARCHIVED,
            Project.published_at <= self._publication_cutoff(),
        )

    def _public_blog_post_query(self):
        return select(BlogPost).where(
            BlogPost.status == PublicationStatus.PUBLISHED,
            BlogPost.published_at.is_not(None),
            BlogPost.published_at <= self._publication_cutoff(),
        )

    def _map_media(self, media_file: MediaFile | None, alt: str | None = None) -> PublicMediaAssetOut | None:
        url = self.media_resolver.resolve(media_file)
        if media_file is None or url is None:
            return None
        return PublicMediaAssetOut(
            id=str(media_file.id),
            url=url,
            alt=alt or media_file.alt_text,
            file_name=media_file.original_filename,
            mime_type=media_file.mime_type,
            width=None,
            height=None,
        )

    def _localized(self, record: object, field_name: str) -> str | None:
        if self.locale != DEFAULT_PUBLIC_LOCALE:
            localized_value = getattr(record, f'{field_name}_{self.locale}', None)
            if isinstance(localized_value, str):
                localized_value = localized_value.strip()
            if localized_value not in (None, ''):
                return localized_value
        return getattr(record, field_name, None)

    def _copy(self, key: str) -> str:
        return _PUBLIC_COPY[self.locale].get(key, _PUBLIC_COPY[DEFAULT_PUBLIC_LOCALE][key])

    def _localized_years_label(self, years: int) -> str:
        return f'{years}{self._copy("years_suffix")}'
