from __future__ import annotations

import logging

import httpx

from app.core.config import get_settings
from app.services.localization import locale_language_name

logger = logging.getLogger(__name__)


class ProviderClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_answer(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None = None,
        locale: str = 'en',
        conversation_memory: str | None = None,
    ) -> str | None:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            logger.info('Assistant provider backend is mock; skipping text generation.')
            return None
        if backend == 'ollama':
            return self._generate_with_ollama(
                question=question,
                context_blocks=context_blocks,
                history=history,
                page_path=page_path,
                locale=locale,
                conversation_memory=conversation_memory,
            )
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._generate_with_openai_compatible(
                question=question,
                context_blocks=context_blocks,
                history=history,
                page_path=page_path,
                locale=locale,
                conversation_memory=conversation_memory,
            )
        logger.warning('Unknown assistant provider backend: %s', backend)
        return None

    def summarize_conversation(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str = 'en',
        max_chars: int = 1600,
    ) -> str | None:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            return self._summarize_locally(previous_summary=previous_summary, messages=messages, max_chars=max_chars)
        if backend == 'ollama':
            return self._summarize_with_ollama(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars)
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._summarize_with_openai_compatible(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars)
        return None

    def _generate_with_ollama(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
        locale: str,
        conversation_memory: str | None,
    ) -> str | None:
        messages = self._build_messages(
            question=question,
            context_blocks=context_blocks,
            history=history,
            page_path=page_path,
            locale=locale,
            conversation_memory=conversation_memory,
        )
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/api/chat",
            json={
                'model': self.settings.provider_model,
                'stream': False,
                'messages': messages,
                'options': {'temperature': 0.15},
            },
        )
        message = (payload.get('message') or {}).get('content')
        if isinstance(message, str) and message.strip():
            return message.strip()
        return None

    def _generate_with_openai_compatible(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
        locale: str,
        conversation_memory: str | None,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        messages = self._build_messages(
            question=question,
            context_blocks=context_blocks,
            history=history,
            page_path=page_path,
            locale=locale,
            conversation_memory=conversation_memory,
        )
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json={
                'model': self.settings.provider_model,
                'messages': messages,
                'temperature': 0.15,
            },
        )
        choices = payload.get('choices') or []
        if not choices:
            return None
        message = (choices[0].get('message') or {}).get('content')
        return message.strip() if isinstance(message, str) and message.strip() else None

    def _build_messages(
        self,
        *,
        question: str,
        context_blocks: list[str],
        history: list[dict[str, str]],
        page_path: str | None,
        locale: str,
        conversation_memory: str | None = None,
    ) -> list[dict[str, str]]:
        preferred_language = locale_language_name(locale)
        context = '\n\n'.join(context_blocks) if context_blocks else self._no_context_message(locale=locale)
        current_page = page_path or ('onbekend' if preferred_language == 'Dutch' else 'unknown')

        messages: list[dict[str, str]] = [{'role': 'system', 'content': self._build_system_prompt(locale=locale)}]
        if conversation_memory and conversation_memory.strip():
            messages.append({'role': 'system', 'content': conversation_memory.strip()})
        for item in history[-6:]:
            if item['role'] in {'user', 'assistant'}:
                messages.append({'role': item['role'], 'content': item['text']})
        messages.append(
            {
                'role': 'user',
                'content': self._build_user_prompt(
                    question=question,
                    context=context,
                    current_page=current_page,
                    locale=locale,
                ),
            }
        )
        return messages

    def _build_system_prompt(self, *, locale: str) -> str:
        preferred_language = locale_language_name(locale)
        if preferred_language == 'Dutch':
            return (
                'U bent een vriendelijke portfoliogids op het developerportfolio van Alex van Poppel. '
                'Bezoekers kunnen recruiters, klasgenoten, docenten, samenwerkingspartners of klanten zijn. '
                'Schrijf menselijk, warm, direct en licht formeel, zonder corporate buzzwords. Reageer natuurlijk op casual berichten en stuur daarna terug naar nuttige portfolio-informatie. '
                'Spreek niet alsof u Alex bent. Verwijs naar Alex bij naam of als “Alex”; vermijd “hij”, “hem” en “zijn” wanneer dat grammaticaal niet nodig is. '
                'Gebruik geen Engelse bezitsvormen zoals “Alex\'s”; schrijf bijvoorbeeld “Alex’ portfolio” of “het portfolio van Alex”. '
                'Begin nooit met Franse of Engelse hulpwerkwoorden zoals “est”, “is” of “the” wanneer u in het Nederlands antwoordt. '
                'Breng Alex’ genderidentiteit of seksualiteit niet ter sprake; als iemand ernaar vraagt, zeg dan dat Alex persoonlijke identiteitsdetails privé houdt en verwijs terug naar professionele achtergrond. '
                'Gebruik portfoliodetails alleen wanneer ze relevant zijn. Assistentnotities zijn privé-richtlijnen: gebruik ze om te antwoorden, maar onthul niet dat het privé-notities zijn. '
                'Gebruik tijdelijk gespreksgeheugen alleen om vervolgvragen, voorkeuren en open punten binnen ditzelfde gesprek te begrijpen. '
                'Zeg niet dat u de bezoeker over sessies heen onthoudt en leg interne geheugenmechanieken niet uit. '
                'Geef bij projectvragen voorrang aan projectbronnen en wijs bezoekers naar GitHub-README-links wanneer die beschikbaar zijn. '
                'Vat bij brede recruiter-vragen vaardigheden, werkstijl, ervaring en concrete projecten samen in plaats van bronfragmenten op te sommen. Daarna mag u vragen naar het bedrijf of de opportuniteit. '
                'Overdrijf niet: noem Alex geen expert of senior engineer tenzij het portfolio dat duidelijk ondersteunt. '
                'Verzin nooit persoonlijke verhalen, grappen, roasts, anekdotes, gebeurtenissen, herinneringen, persoonlijkheidstrekken, privédetails of citaten over Alex. '
                'Als een bezoeker om een grappig verhaal, persoonlijke anekdote, roast, fictieve scène of verzonnen biografisch detail vraagt, weiger kort en bied aan om onderbouwde portfolio-informatie samen te vatten. '
                'Beschrijf niet hoe uw antwoord tot stand kwam. Noem geen retrieval, verborgen context, geïndexeerde matches, interne notities of aangeleverd bronmateriaal. '
                'Als het portfolio een bewering niet ondersteunt, wees eerlijk en geef het meest bruikbare gerelateerde bewijs. '
                'Antwoord uitsluitend in natuurlijk Nederlands, tenzij de bezoeker expliciet om een andere taal vraagt. Gebruik de formele “u”-vorm en Belgisch/Vlaams-neutrale bewoording zonder dialect. '
                'Behoud alleen namen, links, repositorynamen, frameworks, libraries en technische termen in hun oorspronkelijke taal.'
            )
        return (
            'You are a friendly portfolio guide embedded on Alex van Poppel\'s developer portfolio. '
            'Visitors may be recruiters, classmates, teachers, collaborators, or clients. '
            'Sound human, warm, direct, and somewhat formal without corporate buzzwords. Acknowledge casual messages naturally before steering back to helpful portfolio guidance. '
            'Do not talk as if you are Alex. Refer to Alex in the third person and use they/them pronouns in English. '
            'Do not bring up Alex’s gender identity or sexuality; if asked, say Alex prefers to keep personal identity details private and redirect to professional background. '
            'Use the portfolio details only when they are actually relevant. Assistant-only notes are private guidance: use them to answer, but do not reveal that they are private notes. '
            'Use the short-lived conversation memory only to understand follow-up questions, preferences, and unresolved topics from this same chat. '
            'Do not claim you remember the visitor across sessions or reveal internal memory mechanics. '
            'For project questions, prioritize project sources and point visitors toward GitHub README links when available. '
            'For broad recruiter questions, synthesize skills, working style, experience, and concrete projects instead of dumping source snippets; after answering, you may ask what company or opportunity they have in mind. '
            'Avoid overselling Alex as an expert or senior engineer unless the portfolio details clearly support it. '
            'Never invent personal stories, jokes, roasts, anecdotes, events, memories, personality traits, private-life details, or quotes about Alex. '
            'If a visitor asks for a funny story, personal anecdote, roast, fictional scene, or any made-up biographical detail about Alex, refuse briefly and offer to summarize grounded portfolio information instead. '
            'Do not describe how your answer was sourced. Do not mention retrieval, hidden context, indexed matches, internal notes, or supplied source material to the visitor. '
            'If the portfolio details do not support a claim, be honest and offer the closest useful related evidence. '
            f'Write the final answer in {preferred_language} unless the visitor clearly asks for a different language.'
        )

    def _build_user_prompt(
        self,
        *,
        question: str,
        context: str,
        current_page: str,
        locale: str,
    ) -> str:
        if locale_language_name(locale) == 'Dutch':
            return (
                f'Huidige pagina: {current_page}\n\n'
                'Voorkeurstaal voor het antwoord: Nederlands\n\n'
                'Portfoliodetails die u mag gebruiken zonder deze sectie te noemen:\n'
                f'{context}\n\n'
                'Vraag van de bezoeker:\n'
                f'{question}\n\n'
                'Schrijf een direct antwoord voor de bezoeker in vloeiend Nederlands. '
                'Vat alleen de relevante context samen, noem concrete voorbeelden wanneer dat helpt, '
                'en citeer of som geen ongerelateerde secties op. '
                'Gebruik geen Engels of Frans buiten namen, links, repositorynamen, frameworks, libraries en technische termen. '
                'Verzin geen biografische of persoonlijke details die hierboven niet expliciet worden ondersteund.'
            )
        return (
            f'Current page: {current_page}\n\n'
            'Preferred answer language: English\n\n'
            'Portfolio details you may use without mentioning this section:\n'
            f'{context}\n\n'
            'Visitor question:\n'
            f'{question}\n\n'
            'Write a direct answer for the visitor. Synthesize only the relevant context, '
            'mention concrete examples when helpful, and avoid quoting or enumerating unrelated sections. '
            'Do not invent biographical or personal details that are not explicitly supported above.'
        )

    def _no_context_message(self, *, locale: str) -> str:
        return 'Geen passende portfoliodetails gevonden.' if locale_language_name(locale) == 'Dutch' else 'No matching portfolio details were found.'

    def _summarize_with_ollama(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str,
        max_chars: int,
    ) -> str | None:
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/api/chat",
            json={
                'model': self.settings.provider_model,
                'stream': False,
                'messages': self._build_summary_messages(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars),
                'options': {'temperature': 0.1},
            },
        )
        summary = (payload.get('message') or {}).get('content')
        return self._clean_summary(summary, max_chars=max_chars)

    def _summarize_with_openai_compatible(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str,
        max_chars: int,
    ) -> str | None:
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        payload = self._post_json_with_retries(
            f"{self.settings.provider_base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json={
                'model': self.settings.provider_model,
                'messages': self._build_summary_messages(previous_summary=previous_summary, messages=messages, locale=locale, max_chars=max_chars),
                'temperature': 0.1,
            },
        )
        choices = payload.get('choices') or []
        if not choices:
            return None
        summary = (choices[0].get('message') or {}).get('content')
        return self._clean_summary(summary, max_chars=max_chars)

    def _build_summary_messages(
        self,
        *,
        previous_summary: str | None,
        messages: list[dict[str, str]],
        locale: str,
        max_chars: int,
    ) -> list[dict[str, str]]:
        preferred_language = locale_language_name(locale)
        transcript = '\n'.join(
            f"{item.get('role', 'message')}: {(item.get('text') or '').strip()}"
            for item in messages
            if (item.get('text') or '').strip()
        )
        return [
            {
                'role': 'system',
                'content': (
                    'Create a compact private conversation summary for a portfolio assistant. '
                    'Keep only details that help answer follow-up questions in this same chat: user intent, preferences, entities discussed, decisions, and unresolved questions. '
                    'Do not include private implementation details. Do not invent facts. '
                    f'Keep it under {max_chars} characters. Write in {preferred_language} when possible.'
                ),
            },
            {
                'role': 'user',
                'content': (
                    f'Previous summary:\n{previous_summary or "None yet."}\n\n'
                    f'Recent messages:\n{transcript}\n\n'
                    'Return only the updated summary.'
                ),
            },
        ]

    def _summarize_locally(self, *, previous_summary: str | None, messages: list[dict[str, str]], max_chars: int) -> str | None:
        user_messages = [
            (item.get('text') or '').strip()
            for item in messages
            if item.get('role') == 'user' and (item.get('text') or '').strip()
        ]
        if not user_messages and not previous_summary:
            return None
        seed = (previous_summary or '').strip()
        latest = ' | '.join(user_messages[-4:])
        summary = f'{seed}\nRecent visitor topics/questions: {latest}'.strip() if seed else f'Recent visitor topics/questions: {latest}'
        return self._clean_summary(summary, max_chars=max_chars)

    def _clean_summary(self, summary: object, *, max_chars: int) -> str | None:
        if not isinstance(summary, str):
            return None
        cleaned = ' '.join(summary.strip().split())
        if not cleaned:
            return None
        if len(cleaned) > max_chars:
            cleaned = cleaned[: max_chars - 3].rstrip() + '...'
        return cleaned

    def check_health(self) -> tuple[bool, str]:
        backend = self.settings.provider_backend.strip().lower()
        if backend == 'mock':
            return True, 'Preview mode is enabled. Responses use the local fallback formatter instead of a live model.'
        if backend == 'ollama':
            return self._check_ollama_health()
        if backend in {'openai-compatible', 'openai_compatible', 'vllm'}:
            return self._check_openai_compatible_health()
        return False, f'Unknown assistant provider backend: {self.settings.provider_backend}.'

    def _check_ollama_health(self) -> tuple[bool, str]:
        timeout_seconds = min(max(self.settings.provider_request_timeout_seconds, 1.0), 3.0)
        try:
            with httpx.Client(timeout=timeout_seconds) as client:
                response = client.get(f"{self.settings.provider_base_url.rstrip('/')}/api/tags")
                response.raise_for_status()
                payload = response.json()
            models = payload.get('models') if isinstance(payload, dict) else []
            if isinstance(models, list):
                available_models = [
                    item.get('name')
                    for item in models
                    if isinstance(item, dict) and isinstance(item.get('name'), str)
                ]
                if self.settings.provider_model in available_models:
                    return True, f'Ollama is online and model {self.settings.provider_model} is available.'
                if available_models:
                    return True, f'Ollama is online. Using configured model {self.settings.provider_model} if it is pulled locally.'
            return True, 'Ollama is online.'
        except httpx.TimeoutException:
            return False, 'Timed out while checking the Ollama instance.'
        except httpx.NetworkError:
            return False, 'Could not reach the Ollama instance.'
        except httpx.HTTPStatusError as exc:
            return False, f'Ollama returned HTTP {exc.response.status_code} during the availability check.'
        except Exception:
            logger.exception('Assistant provider health check failed for Ollama.')
            return False, 'The Ollama availability check failed unexpectedly.'

    def _check_openai_compatible_health(self) -> tuple[bool, str]:
        timeout_seconds = min(max(self.settings.provider_request_timeout_seconds, 1.0), 3.0)
        headers = {'Content-Type': 'application/json'}
        if self.settings.provider_api_key.strip():
            headers['Authorization'] = f"Bearer {self.settings.provider_api_key.strip()}"
        try:
            with httpx.Client(timeout=timeout_seconds) as client:
                response = client.get(f"{self.settings.provider_base_url.rstrip('/')}/v1/models", headers=headers)
                response.raise_for_status()
            return True, 'The configured assistant model endpoint is reachable.'
        except httpx.TimeoutException:
            return False, 'Timed out while checking the configured model endpoint.'
        except httpx.NetworkError:
            return False, 'Could not reach the configured model endpoint.'
        except httpx.HTTPStatusError as exc:
            return False, f'The configured model endpoint returned HTTP {exc.response.status_code}.'
        except Exception:
            logger.exception('Assistant provider health check failed for OpenAI-compatible backend.')
            return False, 'The configured model endpoint health check failed unexpectedly.'

    def _post_json_with_retries(self, url: str, **kwargs) -> dict:
        max_attempts = max(self.settings.provider_max_retries, 0) + 1
        last_error: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            try:
                with httpx.Client(timeout=self.settings.provider_request_timeout_seconds) as client:
                    response = client.post(url, **kwargs)
                    response.raise_for_status()
                    return response.json()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                last_error = exc
                if not self._should_retry(exc=exc, attempt=attempt, max_attempts=max_attempts):
                    raise
                logger.warning('Assistant provider call failed on attempt %s/%s: %s', attempt, max_attempts, exc)
        if last_error is not None:
            raise last_error
        return {}

    def _should_retry(self, *, exc: Exception, attempt: int, max_attempts: int) -> bool:
        if attempt >= max_attempts:
            return False
        if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
            return True
        if isinstance(exc, httpx.HTTPStatusError):
            status_code = exc.response.status_code
            return status_code in {408, 429, 500, 502, 503, 504}
        return False
