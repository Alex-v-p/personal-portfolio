import { ContactMethod } from '../models/contact-method.model';
import { PROFILE } from './profile.mock';
import { SOCIAL_LINKS } from './social-links.mock';
import { buildContactMethods } from './content.selectors';

export const CONTACT_METHODS: ContactMethod[] = buildContactMethods(PROFILE, SOCIAL_LINKS);
