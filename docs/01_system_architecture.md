# System architecture

The system has two data pipelines: **ingestion** and **inference**.

![System architecture diagram](./assets/HITS-components-presentation.png)

## 📥 Ingestion Pipeline

This section covers the ingestion pipeline, which prepares the chatbot’s knowledge base before the chatbot is made available to users.

### How it works

1. **Select the sources.** The organization identifies the documents and other sources to include in the knowledge base.
2. **Load and extract content.** Suitable loaders process each source and extract its relevant information.
3. **Split the content into chunks.** The extracted text is divided into smaller sections using a chosen strategy, such as fixed-size or structure-based chunking.
4. **Create embeddings.** Each chunk is passed to an **embedding model**, which converts text into a vector of \(N\) dimensions: $$\operatorname{embed}: \mathcal{T} \rightarrow \mathbb{R}^{N}, \qquad x \mapsto \mathbf{v}$$ Here, $\mathcal{T}$ represents the set of text inputs, and $\mathbf{v}$ is the vector representation of a text input $x$.
A useful embedding model places vectors for semantically similar text closer together in the vector space, according to the similarity measure used.


5. **Store the knowledge base.** Each vector is stored alongside its original text chunk in a collection within the **vector database** (hereafter, **VecDB**). This collection forms the knowledge base that the chatbot can retrieve information from.

The ingestion process must be completed before users can access the chatbot. For further details, see the [Ingestion pipeline documentation](./02_ingestion_pipeline.md).



## 💬 Inference Pipeline

The inference pipeline is how users interact with the chatbot. They send messages through a web-based chat interface, similar to interfaces provided by OpenAI, Google, and Anthropic.

### How it works

The **orchestrator** processes each message according to the behaviour configured at startup. The exact steps may vary, but a typical interaction follows this flow:

1. **Receive the message.** The orchestrator receives the user’s message from the chat interface.
2. **Create an embedding.** It converts the message into a vector using the same embedding model used during ingestion.
3. **Retrieve relevant information.** The orchestrator queries the **vector database (VecDB)** for vectors that are semantically similar to the message. The corresponding original text chunks are retrieved.
4. **Prepare the prompt.** It combines the retrieved information with instructions to create a prompt for the **large language model (LLM)**.
5. **Return the response.** The LLM generates an answer, which the orchestrator sends back to the user through the interface.

### Conversation storage

In parallel with responding to the user, the orchestrator stores conversations in a **relational database**. The stored data can be processed later to help evaluate and improve the chatbot.

For further details, see the [Chatbot architecture documentation](./02_chatbot_architecture.md).