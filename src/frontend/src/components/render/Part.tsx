import { ReactNode } from 'react';

import { RenderInlineModel } from './Instance';

/**
 * Inline rendering of a single Part instance
 */
export function RenderPart({ instance }: { instance: any }): ReactNode {
  return (
    <RenderInlineModel
      primary={instance.name}
      secondary={instance.description}
      image={instance.thumnbnail || instance.image}
    />
  );
}

/**
 * Inline rendering of a PartCategory instance
 */
export function RenderPartCategory({ instance }: { instance: any }): ReactNode {
  // TODO: Handle URL

  let lvl = '-'.repeat(instance.level || 0);

  return (
    <RenderInlineModel
      primary={`${lvl} ${instance.name}`}
      secondary={instance.description}
    />
  );
}
