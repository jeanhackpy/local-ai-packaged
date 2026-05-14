---
created: 2024-07-03T02:41:02 (UTC +07:00)
tags: []
source: https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai
author: Julien.cloud
---

# Advanced AI with Fabric and LM Studio

> ## Excerpt


---
# Leveraging Fabr's rapidly evolving AI landscape, developers are constantly seeking innovative ways to improve their applications' intelligence and user experience. Two key players in this space are Fabric and LM Studio, which offer a powerful combination of customizable prompts and local model integration. In this article, we'll delve into the capabilities of these technologies and explore how they can be leveraged for advanced AI interactions.

**What is Fabric?**

Fabric is an open-source framework developed by Hugging Face that enables users to build, train, and deploy custom AI models with ease. By providing a simple and intuitive interface, Fabric [[textgene the process of creating and integrating AI models into various applications. This framework is particularly useful for developers who want to create bespoke AI solutions without requiring extensive expertise in machine learning.

**What is LM Studio?**

LM Studio is an innovative platform that allows users to build, train, and deploy custom language models using a range of pre-trained models as starting points. By providing access to these pre-trained models, LM Studio enables developers to fine-tune their AI models for specific tasks and domains. This platform also offers advanced features such as prompt engineering and model integration, making it an ideal choice for building sophisticated AI applications.

**Customizable Prompts with Fabric and LM Studio**

One of the most significant advantages of using Fabric and LM Studio is the ability to create customizable prompts that can be used to interact with AI models. By designing tailored prompts, developers can significantly improve the accuracy and relevance of their AI-powered applications. For instance, in a chatbot application, a well-crafted prompt can help the AI model understand user intent more effectively, leading to more accurate responses.

**Local Model Integration with Fabric and LM Studio**

Another key benefit of using Fabric and LM Studio is the ability to integrate local models into your applications. This feature allows developers to fine-tune their AI models for specific domains or tasks, which can lead to significant improvements in performance and accuracy. By integrating local models, you can create more personalized and effective AI-powered experiences that are tailored to your application's unique requirements.

**Real-World Applications of Fabric and LM Studio**

The combination of customizable prompts and local model integration offered by Fabric and LM Studio has a wide range of potential applications across various industries. Some examples include:

1. **Chatbots**: By creating customized prompts, chatbots can better understand user intent and provide more accurate responses.
2. **Virtual Assistants**: Local model integration can help virtual assistants like Siri or Alexa understand specific tasks and domains more effectively.
3. **Content Generation**: Fabric and LM Studio can be used to generate high-quality content for various applications, such as writing articles or creating social media posts.

**Conclusion**

In conclusion, Fabric and LM Studio offer a powerful combination of customizable prompts and local model integration that can be leveraged to create advanced AI interactions. By using these technologies, developers can build sophisticated AI-powered applications that are tailored to specific domains or tasks. With the ability to fine-tune models for specific use cases, Fabric and LM Studio have the potential to revolutionize the way we interact with AI in various industries.rator/templates/default/simplify.md|simplifie]]sic and LM Studio for Advanced AI

**

