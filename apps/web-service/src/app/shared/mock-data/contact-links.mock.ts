import { ContactMethod } from '../models/contact-method.model';

export const CONTACT_METHODS: ContactMethod[] = [
  {
    id: 'email',
    label: 'Email',
    value: 'hello@shuzu.dev',
    href: 'mailto:hello@shuzu.dev',
    actionLabel: 'Send Email',
    description: 'Best for project enquiries, internships, and collaboration.'
  },
  {
    id: 'phone',
    label: 'Phone',
    value: '+32 470 31 34 39',
    href: 'tel:+32470313439',
    actionLabel: 'Call',
    description: 'Useful for quick coordination or planning a meeting.'
  },
  {
    id: 'github',
    label: 'GitHub',
    value: 'github.com/shuzu',
    href: 'https://github.com/shuzu',
    actionLabel: 'Connect +',
    description: 'Code samples, experiments, and longer-form project work.'
  },
  {
    id: 'linkedin',
    label: 'LinkedIn',
    value: 'linkedin.com/in/alex-van-poppel',
    href: 'https://linkedin.com/in/alex-van-poppel',
    actionLabel: 'Connect +',
    description: 'Professional background, study path, and experience.'
  },
  {
    id: 'location',
    label: 'Location',
    value: 'Lommel, Belgium',
    href: 'https://maps.google.com/?q=Lommel%2C%20Belgium',
    actionLabel: 'View Map',
    description: 'Available for on-site, hybrid, or remote collaboration.'
  }
];
