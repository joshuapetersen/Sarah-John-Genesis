import { genkit } from 'genkit';
import { googleAI } from '@genkit-ai/googleai';

export default genkit({
  plugins: [
    googleAI(),
  ],
});