[![](data:image/svg+xml,%3csvg%20xmUnlocking the Power of Customizable AI Interactions with Fabric and LM Studio**

In todaylns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27200%27%20height=%27200%27/%3e)![Julien.cloud's photo](

[Julien.cloud](https://hashnode.com/@Xulien)

·[Jun 7, 2024](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai)·

6 min read

## Table of contents

-   [
    
    Introduction
    
    ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-introduction)
-   [
    
    Understanding Fabric
    
    ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-understanding-fabric)
-   [
    
    Installing tools
    
    ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-installing-tools)
    -   [
        
        Fabric
        
        ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-fabric)
    -   [
        
        LM Studio
        
        ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-lm-studio)
    -   [
        
        Integration
        
        ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-integration)
-   [
    
    Using Fabric
    
    ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-using-fabric)
    -   [
        
        Pre-built patterns
        
        ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-pre-built-patterns)
    -   [
        
        Writing Your Own Patterns
        
        ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-writing-your-own-patterns)
    -   [
        
        Use multiple patterns
        
        ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-use-multiple-patterns)
-   [
    
    Conclusion
    
    ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-conclusion)
-   [
    
    Key Takeaways
    
    ](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-key-takeaways)

Show more

# [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-introduction "Permalink")**Introduction**

During my usual YouTube browsing, I stumbled upon a video ([here](https://youtu.be/UbDyjIIGaxQ?si=LCgtyBHuDwLZunG0)) showcasing an AI tool called Fabric, a Python utility that facilitates interaction with AI models. The demo focused on OpenAI's paid version, but I was eager to explore its potential using a local LLM model.

# [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-understanding-fabric "Permalink")**Understanding Fabric**

Fabric is a Python tool that takes text input and submits it to AI models via an API endpoint, along with an advanced prompt.

It includes a library of pre-built advanced prompt templates called **patterns**. These patterns can be customized or created from scratch to fit individual needs.

These two features make Fabric a unique tool. It acts as middleware between the user and the AI engine, allowing anyone to tailor their interactions with AI models, making it easy and efficient to use.

# [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-installing-tools "Permalink")**Installing tools**

## [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-fabric "Permalink")**Fabric**

To install Fabric, follow the guide on the GitHub page: [https://github.com/danielmiessler/fabric](https://github.com/danielmiessler/fabric).

Once installed, you can run basic commands like `fabric --listmodels` to list all available models.

If you want to connect to OpenAI, you can run `fabric --setup`. It will run the initialization phase and ask for your API keys.

However, if you don't want to pay for an OpenAI key, you will need to run your model locally. This is where LM Studio comes into play.

## [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-lm-studio "Permalink")**LM Studio**

LM Studio is a free tool that allows users to download and run models locally on their machines. While it may be slower than using the paid version of OpenAI, it provides an opportunity to test LLM without incurring costs. To use LM Studio, visit [https://lmstudio.ai/docs/welcome](https://lmstudio.ai/docs/welcome) and install it.

## [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-integration "Permalink")**Integration**

Now that you have both Fabric and LM Studio installed, let's connect them.

To integrate Fabric with LM Studio, follow these steps:

1.  Download a model from LM Studio (I tried llama2, llama3, and Gemma, but stopped at llama3 as it's the latest and most advanced model available).
    
2.  Run the LM Studio local server. Increase the context length to the maximum and use your GPU if you have one.
    
    You should end up with something like this:
    
    ![](https://cdn.hashnode.com/res/hashnode/image/upload/v1717759163794/4db52a26-9fc9-4525-909d-7bbf2ca73d67.png?auto=compress,format&format=webp)
    
3.  Configure Fabric by setting the following environment variables:
    

Copy

Copy

```
export OPENAI_BASE_URL=http://localhost:1234/v1
export DEFAULT_MODEL=Meta-Llama-3-8B-Instruct-Q8_0.gguf
export OPENAI_API_KEY=lm-studio
```

That's all. You can now test if Fabric is properly configured with LM Studio by running:

`fabric --listmodels`

It should print the model you've loaded in the LM Studio server.

You can also try to send your first and most important request to Fabric using a generic AI pattern with the following command:

`echo "what is the meaning of life" | fabric -sp ai`

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1717759286205/c52f424f-514b-4987-aac8-c519ecf30090.png?auto=compress,format&format=webp)

# [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-using-fabric "Permalink")**Using Fabric**

## [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-pre-built-patterns "Permalink")**Pre-built patterns**

Patterns are advanced, customizable, and shareable AI prompts. Fabric comes with a library of pre-built patterns that you can use and modify to suit your needs.

You can list all the available patterns with the command `fabric -l`.

Here are some patterns I particularly like:

-   `extract_wisdom`: Extract important information from any text source (blog post, YouTube video transcript, PDF, etc.).
    
-   `ai`: A generic pattern for standard requests.
    
-   `write_pull-request`: To write beautiful PR/MR without effort.
    
-   `agility_story`: For creating agile user stories.
    
-   `provide_guidance` : Your AI psychologist
    

## [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-writing-your-own-patterns "Permalink")**Writing Your Own Patterns**

To demonstrate this capability, I created a custom pattern to improve this blog post. Yes, what you're reading has been generated using the process I'm about to explain – isn't it amazing?

If you look at the pattern library, you'll find a particularly useful pattern called `improve_prompt`. This pattern will help you write your own patterns.

Let's try creating a technical blog post pattern:

Copy

Copy

```
echo "As a technical writer, you take draft content as input and engaging technical guides in the form of blog articles. You provide technical context, explanation, and reference. You write articles of around 2000 words. You provide clear and detailed information. You use simple examples to explain concepts. You provide external links and sources. You provide actionable articles with a mix of theory and tutorial to help people understand concepts by putting things into practice. You write in a balance professional and casual way." | fabric -sp improve_prompt
```

Here is a snapshot of the produce pattern

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1717762366130/a81023d2-9340-4eba-b265-8dba9c7212aa.png?auto=compress,format&format=webp)

Take the output and save it as a file under `/Users/<user>/.config/fabric/patterns/write_tech_blog/`[`system.md`](http://system.md).

This prompt is ready to be used, improved, or customized.

Now, if you list your models with `Fabric -l`, you should see your new pattern.

To pass some data to Fabric, you can use several methods:

-   `echo "data" | Fabric`
    
-   `cat my_file.txt | Fabric`
    
-   `pbpaste | Fabric` which will input text you've copied to your clipboard using ctrl+c
    

To test our new pattern, gather some draft ideas for a blog post and pass them to Fabric with a command like `pbpaste | fabric -s -p write_tech_blog`.

This should give you pretty good articles that you can use right away or customize and improve yourself (or with other patterns).

If you want something different or more detailed, review the pattern file or regenerate it by changing the input of the initial _improve\_prompt_ process.

Crafting prompts is almost an art and definitely an iterative process. To improve your prompt crafting skills, I strongly recommend taking this free course: [https://learn.deeplearning.ai/courses/chatgpt-prompt-eng](https://learn.deeplearning.ai/courses/chatgpt-prompt-eng)

## [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-use-multiple-patterns "Permalink")**Use multiple patterns**

Another great feature of Fabric is its ability to use the output of one Fabric process as input for another. For example, you could extract wisdom from an article and use that to create a Keynote presentation, like this:

Copy

Copy

```
pbpaste | fabric -p extract_wisdom | fabric -s -p create_keynote
```

This will obviously be slower because it runs Fabric twice, but I found this concept of data refinement very powerful and full of potential.

Here is a snapshot of the result for this blog post :

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1717760014208/1b94486c-b9a7-4fac-a8e5-a82e6f8a37ce.png?auto=compress,format&format=webp)

# [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-conclusion "Permalink")**Conclusion**

Fabric and LM Studio offer a powerful combination to seamlessly use the AI platform while extracting the most value from it. By creating custom prompts and patterns, users can fully tailor their interactions with the AI model to suit their needs.

I strongly believe that AI tools are here to extend our capabilities and help us achieve more, faster. These tools have the potential to be as transformative as the industrial revolution, which fundamentally changed the way we work by introducing machines that could perform tasks more efficiently than humans. Similarly, AI will not only replace some jobs but also create entirely new ones that require different skills and competencies.

For now, these tools are still in the early stages and sometimes produce inappropriate or vague content. This is why the output of any AI-powered writing tool should always be reviewed and adapted by humans (for now :)).

# [Permalink](https://hashnode.julien.cloud/leveraging-fabric-and-lm-studio-for-advanced-ai#heading-key-takeaways "Permalink")**Key Takeaways**

-   Fabric is a Python tool that interacts with API AI models and injects custom prompts called patterns.
    
-   Patterns are pre-built templates that can be customised to meet individual needs.
    
-   Writing your own pattern can help you tailor your interactions with the AI model.
    
-   LM Studio is a free tool that allows users to download and run models locally on their machines.
    

.post-floating-bar { bottom: -60px; } .post-floating-bar.animation { -webkit-transition: .2s all; -o-transition: .2s all; transition: .2s all; transition-timing-function: ease-in; } .post-floating-bar.active { bottom: 40px } .post-floating-bar.freeze { bottom: 0!important; position: absolute!important; transition: none!important; } .post-floating-bar.freeze > div { box-shadow: none!important; }

@keyframes slideUpAndFade { from { opacity: 0; transform: translateY(2px); } to { opacity: 1; transform: translateY(0); } } .reaction-count-tooltip-content { box-shadow: hsl(206 22% 7% / 35%) 0px 10px 38px -10px, hsl(206 22% 7% / 20%) 0px 10px 20px -15px; user-select: none; transition: .2s all; animation-duration: 400ms; animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1); will-change: transform, opacity; } .reaction-count-tooltip-content\[data-state='instant-open'\]\[data-side='top'\] { animation-name: slideUpAndFade; } @keyframes shake { 0% { transform: translateX(0) } 25% { transform: translateX(1px) } 50% { transform: translateX(-1px) } 75% { transform: translateX(1px) } 100% { transform: translateX(0) } } .shake { animation-name: shake; animation-iteration-count: 2; animation-duration: 400ms; animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1); will-change: transform, opacity; }

[AI](https://hashnode.julien.cloud/tag/ai?source=tags_bottom_blogs)[#ai-tools](https://hashnode.julien.cloud/tag/ai-tools?source=tags_bottom_blogs)[aitools](https://hashnode.julien.cloud/tag/aitools?source=tags_bottom_blogs)

/
