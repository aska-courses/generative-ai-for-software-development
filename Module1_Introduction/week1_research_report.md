# Generative AI for Software Development — Course Notes (Week1)

## Use Case 1 - Code generators
Models/ LLMs that are used to generate code, complete functions, improve code structure.
### Business values
- Speeds up production and development time using AI inference to suggest code automatically
- Can be used as mentor for junior developers
- Can lower overall cost for common coding tasks 
### Technical and Weak challenges
- Generated code may contain bags
- The AI cannot guarantee the logic of whole code, becuse the large codes exceed Context window of LLM.
- Privacy Issues 
### Implementation
- **GitHub Copilot** — https://github.com/features/copilot - It integrates into various code editors, such as Visual Studio Code, and works by analyzing code context and natural language prompts to offer assistance. 

- **Cursor** —  https://cursor.com/ - Uses large language models to manipulate text with autocomplete and chat query function. It is a fork of Visual Studio Code.

## Use Case 2 - Content generator
Models that are trained to generate marketing content, like product descriptions, images/videos for ads. These Generative AI models use prompt engineering and sometimes fine-tuning to create content that fits a brand voice. 
### Business values
- Faster content creation using AI inference
- Lower costs
- Can be personalized using embedding-based recommendations or tailored prompts
### Technical and Weak challenges
- AI outputs may drift from the brand voice
- Some Ethical Issues (discrimination,racism contents with not proper prompt)
- Current Image generators are not able to write correct texts in the image.

### Implementation
- **OpenAI GPT (ChatGPT / API)** — https://openai.com -  for text generation and creative copy
- **Midjourney / DALL·E** — https://www.midjourney.com / https://openai.com/dall-e  - for  imagegeneration

## Use Case 3 - Summarizer
Models that can be used for summarizing long text/documents.AI uses RAG (retrieval-augmented generation), vector search, and embeddings to find relevant information and generate concise summaries.
### Business values
- Saves analyst time using inference to generate summaries automatically.
- Makes it easier to search across large document
- Helps new ones to get knowledge faster
### Technicaland Weak challenges
- Models could skip important details or introduce mistakes
- Privacy issues
- Embedding models may struggle with very technical language

### Implementation
- **Amazon Kendra / Bedrock** — https://aws.amazon.com —  search and summarization tools with vector search 
- **Cohere / Hugging Face** — https://cohere.ai / https://huggingface.co — model providers with pipelines for summarization and fine-tuning with LLMs